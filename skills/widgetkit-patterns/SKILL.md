---
name: widgetkit-patterns
description: Use this skill for WidgetKit implementation and review across widget extension targets, Widget, WidgetBundle, StaticConfiguration, AppIntentConfiguration, TimelineProvider, AppIntentTimelineProvider, TimelineEntry, reload policies, WidgetCenter, widget families, Lock Screen widgets, StandBy, Smart Stack behavior, interactive widgets, App Intents-backed configuration, ControlWidget, shared App Group data, deep links, push or background reload strategy, previews, snapshots, and extension constraints. Do not use for visual-only widget polish, Live Activity lifecycle, App Intent action design, or App Store screenshot/metadata work unless WidgetKit implementation is in scope.
---

# WidgetKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for WidgetKit source,
extension, timeline, configuration, interaction, and data-refresh workflows.
Visual-only widget review is out of scope.

## When To Use

- Creating or reviewing widget extension targets, `Widget`, `WidgetBundle`,
  Info.plist/capability setup, and extension lifecycle.
- Implementing `StaticConfiguration`, `IntentConfiguration`,
  `AppIntentConfiguration`, `TimelineProvider`, `AppIntentTimelineProvider`,
  `TimelineEntry`, snapshots, previews, and placeholders.
- Designing timeline entries, reload policies, refresh budgets, `WidgetCenter`
  reloads, background refresh handoff, or server-triggered reload strategy.
- Wiring App Group data, shared caches, deep links, URL handling, and app-to-widget
  data preparation.
- Implementing interactive widgets, App Intents-backed controls, Control Center
  widgets, Lock Screen widgets, StandBy, Smart Stack, or family-specific views.
- Debugging missing widgets, stale timelines, unsupported families, memory
  pressure, oversized images, or preview/snapshot failures.

## When Not To Use

- Do not use for visual-only layout, typography, color, widget family polish, or
  native widget feel; visual widget design is out of scope.
- Do not use for Live Activity request/update/end lifecycle; ActivityKit
  lifecycle is out of scope.
- Do not use for App Intent action/entity design unless it is widget
  configuration or interaction wiring; general App Intents design is out of
  scope.
- Do not use for App Store screenshots, metadata, or market messaging.

## Inputs To Inspect

- Widget extension target, entitlements/capabilities, `WidgetBundle`, widget
  configuration, supported families, and deployment targets.
- Timeline provider code, entry model, reload policies, placeholder/snapshot
  paths, preview data, and family-specific rendering.
- Shared data source, App Group paths, caches, async loading, image processing,
  and privacy-sensitive data boundaries.
- App Intent configuration, interactive actions, Control Center widget code,
  deep links, and URL routing.
- Host app reload calls, background refresh/push strategy, logs, and device or
  simulator reproduction notes.

## Workflow

1. Confirm whether the work is WidgetKit implementation or visual-only widget
   design.
2. Verify extension target setup, supported families, configuration type, and
   data ownership before changing timeline code.
3. Keep timeline entries small, deterministic, and precomputed. Move expensive
   network, image, and persistence work out of view rendering.
4. Choose reload policy deliberately and avoid treating widget timelines as
   real-time UI.
5. Use App Groups or other explicit sharing paths for host-app data. Avoid
   reaching into host app runtime state from the extension.
6. Keep App Intents interactions short, deterministic, and compatible with the
   widget extension execution model.
7. Separate ActivityKit Live Activity lifecycle from WidgetKit view rendering
   and configuration.
8. Validate on the relevant widget families and surfaces, not only previews.

## Review Rules

- Do not handle visual-only feedback here when no WidgetKit implementation
  change is involved.
- Do not fetch broad network data or perform heavy image processing inside
  widget body rendering.
- Do not assume reload timing is immediate or exact.
- Do not expose private data on Lock Screen, StandBy, or Smart Stack surfaces
  without a product-level privacy decision.
- Treat new WidgetKit families, Control Center widgets, Smart Stack behavior,
  push reload behavior, and platform-specific rendering as current Apple
  documentation and local SDK gated.

## Validation

- Build the app and widget extension targets.
- Run previews for the supported families, then verify on simulator or device
  when behavior depends on timelines, reloads, interactivity, or system
  surfaces.
- Test placeholder, snapshot, timeline, stale-data, failed-load, and deep-link
  states.
- Test App Group data availability and privacy redaction.
- Inspect extension logs for timeline reload and memory failures.

## Output

Return:

1. WidgetKit implementation versus visual-design boundary
2. Extension/configuration/timeline findings
3. Data, refresh, interaction, and privacy notes
4. Surface and family coverage
5. Validation run or still needed
