# xcodebuild For Simulator

Use `scripts/xcode_build.py` for short build/test summaries and saved logs.
The wrapper uses Apple `xcodebuild` and optionally `xcrun xcresulttool` for
later result inspection.

## Typical Build

```bash
python3 "${SKILL_DIR}/scripts/xcode_build.py" build \
  --workspace App.xcworkspace \
  --scheme App \
  --simulator "iPhone 16 Pro"
```

## Typical Test

```bash
python3 "${SKILL_DIR}/scripts/xcode_build.py" test \
  --project App.xcodeproj \
  --scheme AppTests \
  --destination "platform=iOS Simulator,name=iPhone 16 Pro"
```

`test`, and `build --test`, need a concrete simulator from `--simulator` or
`--destination`; the generic simulator destination only builds. If a scheme is
not supplied, the script tries `xcodebuild -list -json` and uses the first
shared scheme. Report the selected scheme.

## Drill Down

```bash
python3 "${SKILL_DIR}/scripts/xcode_build.py" list-results
python3 "${SKILL_DIR}/scripts/xcode_build.py" show-result --id xcresult-... --errors
python3 "${SKILL_DIR}/scripts/xcode_build.py" show-result --id xcresult-... --warnings
python3 "${SKILL_DIR}/scripts/xcode_build.py" show-result --id xcresult-... --log
python3 "${SKILL_DIR}/scripts/xcode_build.py" list-schemes --workspace App.xcworkspace
```

Default answers should summarize errors and warnings rather than paste full
`xcodebuild` output. Include the saved log path when the log is useful.

## Destination Rules

- Prefer an explicit user-provided destination.
- Use `--simulator` when the user provides a simulator name.
- Use `generic/platform=iOS Simulator` only for build operations that do not
  need a booted device.
- Preserve project-local build instructions over this reference.

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
