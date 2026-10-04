# SwiftUI Performance Basics

Use this file only when ordinary SwiftUI implementation touches a small
invalidation, identity, or image-loading concern and the task has not become
dedicated performance work.

## Out Of Scope

Dedicated performance work stays outside this skill:

- source-level performance smell audits and remediation for update fan-out,
  identity, heavy body work, image cost, animation cost, or layout thrash
- runtime evidence intake and deciding when to involve Instruments
- `.trace`, `xctrace`, Time Profiler, hangs, hitches, signposts, or trace
  capture/analysis

## Local Reminder

For an incidental SwiftUI source edit, at least preserve these basics:

- avoid repeated state writes with the same value
- pass only needed values to child views
- keep heavy work out of `body`
- preserve stable identity in lists and modifier-only state changes
- treat performance claims as hypotheses until validated
