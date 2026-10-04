---
name: group-activities-patterns
description: Use this skill for GroupActivities and SharePlay implementation and review across GroupActivity, GroupSession, GroupSessionMessenger, GroupActivitySharingController, synchronized media playback, participant tracking, GroupSessionJournal, nearby participants, FaceTime/iMessage group experiences, entitlement setup, and session lifecycle. Do not use for generic multiplayer networking, CallKit, AVKit-only playback, or ordinary collaboration UI without GroupActivities.
---

# Group Activities Patterns

## Purpose

Guide implementation, review, and troubleshooting for GroupActivities framework
work, including SharePlay session lifecycle, synchronized state, and group
media/collaboration experiences.

## When To Use

- Defining a `GroupActivity` and activity metadata for a shareable experience.
- Listening for, joining, leaving, or ending `GroupSession` instances.
- Sending and receiving typed messages with `GroupSessionMessenger`.
- Coordinating synchronized media playback or collaborative state during a
  SharePlay session.
- Presenting `GroupActivitySharingController` or system sharing UI.
- Using `GroupSessionJournal`, participant tracking, nearby participants, or
  FaceTime/iMessage group-session behavior.

## When Not To Use

- Do not use for generic multiplayer networking; use the app's networking or
  game-specific owner.
- Do not use for CallKit call lifecycle.
- Do not use for AVKit-only playback without GroupActivities synchronization.
- Do not use for generic collaboration UI that does not create or join a group
  session.

## Inputs To Inspect

- Entitlements, Info.plist keys, activity identifiers, metadata, and eligibility
  checks.
- `GroupActivity` definitions, activation calls, and `sessions()` listeners.
- Session owner lifetime, `join()`, `leave()`, `end()`, state observation, and
  participant handling.
- Messenger message types, delivery mode, large-data handling, and
  cancellation.
- Media coordination, sharing UI, journal/file-transfer behavior, and view
  lifetime.

## Workflow

1. Confirm the task needs GroupActivities rather than generic networking or
   playback.
2. Verify current platform, entitlement, and API availability before promoting
   the feature path.
3. Keep session observation outside transient recreated views.
4. Join sessions only after app state is ready, and leave or end sessions
   intentionally.
5. Store `GroupSessionMessenger` for the lifetime of the session and define
   typed messages with explicit delivery expectations.
6. Keep large payloads out of the messenger; use journal or app-specific
   transfer/storage paths when appropriate.
7. Validate participant state, reconnect/invalidation behavior, sharing UI, and
   synchronized media/state transitions.

## Review Rules

- Do not treat SharePlay as a generic socket or peer-to-peer transport.
- Do not start session listeners from view bodies or other short-lived scopes.
- Do not assume all participants are active, nearby, or on the same platform.
- Do not send sensitive user content through session messages without an
  explicit product need and retention boundary.
- Treat platform availability, session-sharing UI, media coordination, and
  journal behavior as current Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test eligible and ineligible states, activation, session delivery, join,
  leave, end, invalidation, participant changes, and message send/receive.
- Test synchronized media or collaboration behavior with multiple devices or
  simulator/device combinations when possible.

## Output

For implementation or review work, return:

1. GroupActivities versus networking/playback boundary decision
2. Activity, session, and participant lifecycle findings
3. Messenger, journal, and synchronized-state findings
4. Sharing UI and entitlement assumptions
5. Validation run or still needed
