# UIKit And SwiftUI Interop

Use this when a UIKit app hosts SwiftUI screens, embeds UIKit in SwiftUI, or
migrates feature by feature.

## UIKit Root Hosting SwiftUI

- Let the UIKit Coordinator/Router own app-level navigation when UIKit remains
  the root.
- Build SwiftUI screens through feature assembly and wrap them in
  `UIHostingController`.
- Inject dependencies, callbacks, and route closures into SwiftUI ViewModels or
  adapters.
- Keep `UINavigationController` out of SwiftUI ViewModels.

## SwiftUI Island Inside UIKit

- Keep the island's internal state in SwiftUI when the flow is self-contained.
- Surface completion, cancellation, selection, or route requests through
  closures/protocols.
- Avoid sharing mutable global state between UIKit and SwiftUI just to bridge a
  feature.

## UIKit Component Inside SwiftUI

- Keep UIViewControllerRepresentable/UIViewRepresentable wrappers thin.
- Put UIKit delegate glue in a Coordinator object owned by the representable.
- Do not hide business logic inside the representable wrapper.
- Route domain and presentation state through the surrounding SwiftUI
  architecture.

## Migration Rules

- Migrate one flow boundary at a time.
- Keep ownership explicit: UIKit owns app shell, SwiftUI owns feature subtree,
  or vice versa.
- Do not mix two navigation sources of truth for the same flow.
- Add tests around extracted Presenters/ViewModels before replacing UI
  technology.

## PR Checklist

- [ ] Root navigation owner is explicit.
- [ ] SwiftUI screens receive dependencies and route closures through assembly.
- [ ] UIKit types do not leak into SwiftUI ViewModels unnecessarily.
- [ ] Representable wrappers stay thin.
- [ ] Migration preserves one navigation source of truth.
