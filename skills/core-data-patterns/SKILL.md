---
name: core-data-patterns
description: Use this skill for Core Data implementation, review, debugging, or modernization involving NSPersistentContainer, NSPersistentCloudKitContainer, NSManagedObjectContext, NSManagedObject, NSManagedObjectID, NSFetchRequest, NSFetchedResultsController, merge policies, saves, batch insert/delete/update, persistent history tracking, model constraints, validation, schema migration, CloudKit sync, Core Data performance, in-memory stores, or errors such as NSPersistentStoreIncompatibleVersionHashError, NSMergeConflict, cross-context object access, and failed unique NSEntityDescription matches. Do not use for SwiftData, generic database design, networking, package architecture, repository documentation, or non-Core-Data Swift Concurrency migration.
---

# Core Data Patterns

## Purpose

Guide Core Data work with project-compatible persistence patterns, debugging
triage, and small implementation recommendations.

## When To Use

- Setting up or reviewing `NSPersistentContainer` or
  `NSPersistentCloudKitContainer`.
- Choosing view-context vs background-context usage.
- Fixing Core Data threading, context confinement, or object handoff issues.
- Reviewing saves, merge policies, constraints, validation, fetch requests, or
  batch operations.
- Debugging migration, CloudKit sync, persistent history, performance, or test
  setup problems.
- Investigating Core Data errors such as
  `NSPersistentStoreIncompatibleVersionHashError`, `NSMergeConflict`, failed
  unique `NSEntityDescription` matches, or cross-context object access.

## When Not To Use

- Do not use for SwiftData model design or SwiftData CloudKit constraints.
- Do not use for generic database schema design outside Core Data.
- Do not use for networking architecture, package architecture, dependency
  replacement, or repository documentation.
- Do not use for broad Swift Concurrency migration, actor-isolation design,
  `Sendable` fixes, or data-race work unless the concrete problem is Core Data
  context confinement or managed-object handoff. Route broader concurrency work
  to `swift-concurrency-patterns`.

## Inputs To Inspect

- User request, exact error text, stack traces, logs, and reproduction steps.
- Deployment target and platform.
- `*.xcdatamodeld/*/contents`, model versions, entities, relationships,
  constraints, renaming identifiers, and CloudKit settings.
- `NSPersistentContainer` / `NSPersistentCloudKitContainer` setup,
  `persistentStoreDescriptions`, store options, and migration options.
- `viewContext`, background contexts, `performBackgroundTask`, merge policies,
  `automaticallyMergesChangesFromParent`, and query-generation settings.
- Fetch requests, save paths, batch operations, persistent history processing,
  and test Core Data containers.

## Workflow

1. Read local project truth before applying patterns.
2. Classify the task: stack setup, save/merge, fetch, threading/concurrency,
   batch/history, model configuration, migration, CloudKit, performance, or
   testing.
3. Determine deployment-target availability before recommending staged
   migration, deferred migration, composite attributes, or newer APIs.
4. Identify the context involved before fixing behavior: view context for UI
   work, background context for heavy work.
5. Open only the smallest matching reference file. Open
   `references/_index.md` only if routing is unclear.
6. Prefer behavior-preserving fixes and validate with the relevant build,
   migration, sync, performance, or test loop.

## Reference Files To Consult

- `references/project-audit.md`: first-pass project discovery checklist.
- `references/stack-contexts-saving.md`: stack setup, contexts, merge policies,
  saving, and `hasPersistentChanges`.
- `references/threading-concurrency.md`: context confinement,
  `NSManagedObjectID`, `perform`, `performAndWait`, async/await, and routing to
  Swift Concurrency guidance.
- `references/fetching-batch-history.md`: fetch requests,
  `NSFetchedResultsController`, batch operations, and persistent history.
- `references/model-migration-cloudkit.md`: model constraints, validation,
  lightweight/staged/deferred migration, and CloudKit restrictions.
- `references/performance-testing.md`: Instruments, SQL debugging, memory, and
  in-memory test stores.

## Decision Rules

- Never pass `NSManagedObject` instances across contexts, threads, tasks, or
  actors. Pass `NSManagedObjectID` and re-fetch in the destination context.
- Match context to work: keep UI reads and small edits on the view context; use
  background contexts for imports, heavy writes, cleanup, and batch work.
- Use conditional saves. Avoid saving when there are no persistent changes.
- Configure merge policy deliberately when using constraints or concurrent
  writers.
- Treat batch operations as store-level changes: plan for persistent history or
  explicit merging when UI must update.
- Prefer lightweight migration when the model change supports it. Use staged or
  deferred migration only when deployment targets support them and the change
  needs them.
- For CloudKit-backed Core Data, respect CloudKit schema restrictions and treat
  production schema changes as high risk.
- Profile performance claims with Instruments, SQL debug logs, or a local
  benchmark before prescribing broad rewrites.

## Validation Rules

- Build after changing stack setup, model classes, fetches, or generated code.
- Run migration or store-loading checks when model versions or store options
  change.
- Run affected Core Data tests with isolated stores.
- Reproduce sync, history, or batch-operation fixes with realistic store data.
- Confirm no managed object crosses context boundaries after a threading fix.

## Output Format

For reviews or implementation recommendations, return:

1. Phase / stage judgment
2. Core Data surface inspected
3. Findings
4. Recommended changes
5. Compatibility impact
6. Validation performed
7. Risks
8. Next steps

## Failure / Uncertainty Handling

- If deployment target, store type, or CloudKit usage is unknown, report the
  uncertainty before recommending availability-sensitive APIs.
- If a migration is destructive or production CloudKit schema is involved, stop
  and request explicit confirmation before proposing irreversible steps.
- If the task becomes broad Swift Concurrency design rather than Core Data
  confinement, route to `swift-concurrency-patterns`.
