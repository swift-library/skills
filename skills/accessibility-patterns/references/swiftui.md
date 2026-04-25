# SwiftUI Accessibility

Use this file for SwiftUI source changes involving accessibility modifiers,
native controls, grouping, custom actions, focus, rotors, and custom control
representation.

## Native Controls First

Prefer `Button`, `NavigationLink`, `Toggle`, `Picker`, `Stepper`, `Slider`,
`TextField`, `SecureField`, `Link`, `Menu`, `DisclosureGroup`, `List`, and
system sheets before custom gesture-based views.

Use `Button` instead of `onTapGesture` for ordinary activation. If a custom
gesture is unavoidable, add complete accessibility semantics and an action.

## Images And Icon-Only Controls

Decorative asset image:

```swift
Image(decorative: "BackgroundTexture")
```

Decorative SF Symbol:

```swift
Image(systemName: "chevron.right")
    .accessibilityHidden(true)
```

Meaningful image:

```swift
Image("Receipt")
    .accessibilityLabel("Receipt")
```

Icon-only button:

```swift
Button {
    share()
} label: {
    Image(systemName: "square.and.arrow.up")
}
.accessibilityLabel("Share")
```

Prefer a visible or visually-hidden text label where it fits the design:

```swift
Button {
    delete()
} label: {
    Label("Delete", systemImage: "trash")
        .labelStyle(.iconOnly)
}
```

## Element Grouping

Use `.combine` when child text should be read as one phrase:

```swift
VStack(alignment: .leading) {
    Text(order.title)
    Text(order.status)
}
.accessibilityElement(children: .combine)
```

Use `.ignore` only when the parent supplies full semantics:

```swift
VStack(alignment: .leading) {
    Text(product.name)
    Text(product.price, format: .currency(code: product.currencyCode))
}
.accessibilityElement(children: .ignore)
.accessibilityLabel(product.name)
.accessibilityValue(product.price.formatted(.currency(code: product.currencyCode)))
```

Use `.contain` for named groups that users can enter and leave.

## Traits, Values, And Actions

Expose state as traits or values:

```swift
.accessibilityAddTraits(isSelected ? [.isSelected, .isButton] : .isButton)
.accessibilityValue(isEnabled ? "Enabled" : "Disabled")
```

Use custom actions for hidden or gesture-only operations:

```swift
.accessibilityAction(named: "Archive") {
    archive()
}
```

Use adjustable actions for custom sliders, steppers, ratings, pages, and
similar increment/decrement controls:

```swift
.accessibilityAdjustableAction { direction in
    switch direction {
    case .increment: value = min(value + 1, maxValue)
    case .decrement: value = max(value - 1, minValue)
    @unknown default: break
    }
}
```

## Voice Control

Use `accessibilityInputLabels(_:)` when visible labels are absent, changing, or
hard to speak:

```swift
Button {
    buy()
} label: {
    Image(systemName: "cart.badge.plus")
}
.accessibilityLabel("Buy")
.accessibilityInputLabels(["Buy", "Add to Cart"])
```

Voice Control labels should match visible text when visible text exists.

## Focus And Navigation

Use `AccessibilityFocusState` when a SwiftUI view needs to move assistive
technology focus after a screen change, validation error, or important content
replacement. Confirm deployment-target availability before adding it.

Use rotors only when they materially improve navigation through structured
content such as headings, unread items, errors, or search results.

## Custom Controls

For custom controls that visually differ from their accessible behavior, use
`accessibilityRepresentation` when compatible:

```swift
CustomRatingView(value: rating)
    .accessibilityRepresentation {
        Slider(value: $rating, in: 1...5) {
            Text("Rating")
        }
    }
```

If `accessibilityRepresentation` is not available or not appropriate, provide
label, value, traits, and actions manually.

## Dynamic Type And Display Settings

Use built-in text styles and Dynamic Type-aware custom fonts. For custom
spacing or icon sizes that should scale with text, use `@ScaledMetric`.

Use environment values for accessibility settings:

- `accessibilityReduceMotion`
- `accessibilityReduceTransparency`
- `accessibilityDifferentiateWithoutColor`
- `colorSchemeContrast`
- `dynamicTypeSize`

See `display-text-input.md` for detailed text, motion, contrast, and input
rules.

When color carries meaning, also provide a non-color cue when
`accessibilityDifferentiateWithoutColor` is enabled:

```swift
@Environment(\.accessibilityDifferentiateWithoutColor) private var differentiate

HStack {
    if differentiate {
        Image(systemName: status.symbolName)
    }
    Text(status.title)
}
.foregroundStyle(status.color)
```

When motion is decorative or large-scale, respect `accessibilityReduceMotion`
and prefer opacity, small scale changes, or no animation:

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

content
    .transition(reduceMotion ? .opacity : .slide)
```

## Label-Content Pairing

Use `accessibilityLabeledPair` when a visible label and its control or value
are separate views but should be associated semantically:

```swift
@Namespace private var namespace

HStack {
    Text("Volume")
        .accessibilityLabeledPair(role: .label, id: "volume", in: namespace)
    Slider(value: $volume)
        .accessibilityLabeledPair(role: .content, id: "volume", in: namespace)
}
```

## Checklist

- [ ] Native controls are used where possible.
- [ ] Icon-only controls have meaningful labels.
- [ ] Visible text controls are not redundantly relabeled.
- [ ] Decorative images are hidden.
- [ ] Custom controls expose role, value, and activation.
- [ ] Swipe-only or gesture-only operations have accessibility actions.
- [ ] Dynamic Type and Reduce Motion are respected where relevant.
- [ ] Color-coded UI also has a non-color cue when needed.
- [ ] Voice Control can discover and activate controls.
