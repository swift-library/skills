# Stack, Contexts, And Saving

## Stack Setup

- Prefer a dedicated Core Data stack type or persistence controller over
  scattered setup code.
- Configure `persistentStoreDescriptions` before `loadPersistentStores`.
- Use `NSPersistentCloudKitContainer` only when CloudKit sync is intentionally
  enabled.
- Name contexts when it helps logs and debugging.
- Disable undo on non-UI contexts unless the project needs undo support.

## Context Roles

- Use `viewContext` for UI-bound reads and small user-driven edits.
- Use `newBackgroundContext()` or `performBackgroundTask` for imports, cleanup,
  large writes, or long-running work.
- Do not use one context as a global answer to every problem. Context choice
  should match lifetime, queue, and merge needs.

## Merge Policies

- Choose merge policy deliberately when constraints or concurrent writers are
  involved.
- With uniqueness constraints, verify the chosen policy matches product
  behavior: store wins, object wins, overwrite, rollback, or error.
- If multiple contexts write to the same store, set an explicit merge strategy
  for the UI context.

## Saving

- Save only when persistent data changed.
- Avoid unconditional `try? context.save()` in UI update paths.
- Prefer a small helper such as `saveIfNeeded()` when the project style allows
  it.

```swift
extension NSManagedObjectContext {
    var hasPersistentChanges: Bool {
        !insertedObjects.isEmpty ||
        !deletedObjects.isEmpty ||
        updatedObjects.contains { $0.hasPersistentChangedValues }
    }

    func saveIfNeeded() throws {
        guard hasPersistentChanges else { return }
        try save()
    }
}
```

## Error Handling

- Do not silently discard save errors in production paths.
- Preserve the original `Error` for logs, user recovery, or telemetry.
- Treat validation and merge-conflict errors as model or policy signals, not
  just transient failures.
