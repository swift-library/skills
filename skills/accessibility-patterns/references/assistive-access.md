# Assistive Access

Use this file when a task mentions Assistive Access, optimized app mode,
`AssistiveAccess` scenes, cognitively simplified interfaces, or
`UISupportsAssistiveAccess`.

## Scope

Assistive Access is an iOS and iPadOS feature for a simplified system and app
experience. It is not just "larger UI"; it should reduce cognitive load and
surface only essential tasks.

Use this reference for app-level support and scene setup. For ordinary Dynamic
Type, VoiceOver, or Switch Control fixes, use the corresponding references
instead.

## App Declaration

Declare support only when the app has a dedicated or already-appropriate
Assistive Access experience.

```xml
<key>UISupportsAssistiveAccess</key>
<true/>
```

Use full-screen Assistive Access only for apps whose standard interface is
already designed for the mode:

```xml
<key>UISupportsFullScreenInAssistiveAccess</key>
<true/>
```

Do not add these keys as a checklist item without verifying the actual user
experience.

## SwiftUI Scene Pattern

Prefer a dedicated `AssistiveAccess` scene over scattering conditional branches
through the normal app.

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }

        AssistiveAccess {
            AssistiveAccessContentView()
        }
    }
}
```

Inside the scene:

- expose only 1-3 essential tasks
- use clear `NavigationLink` destinations
- add navigation icons to top-level destinations
- keep targets larger than the ordinary 44pt minimum, normally 60pt or more
- avoid hidden gestures and time-limited interactions
- confirm destructive actions

```swift
struct AssistiveAccessContentView: View {
    var body: some View {
        NavigationStack {
            List {
                NavigationLink("Read Messages") {
                    InboxView()
                }
                NavigationLink("Send Message") {
                    ComposeView()
                }
            }
            .navigationTitle("Messages")
            .assistiveAccessNavigationIcon(systemImage: "message.fill")
        }
    }
}
```

## UIKit App Pattern

UIKit apps can route the Assistive Access scene through a SwiftUI hosting scene
delegate. Keep the Assistive Access UI separate from the standard UIKit scene
unless the product intentionally shares a simplified component.

```swift
import SwiftUI
import UIKit

final class AssistiveAccessSceneDelegate: UIHostingSceneDelegate {
    static var rootScene: some Scene {
        AssistiveAccess {
            AssistiveAccessContentView()
        }
    }
}
```

When configuring scenes, route sessions with the Assistive Access role to that
delegate. Check current SDK names and availability before shipping.

## Runtime Detection

Use runtime detection sparingly. Prefer a dedicated scene for large behavior
changes.

For shared components that need minor adaptation, use the SwiftUI environment
value when the deployment target supports it:

```swift
@Environment(\.accessibilityAssistiveAccessEnabled)
private var assistiveAccessEnabled
```

Gate this value for older targets. If the project supports iOS/iPadOS 17, a
dedicated `AssistiveAccess` scene is usually a safer compatibility boundary
than relying on the environment value throughout shared views.

## Design Rules

- Distill to core functionality. Remove settings, filters, secondary actions,
  and rarely used configuration from the Assistive Access flow.
- Use multiple representations: text plus icon or photo, not text alone.
- Make decisions one screen at a time.
- Use explicit buttons instead of swipe, long-press, drag, or hidden gestures.
- Keep navigation consistent and visibly reversible.
- Add confirmations for destructive or irreversible actions.
- Preserve compatibility with VoiceOver, Voice Control, Switch Control, and
  Dynamic Type.

## Testing

Verify on device:

1. Enable Assistive Access in Settings > Accessibility > Assistive Access.
2. Confirm the app appears in Optimized Apps when support is declared.
3. Add the app to the Assistive Access home screen.
4. Complete every essential task in Assistive Access mode.
5. Test with VoiceOver, Voice Control, and Switch Control where relevant.

SwiftUI previews can help during development:

```swift
#Preview(traits: .assistiveAccess) {
    AssistiveAccessContentView()
}
```

## Review Checklist

- [ ] App declaration matches real support.
- [ ] Dedicated scene exposes only essential tasks.
- [ ] Navigation icons exist for top-level destinations.
- [ ] Primary controls are large and easy to identify.
- [ ] Primary tasks do not require hidden gestures.
- [ ] Destructive actions require confirmation.
- [ ] Flow works with VoiceOver, Voice Control, Switch Control, and larger text.

## Common Mistakes

- Declaring support while showing the normal complex app UI.
- Treating Assistive Access as only a larger layout.
- Branching many standard views on Assistive Access state instead of creating a
  simpler scene.
- Keeping caregiver/configuration tasks in the primary user flow.
- Missing navigation icons.
- Requiring reading ability, precise gestures, or time-limited interaction.
