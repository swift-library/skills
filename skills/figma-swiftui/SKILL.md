---
name: figma-swiftui
description: >-
  Use this skill when converting Figma URLs, nodes, selected Figma desktop
  nodes, screenshots, source briefs, design tokens, variants, or assets into
  production SwiftUI for iOS, iPadOS, macOS, watchOS, tvOS, or visionOS using
  Figma MCP context. Covers Figma-to-SwiftUI visual fidelity, Auto Layout to
  SwiftUI layout, Asset Catalog export, responsive device frames, component
  variants, existing-screen adaptation audits, and project-aware native SwiftUI
  implementation. Do not use for web, React, Tailwind implementation, generic
  Figma MCP setup alone, UIKit-only implementation, SwiftUI architecture choice,
  or visual design critique without Figma implementation.
---

# Figma SwiftUI

## Purpose

Translate Figma design inputs into production SwiftUI while preserving native
Apple-platform code style, project conventions, asset fidelity, and visual
parity. This skill builds on the general Figma MCP workflow but owns the
SwiftUI-specific translation layer.

## Relationship To Other Skills

- Use `figma` for generic Figma MCP setup, tool troubleshooting, metadata,
  screenshots, variables, and asset retrieval.
- Use `figma-implement-design` for generic Figma-to-code workflows outside
  Apple-platform SwiftUI.
- Use this skill when the target implementation is SwiftUI or an Apple-platform
  SwiftUI component/screen.
- Use `swiftui-patterns` for SwiftUI API behavior not driven by a Figma design.
- Use `swiftui-design` for visual design critique or polish when the task is
  not Figma-to-code implementation.
- Use `swiftui-architecture` when the Figma task becomes a feature architecture
  choice such as MVVM, MVI, TCA, Clean Architecture, or Coordinator ownership.

## When To Use

- Implementing a Figma screen, component, component set, or flow in SwiftUI.
- Adapting an existing SwiftUI screen to match an updated Figma design.
- Mapping Figma design tokens, colors, typography, spacing, shadows, variants,
  or responsive frames into a SwiftUI design system.
- Exporting Figma-owned icons, logos, illustrations, or image fills into an
  Xcode asset catalog.
- Translating Figma Auto Layout, constraints, fixed/hug/fill sizing, effects,
  and prototype transition intent into native SwiftUI.
- Combining a source brief/ticket with Figma visuals for implementation scope,
  behavior, states, and actions.

## Do Not Use When

- The output target is web, React, Tailwind, HTML, or CSS.
- The task is only Figma MCP setup or login troubleshooting; use `figma`.
- The task is only visual critique with no implementation; use `swiftui-design`.
- The task is UIKit-only implementation; use project context or a UIKit-specific
  skill if one exists.
- The task is choosing SwiftUI feature architecture; use `swiftui-architecture`.
- The Figma link is a prototype or FigJam board rather than a design node; ask
  for a `/design/` or legacy `/file/` node link.

## Required Workflow

1. Read local project truth first:
   - user request and any attached source brief/ticket
   - `AGENTS.md`, `README.md`, project docs
   - Xcode project/package files and existing SwiftUI/design-system code
2. If a source brief, ticket, `.txt`, or `.md` accompanies the Figma work, read
   `references/source-document.md` before any Figma MCP call.
3. Parse the Figma URL or use the selected Figma desktop node:
   - accept `/design/:fileKey/...?...node-id=...`
   - accept legacy `/file/:fileKey/...?...node-id=...`
   - ignore unrelated query parameters such as `m=dev`, `t`, and `page-id`
   - convert URL node IDs from `3166-70147` to MCP node IDs `3166:70147`
4. If the node might be a page, root frame, flow, large container, or
   multi-screen group, read `references/screen-discovery.md` and use metadata
   before fetching expensive design context.
5. Fetch Figma data through MCP:
   - `get_metadata` when discovery is needed
   - `get_design_context` for exact target nodes, using a SwiftUI/iOS prompt
     when the server supports it
   - `get_screenshot` for visual ground truth
   - `get_variable_defs` when variables/tokens are available
   - asset URLs or node screenshots for visible Figma-owned assets
6. Before coding, build a visual asset inventory and read
   `references/asset-handling.md` for any non-text visual element.
7. If updating an existing screen, read `references/adaptation-workflow.md` and
   complete an element-by-element diff audit before editing code.
8. Inspect project dependencies and conventions:
   - image loading libraries such as Kingfisher, SDWebImage, Nuke, or a custom
     image cache
   - animation libraries such as Lottie
   - shared UI/design-system modules
   - token definitions, colors, fonts, spacing helpers, and asset catalog style
9. Translate into native SwiftUI. Do not port React/Tailwind output directly.
10. Validate only as requested by the user or local workflow. If validation is
    requested, compare against the Figma screenshot and use project-supported
    previews, simulator runs, or snapshot tests.

## Reference Routing

- `references/source-document.md`: scope and behavior contract before Figma.
- `references/fetch-strategy.md`: metadata/context/screenshots/token call
  strategy and timeout handling.
- `references/screen-discovery.md`: root/page/flow node mapping before context.
- `references/asset-handling.md`: Figma assets, PNG export, xcassets,
  rendering modes, and system-symbol substitution rules.
- `references/visual-fidelity.md`: exact value extraction, source-of-truth
  priority, visual inventory, and SwiftUI fidelity pitfalls.
- `references/layout-translation.md`: Auto Layout, padding, sizing, scroll,
  effects, and animation translation.
- `references/responsive-layout.md`: iPhone/iPad/macOS/watchOS/tvOS/visionOS
  adaptive SwiftUI from device-specific Figma frames.
- `references/design-token-mapping.md`: Figma variables to SwiftUI color,
  spacing, typography, radius, shadow, and gradient tokens.
- `references/component-variants.md`: Figma component variants to SwiftUI
  enums, styles, optional slots, and system states.
- `references/adaptation-workflow.md`: existing-screen diff audit.

## Core Rules

- Figma context and screenshot are design specifications, not final code.
- The screenshot is visual ground truth; the source brief owns behavior and
  scope when provided.
- Project conventions beat generic snippets.
- Figma-owned visible assets must be real Figma exports unless the user approves
  a substitution.
- Do not replace Figma logos, illustrations, or designed icons with SF Symbols
  or hand-drawn SwiftUI shapes without approval.
- Do not implement iOS system chrome shown in mockups, such as keyboard, status
  bar, Dynamic Island, home indicator, native back button, system alerts, share
  sheet, native search bar, refresh indicator, or native page indicators.
- Prefer native SwiftUI controls when they match the design; custom controls are
  for non-standard visuals or behavior.
- Preserve accessibility: labels, traits, Dynamic Type decisions, contrast, and
  focus/tap target expectations.

## Output Format

For implementation planning, include:

1. Target node/screen and scope
2. Figma data fetched or still needed
3. Asset inventory and export plan
4. SwiftUI structure and existing components to reuse
5. Token/layout/typography mapping
6. Open questions or validation method

For code changes, keep the final response focused on files changed,
implementation decisions, validation performed, and any unresolved fidelity
risks.
