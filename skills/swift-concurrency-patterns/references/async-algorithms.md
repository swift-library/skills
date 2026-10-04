# AsyncAlgorithms Package

Use this when:

- You need time-based operators (debounce, timers) or rate limiting.
- You need to combine multiple async sequences (merge, combineLatest, zip).
- You are migrating from Combine or RxSwift operators to Swift Concurrency equivalents.

Skip this file if:

- You need basic `AsyncStream` bridging for callbacks or delegates. Use `async-sequences.md`.
- You are choosing between `Task`, `async let`, or task groups. Use `tasks.md`.

Jump to:

- Quick Start
- Time-Based Operators
- Combining Operators
- Multi-Consumer Scenarios
- Combine Migration Guide
- Best Practices

---
## Quick Start

Top 5 most common operators:

```swift
import AsyncAlgorithms

// 1. Debounce rapid inputs
for await query in searchQueryStream.debounce(for: .milliseconds(500)) {
    await performSearch(query)
}

// 2. Repeat work on a timer
for await _ in AsyncTimerSequence.repeating(every: .seconds(30)) {
    await refreshFeed()
}

// 3. Merge multiple independent streams
for await message in merge(chat1Messages, chat2Messages) {
    display(message)
}

// 4. Combine dependent values
for await (username, email) in combineLatest(usernameStream, emailStream) {
    validateForm(username: username, email: email)
}

// 5. Zip paired operations
for await (image, metadata) in zip(imageStream, metadataStream) {
    await cache(image: image, metadata: metadata)
}
```

`merge`, `combineLatest`, `zip`, and `chain` are free functions that take two or three sequences, not methods on `AsyncSequence`.

> **See**: [AsyncAlgorithms on GitHub](https://github.com/apple/swift-async-algorithms)

---

## Overview & Installation

### What is AsyncAlgorithms?

Extends Swift's AsyncSequence with time-based operators, stream combination tools, and multi-consumer primitives.

**Use for**:
- Time-based operations: debounce, timers (throttling exists only as underscored `_throttle` in 1.x)
- Combining streams: merge, combineLatest, zip, chain
- Task-to-task handoff with backpressure: AsyncChannel
- Broadcasting one sequence to multiple consumers: share() (1.1+)
- Specific operators: removeDuplicates, chunks, adjacentPairs, compacted

**Use standard library for**:
- Bridging callbacks: AsyncStream
- Simple iteration: for await in sequence
- Single-value operations: async/await

### Installation

```swift
dependencies: [
    .package(url: "https://github.com/apple/swift-async-algorithms", from: "1.0.0")
]

targets: [
    .target(
        name: "MyTarget",
        dependencies: [
            .product(name: "AsyncAlgorithms", package: "swift-async-algorithms")
        ]
    )
]
```

Import:

```swift
import AsyncAlgorithms
```

---

## Time-Based Operators

### debounce(for:tolerance:clock:)

Wait for inactivity before emitting. Use for rapid inputs like search fields.

#### Example: ArticleSearcher

```swift
import AsyncAlgorithms

@MainActor @Observable
final class ArticleSearcher {
    private(set) var results: [Article] = []
    private let queries = AsyncStream.makeStream(of: String.self)

    func search(_ query: String) {
        queries.continuation.yield(query)
    }

    func startDebouncedSearch() {
        Task {
            for await query in queries.stream.debounce(for: .milliseconds(500)) {
                results = await APIClient.searchArticles(query)
            }
        }
    }
}
```

**Benefits**: Automatic cancellation, backpressure, cleaner than manual Task.sleep.

#### ❌ Anti-Pattern

```swift
// Bad: Every keystroke spawns new task
func search(_ query: String) {
    Task {
        try? await Task.sleep(for: .milliseconds(500))
        await performSearch(query)
    }
}
```

**Problem**: Multiple tasks execute simultaneously, causing out-of-order results.

**Solution**: Use `debounce()` for automatic backpressure.

---

### Throttling (no stable operator)

swift-async-algorithms 1.1.7 has no public `throttle`. Throttling ships only as underscored `_throttle(for:clock:latest:)`, `_throttle(for:latest:)`, `_throttle(for:clock:reducing:)`, and `_throttle(for:reducing:)`, which sit outside the package's stable API and can change in any release. In those overloads the first element is emitted immediately; elements arriving less than one interval after the last emission are folded into a pending value, which is emitted when the next element arrives after the interval has passed (or when the base finishes). With `latest: true` (the default) the emitted value is the most recent element; with `latest: false` it is the first element received since the previous emission. The `reducing:` overloads take a `(Reduced?, Element) async -> Reduced` closure instead.

For repeated actions like button taps, gate on the last accepted instant. Use `debounce(for:)` instead when waiting for input to settle is acceptable.

#### Example: Like Button

```swift
import SwiftUI

struct LikeButton: View {
    @State private var isLiked = false
    @State private var lastAcceptedTap: ContinuousClock.Instant?
    private let minimumInterval: Duration = .seconds(1)

    var body: some View {
        Button(action: handleTap) {
            Image(systemName: isLiked ? "heart.fill" : "heart")
        }
    }

    private func handleTap() {
        let now = ContinuousClock.now
        if let lastAcceptedTap, lastAcceptedTap.duration(to: now) < minimumInterval {
            return
        }
        lastAcceptedTap = now
        Task { await toggleLike() }
    }

    private func toggleLike() async {
        isLiked.toggle()
        await APIClient.updateLikeStatus(isLiked: isLiked)
    }
}
```

**Behavior**: The first tap acts immediately; taps within one second of the last accepted tap are dropped. No stream or long-lived task is needed.

---

### AsyncTimerSequence

Emit values at regular intervals. Use for periodic refresh or countdown timers. `repeating(every:)` uses `SuspendingClock`; `init(interval:tolerance:clock:)` requires an explicit clock.

#### Example: Feed Refresh

```swift
import AsyncAlgorithms

@MainActor @Observable
final class FeedViewModel {
    private(set) var articles: [Article] = []
    private var refreshTask: Task<Void, Never>?

    func startAutoRefresh() {
        refreshTask = Task {
            for await _ in AsyncTimerSequence.repeating(every: .seconds(30)) {
                await refreshFeed()
            }
        }
    }

    private func refreshFeed() async {
        articles = await APIClient.fetchLatestArticles()
    }
}
```

#### ❌ Anti-Pattern

```swift
// Bad: Manual timer implementation
func startTimer() {
    Task {
        while !Task.isCancelled {
            performAction()
            try? await Task.sleep(for: .seconds(1))
        }
    }
}
```

**Solution**: Use `AsyncTimerSequence`.

---

## Combining Operators

### merge(_:_:)

Combine sequences into one, emitting as they arrive. **Stable operator ✅**

Use for independent data sources that don't depend on each other. `merge` is a free function for two or three sequences with the same element type: `merge(a, b)` or `merge(a, b, c)`. There is no array or variadic overload in 1.x, so merge a dynamic number of streams with a task group, as in this example.

#### Example: Multi-Room Chat

```swift
import AsyncAlgorithms

actor ChatManager {
    private var messageContinuations: [String: AsyncStream<ChatMessage>.Continuation] = [:]

    func getMessagesStream(roomID: String) -> AsyncStream<ChatMessage> {
        AsyncStream { continuation in
            messageContinuations[roomID] = continuation
        }
    }

    func receiveMessage(_ message: ChatMessage) {
        messageContinuations[message.roomID]?.yield(message)
    }

    func startMonitoring(rooms: [String]) -> AsyncStream<ChatMessage> {
        let streams = rooms.map { getMessagesStream(roomID: $0) }
        let (merged, continuation) = AsyncStream.makeStream(of: ChatMessage.self)
        let task = Task {
            await withTaskGroup(of: Void.self) { group in
                for stream in streams {
                    group.addTask {
                        for await message in stream {
                            continuation.yield(message)
                        }
                    }
                }
            }
            continuation.finish()
        }
        continuation.onTermination = { _ in task.cancel() }
        return merged
    }
}

// Usage
let manager = ChatManager()
let mergedMessages = await manager.startMonitoring(rooms: ["general", "random"])

for await message in mergedMessages {
    print("[\(message.roomID)] \(message.text)")
}
```

**Behavior**: Values emit as they arrive from any source. Order interleaved by timing. Cancellation propagates to all sources.

---

### combineLatest(_:_:)

Combine sequences, emitting tuple when any source emits. Always uses latest values. **Stable operator ✅**

Use for dependent values that need synchronization. A free function for two or three sequences: `combineLatest(a, b)` or `combineLatest(a, b, c)`. It emits only after every base has produced at least one value.

#### Example: Form Validation

```swift
import AsyncAlgorithms
import SwiftUI

struct SignupForm: View {
    @State private var username = ""
    @State private var email = ""
    @State private var password = ""
    @State private var usernameInput = AsyncStream.makeStream(of: String.self)
    @State private var emailInput = AsyncStream.makeStream(of: String.self)
    @State private var passwordInput = AsyncStream.makeStream(of: String.self)
    @State private var formState = FormState.incomplete

    var body: some View {
        Form {
            TextField("Username", text: $username)
            TextField("Email", text: $email)
            SecureField("Password", text: $password)
        }
        .onChange(of: username, initial: true) { usernameInput.continuation.yield(username) }
        .onChange(of: email, initial: true) { emailInput.continuation.yield(email) }
        .onChange(of: password, initial: true) { passwordInput.continuation.yield(password) }
        .task {
            await validateForm()
        }
    }

    private func validateForm() async {
        for await (username, email, password) in
                combineLatest(usernameInput.stream, emailInput.stream, passwordInput.stream)
        {
            formState = await validate(
                username: username,
                email: email,
                password: password
            )
        }
    }
}
```

#### ❌ Anti-Pattern

```swift
// Bad: Manual value combining
actor FormValidator {
    private var currentUsername: String = ""
    private var currentEmail: String = ""

    func updateUsername(_ username: String) {
        currentUsername = username
        checkForm()
    }
}
```

**Solution**: Use `combineLatest()`.

---

### zip(_:_:)

Combine sequences by pairing elements in order. **Stable operator ✅** A free function for two or three sequences: `zip(a, b)` or `zip(a, b, c)`.

#### Example: Image + Metadata

```swift
import AsyncAlgorithms

struct ImageLoader {
    func loadImagesWithMetadata(urls: [URL]) async throws -> [LoadedImage] {
        let imageStream = AsyncThrowingStream<UIImage, Error> { continuation in
            Task {
                for url in urls {
                    let image = try await downloadImage(from: url)
                    continuation.yield(image)
                }
                continuation.finish()
            }
        }

        let metadataStream = AsyncThrowingStream<ImageMetadata, Error> { continuation in
            Task {
                for url in urls {
                    let metadata = try await fetchMetadata(for: url)
                    continuation.yield(metadata)
                }
                continuation.finish()
            }
        }

        var results: [LoadedImage] = []
        for try await (image, metadata) in zip(imageStream, metadataStream) {
            results.append(LoadedImage(image: image, metadata: metadata))
        }
        return results
    }
}
```

**Behavior**: Emits tuple when all sequences emit. Maintains order. Finishes when shortest sequence finishes.

---

### chain(_:_:)

Concatenate sequences sequentially. **Stable operator ✅** A free function for two or three sequences with the same element type: `chain(a, b)` or `chain(a, b, c)`.

#### Example: Paginated Loading

```swift
import AsyncAlgorithms

struct ArticlePaginator {
    func loadAllArticles() -> AsyncStream<[Article]> {
        AsyncStream { continuation in
            Task {
                var page = 1
                var hasMore = true
                while hasMore {
                    let articles = try await fetchPage(page: page)
                    continuation.yield(articles)
                    hasMore = articles.count == 20
                    page += 1
                }
                continuation.finish()
            }
        }
    }
}

// Usage: Chain cache + network
for await articles in chain(loadFromCacheStream(), loadFromNetworkStream()) {
    display(articles)
}
```

**Behavior**: Emits all values from first sequence before starting second.

---

## Utility Operators

### removeDuplicates()

Remove adjacent duplicates. **Stable operator ✅**

```swift
import AsyncAlgorithms

actor ChatHistory {
    private var messageStream = AsyncStream<ChatMessage> { _ in /* ... */ }

    func getUniqueMessages() -> AsyncRemoveDuplicatesSequence<AsyncStream<ChatMessage>> {
        messageStream.removeDuplicates()
    }
}
```

---

### chunks() and chunked()

Collect values into batches. **Stable operator ✅**

```swift
import AsyncAlgorithms

struct BatchProcessor {
    func processLargeDataset(dataStream: AsyncStream<DataItem>) async {
        for await batch in dataStream.chunks(ofCount: 100) {
            await processBatch(batch)
        }
    }

    func chunkedByTime(dataStream: AsyncStream<DataItem>) async {
        for await batch in dataStream.chunked(by: AsyncTimerSequence.repeating(every: .seconds(5))) {
            await processBatch(batch)
        }
    }
}
```

---

### compacted() and adjacentPairs()

```swift
import AsyncAlgorithms

// Remove nil values
for await value in optionalValuesStream.compacted() {
    process(value)
}

// Pair adjacent elements
for await (previous, current) in valuesStream.adjacentPairs() {
    let difference = current - previous
}
```

---

## Multi-Consumer Scenarios

### AsyncChannel

AsyncSequence with backpressure. **Stable operator ✅**

Use for producer-consumer patterns with flow control. `send(_:)` suspends until a consumer takes the value. Each value goes to exactly one awaiting consumer; the channel does not broadcast.

#### Example: Message Queue

```swift
import AsyncAlgorithms

actor MessageQueue {
    private let channel = AsyncChannel<Message>()

    func getMessages() -> AsyncChannel<Message> {
        channel
    }

    func enqueue(_ message: Message) async {
        await channel.send(message)
    }

    func startProcessing() {
        Task {
            for await message in channel {
                await process(message)
            }
        }
    }
}

// Multiple producers
let queue = MessageQueue()
Task { await queue.enqueue(Message(type: .userAction, content: "tap")) }
Task { await queue.enqueue(Message(type: .network, content: "data")) }
await queue.startProcessing()
```

#### ❌ Anti-Pattern

```swift
// Bad: Values split unpredictably
let stream = AsyncStream<Int> { continuation in
    for i in 1...10 {
        continuation.yield(i)
    }
    continuation.finish()
}

Task { for await value in stream { print("Consumer 1: \(value)") } }
Task { for await value in stream { print("Consumer 2: \(value)") } }
```

**Problem**: Each value goes to only one consumer. `AsyncChannel` behaves the same way.

**Solution**: To deliver every value to every consumer, use `share()` (swift-async-algorithms 1.1+, Swift 6.2 compiler, macOS 15 / iOS 18 / tvOS 18 / watchOS 11 / visionOS 2 or later):

```swift
let shared = stream.share()

Task { for await value in shared { print("Consumer 1: \(value)") } }
Task { for await value in shared { print("Consumer 2: \(value)") } }
```

Consumers do not get a replay of values produced before they start iterating. The default `bufferingPolicy: .bounded(1)` lets the slowest consumer pace the source.

---

### AsyncThrowingChannel

Like AsyncChannel but can finish with an error through `fail(_:)`. **Stable operator ✅**

#### Example: WebSocket

```swift
import AsyncAlgorithms

actor WebSocketConnection {
    private let channel = AsyncThrowingChannel<WebSocketMessage, Error>()

    func getMessages() -> AsyncThrowingChannel<WebSocketMessage, Error> {
        channel
    }

    func receiveMessage(_ message: WebSocketMessage) async {
        await channel.send(message)
    }

    func reportError(_ error: Error) {
        channel.fail(error)
    }
}

// Usage
let connection = WebSocketConnection()
do {
    for try await message in await connection.getMessages() {
        handle(message)
    }
} catch {
    print("WebSocket error: \(error)")
}
```

---

## Combine Migration Guide

### Operator Mapping Table

| Combine | AsyncAlgorithms | Status | Alternative |
|---------|-----------------|---------|-------------|
| `.debounce()` | `debounce()` | ✅ Stable | - |
| `.throttle()` | `_throttle()` only | Underscored, not stable | Last-accepted-instant guard, or `debounce()` |
| `.merge()` | `merge(a, b)` | ✅ Stable | Task group for more than three sources |
| `.combineLatest()` | `combineLatest(a, b)` | ✅ Stable | - |
| `.zip()` | `zip(a, b)` | ✅ Stable | - |
| `.append()` | `chain(a, b)` | ✅ Stable | - |
| `.removeDuplicates()` | `removeDuplicates()` | ✅ Stable | - |
| `Timer.publish(every:on:in:)` | `AsyncTimerSequence` | ✅ Stable | - |
| `.share()` | `share()` | ✅ Stable (1.1+) | - |
| `.flatMap()` | - | - | `TaskGroup` |
| `.receive(on:)` | - | - | `Task` / `@MainActor` |
| `.eraseToAnyPublisher()` | - | - | `any AsyncSequence` |

`merge`, `combineLatest`, `zip`, and `chain` are free functions that take two or three sequences. `share()` requires swift-async-algorithms 1.1+, a Swift 6.2 compiler, and macOS 15 / iOS 18 / tvOS 18 / watchOS 11 / visionOS 2 or later. `AsyncChannel` is not a substitute for `.share()`: it hands each value to one consumer.

---

### Migration Examples

#### Example 1: ArticleSearcher

**Before: Combine**

```swift
import Combine

final class ArticleSearcher: ObservableObject {
    @Published private(set) var results: [Article] = []
    @Published var searchQuery = ""

    init() {
        $searchQuery
            .debounce(for: .milliseconds(500), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .flatMap { query in
                APIClient.searchArticles(query)
                    .catch { _ in Just([]) }
            }
            .receive(on: DispatchQueue.main)
            .assign(to: &$results)
    }
}
```

**After: AsyncAlgorithms**

```swift
import AsyncAlgorithms

@MainActor @Observable
final class ArticleSearcher {
    private(set) var results: [Article] = []
    private let queries = AsyncStream.makeStream(of: String.self)

    func search(_ query: String) {
        queries.continuation.yield(query)
    }

    func startDebouncedSearch() {
        Task {
            for await query in queries.stream
                .debounce(for: .milliseconds(500))
                .removeDuplicates()
            {
                do {
                    results = try await APIClient.searchArticles(query)
                } catch {
                    results = []
                }
            }
        }
    }
}
```

**Benefits**: Simpler error handling, no cancellables, automatic cancellation.

---

#### Example 2: Multi-Source Loading

**Before: Combine Merge**

```swift
import Combine

final class ArticleLoader: ObservableObject {
    @Published private(set) var items: [Item] = []

    func loadAllSources() {
        let source1 = APIClient.fetchItems(from: .source1)
        let source2 = APIClient.fetchItems(from: .source2)

        Publishers.Merge(source1, source2)
            .scan([]) { accumulated, new in
                accumulated + new
            }
            .receive(on: DispatchQueue.main)
            .assign(to: &$items)
    }
}
```

**After: TaskGroup**

```swift
import AsyncAlgorithms

@Observable
final class ArticleLoader {
    @MainActor private(set) var items: [Item] = []

    func loadAllSourcesParallel() async {
        await withTaskGroup(of: [Item].self) { group in
            group.addTask {
                await APIClient.fetchItems(from: .source1)
            }
            group.addTask {
                await APIClient.fetchItems(from: .source2)
            }

            for await newItems in group {
                items.append(contentsOf: newItems)
            }
        }
    }
}
```

**Key difference**: For parallel execution, use `TaskGroup` instead of `flatMap`.

---

#### Example 3: Form Validation

**Before: Combine**

```swift
import Combine

final class FormValidator: ObservableObject {
    @Published var username = ""
    @Published var email = ""

    @Published private(set) var formState: FormState = .incomplete

    init() {
        Publishers.CombineLatest2($username, $email)
            .map { username, email in
                validate(username: username, email: email)
            }
            .assign(to: &$formState)
    }
}
```

**After: AsyncAlgorithms or a direct call**

```swift
import AsyncAlgorithms

@MainActor @Observable
final class FormValidator {
    private(set) var username = ""
    private(set) var email = ""
    private(set) var formState: FormState = .incomplete

    private let usernameInput = AsyncStream.makeStream(of: String.self)
    private let emailInput = AsyncStream.makeStream(of: String.self)

    func update(username: String) {
        self.username = username
        usernameInput.continuation.yield(username)
    }

    func update(email: String) {
        self.email = email
        emailInput.continuation.yield(email)
    }

    // Option 1: combineLatest for continuous validation
    func startStreamValidation() {
        Task {
            for await (username, email) in
                    combineLatest(usernameInput.stream, emailInput.stream)
            {
                formState = validate(username: username, email: email)
            }
        }
    }

    // Option 2: validate once, for example on submit
    func validateForm() {
        formState = validate(username: username, email: email)
    }
}
```

**Choose**:
- `combineLatest()`: Continuous validation as fields change; it emits only
  after both fields have produced a value
- Direct call: One-time validation when the user submits

---

## Common Mistakes Agents Make

- **Manual debounce with `Task.sleep`**: This creates multiple concurrent tasks and risks out-of-order results. Use the stream-based `debounce(for:)` operator from AsyncAlgorithms instead.
- **Sharing `AsyncStream` across multiple consumers**: Values split unpredictably between consumers. Use `share()` (swift-async-algorithms 1.1+) to broadcast. `AsyncChannel` is point-to-point, not broadcast like Combine's `.share()`.
- **Calling `merge`, `combineLatest`, `zip`, or `chain` as methods**: In 1.x they are free functions taking two or three sequences, such as `merge(a, b)`. There is no overload for an array of sequences.
- **Using `throttle(for:)`**: 1.x has no stable throttle, only underscored `_throttle`. Use a last-accepted-instant guard or `debounce(for:)`.
- **Looking for a `.flatMap` equivalent**: Use `TaskGroup` for fan-out; the semantics differ from Combine/Rx `flatMap`.
- **Looking for `.receive(on:)` equivalent**: Use `@MainActor` or `Task` context for isolation instead.

## Best Practices

1. **Use time-based operators** for rapid inputs: debounce() for search; for buttons, a last-accepted-instant guard (1.x has no stable throttle)
2. **Combine streams** with merge/combineLatest instead of manual state management
3. **Use AsyncChannel** for task-to-task handoff with backpressure, and share() to broadcast to multiple consumers
4. **Ensure Sendable conformance** when using operators across isolation boundaries
5. **Leverage cancellation** - Task cancellation propagates through all operators
6. **Choose right tool**: AsyncAlgorithms for complex streams, AsyncStream for bridging callbacks
7. **Avoid manual sleep loops** - use AsyncTimerSequence instead

---
