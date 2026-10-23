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

## Build State

`xcode_build.py` stores build/test logs, `.xcresult` bundles, and the
`xcresults-index.json` result-ID index in a per-project user cache:
`$XDG_CACHE_HOME/ios-simulator/<hash>` when `XDG_CACHE_HOME` is set,
otherwise `~/Library/Caches/ios-simulator/<hash>` on macOS or
`~/.cache/ios-simulator/<hash>` on other hosts. The hash is the first 16 hex
characters of SHA-256 of the resolved project root: the parent of the selected
workspace/project, or the current directory when neither is found.

Pass `--state-dir PATH` or set `IOS_SIMULATOR_STATE_DIR` to use an explicit
directory; the option takes precedence. For `list-results` and `show-result`,
use the same project directory, `--workspace`/`--project`, or state override
as the build. Paths in the index are absolute, so result-ID drill-down works
from another directory with the same override. `--log` and `--result-bundle`
can place individual outputs elsewhere.

To clean up, remove that project's cache directory (or the explicit state
directory) after builds and inspection finish. This deletes its logs, bundles
and result-ID index; separately remove outputs placed elsewhere by `--log`
or `--result-bundle` when they are no longer needed.
