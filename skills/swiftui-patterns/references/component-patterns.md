# SwiftUI Component Patterns

Use this file for small SwiftUI component surfaces that do not require a full
architecture decision, full view refactor, or dedicated design pass.

## Controls

- Use native controls and control containers first: `Button`, `Toggle`,
  `Slider`, `Picker`, `Stepper`, `Menu`, `ControlGroup`, `Label`, and
  `LabeledContent`.
- Bind controls to the narrowest state that owns the value.
- Keep side effects out of binding setters; use explicit actions or
  `.onChange` when the side effect matters.
- Prefer labels that describe the value or action, not implementation details.

## Forms

- Use `Form` for settings and structured input when platform-native grouping is
  wanted.
- Use `LabeledContent` for title-value rows, metadata rows, and custom
  value-bearing controls that should align with other form rows.
- Keep validation close to the field that caused it.
- Use sections for related settings; do not make one giant form section.
- For modal forms, keep save/cancel ownership inside the form surface when
  possible.

## Searchable

- Keep search text local unless multiple screens need to share it.
- Use scopes only when the result set has meaningful user-facing categories.
- Show empty results differently from no query.
- Debounce only when the search triggers expensive work.

## Grids

- Use `LazyVGrid` or `LazyHGrid` for scrollable grids with many items.
- Prefer adaptive columns for icon grids and fixed columns only when the
  content size and available width are intentionally constrained.
- Keep cell identity stable; do not derive IDs from transient sort or filter
  positions.
- Move image decoding, thumbnail generation, and cache lookup out of cell
  `body`.

## Haptics

- Treat haptics as confirmation for meaningful state changes, not decoration.
- Keep haptic calls inside explicit user actions or state transitions.
- Avoid firing haptics from `body`, computed view properties, or repeatedly
  evaluated modifiers.
- Gate platform-specific haptic APIs and provide a silent fallback.
- Custom tactile patterns, AHAP resources, advanced players, synchronized
  audio-haptic feedback, and Core Haptics engine lifecycle are out of scope.

## Theming And Dynamic Type

- Prefer system colors, materials, typography, and control styles before
  inventing a theme layer.
- If a theme object exists, inject it at the app or feature root through
  environment, not through globals.
- Do not encode fixed text sizes in reusable components unless the design
  explicitly opts out of Dynamic Type.
- Keep theme tokens semantic: use names like `warningBackground` or
  `primaryAction`, not raw color names.

## Previews

- Add previews for meaningful visual states: empty, loading, populated, error,
  disabled, and Dynamic Type when relevant.
- Inject fake dependencies explicitly instead of using live clients.
- Keep preview data small but realistic enough to expose layout problems.

## Loading And Placeholders

- Use `ProgressView` for short indeterminate work.
- Use `redacted(reason:)` or skeleton rows when layout stability matters during
  loading.
- Keep loading, empty, and error states visually distinct.
- Avoid replacing the whole view tree if a localized placeholder preserves
  identity better.

## Overlays And Toasts

- Use overlays for transient local feedback, not as a global notification
  system.
- Keep toast state scoped to the screen or feature that owns the event.
- Avoid stacking multiple overlay systems in the same view hierarchy.

## Title And Top Bars

- Use system navigation titles, toolbars, and title menus before custom bars.
- Keep custom top bars stable across scroll and navigation state.
- Gate iOS-version-specific top-bar APIs and provide a simpler fallback.

## Input Toolbars

- Keep bottom input bars outside scrolling content when they should remain
  anchored.
- Account for keyboard and safe-area behavior before adding manual offsets.
- Keep send/submit actions explicit and disabled when input is invalid.

## Scroll-Reveal Affordances

- Use scroll-reveal controls only when hidden chrome materially improves focus
  on content.
- Preserve a discoverable path back to the hidden action or detail surface.
- Pair reveal motion with stable hit targets; do not move primary actions away
  from the user's finger during the gesture.
- Use haptics sparingly to confirm reveal thresholds or committed actions.

## Media Viewers

- Keep inline media previews lightweight.
- Present heavy viewers in sheets, full-screen covers, or navigation
  destinations depending on task flow.
- Preserve identity between thumbnail and viewer when using matched
  transitions.
- Keep decoding, resizing, and caching concerns out of `body`.
