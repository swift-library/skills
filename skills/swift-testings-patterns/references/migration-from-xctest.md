# Migration from XCTest

## When to use this reference

Use this file for incremental migration of existing XCTest code to Swift Testing while preserving safety and CI signal.

## Coexistence strategy

- Swift Testing and XCTest can coexist in the same target.
- Migrate incrementally; do not block migration on full rewrite.
- A single source file can import both `XCTest` and `Testing` during migration.
- Keep XCTest where Swift Testing does not apply:
  - UI automation (`XCUIApplication`)
  - performance APIs (`XCTMetric`)
  - Objective-C-only tests

### Mixed import file example

```swift
import XCTest
import Testing
```

## Practical migration order

### Swift 6.4 Interoperability

Swift 6.4 supports deliberate XCTest/Swift Testing assertion interoperability.
Inspect the toolchain, manifest tools version and
`SWIFT_TESTING_XCTEST_INTEROP_MODE` before reusing helpers:

- `limited`: default with older SwiftPM tools versions; Swift Testing assertions
  in XCTest preserve failures, but XCTest failures in Swift Testing are warnings.
  Do not use this mode to prove failure propagation in that latter direction.
- `complete`: default with tools-version 6.4 or newer under the supporting
  toolchain; supports both assertion directions.
- `strict`: XCTest API usage warnings in Swift Testing become `fatalError`;
  supported Swift Testing assertions in XCTest still preserve failures.
- `none`: disable interoperability support.

The environment variable can select a supported mode without raising the
package's tools version. Test the actual runner configuration with an
intentionally failing helper: failure must still fail the test and CI process.
Keep older toolchains on the existing safe native-assertion path. Prefer
`#expect`/`#require` for new Swift Testing code; interoperability allows gradual
reuse and does not replace XCTest UI automation or metrics.
Sources and version checks are in `official-sources.md`.

1. Convert assertions to `#expect` / `#require`.
2. Replace `test...` naming constraints with explicit `@Test`.
3. Reorganize classes into suites where helpful.
4. Collapse repetitive methods into parameterized tests.
5. Add traits/tags for control and test-plan filtering.

## Example conversion: class method -> Swift Testing function

```swift
// Before (XCTest)
final class PriceTests: XCTestCase {
 func testDiscountedTotal() {
 XCTAssertEqual(Price.total(subtotal: 20, discount: 5), 15)
 }
}

// After (Swift Testing)
import Testing

@Test func discountedTotal() {
 #expect(Price.total(subtotal: 20, discount: 5) == 15)
}
```

## Assertion mapping highlights

- Most `XCTAssert*` variants -> `#expect(...)`.
- Optional unwrap checks -> `try #require(optionalValue)`.
- Early-stop semantics -> `#require` instead of global `continueAfterFailure = false`.
- `XCTFail("...")` -> `Issue.record("...")`.

### Table-style quick mappings

```swift
// XCTAssertTrue(isEnabled)
#expect(isEnabled)

// XCTAssertNil(error)
#expect(error == nil)

// XCTAssertThrowsError(try run())
#expect(throws: (any Error).self) { try run() }

// try XCTUnwrap(user)
let user = try #require(user)
```

## Suite model differences

- XCTest: class + `XCTestCase`.
- Swift Testing: struct/actor/class suites, explicit attributes, value-semantics-friendly defaults.
- Setup can move from `setUp` patterns to suite init when appropriate.
- Teardown can move to `deinit` when using class/actor suites.
- XCTest sync tests default to main actor behavior; Swift Testing runs tests on arbitrary tasks unless explicitly isolated (e.g. `@MainActor`).

### Setup migration example

```swift
import Testing

struct SessionTests {
 let session: Session

 init() {
 self.session = Session(environment: .test)
 }

 @Test func startsDisconnected() {
 #expect(session.isConnected == false)
 }
}
```

## Async migration specifics

- Prefer `await` directly for async APIs.
- Convert completion-handler APIs with `withCheckedContinuation`/`withCheckedThrowingContinuation`.
- Replace `XCTestExpectation` patterns with confirmations when testing asynchronous event streams.

### Expectation-style flow -> confirmation

```swift
import Testing

@Test func receivesAtLeastOneEvent() async {
 await confirmation("Receives event", expectedCount: 1...) { confirm in
 confirm()
 }
}
```

## Migration hygiene

- Prefer mechanical, reviewable commits.
- Use editor pattern-replace to accelerate common assertion conversions.
- Avoid accidental assertion mixing. Deliberate helper reuse requires a
  supporting toolchain, an explicit interoperable mode and failure-propagation
  verification as described above.

## Common pitfalls

- Migrating all files at once instead of phased migration.
- Keeping `continueAfterFailure` patterns instead of targeted `#require`.
- Marking every migrated test `@MainActor` unnecessarily.
