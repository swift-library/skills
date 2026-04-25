# Scaffold A SwiftPM macOS App

Use this file when a target repository needs a minimal SwiftPM macOS app shape
without an Xcode app project.

## Steps

1. Create a repo and initialize SwiftPM:

```bash
mkdir MyApp
cd MyApp
swift package init --type executable
```

2. Update `Package.swift` to target macOS and define an executable target for
   the app.
3. Create the app entry point under `Sources/MyApp/`.
4. Use SwiftUI for a windowed app with minimal AppKit glue, or AppKit for a
   menu bar / accessory-style app.
5. If app resources are needed, add `resources: [.process("Resources")]` and
   create `Sources/MyApp/Resources/`.
6. Add `version.env` for packaging metadata.
7. Copy script templates from `assets/templates/` into `Scripts/`.

## Required Shape

- `Package.swift` declares an executable product.
- The executable target contains an app entry point. Prefer a file such as
  `AppMain.swift` for SwiftUI `@main`; avoid `main.swift` with `@main` because
  SwiftPM treats `main.swift` as top-level-code entry.
- Resources live under the executable target when SwiftPM should copy them.
- The bootstrap uses `Resources/README.txt` as a visible placeholder so SwiftPM
  copies the resources directory without warning on hidden placeholder files.
- Packaging scripts live outside `Sources/`, usually in `scripts/` or
  `Scripts/`, based on project convention.
- Version values should come from a small local file such as `version.env` or
  from the release process.

## Bootstrap Template

Use `assets/templates/bootstrap/` when the repository has no app skeleton yet.
After copying it, rename:

- package name
- executable target name
- `Sources/MyApp`
- `APP_NAME`
- bundle identifier
- deployment target

## Minimal Package.swift

```swift
// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .macOS(.v14),
    ],
    products: [
        .executable(name: "MyApp", targets: ["MyApp"]),
    ],
    targets: [
        .executableTarget(
            name: "MyApp",
            path: "Sources/MyApp",
            resources: [
                .process("Resources"),
            ]),
    ]
)
```

## Minimal SwiftUI Entry

```swift
import SwiftUI

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            Text("Hello")
                .padding()
        }
    }
}
```

## Minimal AppKit Entry

```swift
import AppKit

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Initialize app state here.
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
```

## Boundary Checks

- If the app needs Xcode-only capabilities, document that the SwiftPM-only
  path may be insufficient.
- If the task is about UI architecture, do not solve it here; package the
  existing executable and route source decisions to the relevant skill.
- If the app needs sandbox, network, file, or automation entitlements, keep
  entitlements explicit and review them before signing.
