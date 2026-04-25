# Adaptation Workflow

Use this when updating an existing SwiftUI screen to match a Figma design.

## When To Use

- User says adapt, update, align, match, refresh, or bring existing screen to
  Figma.
- User provides a Figma node and names an existing view/screen.
- Existing code already implements part of the design.

## Rule

Do an audit before edits. Adaptation fails most often when the agent changes
obvious structure but misses small spacing, typography, color, asset, or
removal differences.

## Process

1. Read existing screen and subcomponents.
2. Fetch Figma context and screenshot for the target node.
3. Build a categorized diff checklist.
4. Clarify removals, ambiguous elements, and new data requirements.
5. Apply all confirmed changes.
6. Validate if requested.

## Diff Checklist Shape

```text
Structural
- ADD: bottom legal text under CTA
- REMOVE: secondary subtitle currently in HeaderView; confirm removal
- UPDATE: list row order: avatar before title

Layout & Spacing
- UPDATE: root horizontal padding 16 -> 20
- UPDATE: title-to-body gap 8 -> 12
- UPDATE: CTA bottom inset should use safeAreaInset

Typography
- UPDATE: title 24 semibold -> 28 semibold expanded
- UPDATE: body line height 20 -> 22

Colors & Styling
- UPDATE: card fill #FFFFFF -> surface/default token
- UPDATE: border opacity 0.08 -> 0.12

Assets
- ADD: logo node 4:2 as asset catalog image
- UPDATE: chevron currently SF Symbol; Figma owns icon, export asset

Behavior / Data
- ADD: disabled CTA until form valid
- ADD: loading state from brief, not shown in Figma
```

## Clarify Before Editing

Ask when:

- Figma removes content that may be product-required.
- A visible element could be system chrome or custom UI.
- New data appears in Figma but no source exists in code.
- The source brief and Figma disagree.
- Matching Figma exactly would violate accessibility or project conventions.

## Apply Changes

- Do not skip small spacing or opacity differences after they are in the
  checklist.
- Keep unrelated refactors out of the adaptation.
- Reuse existing project components when possible.
- Update snapshots/previews/tests when the project has them.

## Checklist

- [ ] Existing code and subcomponents were inspected.
- [ ] Figma screenshot and context were compared element by element.
- [ ] ADD/UPDATE/REMOVE items are explicit.
- [ ] Removals and ambiguous elements were confirmed.
- [ ] Asset substitutions were not made silently.
- [ ] Behavior from the source brief is preserved.
