# FormatStyle

## Contents

- [Availability](#availability)
- [Core Rules](#core-rules)
- [Replace Legacy Patterns](#replace-legacy-patterns)
- [Numeric, Percent, And Currency](#numeric-percent-and-currency)
- [Dates And Durations](#dates-and-durations)
- [Measurements, Lists, Names, Byte Counts, URLs](#measurements-lists-names-byte-counts-urls)
- [SwiftUI](#swiftui)
- [Review Checklist](#review-checklist)

Use this when:

- Reviewing or writing user-visible formatting in Swift.
- Replacing `String(format:)`, `DateFormatter`, `NumberFormatter`, or other
  `Formatter` subclasses.
- Formatting numbers, currency, percentages, dates, durations, measurements,
  lists, names, byte counts, URLs, or SwiftUI `Text`.

Skip this file if:

- The task is general localization without formatting.
- The repository must support platform versions before basic `FormatStyle`
  availability.

## Availability

- Basic `FormatStyle`: iOS 15+ / macOS 12+.
- Duration and URL styles: iOS 16+ / macOS 13+.
- SwiftUI stopwatch/timer format styles require newer SwiftUI SDKs; confirm the
  target before using them.

Repository-local deployment targets win.

## Core Rules

- Prefer `.formatted()` for simple one-off formatting.
- Prefer explicit `FormatStyle` values for reusable or complex formatting.
- Prefer SwiftUI `Text(value, format: style)` over interpolating a formatted
  string into `Text`.
- Prefer `Decimal` for currency values.
- Format styles are locale-aware by default. Set a specific locale only when
  intentionally formatting for a locale different from the user's environment.
- Do not use `DispatchQueue` merely to format values. Format style values are
  value types and can be used safely without legacy formatter caching patterns.

## Replace Legacy Patterns

| Legacy | Prefer |
|---|---|
| `String(format: "%.2f", value)` | `value.formatted(.number.precision(.fractionLength(2)))` |
| `String(format: "%02d:%02d", minutes, seconds)` | `Duration.seconds(total).formatted(.time(pattern: .minuteSecond))` |
| `String(format: "%d%%", percent)` | `percent.formatted(.percent)` |
| `DateFormatter` | `date.formatted(.dateTime...)` or `Date.FormatStyle` |
| `NumberFormatter` | `.number`, `.percent`, `.currency(code:)` |
| `DateComponentsFormatter` | `Duration.formatted(.units(...))` or `.time(...)` |
| `DateIntervalFormatter` | date interval formatting styles when available |
| `MeasurementFormatter` | `.measurement(...)` |
| `PersonNameComponentsFormatter` | `.name(style:)` |
| `ByteCountFormatter` | `.byteCount(style:)` |

## Numeric, Percent, And Currency

- Use `.number` for decimal/grouping/precision/sign/notation.
- Use `.percent` for percentages; remember integer and floating-point inputs
  have different semantics.
- Use `.currency(code:)` with ISO 4217 currency codes.
- Use `Decimal` for money to avoid binary floating-point surprises.

```swift
amount.formatted(.currency(code: "USD"))
progress.formatted(.percent.precision(.fractionLength(0)))
count.formatted(.number.notation(.compactName))
```

## Dates And Durations

- Use `.dateTime` component composition for locale-aware display.
- Use `.iso8601` for machine-readable ISO output.
- Use `.verbatim` only for fixed, structured output; specify locale, calendar,
  and time zone intentionally.
- Use `Duration` formatting instead of manual hour/minute/second math.

```swift
date.formatted(.dateTime.year().month().day().hour().minute())
Duration.seconds(seconds).formatted(.time(pattern: .hourMinuteSecond))
```

## Measurements, Lists, Names, Byte Counts, URLs

- Measurements can convert units based on locale and usage. Use explicit
  locales in tests when output must be deterministic.
- Use `.list(type:width:)` for localized list text.
- Use `PersonNameComponents` formatting for locale-aware names.
- Use `.byteCount(style:)` for file or memory sizes.
- Use `URL.FormatStyle` only when the target platform supports it.

## SwiftUI

Prefer `Text(_:format:)`:

```swift
Text(price, format: .currency(code: "USD"))
Text(date, format: .dateTime.hour().minute())
Text(progress, format: .percent)
```

Avoid:

```swift
Text("\(price.formatted(.currency(code: "USD")))")
```

`Text(_:format:)` respects environment locale at render time; eager formatting
captures a string too early.

## Review Checklist

- [ ] No C-style `String(format:)` for user-visible values.
- [ ] No legacy `Formatter` subclass when a compatible `FormatStyle` exists.
- [ ] Currency uses `Decimal` unless the project has a justified model type.
- [ ] SwiftUI text uses `format:` when possible.
- [ ] Tests pin locale/calendar/time zone when asserting exact strings.
- [ ] Explicit locale is used only when intentionally overriding user locale.
