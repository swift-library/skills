# TCA Reducer Structure, Actions, And State

Use this when shaping or reviewing a TCA feature boundary. Start from the
local resolved TCA version and nearby feature style; do not migrate syntax just
because a newer example exists.

## Reducer Shape

- Prefer modern `@Reducer` when the resolved package supports it.
- Put canonical state in `State` and domain inputs/outputs in `Action`.
- Keep reducers as the only place that mutates feature state and starts
  effects.
- Keep feature names domain-specific. Avoid `ScreenReducer` or `ViewModel`
  names inside a TCA module unless the project already uses that vocabulary.
- Use small helper methods on the reducer for repeated logic instead of
  dispatching internal actions only to share synchronous work.

Example shape:

```swift
@Reducer
struct SearchFeature {
  @ObservableState
  struct State: Equatable {
    var query = ""
    var results: IdentifiedArrayOf<ResultRow.State> = []
    var isLoading = false
  }

  enum Action: Equatable {
    case queryChanged(String)
    case searchButtonTapped
    case searchResponse(Result<[SearchResult], SearchError>)
    case results(IdentifiedActionOf<ResultRow>)
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case let .queryChanged(query):
        state.query = query
        return .none
      case .searchButtonTapped:
        state.isLoading = true
        return .none
      case let .searchResponse(.success(results)):
        state.isLoading = false
        state.results = IdentifiedArray(uniqueElements: results.map(ResultRow.State.init))
        return .none
      case .searchResponse(.failure):
        state.isLoading = false
        return .none
      case .results:
        return .none
      }
    }
    .forEach(\.results, action: \.results) {
      ResultRow()
    }
  }
}
```

Adjust for local syntax: older projects may use `ReducerProtocol`,
slash-case paths, or non-observation stores.

## Action Organization

- Separate user intents, lifecycle actions, child actions, delegate actions,
  binding actions, effect responses, and navigation/presentation actions.
- Use nested action enums when the feature gets large, but do not hide core
  user intent behind generic names such as `.event` or `.callback`.
- Model delegate outputs explicitly so parent reducers can react without
  reaching into child internals.
- Use result-carrying actions for async responses so success and failure paths
  are visible and testable.
- Include enough identity in response actions to reject stale results when
  multiple requests can overlap.
- Use `Result { try await ... }` in effects or `.run` catch handlers according
  to the local style. The important part is that success and failure become
  explicit reducer inputs.

## State Organization

- Store canonical feature state, navigation state, and presentation state in
  `State`.
- Keep `State` equatable when the feature uses `TestStore` state assertions.
- Use computed properties for cheap derived view values; store derived values
  only when computing them is expensive or they represent a cached domain
  result.
- Avoid duplicating parent state in children. Pass scoped state or use
  `@Shared` only when ownership is genuinely shared.
- Use `@ObservableState` only on state types where the resolved TCA version and
  platform support the observation model.
- Use case-pathable state/action shapes when the feature needs enum case
  scoping, destination reducers, or path reducers. Prefer official macro or
  package support already available through the resolved TCA dependency.

## Reducer Enums

Use reducer enums for destination/path reducers or for a closed set of child
screens. Keep each case mapped to a real child feature. If the enum only
exists to avoid file organization, prefer a struct reducer plus child scopes.

## Review Checks

- Reducer action names describe implementation details rather than user/domain
  intent.
- Parent directly edits child state that should be owned by a child reducer.
- Failure and cancellation paths are not modeled in actions.
- State has derived duplicates that can drift.
- A feature cannot be tested because state/action types are too broad or
  hidden behind view code.
