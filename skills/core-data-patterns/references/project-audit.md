# Project Audit

Use this checklist before broad Core Data reviews or when local constraints are
unknown.

## Deployment And Store

- Find platform and deployment target.
- Identify store type: SQLite, in-memory, binary, or custom.
- Check whether `NSPersistentCloudKitContainer` or CloudKit options are used.
- Check whether the app has extensions, widgets, or app-group stores.

## Model

- Inspect `*.xcdatamodeld/*/contents`.
- Note entities, attributes, relationships, inverses, constraints, validation
  rules, derived attributes, transformables, and model versions.
- Check renaming identifiers before recommending lightweight migration.
- Check whether newer model features are available for the deployment target.

## Stack

- Locate `NSPersistentContainer` or `NSPersistentCloudKitContainer` creation.
- Inspect `persistentStoreDescriptions` before `loadPersistentStores`.
- Check migration options, persistent history tracking, remote change
  notifications, CloudKit options, and store URLs.
- Inspect `viewContext` merge policy, `automaticallyMergesChangesFromParent`,
  query generation, undo manager, and context name.

## Risk Signals

- `NSManagedObject` passed into background contexts, tasks, actors, callbacks,
  or detached work.
- `performAndWait` on UI paths or nested context calls.
- Batch operations without a merge or persistent-history plan.
- Constraint definitions without an intentional merge policy.
- Tests creating multiple independent `NSManagedObjectModel` instances for the
  same entities.

## Debug Flags For Repro Builds

- `-com.apple.CoreData.ConcurrencyDebug 1` for context-thread violations.
- `-com.apple.CoreData.SQLDebug 1` for SQL and query timing visibility.
