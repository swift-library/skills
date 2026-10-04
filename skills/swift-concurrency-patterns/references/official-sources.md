# Official Sources

Use primary documentation for framework contracts and the selected SDK/compiler
for exact declarations. Preserve project deployment targets and supported older
paths. Source inspection is separate from successful compilation or runtime
validation; keep those results with the calling project.

| Source | Claim to check | Method / failure boundary |
| --- | --- | --- |
| [NonisolatedNonsendingByDefault / @concurrent](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0461-async-function-isolation.md) | NonisolatedNonsendingByDefault / @concurrent | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Module default isolation](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0466-control-default-actor-isolation.md) | Module default isolation | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Awaited defer](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0493-defer-async.md) | Awaited defer | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Cancellation shield and runtime support](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0504-task-cancellation-shields.md) | Cancellation shield and runtime support | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| [Incremental target-scoped migration](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/migrationstrategy/) | Incremental target-scoped migration | Read current body, compare local guidance; a fetch failure or session-only example does not validate an API. |
| `xcrun swift --version`, `xcrun --show-sdk-path`, selected SDK `.swiftinterface` | Compiler syntax, API signature and platform availability | Inspect the selected environment; a declaration does not prove macro execution, device behavior or live service access. |

Source bodies and declarations reviewed on 2026-09-12 against Swift 6.4 / SDK 27.0.
Recheck when a source or the toolchain changes.
