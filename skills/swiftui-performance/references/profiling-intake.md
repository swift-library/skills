# SwiftUI Profiling Intake

Use this file when source review is inconclusive or the user already has
runtime evidence.

## Ask For

- Exact interaction that reproduces the issue.
- Device or simulator, OS version, build configuration, and deployment target.
- Xcode/Swift compiler and SDK versions; distinguish build-time type checking
  from runtime update or scrolling symptoms.
- Target view and data volume.
- Whether the symptom is CPU, memory, scrolling, hang, hitch, or excessive
  updates.
- Existing screenshots, logs, `_logChanges()` output, benchmarks, or trace
  notes.

## Route To Instruments

Escalate to Instruments trace work, which is outside this skill, when the task
needs:

- `.trace` recording or parsing.
- Time Profiler, Hangs, Animation Hitches, signposts, or os_log analysis.
- Measured main-thread coverage, hitch duration, fan-in, or timeline evidence.

Keep this skill responsible for mapping source-level findings to likely fixes.

For SwiftUI update costs, distinguish a long body evaluation from many short
updates. Capture the same interaction, data volume, device and build mode before
and after the fix. Follow Cause & Effect paths when available, then recapture
after each targeted fix: one recording may expose only one changing dependency.
