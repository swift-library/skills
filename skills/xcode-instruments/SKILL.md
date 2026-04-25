---
name: xcode-instruments
description: Use this skill for Xcode Instruments and xctrace work involving .trace files, recording traces, analyzing traces, Time Profiler, Hangs, Animation Hitches, SwiftUI template traces, SwiftUI update lanes, signposts, os_log timestamps, performance windows, analyze_trace.py, record_trace.py, connected devices, simulator profiling, or correlating trace evidence to source-level performance findings. Do not use for source-only SwiftUI refactoring, general SwiftUI layout or state design, Swift Charts, Core Data, SwiftData, networking, package architecture, or repository documentation.
---

# Xcode Instruments

## Purpose

Guide Xcode Instruments and `xctrace` recording, analysis, and evidence-based
performance review. Use the bundled scripts for repeatable trace analysis and
recording when local Xcode tools are available.

## When To Use

- The user provides a path ending in `.trace`.
- The task mentions Xcode Instruments, `xctrace`, Time Profiler, Hangs,
  Animation Hitches, SwiftUI template traces, signposts, or `os_log`
  timestamps.
- Recording a trace by attaching to an app, launching an app, selecting a
  device, selecting an Instruments template, or time-boxing a profiling run.
- Correlating trace evidence with source-level performance findings.
- Focusing analysis on a time window, log message, signpost interval, hang, or
  hitch.

## When Not To Use

- Do not use for source-only SwiftUI performance review without trace or
  profiling evidence; use `swiftui-performance`.
- Do not use for source-only SwiftUI state, layout, navigation, accessibility,
  animation, or image refactoring without trace or profiling evidence; use the
  relevant source skill such as `swiftui-patterns` or `accessibility-patterns`.
- Do not use for Swift Charts; use `swift-charts-patterns`.
- Do not use for Core Data or SwiftData persistence design.
- Do not use for broad Swift Concurrency migration, actor-isolation design,
  `Sendable` fixes, or data-race work; use `swift-concurrency-patterns`.
- Do not use for networking architecture, package architecture, dependency
  replacement, or repository documentation.

## Inputs To Inspect

- `.trace` bundle path, requested time window, log text, signpost name, target
  process, device, simulator, or app bundle path.
- Source files only when the user asks to connect trace findings to code.
- Local Xcode tool availability: `xcrun xctrace`, connected devices, simulator
  targets, and Instruments templates.
- Project-local `AGENTS.md`, `README.md`, and performance or profiling docs.

## Workflow

1. Read local project truth first.
2. Decide whether this is trace analysis, trace recording, or source
   correlation from existing trace findings.
3. For analysis, open `references/trace-analysis.md` and prefer
   `scripts/analyze_trace.py`.
4. For recording, open `references/trace-recording.md` and prefer
   `scripts/record_trace.py`.
5. Use `--list-runs`, `--list-logs`, `--list-signposts`, and `--window` before
   full analysis when the user gives a specific run, event, log, or time span.
6. Keep trace-tool findings distinct from source-code recommendations. Route
   source-level SwiftUI performance fixes to `swiftui-performance`; route
   non-performance SwiftUI source fixes to the relevant source skill when they
   go beyond trace interpretation.
7. Report tool gaps explicitly when `xctrace`, devices, templates, or trace
   files are unavailable.

## Reference Files To Consult

- `references/trace-analysis.md`: analyze `.trace` bundles, list logs and
  signposts, choose run windows, and interpret Time Profiler, Hangs, Animation
  Hitches, SwiftUI updates, and cause graphs.
- `references/trace-recording.md`: record traces with `xctrace`, choose
  devices and templates, attach or launch apps, and stop recordings.

Use `references/_index.md` only when the needed reference is unclear.

## Scripts

- `scripts/analyze_trace.py`: parse and summarize existing `.trace` bundles.
- `scripts/record_trace.py`: wrap `xctrace record` for repeatable trace
  capture.

## Decision Rules

- Repository-local truth wins over this skill.
- Do not claim Instruments or `xctrace` evidence unless a trace or local tool
  output supports it.
- Prefer structured script output for analysis, then summarize the result for
  the user.
- Separate measured trace evidence from hypotheses.
- Use physical iOS/iPadOS devices or host Mac for the SwiftUI template lane;
  prefer Time Profiler for simulator recordings when the SwiftUI lane is not
  available.
- If source edits are needed after analysis, apply the relevant source-code
  skill for that area.

## Validation Rules

- Verify the `.trace` path exists before analysis.
- Run script help or tool discovery when command behavior is uncertain.
- Compile bundled Python scripts after editing them.
- For recording, confirm target device/template choices before long-running
  capture when feasible.

## Output Format

For reviews or profiling recommendations, return:

1. Phase / stage judgment
2. Trace or recording surface inspected
3. Findings
4. Recommended changes
5. Compatibility / tooling impact
6. Validation performed
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If `xctrace` is missing or unusable, state the exact tool gap and continue
  with any source-level review the user requested.
- If a trace has multiple runs, list the runs and ask for or choose the most
  relevant run based on the user request.
- If a trace lacks a SwiftUI lane, continue with available Time Profiler,
  Hangs, Animation Hitches, logs, and signposts, and report the missing lane.
