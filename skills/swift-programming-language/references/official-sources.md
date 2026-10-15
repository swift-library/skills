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
| [SE-0517 UniqueBox](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0517-uniquebox.md) | Swift 6.4 single-owner heap value, borrowed mutation, consumption and copyable-content clone | Inspect SDK availability; compile valid access, rejected cloning of noncopyable contents and use after consumption. Check destruction separately from performance. |
| [SE-0527 UniqueArray](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0527-rigidarray-uniquearray.md) | Swift 6.4 growing storage for noncopyable elements and explicit copying | Verify current public declarations and element lifetime; proposal drafts and avoidance of copy-on-write do not establish API availability or benchmark results. |
| [SE-0516 Iterable](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0516-borrowing-sequence.md) | Borrowing iteration over noncopyable elements | Compile an actual loop and subsequent container use; inspect iterator lifetime, throwing behavior and SDK support before converting generic Sequence algorithms. |
| [SE-0524 temporary allocation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0524-span-temporary-allocation.md) | Swift 6.4 temporary `OutputSpan` / `OutputRawSpan`, initialization and scoped cleanup | Compile typed and raw-byte calls; check initialized-element destruction on normal and throwing exits, and reject escaping views. Stack allocation is not guaranteed. |
| [SE-0525 safe raw-byte loading](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0525-rawspan-safe-loading-api.md) | Byte-conversion constraints, bounds-checked unaligned loads and byte-order operations | Inspect each SDK availability; compile valid integer access and a rejected unsupported type. Verify endian round trips separately from binary-format validity, old-system runtime support and performance. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |

Recheck when a source or the toolchain changes.
