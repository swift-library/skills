# Swift 6.4 Cleanup And Cancellation

Use this reference for awaited cleanup and bounded cancellation protection.
Keep existing task ownership, structured concurrency, actor isolation and
project deployment constraints.

## Awaited Defer

With a supporting Swift 6.4 compiler, an async function can await inside
`defer`. The function waits for deferred cleanup before returning and the
cleanup retains the surrounding isolation. It does not create a new task.

```swift
actor CleanupLog {
    var entries: [String] = []
    func append(_ value: String) { entries.append(value) }
}

func work(_ log: CleanupLog) async {
    defer { await log.append("cleanup") }
    await log.append("work")
}
```

On older compilers, explicitly await cleanup on success and error paths.
`defer { Task { ... } }` creates unstructured work and does not guarantee that
cleanup finishes before return. Deferred cleanup can still observe cancellation;
`defer` alone does not shield cancellation-sensitive operations.

## Cancellation Shield

The OS 27 SDK provides `withTaskCancellationShield`. Gate its runtime
availability separately from Swift 6.4 syntax. Inside the shield, task
cancellation is masked; after it ends, the surrounding cancellation state is
restored. Use it only for bounded cleanup that must finish, not an entire
request, retry loop or unbounded network operation.

```swift
@available(anyAppleOS 27.0, *)
func cleanup(_ log: CleanupLog) async {
    await withTaskCancellationShield {
        await log.append("protected cleanup")
    }
}
```

Check the selected SDK and run cancellation/order tests for the affected path.
On older targets retain the existing supported cleanup strategy; do not hide
unavailable APIs behind a compiler-version check alone. Sources are listed in
`official-sources.md`.
