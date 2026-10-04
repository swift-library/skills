# Official Sources

Use primary documentation for framework contracts and the selected SDK/compiler
for exact declarations. Preserve project deployment targets and supported older
paths. Source inspection is separate from successful compilation or runtime
validation; keep those results with the calling project.

| Source | Claim to check | Method / failure boundary |
| --- | --- | --- |
| [Swift 6.3/6.4 language updates](https://developer.apple.com/videos/play/wwdc2026/262/) | Swift 6.3/6.4 language updates | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Swift 6.4 release](https://www.swift.org/blog/swift-6.4-released/) | Release changes and proposal discovery | Follow the exact proposal; a release summary does not establish every feature's first supported version. |
| [SE-0491 module selectors](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0491-module-selectors.md) | `ModuleName::` disambiguation, implemented in Swift 6.3 | Read proposal status and verify ambiguity with the selected compiler; do not move its introduction to 6.4 merely because that release highlights it. |
| [SE-0521 optional opaque/existential syntax](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0521-improved-optional-opaque-and-any.md) | Swift 6.4 `some P?` / `any P?`, composition parentheses and retained old spelling | Compile positive and rejected composition forms; a newer compiler's language mode is not an older compiler test. |
| [SE-0522 source warning control](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0522-source-warning-control.md) | Swift 6.4 `@diagnose`, lexical warning scope and unchanged compilation errors | Check the real warning group, escalation/demotion and an unaffected declaration; preserve the repository's warning policy. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |

Recheck when a source or the toolchain changes.
