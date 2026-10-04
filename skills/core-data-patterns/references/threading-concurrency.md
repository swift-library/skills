# Threading And Concurrency

## Core Rule

Never pass `NSManagedObject` instances across contexts, threads, tasks, or
actors. Pass `NSManagedObjectID` and re-fetch in the destination context.

```swift
let objectID = article.objectID

backgroundContext.perform {
    do {
        let article = try backgroundContext.existingObject(with: objectID)
        article.setValue("Updated", forKey: "title")

        if backgroundContext.hasChanges {
            try backgroundContext.save()
        }
    } catch {
        // Preserve or report the Core Data error using the project's error path.
    }
}
```

## Context Confinement

- Access managed objects only through their owning context.
- Use `context.perform { ... }` for asynchronous context work.
- Use `performAndWait` sparingly, only when synchronous ordering is required and
  deadlock risk is understood.
- Keep view-context work small enough not to block UI.

## Swift Concurrency

- `NSManagedObject` should not be treated as `Sendable`.
- Do not hide Core Data safety warnings with `@unchecked Sendable` on managed
  object types.
- Return value types, DTOs, or object IDs from async Core Data boundaries when
  crossing actors or tasks.
- When using async `context.perform`, keep the context as the isolation point
  for Core Data work.

## Scope Boundary

Stay in this skill for Core Data context confinement, object-ID handoff, and
managed-object access patterns.

Broad actor isolation design, strict-concurrency migration, `Sendable` modeling
outside Core Data, task cancellation architecture, and general data-race
debugging are out of scope.
