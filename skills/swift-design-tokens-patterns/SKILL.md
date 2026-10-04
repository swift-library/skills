---
name: swift-design-tokens-patterns
description: Use this skill when changing, reviewing, refactoring, testing, or debugging the swift-design-tokens package, `SwiftDesignTokens` library, `TokenTool` executable, `TokensPlugin` command plugin, DTCG-style token JSON parsing, canonical token config handling, alias/mode resolution, Colors.xcassets generation, Swift token constant generation, resolved JSON export, or design-token compiler validation. Do not use for app-specific visual styling, design-system consumption APIs, Figma design review, or generic SwiftPM architecture unless the token compiler/package surface is the concrete issue.
---

# Swift Design Tokens Patterns

## Purpose

Guide implementation, review, and troubleshooting for the `swift-design-tokens`
SwiftPM package. The package compiles DTCG-style token JSON into Apple-platform
outputs such as `Colors.xcassets`, Swift constants, and optional resolved-token
JSON.

## When To Use

- Editing `Package.swift` surfaces for `SwiftDesignTokens`, `TokenTool`, or
  `TokensPlugin`.
- Changing token parsing for `$value` / `value`, `modes`, aliases, filters,
  appearances, output paths, strict policies, or resolved exports.
- Debugging generated `Colors.xcassets`, `DesignTokens.swift`, or
  `Resolved.{appearance}.json`.
- Reviewing CLI or SwiftPM command plugin behavior around `generate-tokens`.
- Validating compiler behavior for DTCG token types and unsupported-token
  handling.

## When Not To Use

- App-specific visual styling or token consumption APIs. Route that to the app
  or design-system owner.
- Figma design interpretation or visual design review; design judgment is out
  of scope.
- Generic package target-graph review unless the token compiler package graph
  is the actual task.

## Package Surface

- Package: `swift-design-tokens`.
- Products: `SwiftDesignTokens`, `TokenTool`, `TokensPlugin`.
- Main library types: `TokensConfig`, `TokensCompiler`, `CompilerError`, and
  helper JSON model `J`.
- CLI shape: `TokenTool --config <config.json> [--export-resolved]`.
- Plugin command: `generate-tokens`.

## Workflow

When changing compiler behavior:

1. Inspect the package manifest and public library source first.
2. Keep one canonical config shape. Do not add legacy config compatibility
   unless the owning package explicitly accepts that burden.
3. Keep DTCG `$value` / `value`, appearances, `modes`, aliases, include/exclude
   filters, output paths, and strict policies covered by tests.
4. Preserve supported exports:
   - `color` -> `Colors.xcassets` with Any/Dark appearances.
   - `dimension`, `spacing`, `radius` -> Swift `CGFloat` constants.
   - `duration` -> Swift `Double` seconds.
   - `opacity`, `number`, `string`, `boolean` -> Swift constants.
5. Keep parsed-but-not-exported types explicit: `typography`, `shadow`,
   `gradient`, `cubicBezier`, `border`, and `borderRadius`.
6. Treat optional metadata such as `version` as ignored unless the package
   direction changes.

When changing generated outputs:

1. Change token source/config/compiler logic first; do not hand-edit generated
   assets or Swift constants as source of truth.
2. Verify color space, appearance names, and asset catalog path behavior.
3. Check resolved exports when alias or mode resolution changes.

## Validation

Use the package path in the target repo:

```bash
swift test --package-path <path-to-swift-design-tokens>
swift run --package-path <path-to-swift-design-tokens> TokenTool --config <config.json> --export-resolved
```

If the package is wired into an app or design-system package through the plugin,
also run the consuming build path that exercises generated assets/constants.

## Failure Modes

- Adding a second config dialect creates silent drift between examples,
  compiler behavior, and plugin usage.
- Silent unresolved aliases, invalid units, or missing mode values can generate
  misleading design output.
- Editing generated files without token-source changes hides source-of-truth
  drift.
- Treating app token accessors as compiler truth couples this package to one
  consuming app.
