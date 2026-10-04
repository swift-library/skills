---
name: healthkit-patterns
description: Use this skill for HealthKit implementation and review across HKHealthStore setup, share/read authorization, health data availability, sample queries, statistics queries, observer and anchored object queries, background delivery, sample writing/deleting, units, workouts, HKWorkoutSession, HKLiveWorkoutBuilder, workout mirroring, HealthKit privacy, and health-chart data. Do not use for generic persistence, chart styling only, medical advice, or fitness product copy with no HealthKit behavior.
---

# HealthKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for HealthKit features that
request health-data authorization, query or write samples, handle background
updates, and manage workout sessions.

## When To Use

- Setting up HealthKit capability, usage strings, and `HKHealthStore`.
- Requesting read/share authorization and handling unavailable or denied data.
- Querying samples, statistics, statistics collections, observer updates,
  anchored object changes, or long-running update streams.
- Writing or deleting app-created samples.
- Implementing workout sessions, live workout builders, workout mirroring, or
  health-chart data pipelines.
- Debugging HealthKit units, source/device predicates, background delivery, or
  sensitive-data display.

## When Not To Use

- Do not use for generic persistence or sync with no HealthKit data.
- Do not use for chart visual styling only.
- Do not provide medical advice or clinical interpretation.
- Do not use for fitness marketing copy with no HealthKit implementation.
- Do not invent data-type availability, descriptor API behavior, background
  delivery behavior, or privacy requirements. Verify current Apple
  documentation and device behavior.

## Inputs To Inspect

- HealthKit capability, entitlements, usage strings, and target platforms.
- `HKHealthStore` availability checks, authorization requests, and type sets.
- Query descriptors, sample queries, statistics queries, observer queries,
  anchored object queries, anchors, and units.
- Sample writing/deletion, source/device predicates, and characteristic types.
- Workout configuration, `HKWorkoutSession`, `HKLiveWorkoutBuilder`, delegates,
  mirroring, and watch/iPhone coordination.
- Tests, device data availability, background delivery setup, and privacy UI.

## Workflow

1. Confirm HealthKit availability and platform/device support before requesting
   access.
2. Request the smallest read/share type set needed for the feature.
3. Treat read denial as ambiguous: HealthKit can return empty data without
   explaining whether the user denied access to a type.
4. Use query descriptors or explicit queries with bounded predicates, units,
   source filters, and anchor persistence.
5. For background delivery, pair observer queries with completion handling and
   test delivery on device.
6. For workouts, define the workout configuration, session lifecycle, builder,
   live data source, delegate handling, and sample association.
7. Keep health data display privacy-first and avoid logging sensitive samples.

## Review Rules

- Do not request broad health permissions for a narrow chart or feature.
- Do not assume HealthKit is available on every platform or device.
- Do not infer denial from empty query results alone.
- Do not write samples without clear provenance, units, and user intent.
- Do not miss observer-query completion handlers.
- Do not put sensitive health values into logs, analytics, or previews.

## Validation

- Build the affected app and watch targets if present.
- Test HealthKit unavailable, denied, partially authorized, and authorized
  states.
- Test queries with deterministic sample data and unit conversions.
- Test background delivery and observer completion on device when in scope.
- Test workout start, pause, resume, end, save, and mirroring paths when
  workout behavior changes.

## Output

For implementation or review work, return:

1. Health data types and authorization model
2. Query, unit, sample, and background-delivery findings
3. Workout-session findings, if applicable
4. Privacy and validation status
5. Current-source assumptions for data or platform behavior
