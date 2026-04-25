# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Quick Routing

- Stack setup, context configuration, merge policies, and saves:
  `stack-contexts-saving.md`
- Context confinement, `NSManagedObjectID`, `perform`, `performAndWait`, and
  Core Data plus async/await: `threading-concurrency.md`
- Fetch optimization, `NSFetchedResultsController`, batch operations, and
  persistent history: `fetching-batch-history.md`
- Model constraints, validation, migration, and CloudKit sync:
  `model-migration-cloudkit.md`
- Profiling, SQL debug, memory growth, and test containers:
  `performance-testing.md`
- Project discovery before a broad audit: `project-audit.md`

## Error Routing

- `NSPersistentStoreIncompatibleVersionHashError`: open
  `model-migration-cloudkit.md`.
- `NSMergeConflict` or constraint violations: open
  `stack-contexts-saving.md` and `model-migration-cloudkit.md`.
- Cross-context access, wrong-thread access, or managed-object sendability:
  open `threading-concurrency.md`.
- Batch operation does not update UI: open `fetching-batch-history.md`.
- CloudKit sync or schema issue: open `model-migration-cloudkit.md`.
- Failed unique `NSEntityDescription` match in tests: open
  `performance-testing.md`.
