# Before / After: UIKit Accessibility

Use these examples for UIKit patch shape. Adapt labels, localization, target
OS, and existing architecture to the local project.

## Custom Tappable View

Before:

```swift
final class ProductCardView: UIView {
    var product: Product?
}
```

After:

```swift
final class ProductCardView: UIView {
    var product: Product? {
        didSet { updateAccessibility() }
    }

    override var isAccessibilityElement: Bool {
        get { true }
        set { }
    }

    override var accessibilityTraits: UIAccessibilityTraits {
        get { .button }
        set { }
    }

    override var accessibilityLabel: String? {
        get { product?.name }
        set { }
    }

    override var accessibilityHint: String? {
        get { "Opens product details" }
        set { }
    }

    private func updateAccessibility() {
        UIAccessibility.post(notification: .layoutChanged, argument: self)
    }
}
```

Why:

- Custom views are not accessible controls by default.
- The label and trait make the card discoverable and operable.

## Table Cell Grouping

Before:

```swift
titleLabel.text = invoice.title
subtitleLabel.text = invoice.dueDateText
amountLabel.text = invoice.amountText
```

After:

```swift
isAccessibilityElement = true
accessibilityTraits = [.button]
accessibilityLabel = invoice.title
accessibilityValue = "\(invoice.dueDateText). Amount \(invoice.amountText)"

titleLabel.isAccessibilityElement = false
subtitleLabel.isAccessibilityElement = false
amountLabel.isAccessibilityElement = false
```

Why:

- A dense row becomes one understandable VoiceOver stop.
- Child labels do not duplicate the grouped row.

## Swipe-Only Row Actions

Before:

```swift
// Delete and archive exist only as trailing swipe actions.
```

After:

```swift
override var accessibilityCustomActions: [UIAccessibilityCustomAction]? {
    get {
        [
            UIAccessibilityCustomAction(name: "Archive") { [weak self] _ in
                self?.archive()
                return true
            },
            UIAccessibilityCustomAction(name: "Delete") { [weak self] _ in
                self?.delete()
                return true
            }
        ]
    }
    set { }
}
```

Why:

- VoiceOver, Voice Control, and Switch Control users can reach row actions
  without performing a swipe gesture.

## Dynamic Type Custom Font

Before:

```swift
titleLabel.font = UIFont(name: "AvenirNext-DemiBold", size: 16)
```

After:

```swift
let baseFont = UIFont(name: "AvenirNext-DemiBold", size: 16)
    ?? .preferredFont(forTextStyle: .headline)
titleLabel.font = UIFontMetrics(forTextStyle: .headline).scaledFont(for: baseFont)
titleLabel.adjustsFontForContentSizeCategory = true
```

Why:

- Custom fonts scale with the user's preferred content size.
- The fallback avoids losing text if the font fails to load.
