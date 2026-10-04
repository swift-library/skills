# SwiftUI TCA Fit Check

Use this reference only to decide whether The Composable Architecture is the
right architecture boundary for a SwiftUI feature and whether detailed work
has moved beyond architecture selection.

## Prefer TCA When

- The codebase already imports `ComposableArchitecture`.
- The user explicitly accepts Point-Free's TCA dependency and its style.
- The feature needs deterministic reducer/effect tests, explicit dependency
  injection, child-feature composition, or state-modeled navigation.
- Existing nearby features already use TCA and consistency is the lower-risk
  path.

## Prefer A Smaller Pattern When

- The feature is a small screen with simple local state and no meaningful
  effects.
- The team has not accepted TCA's dependency, learning curve, or architectural
  conventions.
- MVVM, MVI without a dependency, or a coordinator plus local state solves the
  current problem with less migration cost.
- The request is ordinary SwiftUI view layout, controls, animation, or visual
  polish.

## Handoff Boundary

Once TCA is already present or explicitly accepted, stop using this general
architecture skill for implementation details. Reducer, store, effect,
dependency, navigation, presentation, shared-state, and `TestStore` work is
detailed TCA implementation and out of scope here.

## Fit-Check Output

State the fit judgment, the reason TCA is or is not warranted, the local
constraints that drive the decision, and the next step: detailed TCA
implementation for accepted TCA, or the selected MVVM/MVI/Clean/Coordinator
reference for non-TCA work.
