# TCA Closed-Loop Examples

Use this reference when isolated TCA rules would collapse into an API lookup.
The examples are distilled implementation shapes: keep the ownership,
tradeoffs, warning signs, and test scripts; adapt names and syntax to the
project's resolved `ComposableArchitecture` version and local conventions.

Do not copy these examples into a project as a template. Use them to decide:

- which state owns the behavior
- which action records the user or child event
- which dependency owns external work
- which effect is cancellable or restartable
- which test proves the reducer script
- which review finding is a real boundary problem

## Restartable Effect + Dependency + TestStore

Use this shape when a user action starts async work through a dependency and a
newer request should supersede older work, such as search, refresh, preview
generation, or remote validation.

```swift
@Reducer
struct SearchFeature {
  @ObservableState
  struct State: Equatable {
    var query = ""
    var isLoading = false
    var results: IdentifiedArrayOf<ResultRow.State> = []
    var errorMessage: String?
  }

  enum Action: Equatable {
    case queryChanged(String)
    case searchButtonTapped
    case cancelButtonTapped
    case searchResponse(Result<[SearchResult], SearchError>)
    case results(IdentifiedActionOf<ResultRow>)
  }

  private enum CancelID { case search }

  @Dependency(\.searchClient) var searchClient

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case let .queryChanged(query):
        state.query = query
        return .none

      case .searchButtonTapped:
        let query = state.query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !query.isEmpty else {
          state.results = []
          state.errorMessage = nil
          return .none
        }

        state.isLoading = true
        state.errorMessage = nil

        return .run { send in
          do {
            let results = try await searchClient.search(query)
            await send(.searchResponse(.success(results)))
          } catch {
            await send(.searchResponse(.failure(SearchError(error))))
          }
        }
        .cancellable(id: CancelID.search, cancelInFlight: true)

      case .cancelButtonTapped:
        state.isLoading = false
        return .cancel(id: CancelID.search)

      case let .searchResponse(.success(results)):
        state.isLoading = false
        state.results = IdentifiedArray(
          uniqueElements: results.map(ResultRow.State.init(result:))
        )
        return .none

      case let .searchResponse(.failure(error)):
        state.isLoading = false
        state.errorMessage = error.userMessage
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

The matching test is a reducer script, not an HTTP-client test:

```swift
@MainActor
@Test
func searchSuccess() async {
  let store = TestStore(
    initialState: SearchFeature.State(query: "tca")
  ) {
    SearchFeature()
  } withDependencies: {
    $0.searchClient.search = { query in
      #expect(query == "tca")
      return [.fixture]
    }
  }

  await store.send(.searchButtonTapped) {
    $0.isLoading = true
    $0.errorMessage = nil
  }

  await store.receive(.searchResponse(.success([.fixture]))) {
    $0.isLoading = false
    $0.results = [ResultRow.State(result: .fixture)]
  }
}

@MainActor
@Test
func searchFailureClearsLoading() async {
  let store = TestStore(
    initialState: SearchFeature.State(query: "missing")
  ) {
    SearchFeature()
  } withDependencies: {
    $0.searchClient.search = { _ in throw SearchError.notFound }
  }

  await store.send(.searchButtonTapped) {
    $0.isLoading = true
    $0.errorMessage = nil
  }

  await store.receive(.searchResponse(.failure(.notFound))) {
    $0.isLoading = false
    $0.errorMessage = "No results found."
  }
}
```

Preserve this design value:

- capture state before entering the effect
- keep transport and parsing behind a dependency client
- model success and failure as reducer actions
- clear loading on every completed response path
- add cancellation when the work is restartable or view-lifetime bound
- test the visible state transitions and dependency override

Warning signs:

- the effect reads mutable state after suspension
- the view calls the client directly
- the reducer starts async work without a response action
- failures are logged but loading never clears
- tests only assert that the dependency was called

## Unified Destination Presentation

Use this shape when sheets, alerts, dialogs, or popovers are mutually
exclusive. A single destination makes the feature's presentation contract
explicit and gives one reducer composition point.

```swift
@Reducer
struct DetailFeature {
  @ObservableState
  struct State: Equatable {
    var item: Item
    @Presents var destination: Destination.State?
  }

  enum Action: Equatable {
    case editButtonTapped
    case deleteButtonTapped
    case destination(PresentationAction<Destination.Action>)
  }

  @Reducer
  enum Destination {
    case edit(EditItemFeature)
    case confirmDelete(ConfirmationDialogState<DeleteAction>)
  }

  enum DeleteAction: Equatable {
    case confirm
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case .editButtonTapped:
        state.destination = .edit(EditItemFeature.State(item: state.item))
        return .none

      case .deleteButtonTapped:
        state.destination = .confirmDelete(
          ConfirmationDialogState {
            TextState("Delete item?")
          } actions: {
            ButtonState(role: .destructive, action: .confirm) {
              TextState("Delete")
            }
          }
        )
        return .none

      case .destination(.presented(.confirmDelete(.confirm))):
        state.destination = nil
        return .none

      case .destination:
        return .none
      }
    }
    .ifLet(\.$destination, action: \.destination)
  }
}
```

The view should only bind to the destination; it should not maintain a shadow
`@State` flag for the same surface.

```swift
struct DetailView: View {
  @Bindable var store: StoreOf<DetailFeature>

  var body: some View {
    Form {
      Button("Edit") {
        store.send(.editButtonTapped)
      }
      Button("Delete", role: .destructive) {
        store.send(.deleteButtonTapped)
      }
    }
    .sheet(
      item: $store.scope(state: \.destination?.edit, action: \.destination.edit)
    ) { store in
      EditItemView(store: store)
    }
    .confirmationDialog(
      $store.scope(
        state: \.destination?.confirmDelete,
        action: \.destination.confirmDelete
      )
    )
  }
}
```

Preserve this design value:

- parent state owns presentation because presentation affects behavior
- destination enum documents mutually exclusive surfaces
- child presentation is composed with `.ifLet`
- destructive actions are observable and testable
- view code binds to store presentation state instead of inventing flags

Warning signs:

- `@State var isSheetPresented` mirrors `@Presents`
- several optional child states can be non-`nil` even though UI is exclusive
- delete confirmation performs domain mutation in the view closure
- tests never send a presented destination action

Multiple `@Presents` properties are acceptable only when the surfaces are
truly independent and can be visible or pending independently.

## Stack Navigation + Child Delegate

Use `StackState` when a parent owns a push stack. Use child delegate actions
when a child output should change the parent route or parent-owned collection.

```swift
@Reducer
struct ItemsFeature {
  @ObservableState
  struct State: Equatable {
    var items: IdentifiedArrayOf<Item>
    var path = StackState<Path.State>()
  }

  enum Action: Equatable {
    case itemTapped(Item.ID)
    case path(StackActionOf<Path>)
  }

  @Reducer
  enum Path {
    case detail(ItemDetailFeature)
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case let .itemTapped(id):
        guard let item = state.items[id: id] else { return .none }
        state.path.append(.detail(ItemDetailFeature.State(item: item)))
        return .none

      case let .path(.element(id: _, action: .detail(.delegate(.didDelete(id))))):
        state.items.remove(id: id)
        state.path.removeLast()
        return .none

      case .path:
        return .none
      }
    }
    .forEach(\.path, action: \.path) {
      Path()
    }
  }
}
```

The child action should expose output, not parent internals:

```swift
@Reducer
struct ItemDetailFeature {
  @ObservableState
  struct State: Equatable {
    var item: Item
  }

  enum Action: Equatable {
    case deleteButtonTapped
    case delegate(Delegate)

    enum Delegate: Equatable {
      case didDelete(Item.ID)
    }
  }

  var body: some ReducerOf<Self> {
    Reduce { state, action in
      switch action {
      case .deleteButtonTapped:
        return .send(.delegate(.didDelete(state.item.id)))

      case .delegate:
        return .none
      }
    }
  }
}
```

Preserve this design value:

- parent owns route mutation and parent-owned collections
- child owns detail behavior and emits delegate output
- delegate action carries the smallest parent-relevant fact
- the stack reducer composes path children instead of parent switching over
  every child internal action

Warning signs:

- child directly mutates a parent collection through shared state
- parent reaches into child state to infer outputs after the fact
- route pushes happen from SwiftUI navigation closures instead of actions
- pop/delete behavior has no reducer test because it is hidden in the view

## Bad To Good: Review Shapes

These snippets are for code review. They preserve the source value of long
examples by naming the broken boundary and the smallest corrective shape.

### Internal Action Ping-Pong

Bad: private actions are used only to share synchronous reducer logic.

```swift
case let .nameChanged(text):
  state.name = text
  return .send(.recomputeValidation)

case let .ageChanged(age):
  state.age = age
  return .send(.recomputeValidation)

case .recomputeValidation:
  state.canSave = isValid(state)
  return .none
```

Good: synchronous state maintenance stays synchronous.

```swift
case let .nameChanged(text):
  state.name = text
  updateValidation(&state)
  return .none

case let .ageChanged(age):
  state.age = age
  updateValidation(&state)
  return .none

private func updateValidation(_ state: inout State) {
  state.canSave = !state.name.isEmpty && state.age >= 18
}
```

Keep `.send` when the follow-up is a real observable feature event, not when it
only hides a helper method.

### View-Owned Business Logic

Bad: the view validates domain rules and sequences feature behavior.

```swift
Button("Save") {
  store.send(.nameChanged(localName))

  if !localName.isEmpty && selectedRole != nil {
    store.send(.saveButtonTapped)
  } else {
    store.send(.showValidationError)
  }
}
```

Good: the view reports intent; the reducer owns the rule and resulting state.

```swift
Button("Save") {
  store.send(.saveButtonTapped)
}

case .saveButtonTapped:
  guard state.form.isValid else {
    state.destination = .alert(.validationFailed)
    return .none
  }
  return save(&state)
```

The exception is purely visual local state that is not part of the feature
contract, such as focus, hover, transient scroll position, or an animation flag.

### Unscoped Child Stores

Bad: rows receive a parent store and decide which parent actions to send.

```swift
ForEach(store.items) { item in
  ItemRowView(item: item) {
    store.send(.deleteItemButtonTapped(item.id))
  }
}
```

Good: parent scopes child state/action when row behavior is stateful or
reusable.

```swift
ForEach(
  store.scope(state: \.rows, action: \.rows)
) { rowStore in
  ItemRowView(store: rowStore)
}
```

Keep the simpler closure style only for stateless leaf rendering where no child
feature boundary exists.
