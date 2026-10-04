# System Settings Onboarding

Use System Settings guidance when the app cannot complete permission recovery
through a public request API, when the user has already denied a prompt, or when
the service is manually managed.

## Deep Links

Open the closest privacy pane with `NSWorkspace`. Treat these anchors as
best-effort and version-sensitive.

```swift
import AppKit

func openPrivacyPane(anchor: String) {
    let base = "x-apple.systempreferences:com.apple.preference.security"
    guard let url = URL(string: "\(base)?\(anchor)") else { return }

    if !NSWorkspace.shared.open(url),
       let fallback = URL(string: base) {
        NSWorkspace.shared.open(fallback)
    }
}

openPrivacyPane(anchor: "Privacy_ScreenCapture")
```

Observed anchors commonly used in macOS permission onboarding:

| Permission | Anchor |
|---|---|
| Screen Recording / Screen Capture | `Privacy_ScreenCapture` |
| Accessibility | `Privacy_Accessibility` |
| Input Monitoring | `Privacy_ListenEvent` |
| Full Disk Access | `Privacy_AllFiles` |
| Automation | `Privacy_Automation` |

Do not present these as stable public API. Always show the manual path:
System Settings > Privacy & Security > the named permission.

## Floating Guidance

A polished onboarding flow often combines:

1. Permission preflight.
2. Public request API when available.
3. System Settings deep link when manual recovery is needed.
4. A floating panel or popover with the app/helper icon and clear instruction.
5. Polling or a user-driven "I've enabled it" retry action.
6. Relaunch guidance when the permission only takes effect after restart.

Prefer a normal app-owned window or panel first. Use high window levels
sparingly and test multi-display behavior. Avoid blocking the System Settings
window or hiding the target list.

## Window Positioning

Coarse positioning can use the visible window list:

```swift
let options: CGWindowListOption = [.optionOnScreenOnly, .excludeDesktopElements]
let info = CGWindowListCopyWindowInfo(options, kCGNullWindowID) as? [[String: Any]]

let settingsWindow = info?.first {
    ($0[kCGWindowOwnerName as String] as? String) == "System Settings"
}
```

Risks:

- Window names, owners, and bounds may vary by macOS version, locale, display
  setup, permission state, and active Space.
- Detailed cross-app window information may itself be privacy-sensitive.
- This locates a window, not the exact privacy-list row.

Precise UI inspection can use Accessibility APIs after the app is trusted:

```swift
let app = AXUIElementCreateApplication(systemSettingsPID)
```

Use this only when the product already has or can reasonably request
Accessibility trust. It is a poor dependency for first-time Accessibility
permission onboarding.

## Fallback Copy Requirements

Any settings-guidance UI should still work without deep links or window
positioning. It needs:

- the exact permission name users will see in System Settings
- the exact app or helper name users should enable
- a retry or refresh action after the user changes settings
- a restart note only when the target permission actually requires it
