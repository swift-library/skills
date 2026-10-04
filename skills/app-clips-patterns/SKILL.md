---
name: app-clips-patterns
description: Use this skill for App Clips implementation and review across App Clip target setup, invocation URLs, associated domains, app-to-clip code sharing, App Clip experiences, location confirmation, shared data handoff, full-app promotion, local testing, and full-app parity. Do not use for App Store metadata operations alone, release signing alone, general SwiftUI architecture, or ordinary deep-link handling with no App Clip target.
---

# App Clips Patterns

## Purpose

Guide implementation, review, and troubleshooting for lightweight App Clip
experiences that launch from invocation URLs, share code with the full app, and
hand off cleanly to the installed app.

## When To Use

- Creating or reviewing an App Clip target and its relationship to the full app.
- Handling App Clip invocation URLs, default or advanced experiences,
  associated domains, AASA files, and website association.
- Sharing Swift packages, assets, data, App Groups, Keychain items, or sign-in
  state between the App Clip and full app.
- Implementing location confirmation, full-app promotion, App Clip links, or
  local App Clip testing.
- Debugging size, capability, invocation, entitlement, or handoff failures.

## When Not To Use

- Do not use for App Store Connect metadata or marketing setup alone.
- Do not use for signing, provisioning, archive, or release artifact work
  alone.
- Do not use for ordinary universal links or deep links without an App Clip
  target.
- Do not use for broad SwiftUI architecture unless the App Clip/full-app split
  is the main issue.
- Do not invent App Clip size limits, capability restrictions, or distribution
  behavior. Verify current Apple documentation, App Store Connect, and local
  Xcode behavior before relying on them.

## Inputs To Inspect

- App Clip target, parent app target, bundle identifiers, entitlements,
  capabilities, and build settings.
- Shared package/module boundaries, resources, assets, and data containers.
- Invocation URL handling, `NSUserActivity` handling, associated domains, and
  AASA files.
- App Clip experience setup, local experience configuration, and test URLs.
- Handoff paths: App Groups, Keychain sharing, Sign in with Apple, full-app
  deep links, and full-app promotion.

## Workflow

1. Identify the App Clip job: instant task, demo, checkout, sign-in, location
   confirmation, or full-app handoff.
2. Confirm target relationship, bundle ID relationship, entitlements,
   associated domains, and capabilities before changing code.
3. Keep shared code in packages or modules that both the App Clip and full app
   can import without dragging in unsupported or oversized dependencies.
4. Implement invocation handling from the launch URL through user activity and
   route it to a minimal App Clip flow.
5. Review website association, invocation URLs, default/advanced experiences,
   and local test setup.
6. Implement data handoff deliberately: App Group, Keychain access group,
   account sign-in, or explicit full-app URL state.
7. Keep full-app promotion contextual and reversible. Do not block the clip's
   core job behind install prompts.
8. Validate launch, handoff, and full-app parity from real invocation paths.

## Review Rules

- Keep the App Clip narrow. Remove code, assets, and flows that do not serve the
  instant task.
- Do not assume the full app is installed or available.
- Do not persist sensitive state casually in shared containers.
- Keep App Clip and full app URL behavior aligned so the same invocation can
  reach the same product state.
- Treat App Store Connect experience fields, size limits, and capability
  availability as current-official-source gated.

## Validation

- Build both the App Clip and parent app targets.
- Run a local App Clip experience or equivalent invocation URL test.
- Test fresh install, no full app installed, full app installed, and full-app
  handoff paths when feasible.
- Check associated domains/AASA reachability when website launch is in scope.
- Check size, capabilities, and unsupported framework usage before release
  handoff.

## Output

For implementation or review work, return:

1. App Clip goal and invocation surface
2. Target, entitlement, and shared-code status
3. Invocation and handoff findings
4. Full-app parity and promotion notes
5. Validation run or still needed
