---
name: xcode-localization-patterns
description: Use this skill for end-to-end Apple-platform localization implementation and review across Xcode localization settings, String Catalogs, generated symbols, XLIFF or xcloc exchange, pseudolocalization, app/package/framework localized resources, Bundle access, Swift localization APIs, SwiftUI localized text presentation, RTL layout checks, and locale UI tests. Do not use for interface copywriting alone, FormatStyle-only modernization, ordinary SwiftUI text cleanup, or marketing/app-store localization.
---

# Xcode Localization Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple-platform
localization that crosses Xcode resources, build settings, app/package/framework
resource access, runtime string APIs, SwiftUI presentation, and validation.

## When To Use

- Creating, migrating, or reviewing `Localizable.xcstrings`, `.strings`, or
  `.stringsdict` resources.
- Wiring localization for app targets, extensions, Swift packages, frameworks,
  or shared modules.
- Using generated localizable symbols, `String(localized:)`,
  `LocalizedStringResource`, `LocalizedStringKey`, pluralization, interpolation,
  grammar agreement, or localized assets.
- Exporting/importing translator handoff files with XLIFF or xcloc.
- Checking pseudolocalization, locale UI tests, screenshots, RTL layout,
  Dynamic Type, or localized snapshot coverage.
- Debugging missing strings, wrong bundles, stale keys, fixed-format strings,
  concatenation, or locale-dependent test failures.

## When Not To Use

- Do not use for writing or rewriting UI copy only; use `interface-writing`.
- Do not use for FormatStyle-only modernization with no resource workflow; use
  `swift-programming-language`.
- Do not use for ordinary SwiftUI view implementation where localization is
  only a local `Text` or layout concern; use `swiftui-patterns`.
- Do not use for App Store listing localization, screenshots, ASO, or market
  messaging; use the market operations collection.
- Do not invent tool, SDK, generated-symbol, or string-catalog behavior. Verify
  current Xcode and Apple documentation before relying on version-specific
  behavior.

## Inputs To Inspect

- Project targets, package manifests, resource declarations, bundle boundaries,
  build settings, and existing localization settings.
- `*.xcstrings`, `*.strings`, `*.stringsdict`, localized asset catalogs, and
  generated symbol usage.
- Swift and SwiftUI source that reads strings, formats values, interpolates
  text, accesses bundles, or constructs localized resources.
- Translator exchange files, pseudolocalization settings, UI tests, snapshots,
  screenshots, and locale-specific fixtures.

## Workflow

1. Identify the localization owner: app target, extension, framework, Swift
   package, or shared resource bundle.
2. Read existing localization strategy before changing files. Preserve the
   current resource format unless migration is part of the task.
3. Check Xcode project settings, package `resources`, and bundle lookup paths.
   Use `Bundle.main` for app-owned resources, `Bundle.module` for Swift package
   resources, and an explicit framework bundle when the resource is framework
   owned.
4. Prefer String Catalogs and generated localizable symbols when the project and
   toolchain already support them. Keep stable keys when changing visible text.
5. Use `String(localized:)`, `LocalizedStringResource`, `LocalizedStringKey`,
   and SwiftUI `Text` APIs according to the call site. Avoid eager formatting
   when environment locale should apply at render time.
6. Preserve localization semantics: placeholders, interpolation order,
   pluralization, grammar agreement, device variations, measurements, lists,
   person names, dates, numbers, and currency.
7. Review SwiftUI presentation for text expansion, RTL layout, Dynamic Type,
   truncation, ordering, and concatenated `Text` anti-patterns.
8. Use XLIFF or xcloc export/import workflows for translator handoff when the
   task involves external translation.
9. Validate with the smallest meaningful evidence: targeted build, locale run,
   pseudolocalized UI pass, UI test, snapshot, or string-resource inspection.

## Review Rules

- Do not concatenate user-visible localized strings. Use interpolation,
  placeholders, format styles, or catalog entries that let translators reorder
  content.
- Do not use fixed English word order for values, dates, names, lists, units, or
  plurals.
- Do not hard-code `Bundle.main` in reusable packages or frameworks.
- Do not convert localized values to strings too early when SwiftUI should
  resolve locale from the environment.
- Keep nonlocalized identifiers, filenames, product codes, and machine-readable
  values explicit with verbatim or fixed-format handling.
- Locale-sensitive tests must pin locale, calendar, time zone, numbering system,
  and expected fixtures when exact strings matter.

## Validation

- Build the affected target or package after resource changes.
- Run at least one non-default locale for user-visible changes when feasible.
- Use pseudolocalization for layout, clipping, truncation, and missing-key
  checks.
- Run targeted UI tests or snapshots when screens, bundles, or key migrations
  change.
- Check translator export/import workflows when `.xcloc` or XLIFF files are in
  scope.

## Output

For reviews, report:

1. Localization owner and resource format inspected
2. Findings by resource, runtime API, SwiftUI presentation, and validation
3. Specific file/key/API changes needed
4. Tests or manual locale checks run
5. Remaining current-source or toolchain assumptions
