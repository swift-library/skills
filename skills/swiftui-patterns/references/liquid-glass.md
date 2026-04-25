# SwiftUI Liquid Glass Reference (iOS 26+)

## Table of Contents

- [Overview](#overview)
- [Availability](#availability)
- [Core APIs](#core-apis)
- [GlassEffectContainer](#glasseffectcontainer)
- [Glass Button Styles](#glass-button-styles)
- [Morphing Transitions](#morphing-transitions)
- [Advanced Surfaces](#advanced-surfaces)
- [Modifier Order](#modifier-order)
- [Complete Examples](#complete-examples)
- [Fallback Strategies](#fallback-strategies)
- [Design System Notes](#design-system-notes)
- [Review Boundaries](#review-boundaries)
- [Best Practices](#best-practices)
- [Checklist](#checklist)

## Overview

Liquid Glass is Apple's new design language introduced in iOS 26. It provides translucent, dynamic surfaces that respond to content and user interaction. This reference covers the native SwiftUI APIs for implementing Liquid Glass effects.

**Only adopt Liquid Glass when explicitly requested by the user.** Do not proactively convert existing UI to glass effects.

## Availability

All Liquid Glass APIs require iOS 26 or later. Always provide fallbacks:

```swift
if #available(iOS 26, *) {
    // Liquid Glass implementation
} else {
    // Fallback using materials
}
```

## Core APIs

### glassEffect Modifier

The primary modifier for applying glass effects to views:

```swift
.glassEffect(_ style: GlassEffectStyle = .regular, in shape: some Shape = .rect)
```

#### Basic Usage

```swift
Text("Hello")
    .padding()
    .glassEffect()  // Default regular style, rect shape
```

#### With Shape

```swift
Text("Rounded Glass")
    .padding()
    .glassEffect(in: .rect(cornerRadius: 16))

Image(systemName: "star")
    .padding()
    .glassEffect(in: .circle)

Text("Capsule")
    .padding(.horizontal, 20)
    .padding(.vertical, 10)
    .glassEffect(in: .capsule)
```

### GlassEffectStyle

#### Prominence Levels

```swift
.glassEffect(.regular)     // Standard glass appearance
.glassEffect(.prominent)   // More visible, higher contrast
```

#### Tinting

Add color tint to the glass:

```swift
.glassEffect(.regular.tint(.blue))
.glassEffect(.prominent.tint(.red.opacity(0.3)))
```

#### Interactivity

Make glass respond to touch/pointer hover:

```swift
// Interactive glass - responds to user interaction
.glassEffect(.regular.interactive())

// Combined with tint
.glassEffect(.regular.tint(.blue).interactive())
```

**Important**: Only use `.interactive()` on elements that actually respond to user input (buttons, tappable views, focusable elements).

## GlassEffectContainer

Wraps multiple glass elements for proper visual grouping and spacing.

**Glass cannot sample other glass.** The glass material reflects and refracts light by sampling content from an area larger than itself. Nearby glass elements in different containers will produce inconsistent visual results because they cannot sample each other. `GlassEffectContainer` gives grouped elements a shared sampling region, ensuring a consistent appearance.

```swift
GlassEffectContainer {
    HStack {
        Button("One") { }
            .glassEffect()
        Button("Two") { }
            .glassEffect()
    }
}
```

### With Spacing

Control the visual spacing between glass elements:

```swift
GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        GlassChip(icon: "pencil")
        GlassChip(icon: "eraser")
        GlassChip(icon: "trash")
    }
}
```

**Note**: The container's `spacing` parameter should match the actual spacing in your layout for proper glass effect rendering.

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

## Glass Button Styles

Built-in button styles for glass appearance:

```swift
// Standard glass button
Button("Action") { }
    .buttonStyle(.glass)

// Prominent glass button (higher visibility)
Button("Primary Action") { }
    .buttonStyle(.glassProminent)
```

### Custom Glass Buttons

For more control, apply glass effect manually:

```swift
Button(action: { }) {
    Label("Settings", systemImage: "gear")
        .padding()
}
.glassEffect(.regular.interactive(), in: .capsule)
```

## Morphing Transitions

Create smooth transitions between glass elements using `glassEffectID` and `@Namespace`:

```swift
struct MorphingExample: View {
    @Namespace private var animation
    @State private var isExpanded = false

    var body: some View {
        GlassEffectContainer {
            if isExpanded {
                ExpandedCard()
                    .glassEffect()
                    .glassEffectID("card", in: animation)
            } else {
                CompactCard()
                    .glassEffect()
                    .glassEffectID("card", in: animation)
            }
        }
        .animation(.smooth, value: isExpanded)
    }
}
```

### Requirements for Morphing

1. Both views must have the same `glassEffectID`
2. Use the same `@Namespace`
3. Wrap in `GlassEffectContainer`
4. Apply animation to the container or parent

## Advanced Surfaces

### Uniting Multiple Glass Effects

- Group related glass controls in one `GlassEffectContainer` when they should
  visually read as one control cluster.
- Keep the container spacing aligned with the actual stack spacing.
- Do not split a single visual cluster across multiple containers unless the
  surfaces are intentionally independent.

### Background Extension

- Use background extension effects only when content should visually continue
  under system chrome.
- Keep foreground controls legible against extended content.
- Remove older custom blur or darkening layers if the system-provided edge
  treatment already solves the contrast problem.

### Horizontal Scroll Under Sidebar

- When horizontal content scrolls behind a sidebar or floating control group,
  verify that the scroll edge, glass sampling region, and hit targets remain
  stable.
- Avoid putting essential actions only in content that can slide under glass.
- Test both compact and regular width layouts before committing the treatment.

## Modifier Order

**Critical**: Apply `glassEffect` after layout and visual modifiers:

```swift
// CORRECT order
Text("Label")
    .font(.headline)           // 1. Typography
    .foregroundStyle(.primary) // 2. Color
    .padding()                 // 3. Layout
    .glassEffect()             // 4. Glass effect LAST

// WRONG order - glass applied too early
Text("Label")
    .glassEffect()             // Wrong position
    .padding()
    .font(.headline)
```

## Complete Examples

### Toolbar with Glass Buttons

```swift
struct GlassToolbar: View {
    var body: some View {
        if #available(iOS 26, *) {
            GlassEffectContainer(spacing: 16) {
                HStack(spacing: 16) {
                    ToolbarButton(icon: "pencil", action: { })
                    ToolbarButton(icon: "eraser", action: { })
                    ToolbarButton(icon: "scissors", action: { })
                    Spacer()
                    ToolbarButton(icon: "square.and.arrow.up", action: { })
                }
                .padding(.horizontal)
            }
        } else {
            // Fallback toolbar
            HStack(spacing: 16) {
                // ... fallback implementation
            }
        }
    }
}

struct ToolbarButton: View {
    let icon: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.title2)
                .frame(width: 44, height: 44)
        }
        .glassEffect(.regular.interactive(), in: .circle)
    }
}
```

### Card with Glass Effect

```swift
struct GlassCard: View {
    let title: String
    let subtitle: String

    var body: some View {
        if #available(iOS 26, *) {
            cardContent
                .glassEffect(.regular, in: .rect(cornerRadius: 20))
        } else {
            cardContent
                .background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 20))
        }
    }

    private var cardContent: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.headline)
            Text(subtitle)
                .font(.subheadline)
                .foregroundStyle(.secondary)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}
```

### Segmented Control

```swift
struct GlassSegmentedControl: View {
    @Binding var selection: Int
    let options: [String]
    @Namespace private var animation

    var body: some View {
        if #available(iOS 26, *) {
            GlassEffectContainer(spacing: 4) {
                HStack(spacing: 4) {
                    ForEach(options.indices, id: \.self) { index in
                        Button(options[index]) {
                            withAnimation(.smooth) {
                                selection = index
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .glassEffect(
                            selection == index ? .prominent.interactive() : .regular.interactive(),
                            in: .capsule
                        )
                        .glassEffectID(selection == index ? "selected" : "option\(index)", in: animation)
                    }
                }
                .padding(4)
            }
        } else {
            Picker("Options", selection: $selection) {
                ForEach(options.indices, id: \.self) { index in
                    Text(options[index]).tag(index)
                }
            }
            .pickerStyle(.segmented)
        }
    }
}
```

## Fallback Strategies

### Using Materials

```swift
if #available(iOS 26, *) {
    content.glassEffect()
} else {
    content.background(.ultraThinMaterial, in: RoundedRectangle(cornerRadius: 16))
}
```

### Available Materials for Fallback

- `.ultraThinMaterial` - Closest to glass appearance
- `.thinMaterial` - Slightly more opaque
- `.regularMaterial` - Standard blur
- `.thickMaterial` - More opaque
- `.ultraThickMaterial` - Most opaque

### Conditional Modifier Extension

```swift
extension View {
    @ViewBuilder
    func glassEffectWithFallback(
        _ style: GlassEffectStyle = .regular,
        in shape: some Shape = .rect,
        fallbackMaterial: Material = .ultraThinMaterial
    ) -> some View {
        if #available(iOS 26, *) {
            self.glassEffect(style, in: shape)
        } else {
            self.background(fallbackMaterial, in: shape)
        }
    }
}
```

## Design System Notes

### Toolbar Icons

In the new design, toolbar icons use **monochrome rendering** by default. The monochrome palette reduces visual noise and maintains legibility. Use `tint(_:)` only to convey meaning (e.g., a call to action), not for visual effect.

### Sheet Presentations

Partial-height sheets use a Liquid Glass background by default. If you previously used `presentationBackground(_:)` with a custom background, consider removing it to let the new material shine. Sheets can morph out of the glass controls that present them using `navigationZoomTransition`.

### Scroll Edge Effects

An automatic scroll edge effect blurs and fades content under system toolbars to keep controls legible. Remove any custom background-darkening effects behind bar items, as they will interfere.

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

## Review Boundaries

- Use this reference for API correctness, modifier ordering, availability,
  fallback, and source-level implementation review.
- Use `swiftui-design` when the primary task is visual direction, hierarchy,
  spacing, color, or product-level polish.
- Use `xcode-instruments` when the issue depends on measured scrolling,
  animation, hang, hitch, or rendering trace evidence.
- Do not proactively convert an existing interface to Liquid Glass without an
  explicit user request or existing project convention.

## Best Practices

### Do

- Use `GlassEffectContainer` for grouped glass elements (glass cannot sample other glass)
- Apply glass after layout modifiers
- Use `.interactive()` only on tappable elements
- Match container spacing with layout spacing
- Provide material-based fallbacks for older iOS
- Keep glass shapes consistent within a feature
- Use `.glassProminent` only for actions that need stronger visual priority
- Remove custom `presentationBackground(_:)` on sheets to use the default glass material

### Don't

- Apply glass to every element (use sparingly)
- Use `.interactive()` on static content
- Mix different corner radii arbitrarily
- Forget iOS version checks
- Apply glass before padding/frame modifiers
- Nest `GlassEffectContainer` unnecessarily
- Put essential controls in content that can scroll under a glass surface
- Add custom darkening backgrounds behind toolbars (conflicts with scroll edge effect)

## Checklist

- [ ] `#available(iOS 26, *)` with fallback
- [ ] `GlassEffectContainer` wraps grouped elements
- [ ] `.glassEffect()` applied after layout modifiers
- [ ] `.interactive()` only on user-interactable elements
- [ ] `glassEffectID` with `@Namespace` for morphing
- [ ] Consistent shapes and spacing across feature
- [ ] Container spacing matches layout spacing
- [ ] Appropriate prominence levels used
