# Official Sources

Use primary documentation for framework contracts and the selected SDK/compiler
for exact declarations. Preserve project deployment targets and supported older
paths. Source inspection is separate from successful compilation or runtime
validation; keep those results with the calling project.

| Source | Claim to check | Method / failure boundary |
| --- | --- | --- |
| [Compiler/runtime version distinction](https://developer.apple.com/videos/play/wwdc2026/269/) | Compiler/runtime version distinction | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Lazy-container work and lifecycle](https://developer.apple.com/videos/play/wwdc2026/321/) | Lazy-container work and lifecycle | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Long body versus many updates and Cause & Effect](https://developer.apple.com/documentation/xcode/understanding-and-improving-swiftui-performance) | Long body versus many updates and Cause & Effect | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |

Source bodies and declarations reviewed on 2026-09-12 against Swift 6.4 / SDK 27.0.
Recheck when a source or the toolchain changes.
