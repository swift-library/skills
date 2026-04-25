---
name: user-notifications-patterns
description: Use this skill for UserNotifications and APNs implementation and review across notification authorization, local notifications, remote push registration, APNs token handling, payload fields, silent/background pushes, foreground and tap handling, categories, actions, badges, localization keys, notification service/content extensions, delivery debugging, and simulator/device testing. Do not use for marketing push copy alone, App Store release operations, Live Activities, or simulator operation with no notification implementation change.
---

# User Notifications Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple-platform local and
remote notifications using UserNotifications, APNs, notification extensions,
and app routing code.

## When To Use

- Requesting, reviewing, or debugging notification authorization and settings.
- Scheduling local notifications or handling remote push notifications.
- Registering for APNs, handling device token rotation, and diagnosing delivery
  failures.
- Designing payload handling for alerts, badges, sounds, silent/background
  pushes, localization keys, categories, and actions.
- Building notification service or content extensions.
- Routing foreground notifications, notification taps, deep links, or app state
  updates.

## When Not To Use

- Do not use for push marketing copy or campaign planning; use the market
  operations collection.
- Do not use for Live Activities or ActivityKit push updates; use
  `activitykit-patterns`.
- Do not use for simulator lifecycle, screenshots, or device management alone;
  use `ios-simulator`.
- Do not use for release signing or provisioning profile work alone; use
  `apple-platform-release`.
- Do not invent APNs headers, payload fields, entitlement requirements, or
  platform delivery behavior. Verify current Apple documentation and device
  behavior for version-specific claims.

## Inputs To Inspect

- Notification capability, entitlements, provisioning, bundle IDs, and
  environment.
- `UNUserNotificationCenter` authorization, settings, delegate, scheduling, and
  response handling code.
- APNs registration, token upload, server payload generation, and delivery logs.
- Notification categories, actions, localization, badge handling, and deep-link
  routing.
- Notification service/content extension targets, App Group sharing, and media
  attachment handling.

## Workflow

1. Identify notification type: local alert, remote alert, silent/background
   push, communication notification, extension-modified alert, or badge update.
2. Confirm capabilities, entitlements, environment, bundle ID, and APNs token
   registration path.
3. Review authorization flow before scheduling or sending notifications. Handle
   denied, provisional, ephemeral, critical alert, and settings changes only
   when applicable to the app.
4. Keep payloads small, non-sensitive, and explicit about category, thread,
   collapse, badge, sound, localization, mutable content, and content-available
   behavior.
5. Route foreground delivery, tap handling, action handling, and deep links
   through app navigation that is safe for cold launch and resumed state.
6. Use service extensions only when the app must decrypt, download, or modify
   notification content before display.
7. Validate with local scheduling, simulator push, APNs console, command-line
   APNs, or device delivery logs depending on the failure.

## Review Rules

- Do not place secrets or sensitive private data in notification payloads.
- Do not assume a push arrives, arrives once, arrives in order, or launches the
  app immediately.
- Do not upload APNs tokens before user/account context is ready to associate
  them correctly.
- Keep notification tap routing idempotent and safe from any app lifecycle
  state.
- Keep notification extension time, memory, network, and App Group constraints
  explicit.
- Treat critical alerts, communication notifications, and background pushes as
  entitlement and current-policy gated.

## Validation

- Build the affected app and extension targets.
- Check authorization state and settings transitions.
- Test a local notification when local scheduling changes.
- Test simulator or device push delivery when APNs payloads, registration, or
  routing changes.
- Test foreground handling, tap handling, action responses, badge changes, and
  extension modification where applicable.

## Output

For implementation or review work, return:

1. Notification type and delivery path
2. Authorization, entitlement, and token status
3. Payload, routing, and extension findings
4. Delivery validation run or still needed
5. Current-source assumptions for APNs or entitlement behavior
