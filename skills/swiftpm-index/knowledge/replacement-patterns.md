# Replacement Patterns

Read this file after building the target package capability inventory.

Use these mappings as candidate discovery prompts, not final recommendations.

- custom CLI parsing -> `swift-argument-parser`
- custom ordered set / ordered dictionary / deque / heap -> `swift-collections`
- custom sequence, window, chunk, or combinatorics helpers -> `swift-algorithms`
- custom async sequence combinators -> `swift-async-algorithms`
- custom process runner -> `swift-subprocess`
- custom Swift source parser or generator -> `swift-syntax`
- custom Markdown parser or editor -> `swift-markdown`
- custom DocC or script docs generation -> `swift-docc-plugin` / `swift-docc`
- custom test DSL -> `swift-testing`
- custom system path or file descriptor wrappers -> `swift-system`
- custom logging facade -> `swift-log`, usually wrapped
- custom metrics -> `swift-metrics`
- custom tracing or context propagation -> `swift-distributed-tracing` /
  `swift-service-context`
- custom OpenAPI codegen/client/server glue -> `swift-openapi-generator` family
- custom protobuf -> `swift-protobuf`
- custom crypto, certificate, or ASN.1 helpers -> `swift-crypto` /
  `swift-certificates` / `swift-asn1`

Before recommending adoption, run dependency-cost checks from
`rules/recommendation-taxonomy.md`.
