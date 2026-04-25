# SwiftUI Implementation Playbooks

Use this when the user asks for concrete scaffolding, migration steps, or a
fuller playbook after an architecture has been selected.

## Contents

- [Feature Layouts](#feature-layouts)
- [MVVM Shape](#mvvm-shape)
- [MVI Shape](#mvi-shape)
- [TCA Shape](#tca-shape)
- [Clean Architecture Shape](#clean-architecture-shape)
- [Navigation Coordinator Shape](#navigation-coordinator-shape)
- [Reactive Overlay Shape](#reactive-overlay-shape)
- [Migration Paths](#migration-paths)
- [Review Checklist Matrix](#review-checklist-matrix)

## Feature Layouts

Keep layouts local to the repository's existing structure. These are shapes to
adapt, not mandatory folders.

MVVM:

```text
Feature/
  FeatureView.swift
  FeatureViewModel.swift
  FeatureState.swift
  FeatureAssembly.swift
  FeatureRepository.swift
  FeatureRepositoryLive.swift
  FeatureViewModelTests.swift
```

MVI:

```text
Feature/
  FeatureView.swift
  FeatureState.swift
  FeatureIntent.swift
  FeatureAction.swift
  FeatureReducer.swift
  FeatureStore.swift
  FeatureEffects.swift
  FeatureReducerTests.swift
```

TCA:

```text
Feature/
  Feature.swift
  FeatureView.swift
  FeatureClient.swift
  FeatureTests.swift
```

Clean Architecture with SwiftUI adapter:

```text
Feature/
  Domain/
    FeatureEntity.swift
    LoadFeature.swift
    FeatureRepository.swift
  Data/
    FeatureDTO.swift
    FeatureRepositoryLive.swift
  Presentation/
    FeatureView.swift
    FeatureViewModel.swift
    FeatureState.swift
```

## MVVM Shape

Use this when a SwiftUI screen needs explicit state and async behavior but does
not justify a reducer/store.

```swift
@MainActor
@Observable
final class FeatureViewModel {
    private let repository: FeatureRepository
    private var loadTask: Task<Void, Never>?

    var state = FeatureState.idle
    var route: FeatureRoute?

    init(repository: FeatureRepository) {
        self.repository = repository
    }

    func load() {
        loadTask?.cancel()
        loadTask = Task {
            state = .loading
            do {
                let value = try await repository.load()
                state = .loaded(FeatureViewData(value))
            } catch is CancellationError {
                return
            } catch {
                state = .failed(message: error.localizedDescription)
            }
        }
    }

    deinit {
        loadTask?.cancel()
    }
}
```

Review focus:

- View owns the ViewModel with `@State` or receives it through local assembly.
- View sends intents such as `load()`, `retry()`, `save()`.
- ViewModel owns request identity and cancellation.
- Domain values are mapped before they become UI state.

## MVI Shape

Use this when state transitions are central to correctness.

```swift
struct FeatureState: Equatable {
    var isLoading = false
    var items: [ItemViewData] = []
    var errorMessage: String?
}

enum FeatureIntent {
    case appeared
    case retryTapped
    case itemTapped(ItemViewData.ID)
}

enum FeatureAction {
    case response(Result<[Item], Error>)
}

struct FeatureReducer {
    mutating func reduce(
        state: inout FeatureState,
        intent: FeatureIntent
    ) -> FeatureEffect? {
        switch intent {
        case .appeared, .retryTapped:
            state.isLoading = true
            state.errorMessage = nil
            return .load
        case .itemTapped:
            return nil
        }
    }

    mutating func reduce(
        state: inout FeatureState,
        action: FeatureAction
    ) {
        state.isLoading = false
        switch action {
        case .response(.success(let items)):
            state.items = items.map(ItemViewData.init)
        case .response(.failure(let error)):
            state.errorMessage = error.localizedDescription
        }
    }
}
```

Review focus:

- Reducer stays pure.
- Effects are explicit, injected, cancellable, and testable.
- View sends intents and never mutates state directly.
- Tests cover reducer state transitions separately from effect execution.

## TCA Shape

Use this only when the project already uses TCA or explicitly accepts it.

```swift
@Reducer
struct Feature {
    @ObservableState
    struct State: Equatable {
        var items: [ItemViewData] = []
        var isLoading = false
    }

    enum Action: Equatable {
        case appeared
        case response(Result<[Item], FeatureError>)
    }

    @Dependency(\.featureClient) var featureClient

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .appeared:
                state.isLoading = true
                return .run { send in
                    await send(.response(Result { try await featureClient.load() }))
                }
            case .response(.success(let items)):
                state.isLoading = false
                state.items = items.map(ItemViewData.init)
                return .none
            case .response(.failure):
                state.isLoading = false
                return .none
            }
        }
    }
}
```

Review focus:

- Dependencies flow through TCA dependency values.
- Navigation and child state are modeled in State.
- Effects have cancellation rules when requests can overlap.
- `TestStore` covers important action sequences.

## Clean Architecture Shape

Use this when the domain/data boundary matters.

```swift
struct LoadItems {
    var repository: ItemRepository

    func callAsFunction() async throws -> [Item] {
        try await repository.loadItems()
    }
}

protocol ItemRepository {
    func loadItems() async throws -> [Item]
}

@MainActor
@Observable
final class ItemsViewModel {
    private let loadItems: LoadItems

    init(loadItems: LoadItems) {
        self.loadItems = loadItems
    }
}
```

Review focus:

- Domain and use cases do not import SwiftUI.
- DTO mapping happens in data adapters.
- Presentation state contains view data, not transport objects.
- Use case tests run with stub repositories.

## Navigation Coordinator Shape

Use this when a flow has deep links, reusable routes, or multi-screen state.

```swift
enum AppRoute: Hashable {
    case itemDetail(id: Item.ID)
    case settings
}

@MainActor
@Observable
final class FeatureRouter {
    var path: [AppRoute] = []
    var sheet: AppSheet?

    func openItem(id: Item.ID) {
        path.append(.itemDetail(id: id))
    }

    func handle(_ route: AppRoute) {
        path.append(route)
    }
}
```

Review focus:

- Routes are value types.
- Views and ViewModels use closures or router protocols.
- Deep links enter through the root router.
- Router builds destinations or delegates to assembly; it does not fetch data.

## Reactive Overlay Shape

Use this when repeated events and streams matter more than one-shot async calls.

```swift
@MainActor
final class SearchViewModel: ObservableObject {
    @Published var query = ""
    @Published private(set) var results: [ResultViewData] = []

    private var cancellables: Set<AnyCancellable> = []

    init(search: @escaping (String) -> AnyPublisher<[SearchResult], Error>) {
        $query
            .removeDuplicates()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .flatMap { query in search(query).replaceError(with: []) }
            .map { $0.map(ResultViewData.init) }
            .assign(to: &$results)
    }
}
```

Review focus:

- Pipelines live in ViewModel, Store, or dependency clients.
- Scheduler/clocks are injectable when tests need determinism.
- Errors become recoverable state.
- Streams feed the same state model as non-reactive actions.

## Migration Paths

Ad hoc SwiftUI to MVVM:

1. Identify canonical state and user intents.
2. Move async loading and mapping from View to ViewModel.
3. Inject repositories/services into the ViewModel.
4. Add ViewModel tests for success, failure, and cancellation.
5. Keep layout and visual refactors separate.

MVVM to MVI:

1. Convert ViewModel state into a single value state.
2. Name View inputs as intents.
3. Split async outputs into actions.
4. Move synchronous transition logic into a reducer.
5. Add reducer tests before moving effects.

MVVM/MVI to TCA:

1. Confirm dependency acceptance and local TCA precedent.
2. Map state, actions, dependencies, and effects explicitly.
3. Move navigation into feature state.
4. Port tests to `TestStore`.
5. Avoid mixing old ViewModel mutation with reducer-owned state.

Adding Clean Architecture:

1. Extract domain entities and repository protocols.
2. Introduce use cases for business operations.
3. Move DTO mapping into data adapters.
4. Inject use cases into ViewModels/Stores.
5. Test use cases independently from SwiftUI.

Adding Coordinator:

1. Identify routes and ownership.
2. Move route state to a root or feature router.
3. Inject route closures/protocols into features.
4. Route deep links through the root owner.
5. Test route state changes.

## Review Checklist Matrix

- State: one canonical owner, no duplicated mutable sources.
- View: renders state, sends intents, avoids side effects.
- Dependency: live services are injected or assembled outside the feature.
- Async: stale work is cancelled; failures become explicit state.
- Navigation: routes are values or protocols, not scattered presentation calls.
- Testing: state, effects, navigation, and cancellation have targeted tests.
- Scope: architecture change is proportional to the feature risk.
