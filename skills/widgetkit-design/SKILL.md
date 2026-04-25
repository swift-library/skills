---
name: widgetkit-design
description: Use this skill for WidgetKit widget visual design, native widget layout, lock screen and home screen widget polish, widget family adaptation, Gauge usage, containerBackground, widget typography, semantic colors, internal padding, cross-family hierarchy, dense widget rendering, timeline refresh cadence when it affects visual freshness, or app/widget visual consistency. Do not use for general SwiftUI app design, WidgetKit provider architecture unrelated to design, AppIntent configuration, reload plumbing, persistence, networking, Swift Charts, or package architecture.
---

# WidgetKit Design

## Purpose

Guide WidgetKit visual design and design review so widgets feel native,
legible, memory-conscious, and consistent across lock screen and home screen
families.

## When To Use

- Designing or reviewing WidgetKit widget layouts and visual hierarchy.
- Choosing native widget components such as `Gauge` and widget backgrounds.
- Reviewing lock screen circular, rectangular, inline, and home screen widget
  families.
- Fixing widgets that feel manually drawn, clipped, inconsistent across
  families, too dense, or visually disconnected from the app.
- Reviewing timeline refresh cadence when stale data or excessive refreshes
  affect the visible widget experience.

## When Not To Use

- Do not use for general SwiftUI app screen design; use `swiftui-design`.
- Do not use for deep SwiftUI implementation issues in the widget view body;
  use `swiftui-patterns`.
- Do not use for WidgetKit provider architecture, reload plumbing, AppIntent
  configuration, shared storage, entitlements, or background execution unless
  the concrete issue affects design output.
- Do not use for persistence, networking, Swift Charts, package architecture,
  or repository documentation.

## Inputs To Inspect

- Widget screenshots, previews, supported families, and widget source.
- App design conventions that should carry into widgets: typography, color,
  metric formatting, and hierarchy.
- Timeline provider data granularity and refresh policy when visual freshness
  is in scope.
- Dense widget rendering strategies and memory symptoms such as extension
  termination.

## Workflow

1. Identify the widget family/families and the visible design problem.
2. Check whether a native widget component expresses the design better than
   custom drawing.
3. Load only the matching reference file. Open `references/_index.md` if
   routing is unclear.
4. Keep lock screen widgets compact and system-native; keep home widgets
   padded away from rounded edges.
5. Preserve cross-family hierarchy where possible instead of reinventing the
   design per family.
6. Align timeline refresh cadence with the data granularity the design implies.
7. Validate with WidgetKit previews or screenshots for every family touched.

## Reference Files To Consult

- `references/widget-visual-design.md`: `Gauge`, `.containerBackground`,
  family coverage, typography, padding, cross-family hierarchy, dense rendering,
  timeline cadence, and shared app/widget model guidance.
## Decision Rules

- Prefer native WidgetKit components before custom drawing.
- Use `.containerBackground(.fill.tertiary, for: .widget)` or a project-local
  semantic equivalent before hardcoded widget backgrounds.
- Keep typography compact and consistent with the app's visual system.
- Support all families that the product reasonably needs; do not omit common
  lock screen or home screen families without a reason.
- Use explicit internal padding for home widgets to avoid clipping near rounded
  edges.
- Use `Canvas` or similarly lightweight rendering for dense visualizations.
- Match refresh cadence to visual freshness: day-level data should not refresh
  every minute; live percentages should refresh often enough to be honest.

## Review Checklist

- Native widget components are used where they fit.
- Widget background, tint, and typography feel system-native.
- Lock screen widgets are compact and legible.
- Home screen widgets have explicit internal padding.
- Medium and large families share a coherent hierarchy.
- Dense visuals stay within widget memory constraints.
- Timeline refresh cadence matches displayed data granularity.
- App and widget share formatting and calculation rules where the user sees the
  same metric.

## Output Format

For reviews, report findings first by severity with widget family and file/line
references when available. Include the violated widget design rule, user-visible
impact, and concrete adjustment.

For implementation work, summarize:

1. Widget family or surface changed
2. Native component, hierarchy, or background choices affected
3. Timeline/data freshness impact
4. Validation performed
5. Remaining risks
