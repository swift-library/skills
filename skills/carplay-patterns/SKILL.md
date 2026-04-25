---
name: carplay-patterns
description: Use this skill for CarPlay implementation and review across CarPlay entitlements, app category boundaries, CPTemplateApplicationScene, scene delegates, CPInterfaceController, CPListTemplate, CPMapTemplate, CPNowPlayingTemplate, dashboard and instrument-cluster scenes, CarPlay Simulator, template limits, and vehicle display constraints. Do not use for generic SwiftUI/UIKit architecture, ordinary in-app navigation, or Apple-platform release work without CarPlay surfaces.
---

# CarPlay Patterns

## Purpose

Guide implementation, review, and troubleshooting for CarPlay app surfaces,
scene configuration, template-driven UI, category entitlements, and vehicle
display validation.

## When To Use

- Adding or reviewing CarPlay scene configuration with
  `CPTemplateApplicationScene` and `CPTemplateApplicationSceneDelegate`.
- Managing templates through `CPInterfaceController`.
- Building list, grid, map, tab bar, now playing, communication, point-of-
  interest, dashboard, or instrument-cluster surfaces.
- Checking app category boundaries, template limits, completion handlers, and
  simulator/device validation.
- Diagnosing CarPlay entitlement, scene manifest, route preview, map button, or
  Now Playing behavior.

## When Not To Use

- Do not use for ordinary SwiftUI/UIKit navigation that is not displayed in
  CarPlay.
- Do not use for App Store metadata or release handoff; use market or release
  skills as appropriate.
- Do not use for media playback implementation without a CarPlay surface; use
  `avkit-patterns` or `musickit-patterns`.
- Do not use for generic map implementation without CarPlay templates; use
  `mapkit-patterns`.

## Inputs To Inspect

- Entitlements, app category, scene manifest, and deployment target.
- CarPlay scene delegate, interface controller, template hierarchy, and
  completion handlers.
- Category-specific templates and restrictions for navigation, audio,
  communication, information, or point-of-interest apps.
- Dashboard, instrument-cluster, route, trip preview, search, map button, and
  Now Playing integration code.
- CarPlay Simulator configuration and physical vehicle/device notes when
  available.

## Workflow

1. Confirm the task is a CarPlay surface rather than ordinary app UI.
2. Verify current entitlement category, supported template set, and platform
   availability before making implementation claims.
3. Check scene manifest and delegate wiring before template code.
4. Keep template hierarchy shallow enough for the app category and vehicle
   constraints.
5. Handle template completion callbacks, user actions, route/session state, and
   disconnection cleanup.
6. Validate with CarPlay Simulator and, for vehicle-specific behavior, a real
   head unit when possible.

## Review Rules

- Do not place arbitrary UIKit/SwiftUI UI in CarPlay templates unless the
  framework surface supports it for the category.
- Do not assume a template or hierarchy depth is allowed for every app category.
- Do not hide entitlement/category uncertainty in generic architecture advice.
- Do not expose distracting, dense, or unsupported interactions on the vehicle
  display.
- Treat entitlement access, template availability, dashboard/instrument-cluster
  behavior, and vehicle constraints as current Apple documentation and SDK
  gated.

## Validation

- Build the affected app target.
- Test CarPlay scene connection/disconnection, root template setup, push/pop
  template navigation, category-specific user actions, and error handling.
- Run CarPlay Simulator for UI and scene validation; use real vehicle/device
  tests for category or hardware behavior when feasible.

## Output

For implementation or review work, return:

1. CarPlay category and entitlement assumptions
2. Scene, delegate, and interface-controller findings
3. Template hierarchy and category-boundary findings
4. Simulator or vehicle validation run
5. Remaining current Apple documentation or SDK gates
