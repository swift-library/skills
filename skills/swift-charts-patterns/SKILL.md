---
name: swift-charts-patterns
description: Use this skill for Swift Charts implementation, review, refactoring, debugging, or modernization involving import Charts, Chart, Chart3D, BarMark, LineMark, AreaMark, PointMark, RectangleMark, RuleMark, SectorMark, SurfacePlot, AxisMarks, chart axes, legends, ChartProxy, chartOverlay, chartBackground, chartGesture, chart selection, scrollable axes, Plot APIs, AXChartDescriptorRepresentable, Audio Graph, or chart accessibility. Do not use for general SwiftUI layout, navigation, state management, non-chart animation, Core Data, SwiftData, networking, package architecture, or repository documentation.
---

# Swift Charts Patterns

## Purpose

Guide Swift Charts implementation, review, refactoring, and debugging with
project-compatible patterns for chart marks, axes, scales, interaction,
accessibility, fallback behavior, and API availability.

## When To Use

- Implementing or reviewing code that imports `Charts`.
- Choosing or fixing `Chart`, `Chart3D`, marks, plots, axes, scales, legends,
  annotations, or chart styling.
- Debugging `ChartProxy`, `chartOverlay`, `chartBackground`, `chartGesture`,
  chart selection, scrollable axes, or visible domains.
- Checking chart accessibility, Audio Graph behavior, descriptive `.value`
  labels, or `AXChartDescriptorRepresentable`.
- Modernizing chart code while preserving the local deployment target.

## When Not To Use

- Do not use for general SwiftUI state, layout, navigation, sheets, lists,
  focus, text, image, performance, macOS, or Liquid Glass work.
- Do not use for Core Data persistence.
- Do not use for SwiftData schema design or model lifecycle work.
- Do not use for broad Swift Concurrency migration.
- Do not use for networking, package architecture, dependency replacement, or
  repository documentation.

## Inputs To Inspect

- User request, screenshot, accessibility report, chart symptom, or target
  code.
- Files importing `Charts` and nearby SwiftUI container views.
- Deployment target, platform, Swift language mode, and local `AGENTS.md`,
  `README.md`, and architecture docs.
- Existing chart data models, identity choices, localization, accessibility,
  styling, and fallback conventions.

## Workflow

1. Read local project truth first.
2. Confirm the task is actually about Swift Charts. Leave non-chart SwiftUI
   container work to general SwiftUI implementation guidance.
3. Classify the chart surface: marks/plots, axes/scales, styling/legends,
   selection/gestures, `ChartProxy`, `Chart3D`, accessibility, or fallback.
4. Check API availability against the local deployment target before
   recommending iOS 17+, iOS 18+, or iOS 26+ chart APIs.
5. Open only the smallest matching reference file.
6. Preserve local data, architecture, localization, and design constraints.
7. Validate with build, preview, screenshot, interaction, or accessibility
   checks when feasible.

## Reference Files To Consult

- `references/charts.md`: marks, axes, scales, selection, `ChartProxy`,
  styling, plot APIs, and `Chart3D`.
- `references/charts-accessibility.md`: VoiceOver, Audio Graph,
  `AXChartDescriptorRepresentable`, fallback strategies, and version checklist.

Use `references/_index.md` only when the needed reference is unclear.

## Decision Rules

- Repository-local truth wins over this skill.
- Always check `import Charts` before diagnosing unresolved chart symbols.
- Use stable chart data identity: prefer `Identifiable` models or explicit
  `Chart(data, id:)`.
- Use descriptive `.value(_, _)` labels because they drive axes, legends, and
  accessibility.
- Apply chart-wide modifiers to `Chart`, not individual marks, unless the API
  is explicitly mark-scoped.
- Gate newer chart APIs with `#available` and provide a compatible fallback
  when the project supports older OS versions.
- Treat chart accessibility as part of chart correctness, not a separate polish
  pass.

## Validation Rules

- Build after source edits.
- Render previews or screenshots for layout-sensitive chart changes when
  feasible.
- Exercise selection, scrolling, gestures, and fallback branches that changed.
- Check VoiceOver labels, Audio Graph suitability, or chart descriptors for
  accessibility-sensitive work.

## Output Format

For reviews or implementation recommendations, return:

1. Phase / stage judgment
2. Swift Charts surface inspected
3. Findings
4. Recommended changes
5. Compatibility impact
6. Validation performed
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If platform or deployment target is unknown, report that before recommending
  availability-sensitive chart APIs.
- If the task needs broader SwiftUI layout, state, or navigation changes around
  the chart, call that portion out as outside Swift Charts scope.
- If chart behavior cannot be reproduced locally, separate source-level
  findings from unverified runtime assumptions.
