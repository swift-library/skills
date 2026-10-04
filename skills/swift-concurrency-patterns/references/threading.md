# Threading

Use this when:

- You need to understand the relationship between tasks and threads.
- You are debugging suspension points, actor reentrancy, or unexpected execution contexts.
- You need Swift 6.2 behavior guidance (`nonisolated async`, `@concurrent`, `nonisolated(nonsending)`).

Skip this file if:

- You mainly need to protect mutable state. Use `actors.md`.
- You need to make types safe to transfer. Use `sendable.md`.

Jump to:

- Core Concepts (Tasks vs Threads)
- Cooperative Thread Pool
- Suspension Points and Actor Reentrancy
- Swift 6.2 Changes (SE-461, SE-466)
- Default Isolation Domain
- Debugging Thread Execution
- Common Misconceptions
- Migration Strategy

## Core Concepts

### What is a Thread?

System-level resource that runs instructions. High overhead for creation and switching. Swift Concurrency abstracts thread management away.

### Tasks vs Threads

**Tasks** are units of async work, not tied to specific threads. Swift dynamically schedules tasks on available threads from a cooperative pool.

**Key insight**: No direct relationship between one task and one thread.

**Important (Swift 6+)**: Avoid using `Thread.current` inside async contexts. In Swift 6 language mode, `Thread.current` is unavailable from asynchronous contexts and will fail to compile. Prefer reasoning in terms of isolation domains; use Instruments and the debugger to observe execution when needed.

## Cooperative Thread Pool

The cooperative executor manages a bounded worker pool. Pool size and thread
assignment are implementation details; do not rely on one thread per core for
correctness or assume that every task leaves its actor.

### How it works

1. **Bounded workers**: Runtime-managed pool; do not depend on an exact count
2. **Task scheduling**: Tasks scheduled onto available threads
3. **Suspension**: `await` may suspend; suspension frees the thread for other work
4. **Resumption**: Task resumes on any available thread (not necessarily the same one)

```swift
func example() async throws {
    print("Before suspension")
    try await Task.sleep(for: .seconds(1))
    print("After suspension; isolation still defines safe access")
}
```

### Benefits over GCD

**Prevents thread explosion**:
- No excessive thread creation
- No high memory overhead from idle threads
- No excessive context switching
- Priority escalation mitigates inversion when awaiting task results

**Better performance**:
- Fewer threads = less context switching
- Continuations instead of blocking
- CPU cores stay busy efficiently

## Threading Mindset → Isolation Mindset

### Old way (GCD)

```swift
// Thinking about threads
DispatchQueue.main.async {
    // Update UI on main thread
}

DispatchQueue.global(qos: .background).async {
    // Heavy work on background thread
}
```

### New way (Swift Concurrency)

```swift
// Thinking about isolation domains
@MainActor
func updateUI() {
    // Runs on main actor (usually main thread)
}

@concurrent
func heavyWork() async {
    // Swift 6.2+: leaves caller isolation; no particular thread is promised
}
```

### Think in isolation domains

**Don't ask**: "What thread should this run on?"

**Ask**: "What isolation domain should own this work?"

- `@MainActor` for UI updates
- Custom actors for specific state
- Nonisolated for general async work

### Provide hints, not commands

```swift
Task(priority: .userInitiated) {
    await doWork()
}
```

You're describing the nature of work, not assigning threads. Swift optimizes execution.

## Suspension Points

### What is a suspension point?

Moment where task **may** pause to allow other work. Marked by `await`.

```swift
let data = await fetchData() // Potential suspension
```

**Critical**: `await` marks *possible* suspension, not guaranteed. If operation completes synchronously, no suspension occurs.

### Why suspension points matter

1. **Code may pause unexpectedly** - resumes later, possibly different thread
2. **State can change** - mutable state may be modified during suspension
3. **Actor reentrancy** - other tasks can access actor during suspension

`Task.sleep` follows the same rule: it suspends the task rather than blocking a thread. That still does not make actor choice irrelevant. If a delayed retry starts on `@MainActor`, it may wait for main-actor availability before reaching `Task.sleep` when scheduled from another executor or while the main actor is busy. Prefer `@concurrent` when the delay itself is not UI-owned, then hop back with `MainActor.run` for the final UI mutation.

### Actor reentrancy example

```swift
actor BankAccount {
    private var balance: Int = 0

    func deposit(amount: Int) async {
        balance += amount
        print("Balance: \(balance)")

        await logTransaction(amount) // ⚠️ Suspension point

        balance += 10 // Bonus
        print("After bonus: \(balance)")
    }

    func logTransaction(_ amount: Int) async {
        try? await Task.sleep(for: .seconds(1))
    }
}

// Two concurrent deposits
async let _ = account.deposit(amount: 100)
async let _ = account.deposit(amount: 100)

// Unexpected: 100 → 200 → 210 → 220
// Expected:   100 → 110 → 210 → 220
```

**Why**: During `logTransaction`, second deposit runs, modifying balance before first completes.

### Avoiding reentrancy bugs

**Complete actor work before suspending**:

```swift
func deposit(amount: Int) async {
    balance += amount
    balance += 10 // Bonus applied first
    print("Final balance: \(balance)")

    await logTransaction(amount) // Suspend after state changes
}
```

**Rule**: Restore invariants before suspension and revalidate state assumptions
after resumption. Mutating actor state after `await` is allowed, but values
observed before suspension may be stale. Keep this example's balance-and-bonus
transaction together before awaiting its log operation.

## Thread Execution Patterns

### Task Context And MainActor

A regular `Task` inherits its creation context, including actor isolation where
applicable. Its priority does not select a background thread.

```swift
@MainActor
func updateUI() {
    Task {
        MainActor.assertIsolated()
        await performAsync()
        MainActor.assertIsolated()
    }
}

@concurrent
func performAsync() async {
    // Independent work leaves the caller actor with a supporting compiler.
}
```

Observe scheduling with Instruments or the debugger when needed. Assertions
about an actor validate an isolation contract; thread IDs do not prove it.

## Swift 6.2 Changes

### Nonisolated async functions (SE-461)

Without `NonisolatedNonsendingByDefault`, nonisolated async functions use the
generic executor. With that Swift 6.2 upcoming feature enabled, they retain the
caller's isolation unless explicitly `@concurrent`. Check module settings;
compiler version alone does not prove that the feature is enabled.

```swift
class NotSendable {
    func performAsync() async {
        // Remains in the caller isolation with the upcoming feature enabled
    }
}

@MainActor
func caller() async {
    let obj = NotSendable()
    await obj.performAsync()
    // With the feature: retains MainActor isolation for this call
    // Without it: the non-Sendable value crosses an isolation boundary
}
```

### Enabling NonisolatedNonsendingByDefault

With Swift 6.2+ (Xcode 26+) and compatible project settings:

```swift
// Build setting or swift-settings
.enableUpcomingFeature("NonisolatedNonsendingByDefault")
```

### Opting out with @concurrent

Force function to switch away from caller's isolation:

```swift
@concurrent
func performAsync() async {
    // Runs outside the caller actor; thread identity is not the contract
}
```

### nonisolated(nonsending)

Prevent sending non-Sendable values across isolation:

```swift
nonisolated(nonsending) func storeTouch(...) async {
    // Runs on caller's isolation, no value sending
}
```

**Use when**: Method doesn't need to switch isolation, avoiding Sendable requirements.

## Default Isolation Domain (SE-466)

### Configuring default isolation

**Build setting** (Xcode 26+ / Swift 6.2+):
- Default Actor Isolation: `MainActor` or `nonisolated`

**Swift Package** (tools-version 6.2+):

```swift
.target(
    name: "MyTarget",
    swiftSettings: [
        .defaultIsolation(MainActor.self)
    ]
)
```

### Why change default?

Most app code runs on main thread. Setting `@MainActor` as default:
- Reduces false warnings
- Avoids "concurrency rabbit hole"
- Makes migration easier

### Inference with @MainActor default

```swift
// With @MainActor as default:

func f() {} // Inferred: @MainActor

class C {
    init() {} // Inferred: @MainActor
    static var value = 10 // Inferred: @MainActor
}

@MyActor
struct S {
    func f() {} // Inferred: @MyActor (explicit override)
}

```

### Per-module setting

Must opt in for each module/package. Not global across dependencies.

### Backward compatibility

Opt-in only. Default remains `nonisolated` if not specified.

## Debugging Thread Execution

### Observe Isolation

`Thread.current` is unavailable directly in async contexts in Swift 6 mode.
Use debugger/trace observations for scheduling and actor checks such as
`MainActor.assertIsolated()` where main-actor ownership is the contract. A
synchronous wrapper around `Thread.current` can print a momentary diagnostic,
but it does not prove isolation, ordering or post-suspension thread identity.

### Debug navigator

1. Set breakpoint in task
2. Debug → Pause
3. Check Debug Navigator for thread info

### Verify main thread

```swift
assert(Thread.isMainThread)
```

## Common Misconceptions

### ❌ Each Task runs on new thread

**Wrong**. Tasks share limited thread pool, reuse threads.

### ❌ await blocks the thread

**Wrong**. `await` suspends task without blocking thread. Other tasks can use the thread.

### ❌ Task execution order is guaranteed

**Wrong**. Tasks execute based on system scheduling. Use `await` to enforce order.

### ❌ Same task = same thread

**Wrong**. Task can resume on different thread after suspension.

## Why Sendable Matters

Sendability describes values that can safely cross isolation boundaries.
A suspension alone does not imply a transfer, and moving between threads does
not justify bypassing actor ownership. Use immutable `Sendable` values or an
explicit transfer/ownership design when crossing an actual boundary; consult
`sendable.md` for the concrete compiler diagnostic.

## Best Practices

1. **Stop thinking about threads** - think isolation domains
2. **Trust the system** - Swift optimizes thread usage
3. **Use @MainActor for UI** - clear, explicit main thread execution
4. **Minimize suspension points in actors** - avoid reentrancy bugs
5. **Complete state changes before suspending** - prevent inconsistent state
6. **Use priorities as hints** - not guarantees
7. **Make types Sendable** - safe across thread boundaries
8. **Enable Swift 6.2 features** - easier migration, better defaults
9. **Set default isolation for apps** - reduce false warnings
10. **Don't force thread switching** - let Swift optimize

## Migration Strategy

### For new projects (Xcode 26+ / Swift 6.2+)

1. Select `@MainActor` default isolation only for a module whose ownership fits
2. Enable `NonisolatedNonsendingByDefault`
3. Use `@concurrent` for explicit background work

### For existing projects

1. Gradually enable Swift 6 language mode
2. Consider default isolation change
3. Use `@concurrent` to maintain old behavior where needed
4. Migrate module by module

## Decision Tree

```
Need to control execution?
├─ UI updates? → @MainActor
├─ Specific state isolation? → Custom actor
├─ Waiting or non-UI work? → Choose isolation explicitly; async alone does not offload
└─ CPU work must leave caller actor? → @concurrent (Swift 6.2+)

Seeing Sendable warnings?
├─ Can make type Sendable? → Add conformance
├─ Same isolation OK? → nonisolated(nonsending)
└─ Need different isolation? → Make Sendable or refactor
```

## GCD to Isolation Domain Migration

Instead of asking "what thread should this run on?" ask "what isolation domain should own this work?"

- `DispatchQueue.main.async { }` → `@MainActor func updateUI()`
- `DispatchQueue.global().async { }` → `func work() async` (or `@concurrent` if it must leave caller isolation)
- `DispatchQueue(label:).sync { }` → `actor` or `Mutex` for protecting state
- Serial queue for protected state → `actor` (serial isolated access, not FIFO task order)

## Decision Rules

- UI state → usually `@MainActor`
- Mutable shared state → usually an `actor`
- Plain async work with no isolated state → `async` API with explicit ownership
- Work that must hop away from caller isolation under Swift 6.2-era behavior → consider `@concurrent`

## Common Mistakes Agents Make

- Recommending GCD queue hopping when actor isolation already expresses the ownership model.
- Debugging correctness by thread ID instead of by isolation and ordering.
- Treating `await` as a blocking call — it suspends the task, freeing the thread.
- Mapping each `Task` to a conceptual thread.

## Performance Insights

### Why fewer threads = better performance

- **Less context switching**: CPU spends more time on actual work
- **Better cache utilization**: Threads stay on same cores longer
- **No thread explosion**: Predictable resource usage
- **Forward progress**: Avoid blocking cooperative workers; blocking code can still stall them

### Cooperative pool advantages

- Runtime-managed pool sized for the environment
- Prevents oversubscription
- Efficient task scheduling
- Automatic load balancing
