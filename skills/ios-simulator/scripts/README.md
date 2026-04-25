# Scripts

These scripts are small wrappers around local Apple command-line tools and
optional IDB. Run each script with `--help` for the current command surface.

- `sim.py`: `xcrun simctl` lifecycle, app, screenshot, log/streaming, privacy,
  clipboard, push, status-bar, create/delete, selector, and health operations.
- `xcode_build.py`: concise `xcodebuild` build/test wrapper with result IDs,
  cached logs, and drill-down.
- `idb_ui.py`: optional IDB semantic UI inspection, navigation, keyboard,
  gestures, and lightweight accessibility-tree audit.
- `state_capture.py`: screenshot, logs, device state, optional hierarchy, and
  Markdown bug-report summary.
- `test_recorder.py`: current-screen screenshot/tree evidence and Markdown
  test report.
- `visual_diff.py`: screenshot comparison and optional diff image.
- `model_inspector.py`: Core Data and SwiftData model inspection.
