# Before / After: SwiftUI Accessibility

Use these examples for output shape and patch style. Adapt labels, copy,
availability, and localization to the local project.

## Icon-Only Button

Before:

```swift
Button(action: shareDocument) {
    Image(systemName: "square.and.arrow.up")
}
```

After:

```swift
Button(action: shareDocument) {
    Image(systemName: "square.and.arrow.up")
}
.accessibilityLabel("Share") // [VERIFY] Confirm this matches the action.
.accessibilityInputLabels(["Share", "Share Document"])
```

Why:

- VoiceOver reads the action instead of the symbol name.
- Voice Control can activate the button by spoken name.
- Inferred labels should be verified by a human or local product copy.

## Tappable Row Using `onTapGesture`

Before:

```swift
HStack {
    Image(product.thumbnail)
    VStack(alignment: .leading) {
        Text(product.name)
        Text(product.price, format: .currency(code: "USD"))
    }
}
.onTapGesture {
    openProduct(product)
}
```

After:

```swift
Button {
    openProduct(product)
} label: {
    HStack {
        Image(product.thumbnail)
            .accessibilityHidden(true)

        VStack(alignment: .leading) {
            Text(product.name)
            Text(product.price, format: .currency(code: "USD"))
        }
    }
}
.accessibilityLabel("\(product.name), \(product.formattedPrice)")
.accessibilityHint("Opens product details")
```

Why:

- `Button` supplies native activation, focus, and control semantics.
- Decorative thumbnail does not create extra VoiceOver stops.
- The row gets one clear accessible name.

## State In Label

Before:

```swift
Button(action: toggleFavorite) {
    Image(systemName: item.isFavorite ? "star.fill" : "star")
}
.accessibilityLabel(item.isFavorite ? "Favorited" : "Not favorited")
```

After:

```swift
Button(action: toggleFavorite) {
    Image(systemName: item.isFavorite ? "star.fill" : "star")
}
.accessibilityLabel("Favorite")
.accessibilityValue(item.isFavorite ? "On" : "Off")
.accessibilityHint(item.isFavorite ? "Removes from favorites" : "Adds to favorites")
```

Why:

- The control name stays stable.
- State is expressed as a value.
- The hint describes the result of activation.

## Color-Only Status

Before:

```swift
Circle()
    .fill(order.isLate ? .red : .green)
```

After:

```swift
Label(order.isLate ? "Late" : "On time",
      systemImage: order.isLate ? "exclamationmark.triangle.fill" : "checkmark.circle.fill")
    .foregroundStyle(order.isLate ? .red : .green)
```

Why:

- Status is understandable without color.
- VoiceOver and Voice Control get visible text semantics.

## Custom Slider

Before:

```swift
VolumeKnob(value: volume)
```

After:

```swift
VolumeKnob(value: volume)
    .accessibilityLabel("Volume")
    .accessibilityValue("\(Int(volume * 100)) percent")
    .accessibilityAdjustableAction { direction in
        switch direction {
        case .increment: volume = min(volume + 0.1, 1)
        case .decrement: volume = max(volume - 0.1, 0)
        @unknown default: break
        }
    }
```

Why:

- Users can change the value without a precise drag gesture.
- Value changes are announced.
