# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Xcode Instruments

- `trace-analysis.md`: analyze existing `.trace` bundles, list runs, logs,
  signposts, and focus windows, then interpret Time Profiler, Hangs,
  Animation Hitches, SwiftUI lanes, and cause graphs.
- `trace-recording.md`: record new traces with `xctrace`, attach or launch
  apps, choose devices and templates, stop recordings, and handle common
  recording failures.

## Symptom Routing

- User provided a `.trace` path: `trace-analysis.md`.
- User asks for hangs, hitches, jank, slow view, or source correlation from a
  trace: `trace-analysis.md`.
- User asks to focus before, after, between, or during a log or signpost:
  `trace-analysis.md`.
- User asks to record, profile, attach, launch, list devices, or list
  Instruments templates: `trace-recording.md`.
- Source-only SwiftUI performance issue without trace evidence: out of scope.
