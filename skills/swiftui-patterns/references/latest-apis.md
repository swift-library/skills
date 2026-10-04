# Latest SwiftUI APIs Reference

> This reference summarizes modern SwiftUI API replacements from Apple documentation comparisons.

## Table of Contents
- [Xcode 27 And OS 27](#xcode-27-and-os-27)
- [Always Use (iOS 15+)](#always-use-ios-15)
- [When Targeting iOS 16+](#when-targeting-ios-16)
- [When Targeting iOS 17+](#when-targeting-ios-17)
- [When Targeting iOS 18+](#when-targeting-ios-18)
- [When Targeting iOS 26+](#when-targeting-ios-26)

---

## Xcode 27 And OS 27

Separate compiler behavior from runtime availability:

- `@State` initialization changes come with Xcode 27 and can back-deploy to
  iOS 17/macOS 14; see `state-management.md`.
- ContentBuilder changes type checking and can expose source incompatibilities;
  it is not evidence of improved runtime frame time. Use TN3211 from
  `official-sources.md` for the exact diagnostic.
- Prefer closure forms of `overlay`/`background` for builder ambiguities;
  qualify ambiguous types by module and prefer opaque result types where
  appropriate. Preserve the old-target branch when an explicit TupleView or
  empty MapKit builder needs a compatibility fix.
- OS 27 adds HTTP caching and request/session configuration for `AsyncImage`;
  see `image-optimization.md`. Gate new APIs independently from the compiler.
- `reorderContainer` and `swipeActionsContainer` are OS 27 APIs and unavailable
  on tvOS in the 27 SDK. Verify each target declaration before adoption.

Keep the project's deployment target and older API paths. Consult the current
SDK when a session example and a declaration differ.

## Always Use (iOS 15+)

These APIs have been deprecated long enough that there is no reason to use the old variants.

### Compact Replacements

These replacements have minimal API shape changes. Most are near-direct swaps; a few require an additional parameter or structural adjustment:

- **`navigationTitle(_:)`** instead of `navigationBarTitle(_:)`
- **`toolbar { ToolbarItem(...) }`** instead of `navigationBarItems(...)` (structural change)
- **`toolbarVisibility(.hidden, for: .navigationBar)`** (iOS 18+; `toolbar(.hidden, for: .navigationBar)` on iOS 16-17) instead of `navigationBarHidden(_:)`
- **`statusBarHidden(_:)`** instead of `statusBar(hidden:)`; the 27 SDK marks `statusBarHidden(_:)` to be deprecated in favor of `toolbarVisibility(_:for: .statusBar)`, which requires iOS 27
- **`ignoresSafeArea(_:edges:)`** instead of `edgesIgnoringSafeArea(_:)`
- **`preferredColorScheme(_:)`** instead of `colorScheme(_:)`
- **`foregroundStyle(_:)`** instead of `foregroundColor(_:)` (e.g., `.foregroundStyle(.primary)`)
- **`clipShape(.rect(cornerRadius:))`** instead of `cornerRadius()`
- **`overlay(alignment:content:)`** instead of `overlay(_:alignment:)`
- **`textInputAutocapitalization(_:)`** instead of `autocapitalization(_:)` (note: `.never` replaces `.none`)
- **`animation(_:value:)`** instead of `animation(_:)` (adds required `value:` parameter; back-deploys to iOS 13+)

### Presentation

- **Always use `.confirmationDialog(_:isPresented:actions:message:)`** instead of `actionSheet(...)`.
- **Always use `.alert(_:isPresented:actions:message:)`** instead of `alert(isPresented:content:)`.

Both take a title `String`, `isPresented: Binding<Bool>`, an `actions` builder with `Button` items (supporting `role: .destructive` / `.cancel`), and an optional `message` builder:

```swift
.alert("Delete Item?", isPresented: $showAlert) {
    Button("Delete", role: .destructive) { deleteItem() }
    Button("Cancel", role: .cancel) { }
} message: {
    Text("This action cannot be undone.")
}
```

### Text Input

**Always use `onSubmit(of:_:)` and `focused(_:equals:)` instead of `TextField` `onEditingChanged`/`onCommit` callbacks.**

```swift
@FocusState private var isFocused: Bool

TextField("Search", text: $query)
    .focused($isFocused)
    .onSubmit { performSearch() }
```

### Accessibility

**Always use dedicated accessibility modifiers instead of the generic `accessibility(...)` variants.** Use `.accessibilityLabel()`, `.accessibilityValue()`, `.accessibilityHint()`, `.accessibilityAddTraits()`, `.accessibilityHidden()` instead of `.accessibility(label:)`, `.accessibility(value:)`, etc.

### Custom Environment / Container Values

**Always use the `@Entry` macro instead of manual `EnvironmentKey` conformance.** The `@Entry` macro was introduced in Xcode 16 and back-deploys to all OS versions.

```swift
// Modern — one line replaces ~10 lines of EnvironmentKey boilerplate
extension EnvironmentValues {
    @Entry var myCustomValue: String = "Default value"
}
```

### Styling

**Always use `Button` instead of `onTapGesture()` unless you need tap location or count.**

```swift
Button("Tap me") { performAction() }

// Use onTapGesture only when you need location or count
Image("photo")
    .onTapGesture(count: 2) { handleDoubleTap() }
```

### Text

**Avoid concatenating `Text` values with `+`.** Concatenation creates
localization and ordering problems. Prefer interpolation, `LocalizedStringKey`,
or string catalog symbols.

```swift
// Avoid
Text("Hello, ") + Text(name)

// Better
Text("Hello, \(name)")
```

For languages supported by SwiftUI's grammar agreement, prefer automatic
inflection when the string depends on a count:

```swift
Text("^[\(people) person](inflect: true)")
```

### Asset Catalog Symbols

When the project generates asset symbols, prefer those symbols over stringly
typed asset names:

```swift
Image(.avatar)
```

Use string names only when generated symbols are unavailable or the asset name
is genuinely dynamic.

---

## When Targeting iOS 16+

### Navigation

**Use `NavigationStack` (or `NavigationSplitView`) instead of `NavigationView`.** Value-based `NavigationLink(value:)` with `.navigationDestination(for:)` replaces destination-based links.

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(value: item) { Text(item.name) }
    }
    .navigationDestination(for: Item.self) { DetailView(item: $0) }
}
```

### Simple Renames

- **`tint(_:)`** instead of `accentColor(_:)`
- **`autocorrectionDisabled(_:)`** instead of `disableAutocorrection(_:)`
- **`.topBarLeading` / `.topBarTrailing`** instead of deprecated
  `.navigationBarLeading` / `.navigationBarTrailing` toolbar placements.

### Scroll Indicators

Use `.scrollIndicators(.hidden)` instead of legacy initializer flags such as
`showsIndicators: false` when the local deployment target supports it.

### Clipboard

**Prefer `PasteButton` for user-initiated paste UI** to avoid paste prompts. It handles permissions automatically. Use `UIPasteboard` only when you need programmatic or non-`Transferable` clipboard access (triggers the paste permission prompt).

```swift
PasteButton(payloadType: String.self) { strings in
    pastedText = strings.first ?? ""
}
```

---

## When Targeting iOS 17+

### State Management

- **Prefer `@Observable` over `ObservableObject` for new code.** Use `@State` instead of `@StateObject`; use `@Bindable` instead of `@ObservedObject`. See `state-management.md` for full `@Observable` migration patterns.

### Events

**Use `onChange(of:initial:_:)` or `onChange(of:) { }` instead of `onChange(of:perform:)`.**

The deprecated variant passes only the new value. The modern variants provide either both old and new values, or a no-parameter closure.

- **No-parameter** (most common): `.onChange(of: value) { doSomething() }`
- **Old and new values**: `.onChange(of: value) { old, new in ... }`
- **With initial trigger**: `.onChange(of: value, initial: true) { ... }`
- **Deprecated**: `.onChange(of: value) { newValue in ... }` — single-parameter closure

### Sensory Feedback

**Prefer `sensoryFeedback(_:trigger:)` and related overloads instead of `UIImpactFeedbackGenerator`, `UISelectionFeedbackGenerator`, and `UINotificationFeedbackGenerator` in SwiftUI views.**

Attach haptics declaratively to the view that owns the state change, rather than imperatively firing UIKit generators inside button actions.
Custom tactile patterns, AHAP resources, synchronized audio-haptic playback,
and `CHHapticEngine` lifecycle are out of scope; do not embed Core Haptics
engine code in a SwiftUI view.

```swift
@State private var isFavorite = false

Button("Favorite", systemImage: isFavorite ? "heart.fill" : "heart") {
    isFavorite.toggle()
}
.sensoryFeedback(.selection, trigger: isFavorite)
```

Use the conditional overload when feedback should fire only for specific transitions:

```swift
.sensoryFeedback(.selection, trigger: phase) { old, new in
    old == .inactive || new == .expanded
}
```

### Gestures

- **`MagnifyGesture`** instead of `MagnificationGesture` (access magnitude via `value.magnification`)
- **`RotateGesture`** instead of `RotationGesture` (access angle via `value.rotation`)

### Layout

**Consider `containerRelativeFrame()` or `visualEffect()` as alternatives to `GeometryReader` for sizing and position-based effects.** `GeometryReader` is not deprecated and remains necessary for many measurement-based layouts.

```swift
Image("hero")
    .resizable()
    .containerRelativeFrame(.horizontal) { length, axis in length * 0.8 }
```

- **`visualEffect { content, geometry in ... }`** — position-based effects (parallax, offsets) without a `GeometryReader` wrapper.
- **`onGeometryChange(for:of:action:)`** — react to geometry changes of a specific view; useful for driving state/effects. `GeometryReader` is still better when layout itself depends on geometry. Note the two-closure shape:
  ```swift
  .onGeometryChange(for: CGFloat.self) { proxy in proxy.size.height } action: { newHeight in height = newHeight }
  ```
- **`.coordinateSpace(.named("scroll"))`** instead of `.coordinateSpace(name: "scroll")`.

---

## When Targeting iOS 18+

### Tabs

**Use the `Tab` API instead of `tabItem(_:)`.**

```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Search", systemImage: "magnifyingglass") { SearchView() }
    Tab("Profile", systemImage: "person") { ProfileView() }
}
```

When using `Tab(role:)`, all tabs must use the `Tab` syntax. Mixing `Tab(role:)` with `.tabItem()` causes compilation errors.

### Previews

**Use `@Previewable` for dynamic properties in previews.**

```swift
// @Previewable requires iOS 17+
#Preview {
    @Previewable @State var isOn = false
    Toggle("Setting", isOn: $isOn)
}
```

---

## When Targeting iOS 26+

For Liquid Glass APIs (`glassEffect`, `GlassEffectContainer`, glass button styles), see [liquid-glass.md](liquid-glass.md).

### Scroll Edge Effects

**Use `scrollEdgeEffectStyle(_:for:)` to configure scroll edge behavior.**

```swift
ScrollView {
    // content
}
.scrollEdgeEffectStyle(.soft, for: .top)
```

### Background Extension

**Use `backgroundExtensionEffect()` for edge-extending blurred backgrounds.**

Views behind a Liquid Glass sidebar can appear clipped. This modifier mirrors and blurs content outside the safe area so artwork remains visible.

```swift
Image("hero")
    .backgroundExtensionEffect()
```

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Tab Bar

**Use `tabBarMinimizeBehavior(_:)` to control tab bar minimization on scroll.**

```swift
TabView {
    // tabs
}
.tabBarMinimizeBehavior(.onScrollDown)
```

**Use `tabViewBottomAccessory` for persistent controls above the tab bar.** Read `tabViewBottomAccessoryPlacement` from the environment to adapt content when the accessory collapses into the tab bar area.

```swift
TabView {
    // tabs
}
.tabViewBottomAccessory {
    NowPlayingBar()
}
```

**Use `Tab(role: .search)` for a dedicated search tab.** The tab separates from the rest and morphs into a search field when selected.

```swift
TabView {
    Tab("Home", systemImage: "house") { HomeView() }
    Tab("Profile", systemImage: "person") { ProfileView() }
    Tab(role: .search) { SearchResultsView() }
}
```

> Source: "What's new in SwiftUI" (WWDC25, session 256) and "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Toolbars

**On iOS 26.0 and macOS 26.0 or newer, use `ToolbarSpacer` to control grouping of toolbar items.** Fixed spacers visually separate related groups; flexible spacers push items apart.

`ToolbarSpacer` participates in the toolbar content list. In macOS merged
toolbars, especially around `NavigationSplitView` and `inspector`, it is not
column-local spacing. Use `Spacer()` inside a single toolbar item's custom
`ViewBuilder` content for view-level spacing within that item. For deployment
targets below iOS 26.0 or macOS 26.0, avoid referencing `ToolbarSpacer` except
inside an availability guard; use `ToolbarItem { Spacer() }` for the fallback.

```swift
.toolbar {
    ToolbarItem(placement: .topBarTrailing) {
        Button("Up", systemImage: "chevron.up") { }
    }
    ToolbarItem(placement: .topBarTrailing) {
        Button("Down", systemImage: "chevron.down") { }
    }
    ToolbarSpacer(.fixed)
    ToolbarItem(placement: .topBarTrailing) {
        Button("Settings", systemImage: "gear") { }
    }
}
```

Fallback for earlier deployment targets:

```swift
.toolbar {
    ToolbarItem(placement: .topBarTrailing) {
        Spacer()
    }
}
```

**Use `sharedBackgroundVisibility(.hidden)` to remove the glass group background from an individual toolbar item.**

```swift
ToolbarItem(placement: .topBarTrailing) {
    Image(systemName: "person.circle.fill")
        .sharedBackgroundVisibility(.hidden)
}
```

**Use `badge(_:)` on toolbar item content to display an indicator.**

```swift
ToolbarItem(placement: .topBarTrailing) {
    Button("Notifications", systemImage: "bell") { }
        .badge(unreadCount)
}
```

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Search

**Use `searchToolbarBehavior(.minimizable)` to opt into a minimized search button.** The system may automatically minimize search into a toolbar button depending on available space. Use this modifier to explicitly opt in.

```swift
NavigationStack {
    ContentView()
        .searchable(text: $query)
        .searchToolbarBehavior(.minimizable)
}
```

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Animations

**Use `@Animatable` macro instead of manual `animatableData` declarations.** The macro auto-synthesizes `animatableData` from all animatable properties. Use `@AnimatableIgnored` to exclude specific properties. The SDK declares the macro for iOS 13 and later, so it does not require an iOS 26 deployment target.

```swift
@Animatable
struct Wedge: Shape {
    var startAngle: Angle
    var endAngle: Angle
    @AnimatableIgnored var drawClockwise: Bool

    func path(in rect: CGRect) -> Path { /* ... */ }
}
```

> Source: "What's new in SwiftUI" (WWDC25, session 256)

### Presentations

**Use zoom navigation transitions to morph presentations out of their source
view.** On iOS 26 and later, toolbar items and buttons can serve as the source
through `matchedTransitionSource(id:in:)`, and the destination uses
`.navigationTransition(.zoom(sourceID:in:))`.

```swift
.toolbar {
    ToolbarItem {
        Button("Add", systemImage: "plus") { showSheet = true }
            .matchedTransitionSource(id: "addSheet", in: namespace)
    }
}
.sheet(isPresented: $showSheet) {
    AddItemView()
        .navigationTransition(.zoom(sourceID: "addSheet", in: namespace))
}
```

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Controls

**Use `controlSize(.extraLarge)` for extra-large prominent action buttons.**

```swift
Button("Get Started") { }
    .buttonStyle(.borderedProminent)
    .controlSize(.extraLarge)
```

**Use concentric corners for buttons that match their container's corners.**

```swift
Button("Confirm") { }
    .clipShape(.rect(corners: .concentric))
```

**On iOS 26 and later, sliders support tick marks and a neutral value.**

```swift
Slider(value: $speed, in: 0.5...2.0, neutralValue: 1.0) {
    Text("Speed")
} ticks: {
    SliderTick(0.6)
    SliderTick(0.9)
}
```

> Source: "Build a SwiftUI app with the new design" (WWDC25, session 323)

### Rich Text

**Use `TextEditor` with an `AttributedString` binding for rich text editing.** Supports bold, italic, underline, strikethrough, custom fonts, foreground/background colors, paragraph styles, and Genmoji.

```swift
@State private var text: AttributedString = "Hello, world!"

var body: some View {
    TextEditor(text: $text)
}
```

> Source: "Cook up a rich text experience in SwiftUI with AttributedString" (WWDC25, session 280)

### Web Content

**Use `WebView` to display web content.** For richer interaction, create a `WebPage` observable model.

```swift
// Simple URL display
WebView(url: URL(string: "https://example.com")!)

// With observable model
@State private var page = WebPage()

WebView(page)
    .onAppear { page.load(URLRequest(url: myURL)) }
    .navigationTitle(page.title)
```

> Source: "Meet WebKit for SwiftUI" (WWDC25, session 231)

### Drag and Drop

**Use `dragContainer` for multi-item drag operations.** Combine with `DragConfiguration` for custom drag behavior and `onDragSessionUpdated` to observe events. These APIs require macOS 26 or iOS and visionOS 27, and the `.delete` drop operation is macOS-only.

```swift
PhotoGrid(photos: photos)
    .dragContainer(for: Photo.self) { draggedIDs in
        photos.filter { draggedIDs.contains($0.id) }
    }
    .onDragSessionUpdated { session in
        if case .ended(.delete) = session.phase {
            deleteSelectedPhotos()
        }
    }
```

> Source: "What's new in SwiftUI" (WWDC25, session 256)

### Scene Bridging

**On iOS 26 and macOS 26 and later, UIKit and AppKit lifecycle apps can request SwiftUI scenes.** This enables using SwiftUI-only scene types like `MenuBarExtra` and `ImmersiveSpace` from imperative lifecycle apps via `UIApplication.shared.activateSceneSession(for:errorHandler:)`.

> Source: "What's new in SwiftUI" (WWDC25, session 256)

---

## Quick Lookup Table

| Deprecated | Recommended | Since |
|-----------|-------------|-------|
| `navigationBarTitle(_:)` | `navigationTitle(_:)` | iOS 15+ |
| `navigationBarItems(...)` | `toolbar { ToolbarItem(...) }` | iOS 15+ |
| `statusBar(hidden:)` | `statusBarHidden(_:)`; `toolbarVisibility(_:for: .statusBar)` on iOS 27+ | iOS 15+ |
| `edgesIgnoringSafeArea(_:)` | `ignoresSafeArea(_:edges:)` | iOS 15+ |
| `colorScheme(_:)` | `preferredColorScheme(_:)` | iOS 15+ |
| `foregroundColor(_:)` | `foregroundStyle(_:)` | iOS 15+ |
| `cornerRadius(_:)` | `clipShape(.rect(cornerRadius:))` | iOS 15+ |
| `overlay(_:alignment:)` | `overlay(alignment:content:)` | iOS 15+ |
| `actionSheet(...)` | `confirmationDialog(...)` | iOS 15+ |
| `alert(isPresented:content:)` | `alert(_:isPresented:actions:message:)` | iOS 15+ |
| `autocapitalization(_:)` | `textInputAutocapitalization(_:)` | iOS 15+ |
| `accessibility(label:)` etc. | `accessibilityLabel()` etc. | iOS 15+ |
| `TextField` `onCommit`/`onEditingChanged` | `onSubmit` + `focused` | iOS 15+ |
| `animation(_:)` (no value) | `animation(_:value:)` | Back-deploys (iOS 13+) |
| Manual `EnvironmentKey` | `@Entry` macro | Back-deploys (Xcode 16+) |
| Manual `animatableData` | `@Animatable` macro | Back-deploys (iOS 13+) |
| `NavigationView` | `NavigationStack` / `NavigationSplitView` | iOS 16+ |
| `navigationBarHidden(_:)` | `toolbar(.hidden, for: .navigationBar)`; `toolbarVisibility(.hidden, for: .navigationBar)` on iOS 18+ | iOS 16+ |
| `.navigationBarLeading` / `.navigationBarTrailing` | `.topBarLeading` / `.topBarTrailing` | iOS 16+ |
| `accentColor(_:)` | `tint(_:)` | iOS 16+ |
| `disableAutocorrection(_:)` | `autocorrectionDisabled(_:)` | iOS 16+ |
| `UIPasteboard.general` | `PasteButton` | iOS 16+ |
| `showsIndicators: false` scroll initializers | `.scrollIndicators(.hidden)` | iOS 16+ |
| `onChange(of:perform:)` | `onChange(of:) { }` or `onChange(of:) { old, new in }` | iOS 17+ |
| `UIImpactFeedbackGenerator` / `UISelectionFeedbackGenerator` / `UINotificationFeedbackGenerator` | `sensoryFeedback(_:trigger:)` | iOS 17+ |
| `MagnificationGesture` | `MagnifyGesture` | iOS 17+ |
| `RotationGesture` | `RotateGesture` | iOS 17+ |
| `coordinateSpace(name:)` | `coordinateSpace(.named(...))` | iOS 17+ |
| `ObservableObject` | `@Observable` | iOS 17+ |
| `tabItem(_:)` | `Tab` API | iOS 18+ |
| Wrapped `WKWebView` for ordinary web content | `WebView` | iOS 26+ |
| `presentationBackground(_:)` on sheets | Default Liquid Glass sheet material | iOS 26+ |
| Custom toolbar background hacks | `scrollEdgeEffectStyle(_:for:)` | iOS 26+ |
