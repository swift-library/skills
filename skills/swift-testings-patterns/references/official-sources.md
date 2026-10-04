# Official Sources

Use primary documentation for framework contracts and the selected SDK/compiler
for exact declarations. Preserve project deployment targets and supported older
paths. Source inspection is separate from successful compilation or runtime
validation; keep those results with the calling project.

| Source | Claim to check | Method / failure boundary |
| --- | --- | --- |
| [Swift 6.4 XCTest interoperability and migration](https://developer.apple.com/videos/play/wwdc2026/267/) | Swift 6.4 XCTest interoperability and migration | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Interop modes and failure propagation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/testing/0021-targeted-interoperability-swift-testing-and-xctest.md) | Interop modes and failure propagation | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Test-specific reflection (ST-0022)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/testing/0022-customtestreflectable.md) | `CustomTestReflectable`, mirror selection and Swift 6.4 availability | Compare the proposal with the selected Testing library; check ordinary reflection, fallback and actual failed-expectation output. |
| [Transferable attachments (ST-0023)](https://github.com/swiftlang/swift-evolution/blob/main/proposals/testing/0023-attachments-transferable.md) | Apple-platform availability, asynchronous export, content selection and errors | Verify the selected SDK/Testing library, saved attachment bytes and export failure handling; preserve existing encoding paths. |
| [Current language/testing capabilities](https://developer.apple.com/videos/play/wwdc2026/262/) | Current language/testing capabilities | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |
| `swift test --help`, selected Testing module and a failing helper test | Repetition flags, diagnostics and interoperability | Verify the actual runner, mode, exit code and failures; no success claim from help alone. |

Source bodies and declarations reviewed on 2026-09-12 against Swift 6.4 / SDK 27.0.
Recheck when a source or the toolchain changes.
