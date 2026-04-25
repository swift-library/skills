# Apple Package Hints

Read this file after the target package capability inventory suggests an
Apple-authored official package candidate.

This is a curated hint list, not a complete official package catalog. Use it to
recognize common target-code patterns and likely official candidates. Use the
CLI index or P1 official sources for current package facts such as repository,
manifest status, products/modules, platform support, and package status.

## Known High-Value Hints

| Trigger pattern | Candidate | Default review stance | Caution |
|---|---|---|---|
| custom sequence helpers, windows, chunks, combinations, permutations | `swift-algorithms` | Adopt / Wrap | Verify exact API coverage before replacing small helpers. |
| custom ordered set, ordered dictionary, deque, heap | `swift-collections` | Adopt / Wrap | Keep dependency types out of public API when stability matters. |
| custom CLI parser, flags, options, subcommands | `swift-argument-parser` | Adopt / Wrap | Usually relevant only for packages with CLI or tooling surfaces. |
| custom async sequence operators or stream combinators | `swift-async-algorithms` | Adopt / Wrap | Check Swift tools and deployment constraints. |
| custom atomic wrappers or lock-free primitives | `swift-atomics` | Adopt / Wrap | Prefer simpler locks if atomics are not required. |
| custom path, file descriptor, or low-level system wrappers | `swift-system` | Wrap / Reference | Foundation may be sufficient for high-level file APIs. |
| custom numeric types, algorithms, or math helpers | `swift-numerics` | Adopt / Reference | Verify the official package covers the actual numeric model. |
| custom networking runtime or event-loop primitives | `swift-nio` | Wrap / Reference | Dependency weight and public API leakage are frequent blockers. |
| custom logging facade | `swift-log` | Wrap | Avoid exposing logging dependency choices through public API. |
| custom metrics facade | `swift-metrics` | Wrap / Reference | Metrics may belong at application boundaries, not library core. |
| custom tracing propagation | `swift-distributed-tracing` | Wrap / Reference | Use only when tracing is a real package boundary. |
| custom async/service context propagation | `swift-service-context` | Wrap / Reference | Verify relationship to tracing and async boundaries. |
| custom HTTP request, response, or header types | `swift-http-types` | Adopt / Wrap | Avoid duplicating an existing framework's HTTP model. |
| custom OpenAPI code generation or client/server glue | `swift-openapi-generator` | Adopt / Wrap | Check generated-code boundary and plugin/tooling role. |
| custom Protocol Buffers serialization | `swift-protobuf` | Adopt / Wrap | Only relevant when protobuf is an actual wire format. |
| custom crypto primitives or provider abstraction | `swift-crypto` | Adopt / Wrap | Security-sensitive changes require strong source verification. |
| custom ASN.1 parsing | `swift-asn1` | Adopt / Wrap | Usually relevant through certificate or crypto boundaries. |
| custom certificate parsing or validation helpers | `swift-certificates` | Adopt / Wrap | Platform-native certificate APIs may already satisfy needs. |
