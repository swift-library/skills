---
name: background-tasks-patterns
description: BackgroundTasks implementation and debugging for BGTaskScheduler, BGAppRefreshTask, BGProcessingTask, BGContinuedProcessingTask, Info.plist registration, expiration, and completion. Not for ordinary async/await, URLSession-only transfers, or push payload design.
---

# Background Tasks Patterns

## Purpose

Guide implementation, review, and troubleshooting for BackgroundTasks
scheduling, registration, launch handling, expiration, completion, and app
lifecycle correctness.

## When To Use

- Setting up or reviewing `BGTaskScheduler`, `BGTaskRequest`,
  `BGAppRefreshTask`, `BGProcessingTask`, `BGContinuedProcessingTask`, or
  SwiftUI `.backgroundTask`.
- Debugging permitted identifiers, Info.plist configuration, registration
  timing, scheduling errors, expiration, missed completion, or debug launches.
- Coordinating background URLSession events, background push triggers,
  checkpointing, or foreground work that can continue briefly in the
  background.
- Reviewing user expectations around OS scheduling and graceful stale data.
- Reviewing UIKit registration and `setTaskCompleted` lifecycle handling.

## When Not To Use

- Do not use for ordinary async/await, actors, or cancellation without OS
  background scheduling.
- Do not use for URLSession transfer implementation when scheduling is not the
  issue.
- Do not use for notification payload design.
- Do not use for broad app architecture without a concrete background lifecycle
  concern.
- Do not invent scheduling guarantees, background duration, GPU access, or
  platform behavior. Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- Check `BGTaskSchedulerPermittedIdentifiers` and `UIBackgroundModes`:
  app refresh requires `fetch`; processing requires `processing`.
- Info.plist permitted identifiers, background modes, capabilities, and target
  deployment settings.
- Task registration, scheduling, launch handler, expiration handler,
  cancellation, completion, and rescheduling code.
- SwiftUI app lifecycle or UIKit app delegate integration.
- Work checkpoints, persistence, idempotency, background URLSession callbacks,
  push triggers, and logging.
- Debug launch commands, device logs, Energy reports, and failed scheduling
  errors.

## Workflow

1. Classify the background work: app refresh, processing, continued foreground
   work, URLSession handoff, or push-triggered work.
2. Confirm identifiers, Info.plist keys, capabilities, registration timing, and
   task type before changing business logic.
3. Keep work idempotent, resumable, cancellable, and checkpointed.
4. Always install expiration handling and call `setTaskCompleted` exactly once
   for each launched task path.
5. Reschedule intentionally after successful or failed runs when the product
   expects repeated work.
6. Treat OS scheduling as opportunistic. Provide visible stale/offline states
   instead of promising exact run times.
7. Use device logs and debugger launch tools to prove the task actually starts.

## Review Rules

- Register each identifier once; duplicate registration kills the app. Finish
  registration before app launch ends, except for continued-processing tasks.
- Pending requests are limited to one refresh and ten processing tasks;
  submitting a request for an already queued task replaces that request.
- On iOS/tvOS 27+, use `try await submitTaskRequest(_:)` or its completion form;
  the older synchronous submission API is deprecated because it misses errors.
- `BGContinuedProcessingTask` is available on iOS 26+ and must report progress
  through `NSProgressReporting`; apparently stalled work may be expired.
- Background GPU requests require checking `BGTaskScheduler.supportedResources`
  and the `com.apple.developer.background-tasks.continued-processing.gpu` entitlement.
- Do not schedule identifiers that are missing from permitted identifiers.
- Do not register tasks too late in app lifecycle.
- Do not assume a task runs at a requested time or runs at all.
- Do not leave background work unbounded or uncheckpointed.
- Do not hide network, power, or user-force-quit constraints behind generic
  errors.
- Treat `BGContinuedProcessingTask`, background GPU access, and platform
  scheduling behavior as current-source gated.

## Validation

- Build the affected app target.
- Verify Info.plist identifiers and background modes.
- Run debug launch/termination flows for each task type when feasible.
- Test expiration, cancellation, failure, reschedule, and app relaunch paths.
- Test background URLSession and push coordination when those surfaces are in
  scope.

## Output

For implementation or review work, return:

1. Background task type, identifiers, and registration status
2. Scheduling, expiration, checkpointing, and completion findings
3. URLSession, push, lifecycle, and user-state boundaries
4. Validation run or still needed
5. Current-source assumptions for scheduling or platform behavior
