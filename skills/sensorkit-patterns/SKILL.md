---
name: sensorkit-patterns
description: Use this skill for SensorKit implementation and review across SRSensorReader, SRSensor, SRFetchRequest, SRFetchResult, sensor authorization, com.apple.developer.sensorkit.reader.allow entitlement, research-study approval, user consent, sample fetches, deletion records, ambient light, device usage, keyboard metrics, messages/phone usage, visits, wrist detection, speech metrics, face metrics, wrist temperature, ECG, PPG, and high-sensitivity data handling. Do not use for Core Motion app sensors, HealthKit samples, general analytics, or non-research sensor access.
---

# SensorKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for SensorKit research data
access, entitlements, authorization, sample fetching, deletion records, and
high-sensitivity sensor-derived metrics.

## When To Use

- Configuring SensorKit reader entitlements and project metadata for approved
  sensor access.
- Using `SRSensorReader`, `SRSensor`, `SRFetchRequest`, `SRFetchResult`, or
  deletion records.
- Requesting authorization and fetching approved sensor data such as ambient
  light, device usage, keyboard metrics, visits, wrist detection, speech/face
  metrics, wrist temperature, ECG, or PPG.
- Reviewing privacy, consent, storage, research-study boundaries, and data
  minimization for SensorKit data.

## When Not To Use

- Do not use for ordinary accelerometer, gyroscope, pedometer, or motion data;
  use `core-motion-patterns`.
- Do not use for HealthKit samples, workouts, or health authorization; use
  `healthkit-patterns`.
- Do not use for general analytics or non-research sensor access.
- Do not use for product telemetry without SensorKit APIs.
- Do not invent entitlement eligibility, sensor availability, or approval
  status. Verify current Apple documentation and project entitlement state.

## Inputs To Inspect

- Entitlement state, approved sensors, app metadata, research-study
  assumptions, usage descriptions, and consent flows.
- `SRSensorReader`, authorization requests, fetch requests, sample processing,
  deletion records, and error handling.
- Storage, retention, deidentification, export, logs, analytics, and user data
  deletion paths.
- Device/Apple Watch assumptions, test plan, and unsupported-state UI.

## Workflow

1. Confirm the task is approved SensorKit data access, not ordinary Core Motion
   or HealthKit work.
2. Verify entitlement and approved sensor list before designing the feature.
3. Request authorization only with clear research/user value and sensor scope.
4. Keep fetch windows bounded and handle no data, denied, revoked, deleted, and
   unavailable states.
5. Minimize, protect, and retain SensorKit data only as long as the study needs.
6. Keep deletion records and user revocation behavior visible in the data
   pipeline.
7. Validate with devices and accounts that match the approved study setup.

## Review Rules

- Do not treat SensorKit as a general-purpose analytics API.
- Do not access sensors that are not approved in the entitlement.
- Do not log raw high-sensitivity sensor data.
- Do not ignore deletion records or consent revocation.
- Treat entitlement, approval, sensor list, and sample schema behavior as
  current-source gated.

## Validation

- Build the affected app target.
- Verify entitlement and sensor metadata in the signed app.
- Test authorization requested, denied, granted, revoked, no data, deleted
  samples, and unavailable sensors.
- Test fetch bounds, pagination/streaming, storage, and deletion handling.
- Inspect logs, exports, and analytics for accidental raw data leakage.

## Output

For implementation or review work, return:

1. SensorKit entitlement, sensor, and study assumptions
2. Authorization, fetch, deletion, and sample-processing findings
3. Core Motion, HealthKit, privacy, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for SensorKit eligibility or behavior
