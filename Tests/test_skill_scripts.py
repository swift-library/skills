# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Regression checks for simulator state and opt-in release policies."""

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SIM_SCRIPTS = ROOT / "skills/ios-simulator/scripts"
sys.path.insert(0, str(SIM_SCRIPTS))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load("xcode_build", SIM_SCRIPTS / "xcode_build.py")
sim = load("sim", SIM_SCRIPTS / "sim.py")
release = load("check_repo_facts", ROOT / "skills/swiftpm-github-release/scripts/check_repo_facts.py")


class SimulatorStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.env = mock.patch.dict(os.environ, {"XDG_CACHE_HOME": str(self.root / "cache")})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.clear_override = mock.patch.dict(os.environ)
        self.clear_override.start()
        os.environ.pop("IOS_SIMULATOR_STATE_DIR", None)
        self.addCleanup(self.clear_override.stop)

    def args(self, *argv):
        return build.build_parser().parse_args(argv)

    def test_project_cache_is_stable_resolved_and_separate(self):
        project = self.root / "one/App.xcodeproj"
        project.mkdir(parents=True)
        alias = self.root / "alias"
        alias.symlink_to(project.parent, target_is_directory=True)
        first = build.state_dir(self.args("build", "--project", str(project)))
        same = build.state_dir(self.args("show-result", "--id", "id", "--project", str(alias / project.name)))
        other = build.state_dir(self.args("build", "--project", str(self.root / "two/App.xcodeproj")))
        self.assertEqual(first, same)
        self.assertNotEqual(first, other)
        self.assertEqual(first.parent, self.root / "cache/ios-simulator")
        self.assertEqual(len(first.name), 16)
        self.assertFalse(first.exists())

    def test_platform_cache_and_override_precedence(self):
        args = self.args("list-results")
        with mock.patch.dict(os.environ):
            os.environ.pop("XDG_CACHE_HOME")
            with mock.patch.object(build.Path, "home", return_value=self.root), mock.patch.object(build.sys, "platform", "darwin"):
                self.assertEqual(build.state_dir(args).parent, self.root / "Library/Caches/ios-simulator")
            with mock.patch.object(build.Path, "home", return_value=self.root), mock.patch.object(build.sys, "platform", "linux"):
                self.assertEqual(build.state_dir(args).parent, self.root / ".cache/ios-simulator")
        with mock.patch.dict(os.environ, {"IOS_SIMULATOR_STATE_DIR": str(self.root / "environment")}):
            self.assertEqual(build.state_dir(args), self.root / "environment")
            for argv in [("--state-dir", str(self.root / "cli"), "list-results"),
                         ("list-results", "--state-dir", str(self.root / "cli"))]:
                self.assertEqual(build.state_dir(self.args(*argv)), self.root / "cli")

    def test_result_id_drill_down_from_another_directory(self):
        directory = self.root / "state"
        args = self.args("build", "--state-dir", str(directory), "--project", "App.xcodeproj", "--scheme", "App")
        result = argparse.Namespace(returncode=1, stdout="file.swift: error: failed", stderr="")
        with mock.patch.object(build, "require_tool"), mock.patch.object(build, "run_command", return_value=result), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as exit_status:
                build.cmd_build_or_test(args)
        self.assertEqual(exit_status.exception.code, 1)
        index = build.load_index(directory)
        identifier, entry = next(iter(index.items()))
        self.assertTrue(Path(entry["log"]).is_absolute())
        output = io.StringIO()
        with mock.patch.object(build.Path, "cwd", return_value=self.root / "elsewhere"), contextlib.redirect_stdout(output):
            build.cmd_show_result(self.args("show-result", "--state-dir", str(directory), "--id", identifier, "--errors", "--json"))
        self.assertEqual(json.loads(output.getvalue())["errors"], ["file.swift: error: failed"])

    def test_push_temp_payload_removed_on_success_failure_and_serialization_error(self):
        args = argparse.Namespace(payload=None, bundle_id="com.example.app", title="Title", body="Body", badge=None,
                                  no_sound=True, sound=None, timeout=1, json=False)
        for failure in (None, SystemExit(1), RuntimeError("timeout")):
            paths = []
            def run(command, **kwargs):
                paths.append(Path(command[-1]))
                self.assertTrue(paths[-1].exists())
                if failure:
                    raise failure
            with mock.patch.object(sim, "resolve_device", return_value="device"), mock.patch.object(sim, "device_arg"), mock.patch.object(sim, "run_command", side_effect=run), contextlib.redirect_stdout(io.StringIO()):
                if failure:
                    with self.assertRaises(type(failure)):
                        sim.cmd_push(args)
                else:
                    sim.cmd_push(args)
            self.assertFalse(paths[0].exists())
        with mock.patch.object(sim, "resolve_device", return_value="device"), mock.patch.object(sim, "device_arg"), mock.patch.object(sim.json, "dump", side_effect=ValueError("bad JSON")), mock.patch.object(sim.tempfile, "tempdir", str(self.root)):
            with self.assertRaises(ValueError):
                sim.cmd_push(args)
        self.assertEqual(list(self.root.glob("*.apns")), [])

    def test_push_keeps_user_payload_on_failure(self):
        payload = self.root / "user.apns"
        payload.write_text("{}")
        args = argparse.Namespace(payload=str(payload), bundle_id="com.example.app", timeout=1, json=False)
        with mock.patch.object(sim, "resolve_device", return_value="device"), mock.patch.object(sim, "device_arg"), mock.patch.object(sim, "run_command", side_effect=SystemExit(1)):
            with self.assertRaises(SystemExit):
                sim.cmd_push(args)
        self.assertTrue(payload.exists())


class ReleasePolicyTests(unittest.TestCase):
    def run_check(self, flags=(), old_version="1.0.0", next_version="1.0.1"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Package.swift").write_text('// swift-tools-version: 6.1\nlet package = Package(platforms: [.macOS(.v14)])\n')
            def git(repo, *args, **kwargs):
                if args[:2] == ("tag", "--list"):
                    return "v" + old_version
                if args[0] == "show":
                    return '// swift-tools-version: 6.0\nlet package = Package(platforms: [.macOS(.v13)])\n'
                if args[0] == "log":
                    return "abc123\x1fHuman\x1fhuman@example.com\x1fHuman\x1fhuman@example.com\x1fFix\n\nCo-authored-by: Claude <ai@example.com>\x1e"
                return ""
            stdout, stderr = io.StringIO(), io.StringIO()
            argv = ["check_repo_facts.py", str(root), "--next-version", next_version, "--range", "base..HEAD", *flags]
            with mock.patch.object(release, "git", side_effect=git), mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as status:
                    release.main()
            return status.exception.code, stdout.getvalue(), stderr.getvalue()

    def test_default_floor_note_and_allowed_attribution_do_not_fail(self):
        status, output, _ = self.run_check()
        self.assertEqual(status, 0)
        self.assertIn("note:floor-raise", output)
        self.assertIn("swift-tools-version", output)
        self.assertIn("macOS", output)
        self.assertNotIn("ai-trailer", output)

    def test_each_policy_is_opt_in(self):
        status, output, _ = self.run_check(["--forbid-ai-trailers"])
        self.assertEqual(status, 1)
        self.assertIn("ai-trailer\t", output)
        self.assertNotIn("version-bump\t", output)
        status, output, _ = self.run_check(["--breaking-floor-raise"])
        self.assertEqual(status, 1)
        self.assertIn("version-bump\t", output)
        self.assertNotIn("ai-trailer", output)

    def test_breaking_floor_policy_accepts_major_and_zero_minor(self):
        for old, new in [("1.0.0", "2.0.0"), ("0.3.0", "0.4.0")]:
            status, output, _ = self.run_check(["--breaking-floor-raise"], old, new)
            self.assertEqual(status, 0, output)
        status, output, _ = self.run_check(["--breaking-floor-raise"], "0.3.0", "0.3.1")
        self.assertEqual(status, 1)
        self.assertIn("MINOR", output)

    def test_version_file_and_release_configuration_remain_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "VERSION").write_text("v1.2.3\n")
            self.assertEqual(release.pending_version(root, None), "1.2.3")
            (root / ".github").mkdir()
            (root / "version.txt").write_text("version=2.0.0")
            (root / ".github/release.json").write_text(json.dumps({"version_file": "version.txt", "version_pattern": "version=(.*)"}))
            self.assertEqual(release.pending_version(root, None), "2.0.0")
            self.assertEqual(release.pending_version(root, "3.0.0"), "3.0.0")


if __name__ == "__main__":
    unittest.main()
