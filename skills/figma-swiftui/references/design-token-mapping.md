# Design Token Mapping

Use this after fetching Figma variables or when design context exposes colors,
typography, spacing, radii, shadows, or gradients.

## Contents

- [Color](#color)
- [Spacing](#spacing)
- [Typography](#typography)
- [Radius And Stroke](#radius-and-stroke)
- [Shadows](#shadows)
- [Gradients And Opacity](#gradients-and-opacity)
- [Token Checklist](#token-checklist)

## Color

Process:

1. Check project tokens first: asset colors, `Color` extensions, theme objects,
   design-system modules, or generated token files.
2. Match Figma variables by semantic name or exact value.
3. Reuse existing project names where possible.
4. Add new tokens only when no equivalent exists.

Examples:

```swift
extension Color {
    static let surfaceDefault = Color("surfaceDefault")
    static let textPrimary = Color("textPrimary")
}
```

Use Asset Catalog color sets for light/dark variants when available. Use
runtime `colorScheme` branching only if the project already does that or an
asset catalog is not viable.

## Spacing

Map Figma spacing variables to existing spacing constants if they exist.
Otherwise add a single shared namespace:

```swift
enum Spacing {
    static let xsmall: CGFloat = 4
    static let small: CGFloat = 8
    static let medium: CGFloat = 16
}
```

Do not create a parallel spacing system when the project already has one.

## Typography

Carry all relevant fields:

- family
- size
- weight
- line height
- letter spacing
- width/expanded/condensed
- text style role

Prefer project typography tokens when they match. For custom sizes, consider
Dynamic Type support with `@ScaledMetric` or project scaling helpers.

```swift
extension Font {
    static var screenTitle: Font {
        .system(size: 28, weight: .semibold)
    }
}
```

Apply tracking and line-height behavior at call sites or through a reusable text
style helper if the project has one.

## Radius And Stroke

Map radius variables to shared constants. Use `RoundedRectangle` or
`UnevenRoundedRectangle` for per-corner values when supported.

```swift
enum Radius {
    static let card: CGFloat = 16
    static let control: CGFloat = 10
}
```

## Shadows

Keep color, opacity, radius, x, and y. Do not use SwiftUI's default shadow
without explicit values for fidelity-critical components.

```swift
.shadow(
    color: .black.opacity(0.12),
    radius: 16,
    x: 0,
    y: 8
)
```

## Gradients And Opacity

- Preserve gradient stops and direction.
- Use `LinearGradient`, `RadialGradient`, or `AngularGradient` as appropriate.
- Fill opacity belongs on the color; layer opacity belongs on the full view.

## Token Checklist

- [ ] Existing project token system was checked.
- [ ] Light/dark modes are mapped when Figma provides them.
- [ ] Typography includes line height and tracking, not only size.
- [ ] Spacing/radius/shadow values are centralized when reused.
- [ ] New tokens do not duplicate existing semantic tokens.
