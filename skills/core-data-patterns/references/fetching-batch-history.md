# Fetching, Batch Operations, And Persistent History

## Fetch Requests

- Fetch only what the current workflow needs.
- Use `fetchLimit` for single-result or bounded queries.
- Use `fetchBatchSize` for large scrolling lists.
- Use sort descriptors that match the user-visible order.
- Use `relationshipKeyPathsForPrefetching` when a list would otherwise fire
  repeated relationship faults.
- Use aggregate fetches or count requests when objects themselves are not
  needed.

## NSFetchedResultsController

- Use `NSFetchedResultsController` when UIKit table or collection views need
  incremental Core Data updates.
- For SwiftUI, follow the repository's existing approach before introducing a
  controller wrapper.
- Keep fetched results sorted; an FRC requires at least one sort descriptor.

## Batch Operations

- Batch inserts, deletes, and updates operate at the persistent-store level and
  bypass normal object validation and object notifications.
- Do not expect existing in-memory objects or UI fetches to update
  automatically after batch operations.
- Use result types that return object IDs when downstream contexts need merging.
- Avoid batch insert for relationship-heavy creation unless the relationship
  setup is explicitly handled later.

## Persistent History

Persistent history tracking is the usual answer when changes must be merged
across contexts, app extensions, background imports, or batch operations.

Before relying on persistent history, verify:

- `NSPersistentHistoryTrackingKey` is enabled before stores load.
- `NSPersistentStoreRemoteChangeNotificationPostOptionKey` is enabled when
  remote-change notifications are part of the merge path.
- There is a fetch, merge, and cleanup plan for history transactions.

## Common Review Findings

- Fetches with no limit or batch size on large data sets.
- Relationship faults in a loop where prefetching is needed.
- Batch delete/update followed by stale UI because no merge path exists.
- Persistent history enabled but never cleaned.
