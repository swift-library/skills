---
name: swiftui-performance
description: Use this skill for SwiftUI source-level performance implementation guidance, review, diagnosis, and optimization involving slow rendering, janky scrolling, high CPU or memory use, excessive view updates, invalidation fan-out, unstable identity, heavy work in `body`, image cost, animation cost, or layout thrash. Auto-trigger when SwiftUI implementation or review explicitly involves performance-sensitive surfaces such as large lists, image-heavy views, high-frequency state updates, unstable identity, costly layout, or animation hot paths; use manual mode for PR-time performance review before requiring Instruments evidence. Do not use for `.trace`, `xctrace`, Time Profiler, hang, hitch, or signpost capture/analysis; use xcode-instruments.
---

# SwiftUI Performance

## Purpose

Guide SwiftUI source-level performance during implementation and review, then
route to Instruments only when runtime evidence is needed.

## Entry Modes

- Automatic performance guidance: Use during SwiftUI implementation when view
  structure, state fan-out, identity, images, layout, or animation choices can
  materially affect rendering cost.
- Manual performance review: Use when the user asks for PR-time or existing-code
  performance review, diagnosis, or optimization guidance.
- Runtime evidence escalation: Route trace capture and trace interpretation to
  `xcode-instruments`, then return here for source-level remediation when
  useful.

## When To Use

- Diagnosing slow SwiftUI rendering, janky scrolling, high CPU, memory growth,
  excessive updates, or layout thrash.
- Implementing SwiftUI views, lists, images, layout, or animations where update
  fan-out, identity, or body cost is a primary concern.
- Reviewing a SwiftUI diff for performance risk.
- Checking invalidation scope, identity stability, heavy view-body work, image
  costs, animation scope, or observation fan-out.
- Producing a short performance review with likely causes and validation steps.

## When Not To Use

- Do not use for `.trace`, `xctrace`, Time Profiler, hangs, hitches, signposts,
  trace recording, or trace parsing; use `xcode-instruments`.
- Do not use for ordinary view cleanup with no performance symptom; use
  `swiftui-patterns`.
- Do not use for broad architecture selection; use `swiftui-architecture`.
- Do not claim performance improvement without measurement or a clearly stated
  source-level hypothesis.

## Inputs To Inspect

- Target SwiftUI view, model, and state-flow files.
- Symptom, reproduction path, device/simulator, OS, build configuration, and
  before/after observations when available.
- Existing screenshots, previews, tests, logs, benchmarks, or Instruments
  findings if already provided.

## Workflow

1. Classify the symptom: slow render, janky scroll, high CPU, memory growth,
   excessive updates, layout thrash, animation cost, or image cost.
2. Start code-first with `references/code-smells.md`.
3. Separate source-level suspicion from measured evidence.
4. Prefer targeted fixes: narrow state scope, stabilize identity, move heavy
   work out of `body`, downsample images, reduce layout complexity, and narrow
   animation scope.
5. If code review is inconclusive or runtime evidence is necessary, use
   `references/profiling-intake.md` and route trace capture/analysis to
   `xcode-instruments`.
6. Report likely causes, evidence, remediation, and validation steps.

## Reference Files To Consult

- `references/code-smells.md`: source-level SwiftUI performance smell catalog.
- `references/profiling-intake.md`: what runtime evidence to request before
  involving Instruments.
- `references/report-template.md`: compact review output shape.
- `../xcode-instruments/`: trace capture and analysis when needed.

## Decision Rules

- Code-first review is useful, but trace-backed evidence wins.
- Treat performance recommendations as hypotheses until validated.
- Identity, invalidation fan-out, and heavy `body` work are first-pass checks.
- Use `equatable()` only when equality is cheaper than recomputing the subtree.
- Do not store frequently changing values in broad environment dependencies.
- Do not use `@State` as an arbitrary cache for derived model work.

## Validation Rules

- Rebuild after source edits.
- Use previews, screenshots, `_logChanges()`, local benchmarks, or user-provided
  traces to validate the changed path.
- If runtime evidence is required, ask for the smallest trace that reproduces
  the symptom and route analysis to `xcode-instruments`.
- Keep before/after claims tied to the same interaction and build mode.

## Output Format

Return:

1. Phase / stage judgment
2. SwiftUI surface inspected
3. Symptom and evidence
4. Findings, ordered by likely impact
5. Recommended or applied changes
6. Measurement / validation plan
7. Risks and next steps

## Failure / Uncertainty Handling

- If no code is available, ask for the smallest target view/model slice and
  reproduction path.
- If the symptom cannot be explained from source, state that and request trace
  evidence through `xcode-instruments`.
- If performance is a secondary concern inside a larger refactor, keep the
  performance note short and route the main work to the relevant skill.
