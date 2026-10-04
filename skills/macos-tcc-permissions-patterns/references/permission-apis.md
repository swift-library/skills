# Permission APIs

This reference records public API entry points verified against the local
MacOSX26.4.sdk headers on 2026-05-24. Recheck SDK headers or official Apple
documentation before changing availability rules.

## Screen Recording / Screen Capture

Use CoreGraphics when the app needs to capture the screen or enumerate windows
with protected detail.

```swift
import CoreGraphics

let hasAccess = CGPreflightScreenCaptureAccess()
if !hasAccess {
    CGRequestScreenCaptureAccess()
}
```

SDK evidence:

- `CGPreflightScreenCaptureAccess()` is available on macOS 10.15+.
- `CGRequestScreenCaptureAccess()` is available on macOS 10.15+.

Review notes:

- Requesting may route the user through system UI; it does not grant access by
  itself.
- If the user has denied access, open System Settings and provide manual
  recovery instructions.
- Some apps need a relaunch before screen-capture APIs reflect a new grant.

## Accessibility

Use HIServices / ApplicationServices for Accessibility trust checks.

```swift
import ApplicationServices

let options = [
    kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true
] as CFDictionary

let trusted = AXIsProcessTrustedWithOptions(options)
```

SDK evidence:

- `AXIsProcessTrustedWithOptions(_:)` is available on macOS 10.9+.
- `kAXTrustedCheckOptionPrompt` is available on macOS 10.9+.
- `AXIsProcessTrusted()` exists for checks without prompting.

Review notes:

- Do not depend on Accessibility API inspection to guide the first-time
  Accessibility-permission path; it may be exactly what is missing.
- If the app needs global key event monitoring, AppKit headers note that key
  events require Accessibility trust.

## Input Monitoring / Listen Event

Use IOKit HID access APIs for listen-event access when the app needs to monitor
input events.

```swift
import IOKit.hidsystem

let access = IOHIDCheckAccess(kIOHIDRequestTypeListenEvent)
if access != kIOHIDAccessTypeGranted {
    IOHIDRequestAccess(kIOHIDRequestTypeListenEvent)
}
```

SDK evidence:

- `IOHIDCheckAccess(_:)` checks access for an `IOHIDRequestType`.
- `IOHIDRequestAccess(_:)` requests access from the user.
- `kIOHIDRequestTypeListenEvent` is the listen-event request type.

Review notes:

- Post-event and listen-event access are different request types.
- Global event taps and monitors may also intersect with Accessibility trust;
  verify which service the code path actually needs.

## Automation / Apple Events

Use Apple Events APIs when the app automates another app and needs to know
whether the user has granted Automation permission.

```swift
import CoreServices

let status = AEDeterminePermissionToAutomateTarget(
    target,
    eventClass,
    eventID,
    true
)
```

SDK evidence:

- `AEDeterminePermissionToAutomateTarget(...)` is available on macOS 10.14+.

Review notes:

- Automation is target-app-specific. A grant to automate one app does not imply
  permission to automate another.
- Include `NSAppleEventsUsageDescription` when the app sends Apple Events.

## Full Disk Access

There is no general public API that grants Full Disk Access. Product flows
should explain why access is needed, open System Settings as a convenience, and
provide manual fallback instructions.

Review notes:

- Check whether a narrower entitlement, file picker, security-scoped bookmark,
  or user-selected folder can replace Full Disk Access.
- Do not write to private TCC databases or ask users to run broad reset
  commands as normal onboarding.
