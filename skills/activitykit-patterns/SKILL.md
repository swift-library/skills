---
name: activitykit-patterns
description: Use this skill for ActivityKit implementation and review across Live Activities, Dynamic Island, ActivityAttributes, ActivityContent, request/update/end lifecycle, stale dates, relevance, WidgetKit Live Activity UI, push tokens, APNs liveactivity payloads, push-to-start, frequent updates, and device testing. Do not use for widget visual polish only, ordinary notifications, broad SwiftUI architecture, market messaging, or release operations.
---

# ActivityKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for Live Activities that
share current app state through ActivityKit, WidgetKit, SwiftUI, and optional
ActivityKit push notifications.

## When To Use

- Creating, updating, ending, or debugging Live Activities.
- Defining `ActivityAttributes`, `ContentState`, `ActivityContent`, stale
  dates, relevance scores, dismissal behavior, or activity authorization.
- Building Live Activity UI for Lock Screen, Dynamic Island, Smart Stack, Mac,
  or CarPlay surfaces.
- Handling ActivityKit push tokens, remote update payloads, push-to-start, or
  frequent update behavior.
- Reviewing state observation, cleanup, multiple active activities, or device
  test coverage.

## When Not To Use

- Do not use for widget visual review only; use `widgetkit-design`.
- Do not use for ordinary local or remote notifications with no Live Activity;
  use `user-notifications-patterns`.
- Do not use for broad SwiftUI feature architecture unless the Live Activity is
  the main surface.
- Do not use for App Store listing, market messaging, pricing, or release
  operations.
- Do not invent payload limits, cross-device behavior, or platform availability.
  Verify current Apple documentation and the local SDK for version-specific
  ActivityKit behavior.

## Inputs To Inspect

- App target, widget extension target, entitlements, capabilities, and
  `Info.plist` keys for Live Activities.
- `ActivityAttributes`, `ContentState`, request/update/end code, and activity
  observation.
- Widget extension Live Activity configuration and SwiftUI layouts.
- APNs liveactivity server code, payload examples, token handling, and logs.
- Device testing notes, simulator limitations, and fallback UI.

## Workflow

1. Identify the activity type, user-visible duration, update source, and
   interaction surface.
2. Confirm the app and widget extension are configured for Live Activities.
3. Keep static attributes separate from dynamic `ContentState`, and make state
   small, codable, and non-sensitive.
4. Request activities with explicit initial content, stale date, relevance, and
   push type when remote updates are needed.
5. Implement update and end flows with predictable cleanup and dismissal
   behavior.
6. Build Lock Screen and Dynamic Island layouts for the supported families
   without hiding critical state in one presentation only.
7. Handle push token rotation, remote payload shape, APNs headers, delivery
   errors, and push-to-start boundaries when a server is involved.
8. Validate on device whenever the task depends on Live Activity presentation,
   Dynamic Island behavior, push delivery, or frequent updates.

## Review Rules

- Do not put secrets, credentials, precise private data, or bulky payloads in
  activity state.
- Do not treat Live Activities as background execution. The UI reflects state;
  it does not keep the app running.
- Always account for stale state, ended state, denied authorization, and missing
  push tokens.
- Keep WidgetKit UI code separate from state production and server update
  logic.
- Prefer a small number of meaningful concurrent activities over many
  overlapping activities.
- Treat APNs liveactivity headers and payload fields as current-documentation
  gated.

## Validation

- Build app and widget extension targets.
- Start, update, and end a Live Activity locally.
- Test denied authorization, stale state, app relaunch, and cleanup paths.
- Test push token receipt and remote update delivery when server updates are in
  scope.
- Exercise all supported Live Activity presentations on real hardware when
  layout or push behavior matters.

## Output

For implementation or review work, return:

1. Activity type and update source
2. Target/capability/configuration status
3. State model and lifecycle findings
4. UI surface and push delivery findings
5. Validation run or still needed
