---
name: swiftui-patterns
description: Use this skill for SwiftUI view implementation, ordinary review, focused view cleanup/refactoring, and debugging of state/data flow, view structure, layout, lists, navigation and presentation, toolbars, controls/forms, scrolling, text/images, SwiftUI text localization slices, animation, macOS SwiftUI, MenuBarExtra, or Liquid Glass. Do not use for dedicated sibling-domain work such as architecture selection, performance diagnosis, accessibility audits, focus-system audits, Instruments traces, Swift Charts, persistence, networking, package architecture, Xcode localization resource workflows, or concurrency migration.
---

# SwiftUI Patterns

## Purpose

Guide ordinary SwiftUI implementation, review, localized refactoring, and
debugging with project-compatible patterns for state, data flow, view
structure, navigation, layout, controls, text/images, animation, and
platform-specific SwiftUI APIs.

## When To Use

- Reviewing SwiftUI views, making localized pattern-level refactors, or running
  focused cleanup passes for long bodies, subview extraction, action
  extraction, stable view trees, and Observation ownership.
- Choosing property wrappers and data flow: `@State`, `@Binding`,
  `@Bindable`, `@Observable`, `@Environment`, `@FocusState`.
- Restructuring large view bodies, extracting subviews, avoiding unnecessary
  `AnyView`, or using `@ViewBuilder` correctly.
- Fixing list, `ForEach`, table, scroll, app shell, TabView, deep-link,
  navigation, toolbar, sheet, inspector, or simple in-view form focus behavior.
- Noticing small invalidation, identity, or image-loading issues while already
  working on ordinary SwiftUI implementation.
- Implementing or reviewing animations, transitions, tap targets, system
  controls, text localization, macOS SwiftUI windows, `MenuBarExtra`
  utilities, or iOS 26+ Liquid Glass.

## When Not To Use

- Do not use for Core Data persistence; use `core-data-patterns`.
- Do not use for SwiftData schema design or custom DataStore work.
- Do not use for Xcode Instruments `.trace`, `xctrace`, trace recording, or
  trace analysis work; use `xcode-instruments`.
- Do not use for a dedicated SwiftUI performance review focused on slow
  rendering, janky scrolling, high CPU/memory, excessive updates, or layout
  thrash; use `swiftui-performance`.
- Do not use for Swift Charts; use `swift-charts-patterns`.
- Do not use for broad Swift Concurrency migration, actor-isolation design,
  `Sendable` fixes, or data-race work; use `swift-concurrency-patterns`.
- Do not use for dedicated accessibility audits, VoiceOver, Voice Control,
  Switch Control, Full Keyboard Access, Dynamic Type accessibility reviews,
  WCAG mapping, Accessibility Inspector workflows, or App Store Accessibility
  Nutrition Labels; use `accessibility-patterns`.
- Do not use for dedicated Focus Engine audits, tvOS remote focus, UIKit/AppKit
  focus systems, RealityKit hover/focus, Digital Crown focus, focus
  restoration, or focus debugging; use `focus-engine-patterns`.
- Do not use for SwiftUI app or feature architecture selection, architecture
  migration, MVVM, MVI, TCA, Clean Architecture presentation adapters, or
  Coordinator-style navigation ownership; use `swiftui-architecture`.
- Do not use for networking architecture, package architecture, dependency
  replacement, or repository documentation.
- Do not use for Xcode String Catalogs, translator export/import,
  pseudolocalization, localized package/framework resources, bundle lookup, or
  locale UI test planning; use `xcode-localization-patterns`.
- Do not use for lightweight old-API checks when no deeper SwiftUI design or
  behavior question exists; use `swift-programming-language`.

## Inputs To Inspect

- User request, screenshots, preview output, basic SwiftUI accessibility issue,
  or runtime symptom.
- SwiftUI source files under review and nearby parent/child views.
- Deployment target, platform, Swift language mode, and project-local
  `AGENTS.md`, `README.md`, and architecture docs.
- Existing navigation, state ownership, environment injection, styling,
  localization, and accessibility conventions.
- Test or preview setup when a behavior can be verified locally.

## Workflow

1. Read local project truth first.
2. Classify the task: state/data flow, view cleanup, view structure/layout,
   list/scroll, app wiring/routing, navigation/presentation, animation,
   text/basic SwiftUI focus, images, macOS scene/MenuBarExtra behavior, or
   platform/latest APIs.
3. Check deployment-target availability before recommending modern APIs,
   Liquid Glass, macOS-only APIs, or iOS-version-specific modifiers.
4. Open only the smallest matching reference file. Open
   `references/_index.md` only if routing is unclear.
5. If the task is dedicated focus management across Focus Engine, tvOS,
   UIKit/AppKit, RealityKit, Digital Crown, restoration, or focus debugging,
   route that part to `focus-engine-patterns`.
6. If the task is a dedicated accessibility audit or mentions VoiceOver, Voice
   Control, Switch Control, Full Keyboard Access, WCAG, Accessibility
   Inspector, or Nutrition Labels, route that part to `accessibility-patterns`.
7. If the task references `.trace`, `xctrace`, Instruments, trace recording, or
   trace analysis, route that part to `xcode-instruments`.
8. Prefer native SwiftUI APIs over UIKit/AppKit bridging unless bridging is
   required or already established locally.
9. Preserve the project's architecture and style. Improve local data flow and
   testability without mandating MVVM, VIPER, TCA, or another architecture. If
   the user asks to choose, validate, or migrate a SwiftUI architecture, route
   that work to `swiftui-architecture`.
10. Validate with build, previews, targeted tests, accessibility checks,
   screenshots, benchmarks, or trace findings from `xcode-instruments`
   as appropriate.

## Reference Files To Consult

- `references/latest-apis.md`: deprecated API replacements and availability.
- `references/state-management.md`: property wrappers, data flow, Observation.
- `references/view-structure.md`: view extraction, `@ViewBuilder`, `AnyView`.
- `references/view-refactor.md`: focused cleanup passes for long view bodies,
  subview extraction, action extraction, and stable view trees.
- `references/layout-best-practices.md`: layout patterns and GeometryReader
  alternatives.
- `references/list-patterns.md`: `ForEach` identity, `List`, `Table`.
- `references/component-patterns.md`: controls, forms, searchable views,
  previews, grids, haptics, theming, loading placeholders, overlays, top bars,
  input toolbars, scroll-reveal affordances, media.
- `references/app-wiring-and-routing.md`: app shell, TabView, NavigationStack,
  deep links, dependency injection boundaries, and sheet routing when
  architecture is already established.
- `references/sheet-navigation-patterns.md`: sheets, navigation, inspectors.
- `references/scroll-patterns.md`: scroll views and programmatic scrolling.
- `references/text-patterns.md`: localized and verbatim text decisions.
- `references/image-optimization.md`: `AsyncImage`, decoding, downsampling.
- `references/animation-basics.md`: implicit and explicit animations.
- `references/animation-transitions.md`: transitions and matched geometry.
- `references/animation-advanced.md`: phase/keyframe/advanced animation APIs.
- `references/liquid-glass.md`: iOS 26+ Liquid Glass and fallback patterns.
- `references/macos-scenes.md`: macOS scenes, `MenuBarExtra`, menu-bar-only
  utilities, and multi-window setup.
- `references/macos-window-styling.md`: window and toolbar styling.
- `references/macos-views.md`: macOS-specific SwiftUI views and AppKit interop.

Use these only as light reminders during ordinary SwiftUI implementation:

- `references/focus-patterns.md`: route stub for SwiftUI focus knowledge owned
  by `focus-engine-patterns`.
- `references/accessibility-patterns.md`: route stub for SwiftUI accessibility
  knowledge owned by `accessibility-patterns`.
- `references/performance-patterns.md`: route stub for SwiftUI source-level
  performance knowledge owned by `swiftui-performance`.

## Decision Rules

- Repository-local truth wins over this skill.
- `@State` owns view-local state and should be private.
- Use `@Binding` only when the child needs to mutate parent-owned state.
- Prefer `@Observable` with `@State` ownership and `@Bindable` for injected
  observable bindings when deployment targets support Observation.
- Use stable identity for dynamic `ForEach` content. Do not use indices for
  mutable collections.
- Prefer `Button` over `onTapGesture` for ordinary tappable controls.
- Prefer native SwiftUI navigation, presentation, layout, and accessibility
  APIs before bridging.
- Gate version-specific APIs with `#available` and provide sensible fallbacks.
- Adopt Liquid Glass only when explicitly requested or already used by the
  project.
- Treat performance observations as hypotheses unless measured by local
  evidence. Use `swiftui-performance` or `xcode-instruments` when
  performance becomes the primary task.

## Validation Rules

- Build after source edits.
- Render previews or use screenshots for UI behavior and layout-sensitive work
  when feasible.
- Check Dynamic Type, VoiceOver labels, and image-only controls for
  basic SwiftUI accessibility-sensitive changes. Use `accessibility-patterns`
  for dedicated audits or assistive-technology workflows.
- Verify navigation and presentation state through the user path being changed.
- For performance work, use `_logChanges()`, a project-local benchmark, or
  trace findings from `xcode-instruments` before claiming improvement.

## Output Format

For reviews or implementation recommendations, return:

1. Phase / stage judgment
2. SwiftUI surface inspected
3. Findings
4. Recommended changes
5. Compatibility impact
6. Validation performed
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If platform or deployment target is unknown, report that before recommending
  availability-sensitive APIs.
- If the request becomes a dedicated accessibility audit, keep SwiftUI source
  observations concise and route the accessibility-specific work to
  `accessibility-patterns`.
- If a design request crosses into architecture choice, state management
  framework selection, or app-wide routing design, keep the recommendation
  incremental and ask before imposing a new architecture.
- If a performance task needs Instruments evidence, use
  `xcode-instruments` for trace capture or analysis, then continue with the
  relevant source-level SwiftUI skill where useful.
