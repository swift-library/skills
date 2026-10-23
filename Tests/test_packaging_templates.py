# SPDX-License-Identifier: Apache-2.0 WITH Swift-exception
"""Run packaging templates with deterministic tool doubles, without signing credentials."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "skills/swiftpm-macos-app-packaging/assets/templates"

# Tool doubles record architectures and notarization file modes; no Apple services run.
TOOLS = r'''
import json, os, pathlib, plistlib, stat, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
if name == "PlistBuddy":
    key = args[1].split(":")[-1]
    print(plistlib.loads(pathlib.Path(args[-1]).read_bytes())[key])
elif name == "lipo":
    if args[0] == "-archs":
        print(pathlib.Path(args[1]).read_text().strip())
    else:
        inputs = args[1:args.index("-output")]
        arches = sorted({arch for path in inputs for arch in pathlib.Path(path).read_text().split()})
        pathlib.Path(args[-1]).write_text(" ".join(arches))
elif name == "ditto":
    pathlib.Path(args[-1]).write_text("archive")
    if os.environ.get("FAIL_DITTO"):
        sys.exit(9)
elif name == "xcrun" and args[:2] == ["notarytool", "submit"]:
    archive = pathlib.Path(args[2])
    data = {"directory": str(archive.parent), "directory_mode": stat.S_IMODE(archive.parent.stat().st_mode),
            "zip_mode": stat.S_IMODE(archive.stat().st_mode)}
    if "--key" in args:
        key = pathlib.Path(args[args.index("--key") + 1])
        data["key_mode"] = stat.S_IMODE(key.stat().st_mode)
        data["key_exists"] = key.is_file()
    pathlib.Path(os.environ["NOTARY_OBSERVATIONS"]).write_text(json.dumps(data))
    if os.environ.get("FAIL_NOTARY"):
        sys.exit(7)
'''


class PackagingTemplateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        tool = self.bin / "tool"
        tool.write_text(f"#!{sys.executable}\n" + TOOLS)
        tool.chmod(0o755)
        for name in ["swift", "lipo", "plutil", "PlistBuddy", "codesign", "xattr", "install_name_tool", "ditto", "xcrun", "spctl", "stapler"]:
            (self.bin / name).symlink_to(tool)
        (self.root / "scripts").mkdir()
        (self.root / "tmp").mkdir()
        (self.root / "version.env").write_text("MARKETING_VERSION=1.2.3\nBUILD_NUMBER=4\n")
        self.env = {**os.environ, "PATH": str(self.bin) + os.pathsep + os.environ["PATH"],
                    "TMPDIR": str(self.root / "tmp"), "APP_NAME": "Example", "ARCHES": "arm64 x86_64",
                    "MARKETING_VERSION": "9.9.9", "BUILD_NUMBER": "999",
                    "DITTO_BIN": str(self.bin / "ditto"), "NOTARY_OBSERVATIONS": str(self.root / "notary.json")}
        for key in ["APP_STORE_CONNECT_API_KEY_P8", "APP_STORE_CONNECT_KEY_ID", "APP_STORE_CONNECT_ISSUER_ID", "NOTARY_PROFILE", "APP_ENTITLEMENTS", "APP_IDENTITY", "FAIL_DITTO", "FAIL_NOTARY"]:
            self.env.pop(key, None)

    def template(self, name):
        target = self.root / "scripts" / name
        # PlistBuddy uses an absolute system path in the template.
        target.write_text((TEMPLATES / name).read_text().replace("/usr/libexec/PlistBuddy", str(self.bin / "PlistBuddy")))
        target.chmod(0o755)
        return target

    def run_script(self, name):
        return subprocess.run(["bash", str(self.template(name))], cwd=self.root, env=self.env,
                              capture_output=True, text=True)

    def build_outputs(self, arches=("arm64", "x86_64"), versioned=False):
        for arch in arches:
            build = self.root / f".build/{arch}-apple-macosx/release"
            build.mkdir(parents=True)
            (build / "Example").write_text(arch)
            framework = build / "Support.framework"
            framework.mkdir()
            if versioned:
                binary = framework / "Versions/A/Support"
                binary.parent.mkdir(parents=True)
                (framework / "Versions/Current").symlink_to("A")
                (framework / "Support").symlink_to("Versions/Current/Support")
            else:
                binary = framework / "Support"
            binary.write_text(arch)
            binary.chmod(0o755)

    def test_universal_framework_and_executable_have_all_architectures(self):
        self.build_outputs(versioned=True)
        # A generic output must not mask the architecture-specific frameworks.
        stale = self.root / ".build/release/Support.framework"
        stale.mkdir(parents=True)
        (stale / "Support").write_text("arm64")
        result = self.run_script("package_app.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        contents = self.root / "Example.app/Contents"
        for binary in [contents / "MacOS/Example", contents / "Frameworks/Support.framework/Support"]:
            self.assertEqual(set(binary.read_text().split()), {"arm64", "x86_64"})
        self.assertTrue((contents / "Frameworks/Support.framework/Support").is_symlink())
        self.assertIn("<string>1.2.3</string>", (contents / "Info.plist").read_text())

    def test_missing_framework_architecture_fails_for_either_build(self):
        self.build_outputs()
        for missing in ("arm64", "x86_64"):
            framework = self.root / f".build/{missing}-apple-macosx/release/Support.framework"
            shutil.rmtree(framework)
            result = self.run_script("package_app.sh")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(f"Missing Support.framework binary for {missing}", result.stderr)
            framework.mkdir()
            (framework / "Support").write_text(missing)

    def test_generic_framework_cannot_hide_missing_architecture_builds(self):
        self.build_outputs()
        for arch in ("arm64", "x86_64"):
            shutil.rmtree(self.root / f".build/{arch}-apple-macosx/release/Support.framework")
        generic = self.root / ".build/release/Support.framework"
        generic.mkdir(parents=True)
        (generic / "Support").write_text("arm64")
        result = self.run_script("package_app.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing Support.framework binary for arm64", result.stderr)

    def test_single_arch_framework_copy_is_preserved(self):
        self.env["ARCHES"] = "arm64"
        self.build_outputs(arches=("arm64",))
        result = self.run_script("package_app.sh")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "Example.app/Contents/Frameworks/Support.framework/Support").read_text(), "arm64")

    def test_framework_architecture_verification_rejects_wrong_slice(self):
        self.build_outputs()
        (self.root / ".build/x86_64-apple-macosx/release/Support.framework/Support").write_text("arm64")
        result = self.run_script("package_app.sh")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("arch mismatch", result.stderr)

    def prepare_notary(self):
        app = self.root / "Example.app"
        app.mkdir(exist_ok=True)
        packager = self.root / "scripts/package_app.sh"
        packager.write_text("#!/bin/sh\nexit 0\n")
        packager.chmod(0o755)

    def test_private_notary_files_and_cleanup_with_api_key_and_profile(self):
        self.prepare_notary()
        for mode in ("api", "profile"):
            if mode == "api":
                self.env.update(APP_STORE_CONNECT_API_KEY_P8="PRIVATE-TEST-KEY\\nCONTENT", APP_STORE_CONNECT_KEY_ID="test-id", APP_STORE_CONNECT_ISSUER_ID="test-issuer")
            else:
                self.env.pop("APP_STORE_CONNECT_API_KEY_P8")
                self.env["NOTARY_PROFILE"] = "test-profile"
            for fail in (False, True):
                self.env["FAIL_NOTARY"] = "1" if fail else ""
                result = self.run_script("sign-and-notarize.sh")
                self.assertEqual(result.returncode, 7 if fail else 0, result.stderr)
                observed = json.loads((self.root / "notary.json").read_text())
                self.assertEqual(observed["directory_mode"], 0o700)
                self.assertEqual(observed["zip_mode"], 0o600)
                if mode == "api":
                    self.assertEqual(observed["key_mode"], 0o600)
                    self.assertTrue(observed["key_exists"])
                self.assertFalse(Path(observed["directory"]).exists())
                self.assertNotIn("PRIVATE-TEST-KEY", result.stdout + result.stderr)
        self.assertTrue((self.root / "Example-1.2.3.zip").exists())
        self.assertEqual(list((self.root / "tmp").iterdir()), [])

    def test_notary_cleanup_on_missing_credentials_and_archive_failure(self):
        self.prepare_notary()
        result = self.run_script("sign-and-notarize.sh")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Missing notarization credentials", result.stderr)
        self.assertEqual(list((self.root / "tmp").iterdir()), [])
        self.env["FAIL_DITTO"] = "1"
        result = self.run_script("sign-and-notarize.sh")
        self.assertEqual(result.returncode, 9, result.stderr)
        self.assertEqual(list((self.root / "tmp").iterdir()), [])

    def test_both_templates_require_complete_version_file(self):
        for name in ("package_app.sh", "sign-and-notarize.sh"):
            (self.root / "version.env").write_text("MARKETING_VERSION=1.2.3\n")
            result = self.run_script(name)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("version.env must declare BUILD_NUMBER", result.stderr)
            (self.root / "version.env").unlink()
            result = self.run_script(name)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("version.env is required", result.stderr)


if __name__ == "__main__":
    unittest.main()
