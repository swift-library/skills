# Before / After: AppKit Accessibility

Use these examples for macOS AppKit patch shape. Adapt labels, keyboard
shortcuts, and focus behavior to the local app.

## Icon-Only `NSButton`

Before:

```swift
let shareButton = NSButton()
shareButton.image = NSImage(named: "share")
shareButton.isBordered = false
```

After:

```swift
let shareButton = NSButton()
shareButton.image = NSImage(named: "share")
shareButton.isBordered = false
shareButton.setAccessibilityLabel("Share") // [VERIFY]
shareButton.toolTip = "Share"
```

Why:

- VoiceOver has a meaningful control name.
- Tooltip improves discoverability for pointer and keyboard users.

## Custom `NSView` Control

Before:

```swift
final class ClickableCardView: NSView {
    var onActivate: (() -> Void)?

    override func mouseDown(with event: NSEvent) {
        onActivate?()
    }
}
```

After:

```swift
final class ClickableCardView: NSView {
    var onActivate: (() -> Void)?

    override var acceptsFirstResponder: Bool { true }

    override func accessibilityRole() -> NSAccessibility.Role? { .button }
    override func accessibilityLabel() -> String? { "Open details" }

    override func mouseDown(with event: NSEvent) {
        onActivate?()
    }

    override func keyDown(with event: NSEvent) {
        switch event.keyCode {
        case 36, 49:
            onActivate?()
        default:
            super.keyDown(with: event)
        }
    }
}
```

Why:

- The custom view can be reached and activated by keyboard.
- VoiceOver receives role and label.

## Table Row Summary

Before:

```swift
// Row visually shows title, assignee, and due date in separate cells.
```

After:

```swift
final class TaskRowView: NSTableRowView {
    var taskName = "" { didSet { updateAccessibility() } }
    var assignee = "" { didSet { updateAccessibility() } }
    var dueDate = "" { didSet { updateAccessibility() } }

    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setAccessibilityElement(true)
        updateAccessibility()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setAccessibilityElement(true)
        updateAccessibility()
    }

    private func updateAccessibility() {
        setAccessibilityLabel(taskName)
        setAccessibilityValue("Assigned to \(assignee), due \(dueDate)")
    }
}
```

Why:

- Dense table content gets a concise row summary.
- The accessible value stays synchronized with row data.
