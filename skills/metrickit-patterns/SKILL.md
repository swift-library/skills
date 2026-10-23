---
name: metrickit-patterns
description: MetricKit telemetry implementation and review for MXMetricManager, metric/diagnostic payloads, crash and hang reports, signposts, JSON export, and delayed delivery. Not for Instruments trace recording or source-only performance refactoring.
---

# MetricKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for MetricKit telemetry in
Apple-platform apps. This skill owns runtime metrics and diagnostics delivered
by the system; interactive Instruments profiling and `.trace` analysis are out
of scope.

## When To Use

- Adding or reviewing `MXMetricManager` subscribers and payload handling.
- Processing `MXMetricPayload` or `MXDiagnosticPayload` reports.
- Interpreting app launch, runtime, CPU, memory, responsiveness, network,
  cellular, disk-write, crash, hang, CPU exception, or app-exit diagnostics.
- Capturing custom signpost metrics and correlating them with runtime payloads.
- Persisting payloads, exporting JSON, uploading to a backend, or correlating
  with Xcode Organizer.
- Designing redaction and sampling policies for performance diagnostics.
- Inspecting `MXMetricManagerSubscriber`, `MXCallStackTree`,
  `MXSignpostMetric`, and delayed telemetry delivery.

## When Not To Use

- Do not use for recording or parsing Instruments `.trace` bundles.
- Do not use for source-only SwiftUI or general performance refactors without
  MetricKit payloads.
- Do not use for generic analytics event taxonomy unless MetricKit payloads are
  part of the event pipeline.
- Do not use for crash-reporting SDK setup unless MetricKit diagnostics are in
  scope.

## Inputs To Inspect

- App lifecycle setup for `MXMetricManager.shared`, subscriber registration,
  subscriber removal, and launch timing.
- Subscriber callbacks, payload persistence, JSON export, backend upload, and
  retry behavior.
- Metric and diagnostic categories used by the feature: launch, CPU, memory,
  responsiveness, network, cellular, disk, crash, hang, and app exit.
- `MXCallStackTree` handling, symbolication/correlation workflow, privacy
  filtering, and payload retention.
- Custom signpost metric setup and any Xcode Organizer or backend dashboards.

## Workflow

1. Confirm the task is MetricKit telemetry, not interactive Instruments
   profiling.
2. Check the deployment target before choosing the API family. The iOS 27 and
   macOS 27 SDKs mark the Objective-C `MX*` manager, subscriber, and payload
   types as to be deprecated and name Swift `MetricManager`
   (`metricReports`, `diagnosticReports`), `MetricReport`, `DiagnosticReport`,
   and `CallStackTree` as replacements. Keep `MX*` code for earlier deployment
   targets.
3. Register subscribers early enough for the app lifecycle being measured.
4. Persist payloads before expensive processing or upload so delivery is not
   lost during app termination.
5. Keep metrics and diagnostics separate: metrics are aggregate reports, while
   diagnostics are issue-specific payloads with stack and context data.
6. Export JSON or dictionaries only after deciding what data must be redacted,
   sampled, retained, or uploaded.
7. Correlate MetricKit payloads with app versions, build numbers, device/OS
   metadata, signposts, and source changes.
8. For custom metrics, verify signpost category/name consistency and avoid
   over-instrumenting hot paths.
9. Treat delivery timing, diagnostic availability, stack formats, and Organizer
   behavior as current-documentation and local-device gated.

## Review Rules

- Do not claim real performance results unless a MetricKit payload, Organizer
  report, or local device run supports them.
- Do not block app launch or foreground responsiveness while processing
  payloads.
- Do not upload raw stack traces, paths, identifiers, or user-correlatable data
  without redaction and product approval.
- Do not replace trace-based root-cause work with MetricKit aggregates when a
  precise local profile is needed.
- Do not assume payload delivery is immediate or available in development runs.

## Validation

- Build the affected app targets and confirm subscriber setup compiles.
- Test subscriber registration/removal and payload persistence paths.
- Exercise JSON export and backend upload with fixture payloads or locally
  captured reports when available.
- Verify redaction, retry, and retention behavior.
- Cross-check any actionable performance conclusion with Xcode Organizer,
  Instruments, logs, or source code when the payload alone is insufficient.

## Output

Return:

1. MetricKit surface and Instruments boundary
2. Subscriber, payload, persistence, and upload findings
3. Metrics/diagnostics interpretation
4. Privacy and retention concerns
5. Validation run or still needed
