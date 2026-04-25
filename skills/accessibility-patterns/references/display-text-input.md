# Display, Text, And Input Accessibility

Use this file for Dynamic Type, display settings, touch targets, keyboard
navigation, Voice Control, Switch Control, and other non-pointer input paths.

## Dynamic Type And Larger Text

Prefer system text styles over fixed font sizes.

SwiftUI:

```swift
Text(title)
    .font(.body)
```

UIKit:

```swift
label.font = .preferredFont(forTextStyle: .body)
label.adjustsFontForContentSizeCategory = true
```

For custom fonts, scale relative to a text style:

- SwiftUI: `Font.custom(_:size:relativeTo:)`
- UIKit: `UIFontMetrics(forTextStyle:).scaledFont(for:)`

For non-text values that should track the user's text size, use `@ScaledMetric`
or UIKit layout adaptation.

Avoid:

- fixed heights around multiline text
- `minimumScaleFactor` as a first response to clipping
- single-line labels for content that can grow
- hiding essential text at larger sizes

Adapt layout at accessibility sizes with wrapping, stack axis changes,
scrolling, or simplified presentation.

## Large Content Viewer

Do not scale every fixed chrome control with Dynamic Type. For small toolbar,
tab bar, navigation, or icon controls, use Large Content Viewer support when
compatible:

- SwiftUI: `.accessibilityShowsLargeContentViewer()`
- UIKit: `UILargeContentViewerInteraction`

Use it when a fixed visual target needs an enlarged preview.

## Display Settings

Respect system display preferences:

- Reduce Motion: remove decorative motion and replace meaningful motion with
  lower-motion feedback such as opacity or concise state changes.
- Differentiate Without Color: pair color with shape, text, iconography, or
  semantic state.
- Increase Contrast: use semantic colors and verify text/icon contrast in light
  and dark appearances.
- Reduce Transparency: replace blur/material-dependent contrast with opaque or
  higher-contrast surfaces when needed.
- Bold Text and Button Shapes: ensure custom UI still communicates hierarchy
  and affordance.

Do not branch entire layout semantics on whether VoiceOver is running. Adapt
to the concrete setting or user need.

## Touch Targets

Interactive controls should have an effective target of at least 44x44 points
on iOS and iPadOS when practical. Expand the hit area without distorting the
visual design when needed.

Small inline controls should still be reachable, identifiable, and operable
with touch, VoiceOver, Voice Control, Switch Control, and keyboard where
applicable.

## Voice Control

Voice Control depends on accessible names and discoverable elements.

- Visible labels should match the command users can speak.
- Icon-only controls need accessible labels and often input labels.
- Multiple controls with the same label create ambiguity.
- Hidden or swipe-only actions need voice-accessible alternatives.
- Test with "Show Names" and "Show Numbers".

SwiftUI:

```swift
.accessibilityInputLabels(["Compose", "New Message"])
```

UIKit:

```swift
button.accessibilityUserInputLabels = ["Compose", "New Message"]
```

## Switch Control

Switch Control users scan through reachable elements and actions.

- Avoid tiny, time-limited, or gesture-only interactions.
- Group related content when it reduces scan fatigue without hiding controls.
- Expose custom actions for row actions, hidden actions, and gesture-only
  operations.
- Ensure modals, popovers, and custom overlays do not trap scanning.

## Full Keyboard Access

Keyboard users must be able to reach and operate all interactive elements.

- Preserve visible focus.
- Ensure Tab / Shift-Tab order is predictable.
- Support arrows for lists, tables, grids, segmented controls, and menus where
  users expect them.
- Provide a keyboard path for dismissing modals, popovers, and custom panels.
- Avoid mouse-only hover affordances.

## Color, Contrast, And Non-Color Cues

Color can support status, but it must not be the only signal. Add text, icons,
shape, pattern, or VoiceOver value for states such as error, success, selected,
disabled, warning, and required.

Verify contrast in both light and dark appearance, with increased contrast
enabled when relevant. Do not assume a color pair that passes in one appearance
passes in another.

## Checklist

- [ ] Text uses system styles or Dynamic Type-aware custom fonts.
- [ ] Large accessibility sizes do not clip essential content.
- [ ] Motion, transparency, contrast, and color-only state are handled.
- [ ] Controls have effective targets and visible focus where applicable.
- [ ] Voice Control can discover and activate controls by name.
- [ ] Switch Control can reach and operate custom or hidden actions.
- [ ] Keyboard users can complete the flow without a pointer.
