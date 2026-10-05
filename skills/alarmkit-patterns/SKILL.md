---
name: alarmkit-patterns
description: Use this skill for AlarmKit implementation and review across authorization, AlarmManager, alarm versus timer decisions, Alarm.Schedule, scheduling/configuration, state observation, countdowns, AlarmAttributes, AlarmPresentation, AlarmPresentationState, AlarmButton, stop/snooze/secondary actions, Live Activity/widget extension wiring, and Info.plist setup. Do not use for EventKit calendar alarms, generic local notifications, or ActivityKit-only UI without AlarmKit scheduling.
---

# AlarmKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for AlarmKit alarms and
countdown timers with system-managed alarm UI, authorization, state observation,
and Live Activity presentation wiring.

## When To Use

- Requesting AlarmKit authorization and configuring Info.plist usage text.
- Scheduling one-time alarms, repeating alarms, timers, or countdowns with
  `AlarmManager` and `Alarm.Schedule`.
- Building `AlarmAttributes`, `AlarmPresentation`, `AlarmPresentationState`,
  and `AlarmButton` content.
- Handling stop, snooze, countdown, secondary actions, and App Intent actions.
- Observing alarm updates, persisting identifiers, and reconciling missing
  one-shot alarms.
- Wiring widget extensions or Live Activity presentation for countdown states.

## When Not To Use

- Do not use for EventKit calendar/reminder alarms.
- Do not use for generic local notifications.
- Do not use for ActivityKit UI alone without AlarmKit scheduling.
- Do not treat AlarmKit timers as a background execution mechanism.

## Inputs To Inspect

- `NSAlarmKitUsageDescription`, authorization flow, and deployment target.
- Alarm IDs, schedule configuration, countdown duration, metadata, and
  presentation state.
- `AlarmManager` calls, alarm update observation, cancellation, pause/resume,
  snooze, and stop handling.
- Widget extension, ActivityKit attributes, and App Intent action wiring.
- Persistence used to reconcile fired, missing, or canceled alarms.

## Workflow

1. Confirm the feature needs AlarmKit rather than EventKit or notifications.
2. Verify current OS availability, authorization behavior, and presentation
   requirements before making claims.
3. Request or handle authorization before scheduling, and provide a valid usage
   description.
4. Choose alarm, repeating alarm, timer, or countdown semantics explicitly.
5. Persist alarm IDs and any app-side model needed to reconcile daemon state.
6. Subscribe to alarm updates and handle fired, stopped, paused, resumed,
   snoozed, canceled, and missing states.
7. Add widget extension support when countdown presentation requires it.

## Review Rules

- Do not confuse EventKit alarms with AlarmKit alarms.
- Do not schedule alarms without handling denied authorization and invalid
  scheduling errors.
- Do not assume an alarm missing from updates is still scheduled.
- Build alert presentations with
  `AlarmPresentation.Alert(title:secondaryButton:secondaryButtonBehavior:)`.
  Initializers that take `stopButton:` are deprecated as of iOS 26.1; the
  system provides the stop control. Apps that deploy to iOS 26.0 keep the
  older initializer behind `if #available(iOS 26.1, *)`.
- Do not put sensitive user content into alarm metadata or logs.
- Treat Dynamic Island, Lock Screen, StandBy, paired watch forwarding, widget
  extension needs, and OS availability as current Apple documentation and SDK
  gated.

## Validation

- Build the app and widget extension targets.
- Test authorized, denied, schedule, fire, stop, snooze, pause/resume,
  cancellation, one-shot reconciliation, repeating schedules, and countdown
  presentation paths.
- Test device presentation when simulator behavior cannot prove the alarm path.

## Output

For implementation or review work, return:

1. AlarmKit versus EventKit/notification boundary decision
2. Authorization, schedule, and identifier findings
3. Presentation, button, App Intent, and widget-extension findings
4. State observation and reconciliation findings
5. Validation run or still needed
