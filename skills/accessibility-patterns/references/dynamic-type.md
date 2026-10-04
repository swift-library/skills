# Dynamic Type And Larger Text

Use this file when text scaling, custom fonts, clipped text, fixed layouts, or
the Larger Text Nutrition Label is in scope.

## Baseline

Prefer system text styles. They scale automatically and carry semantic meaning
across platforms.

SwiftUI:

```swift
Text(title)
    .font(.headline)
```

UIKit:

```swift
label.font = .preferredFont(forTextStyle: .headline)
label.adjustsFontForContentSizeCategory = true
```

Avoid fixed font sizes for user-facing content unless the content is genuinely
decorative or the project has a carefully scaled design-system wrapper.

## Custom Fonts

SwiftUI custom font:

```swift
Text(title)
    .font(.custom("BrandText-Regular", size: 17, relativeTo: .body))
```

UIKit custom font:

```swift
let base = UIFont(name: "BrandText-Regular", size: 17)!
label.font = UIFontMetrics(forTextStyle: .body).scaledFont(for: base)
label.adjustsFontForContentSizeCategory = true
```

Use a fallback system font if the custom font can fail to load.

## Scaled Non-Text Values

Scale spacing, icon sizes, and custom control dimensions only when they need to
track text size.

```swift
@ScaledMetric(relativeTo: .body) private var iconSize = 20
```

Do not scale every layout value. At large sizes, reflow is often better than
making every visual element bigger.

## Layout Adaptation

Common fixes:

- allow multiline text with `numberOfLines = 0` or SwiftUI wrapping
- remove fixed heights around text
- switch horizontal stacks to vertical layouts at large sizes
- use scrolling when content cannot reasonably fit
- preserve primary content over decorative chrome
- avoid `minimumScaleFactor` as the first fix

SwiftUI example:

```swift
ViewThatFits(in: .horizontal) {
    HStack {
        Text(label)
        Spacer()
        Text(value)
    }

    VStack(alignment: .leading) {
        Text(label)
        Text(value)
    }
}
```

For older targets, use `dynamicTypeSize` or platform-specific content size
category checks.

## Large Content Viewer

Small fixed chrome controls should not necessarily scale to 200%. Use Large
Content Viewer for tab, toolbar, navigation, and compact icon controls when
the deployment target supports it.

SwiftUI:

```swift
Button {
    openSettings()
} label: {
    Image(systemName: "gearshape")
}
.accessibilityLabel("Settings")
.accessibilityShowsLargeContentViewer()
```

UIKit:

```swift
button.showsLargeContentViewer = true
button.largeContentTitle = "Settings"
button.addInteraction(UILargeContentViewerInteraction())
```

## UIKit Change Handling

React to content size category changes only when the view has custom layout
work. `traitCollectionDidChange(_:)` is deprecated as of iOS 17; on iOS 17 and
later, use the trait change registration APIs from `UITraitChangeObservable`:

```swift
registerForTraitChanges([UITraitPreferredContentSizeCategory.self]) { (self: Self, _: UITraitCollection) in
    self.updateLayoutForContentSizeCategory()
}
```

Keep the override only for deployment targets below iOS 17:

```swift
override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
    super.traitCollectionDidChange(previousTraitCollection)
    if traitCollection.preferredContentSizeCategory != previousTraitCollection?.preferredContentSizeCategory {
        updateLayoutForContentSizeCategory()
    }
}
```

## Testing

Test:

- all standard text sizes
- largest accessibility size
- smallest size if density matters
- portrait and landscape on iPhone/iPad
- split view where supported
- localized long strings

Xcode previews and Canvas variants are useful for early checks. Final Larger
Text claims still need common-task testing on device.

## Checklist

- [ ] User-facing text uses text styles or scaled custom fonts.
- [ ] Custom font fallback exists where font loading can fail.
- [ ] Non-text measurements scale only when needed.
- [ ] Large sizes do not clip, overlap, or hide essential content.
- [ ] Horizontal layouts reflow when needed.
- [ ] Fixed chrome uses Large Content Viewer when appropriate.
- [ ] Common tasks work at the largest relevant text size.
