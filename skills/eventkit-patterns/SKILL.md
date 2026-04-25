---
name: eventkit-patterns
description: Use this skill for EventKit and EventKitUI implementation and review across EKEventStore, calendar and reminder authorization, full versus write-only calendar access, usage-description keys, event/reminder CRUD, predicates, recurrence rules, alarms, writable calendar selection, EKEventStoreChanged, EventKitUI editors/viewers, and SwiftUI wrappers. Do not use for generic scheduling models, notification delivery, interface copy only, or calendar server backends with no EventKit behavior.
---

# EventKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for calendar and reminder
features that use EventKit and EventKitUI inside Apple-platform apps.

## When To Use

- Requesting or reviewing calendar/reminder access with `EKEventStore`.
- Choosing full calendar access, write-only calendar access, reminder access,
  or EventKitUI flows that need no direct data fetch.
- Creating, fetching, editing, deleting, or saving calendar events and reminders.
- Handling recurrence, alarms, structured locations, calendar selection,
  writable-calendar filtering, batching, or database-change notifications.
- Wrapping `EKEventViewController`, `EKEventEditViewController`, or
  `EKCalendarChooser` in SwiftUI.

## When Not To Use

- Do not use for generic scheduling data models that do not touch EventKit.
- Do not use for notification delivery; use `user-notifications-patterns`.
- Do not use for copywriting permission prompts only; use `interface-writing`.
- Do not use for CalDAV/server calendar sync unless EventKit app behavior is in
  scope.
- Do not invent access-level behavior, deprecated request behavior, or
  EventKitUI platform limits. Verify current Apple documentation and local SDK.

## Inputs To Inspect

- `Info.plist` usage-description keys and target platform.
- `EKEventStore` lifecycle, authorization checks, request calls, and ownership.
- Event/reminder fetch predicates, save/delete flows, recurrence, alarms,
  calendars, sources, and commits.
- EventKitUI controllers, SwiftUI wrappers, dismissal, delegates, and selected
  calendar state.
- Tests, simulator/device calendar data, permission state, and database-change
  handling.

## Workflow

1. Identify whether the app needs to create only, read and write events, manage
   reminders, or present EventKitUI without direct data access.
2. Choose the narrowest calendar/reminder access level and matching
   usage-description key.
3. Own one event store consistently for related objects. Do not mix EventKit
   objects from different stores.
4. Use predicates for date ranges or reminders, and handle empty results,
   authorization changes, and stale object identifiers.
5. Save/delete with explicit span, commit, rollback, and error handling when
   batching changes.
6. Listen for `EKEventStoreChanged` when external Calendar changes affect app
   state.
7. Validate full, write-only, denied, and no-calendar states as applicable.

## Review Rules

- Do not request full calendar access when write-only access or EventKitUI is
  enough.
- Do not fetch all events without a bounded predicate.
- Do not reuse `EKObject` instances across different event stores.
- Do not assume saved event identifiers remain valid forever.
- Do not ignore recurrence span when editing or deleting repeating events.
- Keep SwiftUI wrapper dismissal and delegate ownership explicit.

## Validation

- Build the affected app target.
- Test access-level transitions: not determined, denied, write-only, full, and
  reminder access where applicable.
- Test create, edit, delete, recurrence, alarm, and calendar-selection paths.
- Test `EKEventStoreChanged` refresh behavior when external Calendar changes are
  relevant.
- Test EventKitUI presentation and dismissal on the target platforms.

## Output

For implementation or review work, return:

1. Event/reminder access model
2. Event store ownership and CRUD findings
3. EventKitUI, recurrence, and notification findings
4. Validation run or still needed
5. Current-source assumptions for access-level behavior
