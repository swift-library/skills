# Command Map

Use this when translating upstream-style `ios-simulator-skill` commands to this
skill's compact script surface.

## Build And Result Drill-Down

| Upstream capability | Local command |
| --- | --- |
| `build_and_test.py --project App.xcodeproj` | `xcode_build.py build --project App.xcodeproj` |
| `build_and_test.py --project App.xcodeproj --test` | `xcode_build.py build --project App.xcodeproj --test` or `xcode_build.py test --project App.xcodeproj` |
| `build_and_test.py --get-errors ID` | `xcode_build.py show-result --id ID --errors` |
| `build_and_test.py --get-warnings ID` | `xcode_build.py show-result --id ID --warnings` |
| `build_and_test.py --get-log ID` | `xcode_build.py show-result --id ID --log` |
| `build_and_test.py --list-xcresults` | `xcode_build.py list-results` |

`xcode_build.py` also accepts the upstream-style flat build/test flags for
common migration cases.

## Simulator And App Operations

| Upstream capability | Local command |
| --- | --- |
| `sim_list.py` / selector suggestions | `sim.py list` / `sim.py suggest` |
| `simctl_create.py` | `sim.py create` |
| `simctl_boot.py` | `sim.py boot` |
| `simctl_shutdown.py` | `sim.py shutdown` |
| `simctl_erase.py` | `sim.py erase` |
| `simctl_delete.py` | `sim.py delete` |
| `app_launcher.py --install` | `sim.py install` |
| `app_launcher.py --launch` | `sim.py launch` |
| `app_launcher.py --restart` | `sim.py restart` |
| `app_launcher.py --terminate` | `sim.py terminate` |
| `app_launcher.py --uninstall` | `sim.py uninstall` |
| `app_launcher.py --open-url` | `sim.py open-url` |
| `app_launcher.py --list` | `sim.py app-list` |
| `app_launcher.py --state` | `sim.py app-state` |
| `log_monitor.py` | `sim.py logs` |
| `clipboard.py` | `sim.py clipboard` |
| `privacy_manager.py` | `sim.py privacy` |
| `push_notification.py` | `sim.py push` |
| `status_bar.py` | `sim.py status-bar` |
| `sim_health_check.sh` | `sim.py health` |

Most local commands accept both `--device` and `--udid`.

## IDB UI Operations

| Upstream capability | Local command |
| --- | --- |
| `screen_mapper.py` | `idb_ui.py map` |
| `navigator.py --find-text` | `idb_ui.py find --find-text` or `idb_ui.py tap-text` |
| `navigator.py --find-type` | `idb_ui.py find --find-type` |
| `navigator.py --find-id` | `idb_ui.py find --find-id` |
| `navigator.py --tap-at` | `idb_ui.py tap --x X --y Y` |
| `navigator.py --enter-text` | `idb_ui.py find ... --enter-text` |
| `gesture.py --swipe` | `idb_ui.py swipe --direction` |
| `gesture.py --scroll` | `idb_ui.py scroll --direction --amount` |
| `gesture.py --refresh` | `idb_ui.py refresh` |
| `gesture.py --pinch` | `idb_ui.py pinch` |
| `gesture.py --long-press` | `idb_ui.py long-press` |
| `keyboard.py --type` | `idb_ui.py type` |
| `keyboard.py --key` | `idb_ui.py key` |
| `keyboard.py --button` | `idb_ui.py button` |
| `keyboard.py --clear` | `idb_ui.py clear` |
| `keyboard.py --dismiss` | `idb_ui.py dismiss` |
| `accessibility_audit.py` | `idb_ui.py audit` |

## Testing And Analysis

| Upstream capability | Local command |
| --- | --- |
| `app_state_capture.py` | `state_capture.py` |
| `test_recorder.py` | `test_recorder.py` |
| `visual_diff.py` | `visual_diff.py` |
| `model_inspector.py` | `model_inspector.py` |
