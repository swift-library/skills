# Performance And Testing

## Performance

Measure before rewriting.

- Use Instruments Time Profiler for slow fetches, saves, migrations, or import
  flows.
- Use Allocations for memory growth and retained managed objects.
- Use `-com.apple.CoreData.SQLDebug 1` in repro builds to inspect SQL, query
  count, and query timing.
- Look for N+1 relationship faults, unbounded fetches, large main-context
  saves, and repeated save calls with no persistent changes.

## Memory Patterns

- Keep background imports scoped to a background context.
- Save and reset long-lived import contexts in batches when importing large
  data sets.
- Avoid retaining managed objects longer than needed in caches or view models;
  keep object IDs or value snapshots when crossing lifetimes.

## Testing

- Prefer in-memory stores for fast isolated Core Data tests unless SQLite
  behavior itself is under test.
- Use a shared `NSManagedObjectModel` in tests to avoid duplicate entity
  description conflicts.
- Create deterministic test data helpers close to the test target.
- Tear down contexts and containers after each test.
- Use a real SQLite temporary store for migration tests, persistent history
  tests, CloudKit-adjacent store option tests, or SQL/performance behavior.

## Common Test Error

`Failed to find a unique match for an NSEntityDescription` often means tests
created multiple model instances defining the same managed object classes.
Prefer a shared model instance for the test container.
