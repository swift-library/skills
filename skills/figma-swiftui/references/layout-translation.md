# Layout Translation

Use this to translate Figma layout concepts into SwiftUI.

## Contents

- [Auto Layout](#auto-layout)
- [Sizing](#sizing)
- [Absolute Frames](#absolute-frames)
- [Scroll](#scroll)
- [Typography](#typography)
- [Color And Effects](#color-and-effects)
- [Components](#components)
- [Minimal Examples](#minimal-examples)
- [Animations](#animations)

## Auto Layout

| Figma | SwiftUI |
|---|---|
| Vertical Auto Layout | `VStack(spacing:alignment:)` |
| Horizontal Auto Layout | `HStack(spacing:alignment:)` |
| Wrap | `LazyVGrid`, custom flow layout, or project component |
| Gap | stack `spacing` |
| Padding | `.padding(...)` before background |
| Align left/top | `.frame(maxWidth: .infinity, alignment: .leading)` as needed |
| Space between | `Spacer()` or `.frame(maxWidth: .infinity)` with alignment |

Use leading/trailing rather than left/right unless the project intentionally
ignores right-to-left layout.

## Sizing

| Figma | SwiftUI |
|---|---|
| Hug contents | intrinsic SwiftUI size; avoid unnecessary frame |
| Fill container | `.frame(maxWidth: .infinity)` or max height as appropriate |
| Fixed width/height | `.frame(width:height:)` |
| Min/max constraints | `.frame(minWidth:idealWidth:maxWidth:...)` |
| Preserve aspect ratio | `.aspectRatio(ratio, contentMode:)` |
| Clip content | `.clipped()` or shape clip |

Avoid fixed screen-size frames unless the design is a fixed asset or the user
only targets one device class.

## Absolute Frames

Figma frames without Auto Layout often use absolute x/y positions. Prefer
semantic stacks when possible. Use `ZStack`, alignment, and offsets only when
the design is genuinely layered or spatial.

Do not build an entire screen as absolute offsets if the UI contains normal
content flow, text wrapping, or Dynamic Type.

## Scroll

- Figma clipped vertical overflow -> `ScrollView(.vertical)`.
- Figma clipped horizontal overflow -> `ScrollView(.horizontal)`.
- Repeating card rows -> `LazyVStack` or `LazyVGrid`.
- Avoid `List` when Figma shows a custom flat list without platform row
  behavior.
- Use `.safeAreaInset` for pinned bottom CTAs or toolbars when appropriate.

## Typography

| Figma | SwiftUI |
|---|---|
| Font family | project font, custom font, or system fallback |
| Weight | `Font.Weight` |
| Size | `.font(.system(size:weight:design:))` or project token |
| Line height | `.lineSpacing(...)` plus layout tuning |
| Letter spacing | `.tracking(...)` |
| Expanded/condensed | `.fontWidth(...)` when available |

Prefer project typography tokens if they match; otherwise preserve Figma values
for fidelity-critical screens.

## Color And Effects

| Figma | SwiftUI |
|---|---|
| Solid fill | `Color` token or asset color |
| Opacity | color alpha or `.opacity()` depending on layer vs fill opacity |
| Linear gradient | `LinearGradient` |
| Radial gradient | `RadialGradient` |
| Corner radius | `.clipShape(.rect(cornerRadius:))` |
| Uneven corners | `UnevenRoundedRectangle` where available |
| Stroke | `.overlay(shape.stroke(...))` |
| Drop shadow | `.shadow(color:radius:x:y:)` |
| Blur | `.blur(radius:)` or material background |
| Mask | `.mask { ... }` |
| Blend mode | `.blendMode(...)` |
| Liquid Glass | `glassEffect` only when target SDK supports it |

## Components

- Figma button -> project button component or `Button` with custom style.
- Text input -> `TextField`, `SecureField`, or `TextEditor`.
- Toggle -> `Toggle` with project/custom style if needed.
- Image -> asset catalog or project remote image loader.
- Card -> background + clip shape + stroke/shadow as needed.
- Sheet/modal -> `.sheet`, `.fullScreenCover`, or project routing.
- Navigation bar -> native `.navigationTitle`/toolbar when it matches; custom
  header only when design is meaningfully custom.
- Component instance -> search existing SwiftUI components before creating a
  new one.

## Minimal Examples

Figma vertical Auto Layout card:

```text
Frame: vertical, gap 12, padding 16, fill #FFFFFF, radius 16, shadow
Children: title text, body text, CTA
```

SwiftUI:

```swift
VStack(alignment: .leading, spacing: 12) {
    Text(title)
        .font(.headline)

    Text(body)
        .font(.subheadline)
        .foregroundStyle(.secondary)

    Button("Continue", action: continueAction)
        .buttonStyle(.borderedProminent)
}
.padding(16)
.frame(maxWidth: .infinity, alignment: .leading)
.background(Color("surfaceDefault"))
.clipShape(.rect(cornerRadius: 16))
.shadow(color: .black.opacity(0.10), radius: 18, x: 0, y: 8)
```

Bottom pinned CTA from Figma frame:

```swift
ScrollView {
    content
        .padding(.horizontal, 20)
}
.safeAreaInset(edge: .bottom) {
    Button("Continue", action: continueAction)
        .frame(maxWidth: .infinity)
        .padding(.horizontal, 20)
        .padding(.vertical, 12)
        .background(.regularMaterial)
}
```

Flat custom list:

```swift
ScrollView {
    LazyVStack(spacing: 0) {
        ForEach(items) { item in
            RowView(item: item)
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
        }
    }
}
```

## Animations

Prototype transitions are intent, not exact SwiftUI code.

- dissolve -> opacity transition
- slide/move -> move transition or navigation
- push -> `NavigationStack`
- smart animate -> state-driven animation or matched geometry
- complex animation asset -> use project animation library such as Lottie if
  already present

Do not over-animate static mockups. Ask before implementing complex sequenced
animations.
