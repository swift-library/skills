---
name: swiftui-design
description: Use this skill for SwiftUI visual design, native Apple UI polish, and design review involving spacing, typography, semantic colors, component sizing, grouped content, cards, navigation chrome, system controls, tap targets, visual hierarchy, interactive editors, crop/collage/layout tools, screenshots, previews, or UI that feels non-native. Do not use for WidgetKit widget design, SwiftUI state/data-flow bugs, deep layout behavior, navigation routing, source-level performance, Swift Charts, persistence, networking, or package architecture.
---

# SwiftUI Design

## Purpose

Guide SwiftUI visual design and design review so app screens feel native,
polished, restrained, and internally consistent. Focus on visual hierarchy,
spacing, typography, color, component proportion, grouped content, controls,
and editor surfaces.

## When To Use

- Reviewing SwiftUI screenshots, previews, or source for visual polish.
- Creating or refining native-feeling app screens and reusable components.
- Fixing UI that feels visually noisy, over-decorated, oddly spaced, too large,
  low contrast, or inconsistent with Apple platform conventions.
- Choosing spacing, font hierarchy, semantic colors, card/group styling,
  divider usage, progress indicator sizing, row sizing, and navigation chrome.
- Reviewing interactive editors such as crop, collage, canvas, media-framing,
  layout-picker, and multi-mode configuration surfaces.

## When Not To Use

- Do not use for WidgetKit widget design; use `widgetkit-design`.
- Do not use for SwiftUI state/data-flow correctness, navigation routing,
  sheet mechanics, deep layout behavior, macOS windows, or Liquid Glass API
  correctness; use `swiftui-patterns`.
- Do not use for source-level SwiftUI performance; use
  `swiftui-performance`.
- Do not use for accessibility implementation; use `accessibility-patterns`.
- Do not use for Swift Charts; use `swift-charts-patterns`.
- Do not use for persistence, networking, package architecture, or repository
  documentation.

## Inputs To Inspect

- Screenshots, preview renders, Figma context, user-visible issue reports, or
  SwiftUI source.
- Existing design conventions: spacing constants, typography, colors, component
  shapes, navigation style, control style, and platform target.
- Dynamic Type, color scheme, localization length, and device size constraints
  when relevant.
- For editors: source of truth for selected item, geometry math, gestures,
  safe-area handling, and export/render path.

## Workflow

1. Classify the design problem: spacing, typography, color, component sizing,
   grouped content, navigation chrome, controls, editor surface, or holistic
   polish.
2. Inspect the smallest useful screen/component surface and nearby conventions.
3. Load only the matching reference file. Open `references/_index.md` if
   routing is unclear.
4. Prefer native SwiftUI and system styling before custom drawing, gradients,
   borders, and hardcoded colors.
5. Keep recommendations concrete: exact spacing, font role, color role,
   component size, or view structure.
6. Preserve product identity, but remove visual noise that does not serve the
   workflow.
7. Validate visually when code changes affect layout, screenshots, Dynamic
   Type, color scheme, or editor geometry.

## Reference Files To Consult

- `references/visual-design-principles.md`: spacing grid, typography,
  semantic colors, sizing, cards/groups, navigation chrome, controls, and
  pre-ship checklist.
- `references/interactive-editor-design.md`: crop/collage/canvas editor
  state, shared geometry, gestures, fixed layouts, safe areas, and settings
  surfaces.
## Decision Rules

- Use restraint over decoration. Every custom visual element should serve
  hierarchy, affordance, state, or brand.
- Prefer a small spacing scale based on 4/8 point increments.
- Prefer fewer font sizes with clear role and weight differences.
- Prefer semantic system colors and hierarchical foreground styles over
  hardcoded light/dark colors and many opacity values.
- Use system components and control semantics before manually composing common
  controls.
- Keep grouped content native: simple backgrounds, modest corner radii, system
  dividers, and clear internal padding.
- Avoid `minimumScaleFactor` as a layout bandage; fix the container, wrapping,
  hierarchy, or content length first.
- For exclusive choices, use one selected value rather than independent
  booleans.
- For editor UIs, centralize geometry and interaction state so preview,
  gesture, and export paths agree.

## Review Checklist

- Spacing values follow a consistent grid and hierarchy.
- Typography uses a limited scale and roles are visually distinct.
- Color choices adapt to light/dark mode and accessibility settings.
- Cards, grouped sections, rows, strokes, and progress indicators are
  proportional to their context.
- Controls use system affordances and preserve labels/tap targets.
- Navigation chrome is compact and does not compete with content.
- Editor screens keep the editable stage dominant and expose one focused
  settings surface at a time.
- Text fits without overlapping, truncating critical information, or depending
  on tiny scale factors.

## Output Format

For design reviews, report findings first by severity with screenshot regions
or file/line references when available. Include the visual rule, user-visible
impact, and concrete adjustment.

For implementation work, summarize:

1. Design surface changed
2. Visual system choices affected
3. Compatibility and accessibility impact
4. Validation performed
5. Remaining risks
