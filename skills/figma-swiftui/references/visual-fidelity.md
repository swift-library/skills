# Visual Fidelity

Use this before implementing nontrivial screens and when final output must
match Figma closely.

## Contents

- [Source Priority](#source-priority)
- [Visual Inventory](#visual-inventory)
- [Exact Values](#exact-values)
- [SwiftUI Defaults That Drift](#swiftui-defaults-that-drift)
- [Minimal Examples](#minimal-examples)
- [System Chrome](#system-chrome)
- [Screenshot Cross-Check](#screenshot-cross-check)

## Source Priority

1. User/source brief for scope, behavior, and product states.
2. Figma screenshot for visual appearance.
3. Figma design context for exact values.
4. Figma variables for token names and modes.
5. Existing project design system for implementation names and conventions.
6. Agent inference only when the above sources do not specify something.

When screenshot and design context conflict, inspect the screenshot and ask if
the difference is material.

## Visual Inventory

Before coding, summarize the screen by sections:

```text
Root: 390x844 iPhone frame
System chrome: status bar and home indicator, skip
Header: custom title, back icon asset, 16 horizontal padding
Form: email field, password field, 12 gap
CTA: primary button, disabled and enabled variants
Assets: logo node 4:2, eye icon node 4:8
States from brief: loading, invalid email, auth failure
```

Keep this as scratch unless the user asks for an implementation plan.

## Exact Values

- Use arbitrary or inline values from MCP output literally before rounding.
- Carry color, opacity, gradient stops, shadow offset, blur, radius, stroke
  width, spacing, and padding.
- For text, carry family, size, weight, line height, letter spacing, and width
  when present.
- Map project tokens by value or semantic role; do not create parallel tokens if
  a matching project token already exists.

## SwiftUI Defaults That Drift

Text:

- `.font(.system(size:))` does not guarantee Figma line height.
- Use `.tracking()` for Figma letter spacing.
- Expanded or condensed text needs font width support when available.
- Test real content length, not only Figma placeholder text.

Buttons:

- A default `Button` applies system styling. Use `.buttonStyle(.plain)` or a
  project button style for custom Figma buttons.

Stacks:

- `VStack` and `HStack` have default spacing. Always set `spacing`.
- Applying `.padding` before or after `.background` changes the rendered box.
  Figma inner padding usually means padding before background.

Images:

- Match `.fit` vs `.fill` to Figma clipping.
- Template icons require template rendering and foreground styling.

Lists:

- `List` adds row insets, separators, and platform styling. Use `ScrollView`
  plus `LazyVStack` when the design is a flat custom list.

Navigation:

- `NavigationStack` adds platform title and bar behavior. Use native navigation
  when it matches; use a custom header only for non-standard designs.

Shadows:

- SwiftUI default shadow opacity is rarely the Figma value. Use explicit color,
  radius, x, and y.

## Minimal Examples

Figma text style:

```text
font: SF Pro
size: 16
weight: 600
line-height: 22
letter-spacing: -0.32
```

SwiftUI shape:

```swift
Text(title)
    .font(.system(size: 16, weight: .semibold))
    .tracking(-0.32)
    .lineSpacing(6) // line-height - font-size
```

Figma custom button:

```swift
Button(action: submit) {
    Text("Continue")
        .font(.system(size: 17, weight: .semibold))
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
        .background(Color.accentColor)
        .clipShape(.rect(cornerRadius: 14))
}
.buttonStyle(.plain)
```

Figma card shadow:

```swift
RoundedRectangle(cornerRadius: 16)
    .fill(Color("surfaceDefault"))
    .shadow(color: .black.opacity(0.10), radius: 18, x: 0, y: 8)
```

## System Chrome

Skip iOS-provided elements that designers include for context:

- status bar, Dynamic Island, battery, signal, and time
- keyboard and emoji picker
- home indicator
- native navigation back button
- native tab bar when using `TabView`
- system alerts/action sheets
- share sheet
- native search bar when using `.searchable`
- pull-to-refresh indicator
- native page dots for page-style `TabView`

Ask if an element could be either custom or system-provided.

## Screenshot Cross-Check

Before implementation:

- identify system chrome to skip
- locate all visible assets
- note exact section spacing and alignment
- record device frame size and safe-area assumptions

After implementation, compare:

- layout, spacing, alignment, and sizing
- typography and line wrapping
- colors, opacity, gradients, shadows, and strokes
- asset presence and rendering mode
- custom states, dark mode, and responsive variants if provided
