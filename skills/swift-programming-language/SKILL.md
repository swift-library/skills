---
name: swift-programming-language
description: >-
  Use this skill for broad Swift or Apple-platform language and API baseline
  work when no deeper domain skill fits: AI-generated Swift code review,
  obvious modernization, Swift API Design Guidelines, naming and argument
  labels, documentation comments, FormatStyle and .formatted() usage, Date.now,
  count(where:), modern Foundation APIs, lightweight Observation or SwiftUI
  baseline checks, accessible image buttons, force unwrap and force try caution,
  user-visible error handling, baseline localization API checks, project
  structure, tests, secrets, obvious secret-storage mistakes, SwiftLint, Google
  Swift style reference checks, or Xcode MCP usage. Do not use it for deep Swift Concurrency
  diagnostics or migration, deep SwiftUI, SwiftData
  implementation/schema/query/migration/sync work, CoreData, Keychain Services
  implementation, CryptoKit, certificate trust, networking, package
  architecture, dependency replacement, or repository documentation work.
---

# The Swift Programming Language

## Description

Use this skill for broad Swift language, Foundation, and API-design baseline
work when no deeper domain skill is the right fit. It covers obvious
modernization, Swift API Design Guidelines, FormatStyle usage, naming,
argument labels, documentation comments, lightweight Observation / SwiftUI
baseline checks, Google Swift style reference checks, baseline localization API
checks, project structure, tests, obvious secret-storage mistakes, and SwiftLint.

Do not use it for deep Swift Concurrency diagnostics or migration, deep
SwiftUI, SwiftData implementation/schema/query/migration/sync work, CoreData,
networking, package architecture, dependency replacement, or repository
documentation work.

## Use When

- Reviewing AI-generated Swift or SwiftUI code against a lightweight baseline.
- Checking API naming, argument labels, documentation comments, old
  Foundation formatting, Observation, SwiftUI baseline, baseline localization
  API usage, SwiftData CloudKit, testing, obvious secret-storage mistakes, or
  Xcode MCP patterns.
- Replacing obvious old API usage with compatible modern APIs.
- Reviewing or writing user-visible formatting with `FormatStyle`,
  `.formatted()`, or SwiftUI `Text(_:format:)`.
- Designing or reviewing Swift APIs for clear call sites and guideline-aligned
  naming.
- Checking Google Swift style only when the repository or user explicitly
  requests that style.
- Applying lightweight Swift coding checks to a SwiftUI app project.
- Checking baseline SwiftData CloudKit constraints.
- Checking baseline localization API usage, formatting, project-structure,
  testing, obvious secret-storage mistakes, and Xcode MCP guidance.

## Do Not Use When

- The task requires deep SwiftUI implementation, state, navigation, layout,
  performance, accessibility, animation, Charts, or platform-specific SwiftUI
  guidance. Use `swiftui-patterns` instead.
- The task requires nontrivial Swift Concurrency diagnostics, Swift 6 strict
  concurrency migration, actor-isolation design, data-race work, or `Sendable`
  fixes. Use `swift-concurrency-patterns` instead.
- The task requires SwiftData implementation, schema design, custom DataStore,
  query, migration, CloudKit sync, or troubleshooting work. Use
  `swiftdata-patterns` instead.
- The task requires CoreData migration or persistent store design.
- The task requires nontrivial Keychain Services implementation, access
  control, keychain sharing, biometric-protected secrets, credential migration,
  or keychain testing. Use `keychain-patterns` instead.
- The task requires CryptoKit algorithm selection, cryptographic correctness,
  Secure Enclave key operations, nonce handling, or crypto tests. Use
  `cryptokit-patterns` instead.
- The task requires certificate trust, pinning, SPKI hashes, client
  certificates, mTLS, or URLSession trust challenge handling. Use
  `certificate-trust-patterns` instead.
- The task requires networking architecture.
- The task requires package dependency replacement analysis.
- The task requires repository documentation scaffolding.
- The task requires full package architecture or module-boundary design beyond
  baseline coding patterns.
- The task requires Xcode String Catalogs, generated localizable symbols,
  XLIFF/xcloc exchange, pseudolocalization, localized package/framework
  resources, bundle lookup, RTL validation, or locale UI tests. Use
  `xcode-localization-patterns` instead.

## Workflow

1. Read local project truth first:
   - user request
   - `AGENTS.md`
   - `README.md`
   - `Package.swift`
   - relevant architecture docs
2. Determine whether the project actually matches the baseline assumptions:
   - iOS 26+
   - Swift 6.2+
   - SwiftUI app
   - SwiftData usage
   - string catalog usage
   - Xcode MCP availability
3. Apply only compatible baseline rules.
4. If local deployment targets or project constraints conflict with a modern
   API assumption, preserve local constraints and report the mismatch.
5. Produce a concise review or change recommendation.

## Read Next

- Read `rules/baseline.md` when applying or reviewing baseline rules.
- Read `references/format-style.md` when replacing legacy `Formatter`,
  `String(format:)`, or eager SwiftUI text formatting.
- Read `references/api-design-guidelines.md` when designing or reviewing Swift
  API names, argument labels, documentation comments, overloads, or fluent
  call-site usage.
- Read `references/google-swift-style.md` only when the repository explicitly
  adopts Google Swift style, the user asks for it, or the task is a style
  review of source-file structure, imports, formatting, comments, access
  control, or stricter layout conventions.
- Read `examples/review-output.md` only when output shape is unclear.

## Local Override Rule

Repository-local truth wins over this skill.

Explicit user instructions, local `AGENTS.md`, local `README.md`,
`Package.swift`, and architecture docs override this baseline. Report conflicts
instead of forcing baseline assumptions onto a repository that does not declare
them.

## Output Format

Outputs must include:

1. Phase / stage judgment
2. Findings
3. Recommended changes
4. Compatibility impact
5. Risks
6. Next steps
