---
name: core-motion-patterns
description: Use this skill for Core Motion implementation and review across CMMotionManager, CMDeviceMotion, accelerometer, gyroscope, magnetometer, attitude reference frames, CMPedometer, CMMotionActivityManager, CMAltimeter, CMHeadphoneMotionManager, CMWaterSubmersionManager, NSMotionUsageDescription, NSFallDetectionUsageDescription, availability checks, sampling intervals, live updates, historical queries, sensor fusion, and battery/privacy tradeoffs. Do not use for HealthKit samples, SensorKit research data access, Core Location, or generic animation.
---

# Core Motion Patterns

## Purpose

Guide implementation, review, and troubleshooting for Core Motion sensor data,
device motion, pedometer/activity updates, altimeter data, headphone motion,
submersion data, and motion-related privacy/performance behavior.

## When To Use

- Using `CMMotionManager`, accelerometer, gyroscope, magnetometer,
  `CMDeviceMotion`, attitude reference frames, or sensor fusion data.
- Querying or streaming `CMPedometer`, `CMMotionActivityManager`,
  `CMAltimeter`, headphone motion, or water submersion data.
- Reviewing `NSMotionUsageDescription`, `NSFallDetectionUsageDescription`,
  availability checks, sampling intervals, queues, and battery use.
- Debugging simulator/device differences, noisy data, coordinate frames,
  smoothing, and lifecycle cleanup.

## When Not To Use

- Do not use for HealthKit samples, workouts, or health authorization; use
  `healthkit-patterns`.
- Do not use for SensorKit research-study data access; use
  `sensorkit-patterns`.
- Do not use for Core Location, maps, or geofencing unless motion APIs are the
  concrete issue.
- Do not use for generic SwiftUI animation or gesture design.
- Do not invent sensor availability, platform behavior, or permission rules.
  Verify current Apple documentation and physical device behavior.

## Inputs To Inspect

- Usage-description keys, platform targets, device assumptions, and data
  retention/logging policy.
- Motion manager, sensor availability checks, update intervals, queues,
  start/stop lifecycle, and data smoothing code.
- Pedometer/activity/altimeter/headphone/submersion query and live update code.
- Tests, device logs, battery/performance evidence, and fallback UI.

## Workflow

1. Classify the motion source: raw sensors, processed device motion, pedometer,
   activity, altitude, headphone motion, or specialized watch data.
2. Check availability and usage-description keys before starting services.
3. Choose sampling interval and queue based on product need, not maximum rate.
4. Keep start/stop lifecycle explicit and tie it to view/app lifecycle.
5. Normalize coordinate frames, reference frames, units, smoothing, and
   timestamp handling at the boundary.
6. Keep sensitive movement data out of logs and analytics unless explicitly
   needed.
7. Validate on physical devices representative of the target feature.

## Review Rules

- Do not access motion APIs without required usage-description keys.
- Do not sample continuously when event- or query-based APIs fit the task.
- Do not assume simulator data proves sensor behavior.
- Do not mix HealthKit, SensorKit, and Core Motion ownership.
- Treat specialized sensors, watch behavior, and visionOS support as
  current-source gated.

## Validation

- Build the affected app target.
- Test unavailable, denied, stopped, backgrounded, high-rate, low-rate, and
  lifecycle cleanup paths.
- Test physical device orientation, movement, stationary/noise, and negative
  cases.
- Test pedometer/activity/altimeter historical query boundaries when in scope.
- Inspect battery, CPU, and logs for long-running sensor features.

## Output

For implementation or review work, return:

1. Core Motion sensor surface, permission, and platform assumptions
2. Sampling, lifecycle, coordinate, and data-processing findings
3. HealthKit, SensorKit, privacy, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for sensor behavior
