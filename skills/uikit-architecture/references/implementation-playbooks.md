# UIKit Implementation Playbooks

Use this when the user asks for concrete scaffolding, migration steps, or a
fuller playbook after a UIKit architecture has been selected.

## Contents

- [Module Layouts](#module-layouts)
- [MVP Shape](#mvp-shape)
- [MVVM Shape](#mvvm-shape)
- [VIPER Shape](#viper-shape)
- [Coordinator Shape](#coordinator-shape)
- [Clean Architecture Shape](#clean-architecture-shape)
- [Reactive Shape](#reactive-shape)
- [SwiftUI Interop Shape](#swiftui-interop-shape)
- [Migration Paths](#migration-paths)
- [Review Checklist Matrix](#review-checklist-matrix)

## Module Layouts

Adapt these to the repository's existing feature layout.

MVP:

```text
Feature/
  FeatureViewController.swift
  FeatureView.swift
  FeaturePresenter.swift
  FeatureViewData.swift
  FeatureAssembly.swift
  FeaturePresenterTests.swift
```

UIKit MVVM:

```text
Feature/
  FeatureViewController.swift
  FeatureViewModel.swift
  FeatureViewState.swift
  FeatureAssembly.swift
  FeatureViewModelTests.swift
```

VIPER:

```text
Feature/
  View/
  Presenter/
  Interactor/
  Entity/
  Router/
  FeatureModule.swift
```

Coordinator:

```text
Navigation/
  AppCoordinator.swift
  FeatureCoordinator.swift
  NavigationRouter.swift
Feature/
  FeatureAssembly.swift
```

## MVP Shape

Use this when the ViewController should be passive and Presenter tests are the
main goal.

```swift
protocol ProfileView: AnyObject {
    func render(_ viewData: ProfileViewData)
    func showLoading(_ isLoading: Bool)
    func showError(_ message: String)
}

final class ProfilePresenter {
    private let repository: ProfileRepository
    private var loadTask: Task<Void, Never>?
    private var requestID: UUID?

    weak var view: ProfileView?

    init(repository: ProfileRepository) {
        self.repository = repository
    }

    func viewDidLoad() {
        let requestID = UUID()
        self.requestID = requestID
        loadTask?.cancel()
        loadTask = Task { [repository, weak self] in
            await MainActor.run { self?.view?.showLoading(true) }
            do {
                let profile = try await repository.loadProfile()
                await MainActor.run {
                    guard self?.requestID == requestID else { return }
                    self?.view?.showLoading(false)
                    self?.view?.render(ProfileViewData(profile))
                }
            } catch is CancellationError {
                return
            } catch {
                await MainActor.run {
                    guard self?.requestID == requestID else { return }
                    self?.view?.showLoading(false)
                    self?.view?.showError(error.localizedDescription)
                }
            }
        }
    }
}
```

Review focus:

- `view` is weak and protocol-typed.
- ViewController forwards lifecycle and actions to Presenter.
- Presenter owns formatting, validation, loading, and error mapping.
- Navigation leaves through a router/coordinator protocol.

## MVVM Shape

Use UIKit MVVM when rendering from a state object is clearer than command-style
View protocol methods.

```swift
@MainActor
final class ProfileViewModel {
    private let repository: ProfileRepository
    private var loadTask: Task<Void, Never>?

    var onStateChange: ((ProfileViewState) -> Void)?
    private(set) var state: ProfileViewState = .idle {
        didSet { onStateChange?(state) }
    }

    init(repository: ProfileRepository) {
        self.repository = repository
    }

    func load() {
        loadTask?.cancel()
        loadTask = Task {
            state = .loading
            do {
                state = .loaded(ProfileViewData(try await repository.loadProfile()))
            } catch is CancellationError {
                return
            } catch {
                state = .failed(error.localizedDescription)
            }
        }
    }
}
```

Review focus:

- ViewController renders state and owns UIKit binding lifecycle.
- ViewModel has no `UINavigationController` dependency.
- Bindings are cancelled or nilled with lifecycle.
- State transitions are testable without UIKit.

## VIPER Shape

Use VIPER when a large UIKit feature needs strict roles.

```swift
protocol ProfilePresenting: AnyObject {
    func viewDidLoad()
    func editTapped()
}

protocol ProfileInteracting {
    func loadProfile() async throws -> Profile
}

protocol ProfileRouting {
    func showEditProfile()
}

final class ProfilePresenter: ProfilePresenting {
    weak var view: ProfileView?
    private let interactor: ProfileInteracting
    private let router: ProfileRouting

    init(interactor: ProfileInteracting, router: ProfileRouting) {
        self.interactor = interactor
        self.router = router
    }

    func editTapped() {
        router.showEditProfile()
    }
}
```

Review focus:

- View renders and forwards events.
- Presenter coordinates View, Interactor, and Router.
- Interactor owns business actions and data access.
- Router owns navigation and module assembly.
- Entity/domain data is not formatted for display.

## Coordinator Shape

Use Coordinator when the flow, not a single screen, is the architecture problem.

```swift
protocol Coordinator: AnyObject {
    var children: [Coordinator] { get set }
    func start()
}

final class FeatureCoordinator: Coordinator {
    var children: [Coordinator] = []
    private let router: NavigationRouting
    private let dependencies: FeatureDependencies

    init(router: NavigationRouting, dependencies: FeatureDependencies) {
        self.router = router
        self.dependencies = dependencies
    }

    func start() {
        let viewController = FeatureAssembly.build(
            dependencies: dependencies,
            onDetail: { [weak self] id in self?.showDetail(id: id) }
        )
        router.setRoot(viewController)
    }
}
```

Review focus:

- Coordinator creates screens and passes dependencies.
- Child coordinators are retained before start and removed on completion.
- ViewControllers/ViewModels receive closures or router protocols.
- Coordinator does not fetch data or apply business rules.

## Clean Architecture Shape

Use this when domain actions should be tested without UIKit.

```swift
struct LoadProfile {
    let repository: ProfileRepository

    func callAsFunction() async throws -> Profile {
        try await repository.loadProfile()
    }
}

protocol ProfileRepository {
    func loadProfile() async throws -> Profile
}

final class LiveProfileRepository: ProfileRepository {
    private let api: ProfileAPI

    init(api: ProfileAPI) {
        self.api = api
    }
}
```

Review focus:

- Use cases and entities do not import UIKit.
- Repositories map DTOs to domain values.
- Presenter/ViewModel maps domain values to display output.
- Tests can exercise use cases with stubs.

## Reactive Shape

Use Combine or Rx only when repeated events and streams justify it.

```swift
final class SearchViewModel {
    @Published var query = ""
    @Published private(set) var results: [SearchViewData] = []

    private var cancellables: Set<AnyCancellable> = []

    init(search: @escaping (String) -> AnyPublisher<[SearchResult], Error>) {
        $query
            .removeDuplicates()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .flatMap { search($0).replaceError(with: []) }
            .map { $0.map(SearchViewData.init) }
            .assign(to: &$results)
    }
}
```

Review focus:

- Pipelines live in Presenter/ViewModel/Interactor, not ViewController bodies.
- Scheduling is injectable where tests need determinism.
- Errors map to recoverable view state.
- Subscriptions are scoped to feature lifetime.

## SwiftUI Interop Shape

Use this when a UIKit app hosts SwiftUI screens or migrates incrementally.

```swift
enum SwiftUIFeatureAssembly {
    static func build(
        dependencies: FeatureDependencies,
        onComplete: @escaping () -> Void
    ) -> UIViewController {
        let viewModel = SwiftUIFeatureViewModel(
            repository: dependencies.repository,
            onComplete: onComplete
        )
        return UIHostingController(rootView: SwiftUIFeatureView(viewModel: viewModel))
    }
}
```

Review focus:

- UIKit root coordinator still owns app-level navigation.
- SwiftUI receives dependencies and route callbacks through assembly.
- `UIHostingController` is at the boundary, not scattered through feature code.
- A SwiftUI subtree can own internal `NavigationStack` state if it is
  self-contained.

## Migration Paths

Fat controller to MVP:

1. Define a View protocol around current rendering operations.
2. Move formatting, validation, and loading orchestration to Presenter.
3. Inject services/repositories into Presenter.
4. Make ViewController forward actions.
5. Add Presenter tests with a mock View.

Fat controller to MVVM:

1. Define a view state model.
2. Move mapping and async work to ViewModel.
3. Bind ViewController rendering to state changes.
4. Move navigation to values, closures, or Coordinator.
5. Add ViewModel state tests.

UIKit MVC to VIPER:

1. Extract Interactor for business/data operations.
2. Extract Presenter for display mapping and view commands.
3. Extract Router/Assembly for navigation and module construction.
4. Add boundary protocols only where they help testing or module isolation.
5. Add Presenter and Interactor contract tests.

Scattered navigation to Coordinator:

1. Inventory push/present/deeplink calls.
2. Define route methods on a coordinator/router.
3. Pass navigation closures into modules.
4. Retain child coordinators for child flows.
5. Test router calls with spies.

UIKit to SwiftUI increment:

1. Choose one flow boundary.
2. Extract Presenter/ViewModel before replacing UI technology.
3. Wrap SwiftUI with `UIHostingController` from assembly.
4. Keep one owner for navigation.
5. Preserve tests around presentation logic.

## Review Checklist Matrix

- ViewController: renders and forwards events; no business/data orchestration.
- Presenter/ViewModel: owns presentation state, mapping, validation, and async.
- Interactor/use case: owns business action; no navigation or UIKit rendering.
- Router/Coordinator: owns navigation and assembly; no business logic.
- Dependency: live infrastructure is injected, not constructed deep in UI.
- Async: stale tasks/subscriptions cancel; errors have explicit UI paths.
- Testing: presenter/view-model/use-case/router contracts are testable without
  real infrastructure or UIKit presentation timing.
