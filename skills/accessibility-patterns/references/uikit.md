# UIKit Accessibility

Use this file for UIKit source changes involving `UIAccessibility`, view
controllers, cells, custom views, Dynamic Type, focus, announcements, and hit
targets.

## Element Basics

For custom views, decide whether the container or its children should be
accessible elements.

```swift
cardView.isAccessibilityElement = true
cardView.accessibilityLabel = title
cardView.accessibilityValue = status
cardView.accessibilityTraits = [.button]
```

Do not make a container accessible if users need to interact with its child
controls separately.

## Labels, Values, Hints, Traits

- `accessibilityLabel`: what the element is.
- `accessibilityValue`: current state or data.
- `accessibilityHint`: consequence or usage when not obvious.
- `accessibilityTraits`: role and state, such as `.button`, `.header`,
  `.selected`, `.notEnabled`, `.updatesFrequently`, or `.adjustable`.

Use localized strings for all user-facing accessibility text.

Avoid `accessibilityIdentifier` for VoiceOver. It is for UI automation.

## Cells And Dense Rows

For `UITableViewCell` or `UICollectionViewCell`, group row content when a
single row stop improves comprehension:

```swift
contentView.isAccessibilityElement = true
contentView.accessibilityLabel = "\(title), \(subtitle)"
contentView.accessibilityValue = status
contentView.accessibilityTraits = [.button]
```

Keep child controls separate when the row contains independent buttons,
switches, steppers, or text fields.

Use `accessibilityElements` to define order only when visual and source order
cannot be aligned structurally.

## Custom Actions

Expose hidden row actions, swipe actions, and secondary controls with
`UIAccessibilityCustomAction`:

```swift
accessibilityCustomActions = [
    UIAccessibilityCustomAction(name: "Archive") { [weak self] _ in
        self?.archive()
        return true
    }
]
```

For Switch Control, custom actions can make gesture-only behavior reachable.
Confirm the action names are localized.

## Adjustable Controls

Custom sliders, ratings, page controls, or steppers should expose adjustable
behavior:

```swift
override var accessibilityTraits: UIAccessibilityTraits {
    get { super.accessibilityTraits.union(.adjustable) }
    set { super.accessibilityTraits = newValue }
}

override func accessibilityIncrement() {
    value = min(value + 1, maxValue)
}

override func accessibilityDecrement() {
    value = max(value - 1, minValue)
}
```

Keep the value updated after changes.

## Focus And Announcements

Use `UIAccessibility.post` deliberately:

```swift
UIAccessibility.post(notification: .screenChanged, argument: titleLabel)
UIAccessibility.post(notification: .layoutChanged, argument: errorLabel)
UIAccessibility.post(notification: .announcement, argument: "Upload complete")
```

- `.screenChanged`: substantial navigation or modal context change.
- `.layoutChanged`: important content update within current screen.
- `.announcement`: non-focus-changing status.

Avoid announcement spam during rapid progress updates.

## Dynamic Type

Prefer text styles:

```swift
label.font = .preferredFont(forTextStyle: .body)
label.adjustsFontForContentSizeCategory = true
label.numberOfLines = 0
```

For custom fonts, use `UIFontMetrics`:

```swift
let baseFont = UIFont(name: "BrandText-Regular", size: 17)!
label.font = UIFontMetrics(forTextStyle: .body).scaledFont(for: baseFont)
label.adjustsFontForContentSizeCategory = true
```

Avoid fixed heights that clip at accessibility sizes. Adapt stack axis,
constraints, and scrolling behavior where needed.

## Large Content Viewer

For fixed chrome controls such as navigation, toolbar, and tab bar items, use
Large Content Viewer support instead of scaling chrome to extreme text sizes
when compatible with the deployment target.

Use `UILargeContentViewerInteraction` for custom fixed-size elements when
users need an enlarged preview.

## Hit Targets

Interactive controls should have an effective target of at least 44x44 points
on iOS. Expand hit testing when the visual affordance must stay small:

```swift
override func point(inside point: CGPoint, with event: UIEvent?) -> Bool {
    bounds.insetBy(dx: -8, dy: -8).contains(point)
}
```

Keep visual and accessible activation behavior aligned.

## Checklist

- [ ] Custom tappable views expose control semantics.
- [ ] Icon-only controls have localized labels.
- [ ] Changing states expose values or traits.
- [ ] Complex cells have sensible grouping and order.
- [ ] Dynamic Type uses text styles or `UIFontMetrics`.
- [ ] Screen changes and errors move focus or announce appropriately.
- [ ] Swipe-only or gesture-only actions have accessible alternatives.
- [ ] `accessibilityIdentifier` is not mistaken for a user-facing label.
