# Responsive SwiftUI From Figma

Use this when Figma contains fixed device frames, multiple device variants, or
the project supports more devices than the linked frame.

## Ask About Device Scope

Ask before implementing when:

- only an iPhone frame is provided but the app supports iPad or macOS
- only an iPad/macOS frame is provided but the app supports iPhone
- Figma contains separate iPhone and iPad frames
- frame sizes imply watchOS, tvOS, or visionOS but the project scope is unclear

## Fixed Values To Adapt

Keep fixed values for:

- icon display sizes
- avatar sizes
- intentional card heights
- border widths
- corner radii

Adapt values for:

- full-screen widths
- long text containers
- grids
- bottom bars and safe-area-aware controls
- multi-column sections

## SwiftUI Tools

- `GeometryReader` for proportional layout only when container measurements are
  truly needed.
- `containerRelativeFrame` when supported and appropriate.
- `ViewThatFits` for alternate compact/expanded layouts.
- `@Environment(\.horizontalSizeClass)` for iPhone/iPad layout switching.
- `NavigationSplitView` for sidebar/detail designs.
- `LazyVGrid` or `Grid` for multi-column content.
- `.safeAreaInset` for bottom CTAs and toolbars.

## Merging Multi-Device Frames

When Figma provides iPhone and iPad frames:

1. Fetch context and screenshots for each device frame.
2. Identify shared content and device-specific layout changes.
3. Implement one SwiftUI view with adaptive branches.
4. Keep typography and tokens shared unless Figma explicitly changes them.
5. Validate each device class separately if requested.

## Common Patterns

| Figma | SwiftUI |
|---|---|
| iPhone stacked sections, iPad side by side | size class switch between `VStack` and `HStack` |
| iPhone list, iPad grid | `LazyVGrid` with adaptive columns |
| iPad sidebar + detail | `NavigationSplitView` |
| fixed card width in phone frame | max width plus horizontal padding |
| bottom fixed CTA | `.safeAreaInset(edge: .bottom)` |
| content centered on wide screens | max content width and centered frame |

## Checklist

- [ ] Device/platform scope is explicit.
- [ ] Fixed values are intentional, not copied screen constraints.
- [ ] Safe areas are handled by SwiftUI, not hard-coded mockup offsets.
- [ ] Multi-device frames produce one adaptive implementation when practical.
- [ ] Text wrapping and Dynamic Type do not break layout.
