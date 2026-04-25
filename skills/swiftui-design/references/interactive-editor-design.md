# Interactive Editor Design

Use this reference for crop, collage, canvas, media-framing, layout-picker, and
other direct-manipulation SwiftUI editor surfaces.

## Presentation State

Present editor flows from payload state rather than a boolean plus separate
data. This prevents empty or stale editor presentations.

```swift
@State private var activeCropRequest: CropRequest?

.sheet(item: $activeCropRequest) { request in
    CropEditor(request: request)
}
```

Avoid:

```swift
@State private var showCropEditor = false
@State private var selectedImage: UIImage?
```

## Shared Geometry Model

If the user previews pan, zoom, crop, or layout live and later exports the
result, preview and export must share one geometry model.

Rules:

- Normalize adjustment values in one place.
- Use the same bounds and transforms for preview and render.
- Treat zooming out to reveal background as an explicit design decision, not an
  accidental editor-only exception.
- Keep slot, image, crop, and export coordinate conversions out of scattered
  view modifiers.

## Gesture Coordination

Tap, long-press-drag, and pinch compete in SwiftUI unless modeled explicitly.

- Use one interaction state for the active tile, card, or canvas item.
- Decide which gesture has priority and which can run simultaneously.
- Reset temporary gesture state deliberately when selection changes.
- Prefer one coherent state machine over booleans attached to individual
  gestures.

## Fixed Editor Layout

If an editor screen must not scroll, budget vertical space top-down using named
regions:

- header
- canvas stage
- settings region
- bottom toolbar

Keep the sizing math centralized. Do not let every subview invent its own
height. The editable stage should remain visually dominant.

## Custom Headers And Safe Areas

If replacing the system navigation bar:

- Be explicit about whether the parent already respects the safe area.
- Do not add `safeAreaInsets.top` reflexively; double-counting creates obvious
  dead space.
- Keep custom headers compact enough to read as navigation chrome.

## Settings Surfaces

When an editor has several configuration modes such as layout, border, ratio,
or background, show one active settings surface at a time. Stacking every
control on screen weakens the canvas and makes the editor harder to scan.

## Review Checklist

- [ ] Presentation state is payload-driven.
- [ ] Preview and export share geometry.
- [ ] Gesture priority and simultaneous behavior are intentional.
- [ ] Temporary gesture state resets when selection changes.
- [ ] No-scroll layouts use centralized region sizing.
- [ ] Custom headers do not double-count safe-area insets.
- [ ] Only one settings surface is active at a time.
