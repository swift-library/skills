# Official Sources

Use primary documentation for framework contracts and the selected SDK/compiler
for exact declarations. Preserve project deployment targets and supported older
paths. Source inspection is separate from successful compilation or runtime
validation; keep those results with the calling project.

| Source | Claim to check | Method / failure boundary |
| --- | --- | --- |
| [Framework model and capability updates](https://developer.apple.com/videos/play/wwdc2026/241/) | Framework model and capability updates | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [LanguageModel/Executor provider contracts](https://developer.apple.com/videos/play/wwdc2026/339/) | LanguageModel/Executor provider contracts | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Current capability initializer](https://developer.apple.com/documentation/foundationmodels/languagemodelcapabilities) | Current capability initializer | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |

Source bodies and declarations reviewed on 2026-09-12 against Swift 6.4 / SDK 27.0.
Recheck when a source or the toolchain changes.
