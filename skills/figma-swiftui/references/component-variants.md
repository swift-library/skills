# Component Variants

Use this when Figma component variants need to become SwiftUI component APIs.

## Contents

- [Identify Variants](#identify-variants)
- [Prefer System State First](#prefer-system-state-first)
- [Style Variants](#style-variants)
- [Size Variants](#size-variants)
- [Content Toggles](#content-toggles)
- [Ask Before Broad APIs](#ask-before-broad-apis)
- [Minimal Example](#minimal-example)
- [Checklist](#checklist)

## Identify Variants

Look for Figma properties such as:

- state: default, pressed, disabled, selected, focused, error
- size: small, medium, large
- style/type: primary, secondary, destructive, ghost
- content toggles: icon, subtitle, badge, loading indicator
- density/platform: compact, regular, iPad, macOS

Fetch sibling variants when a component set is needed, not only the default
instance.

## Prefer System State First

Map to native SwiftUI mechanisms when the variant is already a system concept:

- disabled -> `.disabled(...)`
- pressed -> `ButtonStyle.Configuration.isPressed`
- focused -> `@FocusState` or focused modifiers
- selected -> `Toggle`, `Picker`, custom selection state, or project component
- loading -> explicit state only if the design has a real loading visual

Only create custom state enums for states not covered by system behavior.

## Style Variants

Use one enum when variants differ mainly by color, border, font, or icon:

```swift
enum ActionButtonVariant {
    case primary
    case secondary
    case destructive
}
```

Use separate components or styles when variants change structure, layout, or
semantics substantially.

## Size Variants

For system controls, prefer `.controlSize(...)` when it matches.

For custom components, use a size enum that maps to padding, height, font, and
icon size:

```swift
enum ChipSize {
    case compact
    case regular

    var horizontalPadding: CGFloat {
        switch self {
        case .compact: 8
        case .regular: 12
        }
    }
}
```

## Content Toggles

Use optional parameters for simple slots:

```swift
struct ActionButton: View {
    let title: String
    let icon: Image?
    let isLoading: Bool
}
```

Use generic `@ViewBuilder` slots when slot content can vary structurally:

```swift
struct Card<Accessory: View>: View {
    let title: String
    @ViewBuilder var accessory: () -> Accessory
}
```

## Ask Before Broad APIs

If a Figma component set implies a reusable design-system component, summarize
the detected variants and ask whether to:

- implement only the current instance
- extend an existing project component
- create a reusable SwiftUI component with variant API

## Minimal Example

Use a variant enum when Figma changes color/border/icon but the component
structure is the same:

```swift
enum PillButtonVariant {
    case primary
    case secondary

    var background: Color {
        switch self {
        case .primary: Color("accent")
        case .secondary: Color("surfaceSubtle")
        }
    }

    var foreground: Color {
        switch self {
        case .primary: .white
        case .secondary: Color("textPrimary")
        }
    }
}

struct PillButton: View {
    let title: String
    var variant: PillButtonVariant = .primary
    var icon: Image?
    var action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 8) {
                if let icon {
                    icon
                        .renderingMode(.template)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 16, height: 16)
                }
                Text(title)
            }
            .font(.system(size: 15, weight: .semibold))
            .foregroundStyle(variant.foreground)
            .padding(.horizontal, 14)
            .padding(.vertical, 10)
            .background(variant.background)
            .clipShape(.capsule)
        }
        .buttonStyle(.plain)
    }
}
```

If the pressed/disabled visuals are Figma variants, prefer a `ButtonStyle`
when those states should be automatic.

## Checklist

- [ ] All relevant Figma variants were fetched or accounted for.
- [ ] System states use system mechanisms when possible.
- [ ] Variant API is proportional to project reuse.
- [ ] Optional slots do not force placeholder views.
- [ ] Existing project components are reused or extended first.
