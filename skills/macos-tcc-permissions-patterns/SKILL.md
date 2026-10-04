---
name: macos-tcc-permissions-patterns
description: Use this skill for macOS TCC privacy permission implementation and review involving Screen Recording, Accessibility, Input Monitoring, Full Disk Access, Automation, System Settings privacy deep links, drag-to-authorize app bundles, helper app permission identity, prompt-state pitfalls, and onboarding fallback behavior. Do not use for PermissionKit child communication permissions, general SwiftUI layout, app packaging/signing, ordinary sandbox entitlements, or accessibility audits unless they are part of a macOS TCC permission flow.
---

# macOS TCC Permissions Patterns

## Purpose

Guide macOS privacy-permission flows where app capability depends on TCC
authorization, System Settings, or user-driven trust decisions. This skill
focuses on implementation shape, permission identity, onboarding UX, and review
risks for macOS apps and helpers.

## When To Use

- Implementing or reviewing Screen Recording, Accessibility, Input Monitoring,
  Full Disk Access, or Automation permission flows.
- Opening System Settings privacy panes or building fallback instructions when
  the app cannot request a permission directly.
- Providing a draggable `.app` bundle so the user can add the app or helper to
  a System Settings privacy list.
- Diagnosing why the wrong app, helper, login item, XPC service, or command-line
  tool appears in privacy settings.
- Positioning a permission guide near System Settings, including brittle window
  lookup or Accessibility API strategies.

## When Not To Use

- Do not use for Apple PermissionKit child/guardian communication flows.
- Do not use for ordinary SwiftUI view layout, navigation, or visual design.
- Do not use for app bundle construction, code signing, notarization, or
  release packaging unless the issue is the TCC identity that will be granted.
- Do not use for full accessibility audits, VoiceOver semantics, or WCAG review
  unless the Accessibility permission flow itself is being implemented.
- Do not use for framework-specific authorization flows, such as Contacts,
  HealthKit, MusicKit, Photos, or Notifications.

## Inputs To Inspect

- Permission type, user flow, deployment target, sandbox state, bundle IDs, and
  whether the requesting code runs in the main app, helper app, XPC service,
  login item, extension, or CLI tool.
- Existing `Info.plist` usage descriptions, entitlements, hardened runtime,
  launch services setup, and helper installation paths.
- Permission-check/request code, System Settings links, onboarding copy,
  drag-and-drop source code, window positioning code, and restart/retry logic.
- Local macOS version and current SDK headers when API availability or behavior
  is in doubt.

## Workflow

1. Identify the exact TCC service and the process identity that needs access.
2. Check whether there is a public API to preflight or request the permission.
   Read `references/permission-apis.md` for Screen Recording, Accessibility,
   Input Monitoring, Automation, and Full Disk Access.
3. If System Settings is part of the flow, read
   `references/system-settings-onboarding.md` for deep links, fallback
   behavior, and window guidance boundaries.
4. If the UI asks the user to drag the app into a privacy list, read
   `references/drag-to-authorize.md` and make sure the dragged URL is the
   actual bundle that needs trust.
5. For helpers, login items, XPC, CLI tools, or Electron-style helper bundles,
   read `references/identity-and-validation.md` before changing UI or code.
6. Implement the narrowest flow: preflight, request when public API exists,
   open settings when needed, show a clear manual path, poll or retry after the
   user changes settings, and tell the user when a restart is required.
7. Validate the denied, not-determined, granted, wrong-helper, already-open
   System Settings, multi-display, and post-restart states.

## Reference Files To Consult

- `references/permission-apis.md`: current SDK-verified public APIs and service
  boundaries.
- `references/system-settings-onboarding.md`: settings deep links, fallbacks,
  floating guidance, and window positioning limits.
- `references/drag-to-authorize.md`: AppKit and SwiftUI drag sources for
  `.app` bundles.
- `references/identity-and-validation.md`: TCC identity, helpers, resets, and
  QA checks.

## Decision Rules

- The granting subject is the process or bundle that performs the protected
  operation. Do not assume the main app permission covers a helper.
- Prefer a public preflight/request API when one exists. Use System Settings
  guidance when no public request API exists or when the user has already
  denied a prompt.
- Treat `x-apple.systempreferences:` anchors as best-effort routing, not stable
  public API. Always provide a human-readable fallback path.
- Do not claim the app can grant, toggle, or bypass TCC. The user must approve
  in system UI.
- Do not depend on Accessibility API window inspection to guide a first-time
  Accessibility permission flow.
- Avoid private TCC database writes, broad reset commands, or scripted UI
  clicks in product code.

## Validation Rules

- Build the affected macOS target after source edits.
- Test fresh install, denied, granted, revoked, and upgraded-app states.
- Verify the app or helper displayed in System Settings is the same bundle that
  performs the protected operation.
- Confirm the UI still works when System Settings fails to open the requested
  pane, opens on another display, or already has a different privacy pane open.
- For drag-to-authorize flows, drag the item into the target privacy list and
  verify the resulting entry and toggle state.
- For API claims, confirm current local SDK headers or official Apple
  documentation before updating skill rules or app code.

## Output Format

For implementation or review work, return:

1. TCC service and requesting identity
2. Public API path versus System Settings path
3. Onboarding and drag-to-authorize behavior
4. Helper, entitlement, and restart risks
5. Validation performed or still required
6. Remaining macOS-version or user-state uncertainty

## Failure / Uncertainty Handling

- If the protected operation's process identity is unclear, inspect launch and
  helper code before changing permission UI.
- If a System Settings deep link does not work on the current macOS version,
  fall back to opening Privacy & Security and show manual instructions.
- If window positioning requires Accessibility permission that the app is
  trying to obtain, use coarse placement or static instructions instead.
- If current SDK or official docs cannot verify an API or availability claim,
  mark the guidance as observed or needing verification rather than turning it
  into a rule.
