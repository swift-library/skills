---
name: ios-simulator
description: Use this skill for iOS Simulator automation and diagnostics when work involves xcrun simctl, simulator device list/suggest/create/boot/shutdown/erase/delete, environment health checks, installing or launching .app bundles, app state, opening deep links, screenshots, simulator status bar overrides, clipboard paste setup, simulator permissions, simulated push notifications, simulator logs or log streaming, xcodebuild build/test runs for iOS Simulator destinations, xcresult summaries and drill-down, visual screenshot diffs, app state capture, test evidence recording, Core Data or SwiftData model inspection from project files, or optional IDB semantic UI interaction such as accessibility-tree inspection, screen mapping, accessibility-tree audit, tapping by text/type/id, typing, special keys, hardware buttons, swiping, scrolling, long press, pinch, or refresh. Do not use for Xcode Instruments .trace analysis, source-only SwiftUI or UIKit code review, dedicated accessibility audits, Core Data schema design, SwiftData schema design, networking, package architecture, or repository documentation.
---

# iOS Simulator

## Purpose

Provide small, script-backed workflows for operating iOS Simulator targets,
building and testing against simulator destinations, and inspecting or driving
simulator UI when local tools are available.

This is an automation skill, not a Swift coding-pattern skill. Keep source-code
fixes in the relevant source skill after simulator evidence identifies the
problem.

## When To Use

- Listing, selecting, booting, shutting down, erasing, creating, or deleting
  simulator devices.
- Installing, uninstalling, launching, terminating, or deep-linking into an
  iOS app in Simulator.
- Capturing screenshots, simulator logs, status bar overrides, app
  permissions, clipboard state, app state, environment health, or simulated
  push notifications.
- Running `xcodebuild` build or test commands for an iOS Simulator destination
  and returning concise summaries with cached result drill-down.
- Using optional IDB to inspect the accessibility tree, map interactive
  elements, tap by visible text, type/id, type text, press keys/buttons,
  perform gestures, or run a lightweight accessibility-tree audit.
- Comparing screenshots, capturing app state bundles, recording test evidence,
  or inspecting Core Data / SwiftData model declarations from project files.

## When Not To Use

- Do not use for Xcode Instruments `.trace`, `xctrace`, Time Profiler, hangs,
  hitches, or signpost analysis; use `xcode-instruments`.
- Do not use for source-only SwiftUI, UIKit, or architecture review without a
  simulator operation.
- Do not use for dedicated accessibility audits, WCAG mapping, Accessibility
  Inspector workflows, or Nutrition Labels; use `accessibility-patterns`.
- Do not use for Core Data or SwiftData schema design, persistence fixes,
  migration, query/context implementation, networking, package architecture,
  dependency replacement, or repository documentation. This skill may still
  inspect Core Data / SwiftData model declarations from project files as a
  simulator diagnostic.
- Do not claim UI semantics from screenshots alone when IDB or another
  accessibility-tree source was not used.

## Inputs To Inspect

- User request, app bundle path, bundle identifier, URL/deep link, target
  simulator name or UDID, destination string, scheme, workspace/project path,
  screenshot/log output path, APNs payload, or requested UI text.
- Local project truth: `AGENTS.md`, `README.md`, build instructions, Xcode
  project/workspace files, schemes, and test targets.
- Local tool availability: `xcrun simctl`, `xcodebuild`, `xcrun xcresulttool`,
  and optional `idb`.

## Workflow

1. Read local project truth first when the request touches a project build,
   app bundle, test target, or repository-specific simulator convention.
2. Classify the request as simulator operation, app operation, build/test,
   log/screenshot capture, permissions/environment setup, push/status bar,
   visual diff, state/test capture, model inspection, or optional IDB UI
   interaction.
3. Open only the matching reference file. Use `references/_index.md` only when
   routing is unclear.
4. Prefer the bundled scripts over ad hoc shell commands when they cover the
   operation.
5. Keep output concise by default. Use JSON or detailed logs only when the user
   asks or the first summary is insufficient.
6. Treat IDB as optional. If `idb` is unavailable, continue with `simctl` or
   report which semantic UI operation is blocked.
7. If simulator evidence points to a source-code fix, hand off to the relevant
   SwiftUI, UIKit, accessibility, concurrency, persistence, or architecture
   skill for the source change.

## Reference Files To Consult

- `references/simctl.md`: simulator lifecycle, app lifecycle, screenshots,
  logs, permissions, status bar, clipboard, health checks, and push
  notifications.
- `references/xcodebuild.md`: build/test wrapper, simulator destinations,
  xcresult and log drill-down.
- `references/idb.md`: optional semantic UI inspection and interaction through
  IDB.
- `references/output.md`: concise output, JSON, failure handling, and handoff
  expectations.
- `references/command-map.md`: capability mapping to this skill's compact
  commands. Read when translating examples or checking execution parity.
- `references/troubleshooting.md`: dense failure diagnosis and recovery
  commands. Read only after a command fails or the environment is unclear.
- `references/test-patterns.md`: repeatable simulator test flows. Read only
  when the user asks for a test runbook or multi-step simulator workflow.

Use `references/_index.md` only when the needed reference is unclear.

## Scripts

- `scripts/sim.py`: `xcrun simctl` device lifecycle, app lifecycle, screenshot,
  logs/streaming, privacy, clipboard, push, status bar, and health operations.
- `scripts/xcode_build.py`: concise `xcodebuild` build/test wrapper, cached
  result IDs, log drill-down, and `xcresulttool` summary hooks.
- `scripts/idb_ui.py`: optional IDB screen map, semantic find/tap/type,
  keyboard, hardware buttons, gestures, and lightweight audit.
- `scripts/state_capture.py`: screenshot, logs, device state, optional IDB
  hierarchy, and Markdown bug-report summary.
- `scripts/test_recorder.py`: screenshot plus optional accessibility tree and
  Markdown test evidence bundle.
- `scripts/visual_diff.py`: Pillow-backed screenshot comparison and diff image
  output.
- `scripts/model_inspector.py`: Core Data `.xcdatamodeld` and SwiftData
  `@Model` inspection from project files.

## Decision Rules

- Repository-local truth wins over this skill.
- Use Apple command-line tools for simulator and build operations before
  introducing third-party dependencies.
- IDB-dependent commands must say when IDB is required and unavailable.
- Avoid long raw logs in the answer. Save logs to files or summarize the
  relevant lines.
- Do not hide command failures; include the command surface, exit code, and the
  actionable stderr summary.
- Do not infer app behavior from one screenshot when a semantic tree, logs, or
  test result is needed.

## Validation Rules

- Run `python3 <script> --help` after editing bundled scripts.
- Compile edited Python scripts with `python3 -m py_compile`.
- Verify tool availability before operations that require local Xcode, a
  booted simulator, or IDB.
- For destructive simulator operations such as erase/delete, require an
  explicit simulator name/UDID and confirmation flag when scripting.

## Output Format

For simulator/build investigations, return:

1. Phase / stage judgment
2. Simulator or build surface inspected
3. Actions performed
4. Findings
5. Compatibility / tooling impact
6. Validation performed
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If Xcode command-line tools are missing, state that `xcrun simctl` or
  `xcodebuild` is unavailable and stop simulator automation.
- If no simulator is booted, list available devices or recommend a specific
  boot command rather than guessing.
- If multiple simulators match a name, list the candidates and require a more
  specific name or UDID before destructive operations.
- If the project has no discoverable scheme, ask for the scheme or report the
  exact project/workspace inspected.
