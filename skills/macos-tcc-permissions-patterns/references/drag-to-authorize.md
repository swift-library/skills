# Drag To Authorize

Some macOS privacy lists accept a dragged `.app` bundle. The app can provide a
drag source that writes the bundle file URL to the drag pasteboard; System
Settings remains the target and the user still approves the permission.

This is not a bypass. It only helps the user add the correct app or helper to a
privacy list.

## AppKit Drag Source

Use AppKit when the onboarding control needs custom drag imagery, stable
desktop behavior, or precise pasteboard contents.

```swift
import AppKit

final class DraggableAppView: NSView, NSDraggingSource {
    var appURL: URL = Bundle.main.bundleURL

    override func mouseDown(with event: NSEvent) {
        let item = NSDraggingItem(pasteboardWriter: appURL as NSURL)
        let icon = NSWorkspace.shared.icon(forFile: appURL.path)

        item.setDraggingFrame(bounds, contents: icon)
        beginDraggingSession(with: [item], event: event, source: self)
    }

    func draggingSession(
        _ session: NSDraggingSession,
        sourceOperationMaskFor context: NSDraggingContext
    ) -> NSDragOperation {
        .copy
    }
}
```

Review points:

- Use the bundle that needs trust, not necessarily `Bundle.main`.
- Keep the drag operation as `.copy`; the app is not being moved.
- Set a drag image that looks like the app/helper users will see in System
  Settings.

## SwiftUI Drag Source

SwiftUI can be enough for simple rows:

```swift
import SwiftUI
import AppKit

struct DraggableAppRow: View {
    let appURL: URL

    var body: some View {
        HStack {
            Image(nsImage: NSWorkspace.shared.icon(forFile: appURL.path))
            Text(appURL.deletingPathExtension().lastPathComponent)
        }
        .onDrag {
            NSItemProvider(contentsOf: appURL) ?? NSItemProvider()
        }
    }
}
```

Prefer an AppKit bridge if the SwiftUI drag source does not behave as a file
URL in the target System Settings list.

## UX Requirements

- Say what to drag and where to drop it.
- Show the same display name and icon that will appear in System Settings.
- Include an alternate manual path for users who do not discover or cannot use
  drag and drop.
- Do not imply dropping the app completes authorization when the user still
  needs to turn on a toggle or relaunch.

## Failure Modes

- The user drags the main app, but the helper performs the protected action.
- The app is translocated, unsigned, ad-hoc signed differently between builds,
  or launched from a temporary path, causing confusing TCC entries.
- System Settings is on another display or has a different privacy pane open.
- The target list accepts the drag but leaves the toggle off.
