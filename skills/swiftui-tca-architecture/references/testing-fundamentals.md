# TCA Testing Fundamentals

Use this for first-pass `TestStore` setup, Equatable state, naming, and mock
dependency boundaries.

## Equatable State

- `TestStore` assertions work best when feature state is equatable.
- If a field cannot be equatable, ask whether it belongs in feature state,
  dependency state, or a test-specific wrapper.
- Keep state mutation assertions concrete. Hard-coded expected values usually
  prove more than repeating the reducer logic in the test.

## Basic Test Store

```swift
@MainActor
struct SearchFeatureTests {
  @Test
  func searchSuccess() async {
    let store = TestStore(initialState: SearchFeature.State()) {
      SearchFeature()
    } withDependencies: {
      $0.searchClient.search = { _ in [SearchResult.fixture] }
    }

    await store.send(.searchButtonTapped) {
      $0.isLoading = true
    }
    await store.receive(.searchResponse(.success([SearchResult.fixture]))) {
      $0.isLoading = false
      $0.results = [ResultRow.State(result: SearchResult.fixture)]
    }
  }
}
```

Adjust imports and `@Test`/XCTest style to the local test framework.

## Naming

- Name tests by behavior, not implementation: `searchSuccess`,
  `cancelSearchWhenQueryChanges`, `dismissesEditorAfterSave`.
- A good TCA test reads as a script of user actions and effect responses.
- Avoid naming tests after private helper actions unless the helper action is
  part of the feature contract.

## Store Setup

- Use the smallest initial state that represents the scenario.
- Override every dependency the path can touch.
- Seed clocks, UUIDs, dates, shared state, and clients to deterministic values.
- Prefer one behavior per test unless the feature contract is the sequence.

## Mock Dependencies

- Verify dependency input when it is part of behavior.
- Use failing defaults for dependencies that should not be called.
- Return domain values, not SDK fixtures, unless the feature owns SDK mapping.

## Review Checks

- Tests instantiate only views and never exercise reducer behavior.
- State is not equatable because non-domain objects were stored in it.
- Dependency overrides are broad globals shared across tests.
- Test closures contain reducer-like logic instead of expected results.
