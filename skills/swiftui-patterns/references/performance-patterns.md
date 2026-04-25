# SwiftUI Performance Route

SwiftUI source-level performance knowledge belongs to
`swiftui-performance`.

Use this route only when ordinary SwiftUI implementation touches a small
invalidation, identity, or image-loading concern and the task has not become
dedicated performance work.

## Route

- Source-level performance smells, remediation patterns, update fan-out,
  identity, heavy body work, image cost, animation cost, or layout thrash:
  `../swiftui-performance/references/code-smells.md`
- Runtime evidence intake and when to involve Instruments:
  `../swiftui-performance/references/profiling-intake.md`
- `.trace`, `xctrace`, Time Profiler, hangs, hitches, signposts, or trace
  capture/analysis:
  use `xcode-instruments`.

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- avoid repeated state writes with the same value
- pass only needed values to child views
- keep heavy work out of `body`
- preserve stable identity in lists and modifier-only state changes
- treat performance claims as hypotheses until validated
