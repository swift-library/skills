---
name: swiftui-patterns
description: Use this skill for SwiftUI view implementation, ordinary review, focused view cleanup/refactoring, and debugging of state/data flow, view structure, layout, lists, navigation and presentation, toolbars, controls/forms, Form/Section/LabeledContent implementation, native control primitive refactors, scrolling, text/images, SwiftUI text localization slices, animation, macOS SwiftUI, MenuBarExtra, or Liquid Glass. Do not use for dedicated work on architecture selection, performance diagnosis, accessibility audits, focus-system audits, Instruments traces, Swift Charts, persistence, networking, package architecture, Xcode localization resource workflows, or concurrency migration.
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
- Implementing or refactoring native SwiftUI primitives such as `Form`,
  `Section`, `LabeledContent`, `Label`, `Toggle`, `Picker`, `TextField`,
  `Button`, `Menu`, `NavigationLink`, `List`, or `Table`, including replacing
  manual rows with system primitives while preserving state, bindings,
  availability, previews, and validation.
- Noticing small invalidation, identity, or image-loading issues while already
  working on ordinary SwiftUI implementation.
- Implementing or reviewing animations, transitions, tap targets, system
  controls, simple `.sensoryFeedback` state-triggered haptics, text
  localization, macOS SwiftUI windows, `MenuBarExtra` utilities, or platform
  SDK 26+ Liquid Glass.

## When Not To Use

- Do not use for Core Data persistence.
- Do not use for SwiftData schema design or custom DataStore work.
- Do not use for Xcode Instruments `.trace`, `xctrace`, trace recording, or
  trace analysis work.
- Do not use for a dedicated SwiftUI performance review focused on slow
  rendering, janky scrolling, high CPU/memory, excessive updates, or layout
  thrash.
- Do not use for Swift Charts.
- Do not use for broad Swift Concurrency migration, actor-isolation design,
  `Sendable` fixes, or data-race work.
- Do not use for dedicated accessibility audits, VoiceOver, Voice Control,
  Switch Control, Full Keyboard Access, Dynamic Type accessibility reviews,
  WCAG mapping, Accessibility Inspector workflows, or App Store Accessibility
  Nutrition Labels.
- Do not use for dedicated Focus Engine audits, tvOS remote focus, UIKit/AppKit
  focus systems, RealityKit hover/focus, Digital Crown focus, focus
  restoration, or focus debugging.
- Do not use for SwiftUI app or feature architecture selection, architecture
  migration, MVVM, MVI, TCA, Clean Architecture presentation adapters, or
  Coordinator-style navigation ownership.
- Do not use for networking architecture, package architecture, dependency
  replacement, or repository documentation.
- Do not use for Xcode String Catalogs, translator export/import,
  pseudolocalization, localized package/framework resources, bundle lookup, or
  locale UI test planning.
- Do not use for lightweight old-API checks when no deeper SwiftUI design or
  behavior question exists.
- Do not use for custom Core Haptics engines, AHAP files, advanced haptic
  players, or audio-haptic pattern authoring.

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
   treat that part as out of scope and keep only local SwiftUI focus edits.
6. If the task is a dedicated accessibility audit or mentions VoiceOver, Voice
   Control, Switch Control, Full Keyboard Access, WCAG, Accessibility
   Inspector, or Nutrition Labels, treat that part as out of scope and keep
   only basic SwiftUI accessibility modifiers.
7. If the task references `.trace`, `xctrace`, Instruments, trace recording, or
   trace analysis, leave trace capture and analysis out of scope and use only
   the resulting findings.
8. Prefer native SwiftUI APIs over UIKit/AppKit bridging unless bridging is
   required or already established locally.
9. Preserve the project's architecture and style. Improve local data flow and
   testability without mandating MVVM, VIPER, TCA, or another architecture. If
   the user asks to choose, validate, or migrate a SwiftUI architecture, treat
   that work as out of scope.
10. Validate with build, previews, targeted tests, accessibility checks,
   screenshots, benchmarks, or Instruments trace findings as appropriate.

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
- `references/liquid-glass.md`: platform SDK 26+ Liquid Glass and fallback
  patterns.
- `references/macos-scenes.md`: macOS scenes, `MenuBarExtra`, menu-bar-only
  utilities, and multi-window setup.
- `references/macos-window-styling.md`: window and toolbar styling.
- `references/macos-views.md`: macOS-specific SwiftUI views and AppKit interop.

Use these only as light reminders during ordinary SwiftUI implementation:

- `references/focus-patterns.md`: basic SwiftUI `@FocusState` reminders and
  the dedicated-focus boundary.
- `references/accessibility-basics.md`: basic SwiftUI accessibility reminders
  and the dedicated-audit boundary.
- `references/performance-patterns.md`: incidental SwiftUI performance
  reminders and the dedicated-performance boundary.

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
- If the main question is which visible control primitive fits the UI, that
  visual-design choice is out of scope; after the primitive is chosen,
  implement or refactor it here.
- Gate version-specific APIs with `#available` and provide sensible fallbacks.
- Adopt Liquid Glass only when explicitly requested or already used by the
  project.
- Treat performance observations as hypotheses unless measured by local
  evidence. Dedicated performance diagnosis and trace analysis are out of
  scope when performance becomes the primary task.

## Validation Rules

- Build after source edits.
- Render previews or use screenshots for UI behavior and layout-sensitive work
  when feasible.
- Check Dynamic Type, VoiceOver labels, and image-only controls for
  basic SwiftUI accessibility-sensitive changes. Dedicated audits and
  assistive-technology workflows are out of scope.
- Verify navigation and presentation state through the user path being changed.
- For performance work, use `_logChanges()`, a project-local benchmark, or
  Instruments trace findings before claiming improvement.

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
  observations concise and state that the accessibility-specific audit is out
  of scope.
- If a design request crosses into architecture choice, state management
  framework selection, or app-wide routing design, keep the recommendation
  incremental and ask before imposing a new architecture.
- If a performance task needs Instruments evidence, ask for trace findings
  rather than capturing or analyzing traces here, then continue with
  source-level SwiftUI changes where useful.
