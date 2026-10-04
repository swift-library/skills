# Troubleshooting and Updates

## Frequent Failure Modes

- `missingModelContext`: no valid container wiring for current execution path.
- `modelValidationFailure`: schema/model constraints are violated at save time.
- `unsupportedPredicate` / `unsupportedSortDescriptor`: expression is not supported for store-side evaluation.
- `includePendingChangesWithBatchSize`: invalid fetch configuration combination.
- `historyTokenExpired`: history token points to pruned transactions.
- `unknownSchema` / `backwardMigration`: migration path is invalid or unsupported.

## Practical Debug Sequence

1. Confirm container and schema setup.
2. Confirm deployment target supports the APIs in use.
3. Reproduce with a minimal `FetchDescriptor` and no optional filters.
4. Validate delete predicates and save boundaries.
5. Validate history token lifecycle (load, use, persist, cleanup).
6. Validate CloudKit mode (`automatic`, explicit container, or `.none`).

## API Availability Snapshot

- SwiftData base APIs (`@Model`, `ModelContainer`, `ModelContext`, `Query`): iOS 17+.
- Persistent history descriptor and many history/data-store APIs: iOS 18+.
- `#Unique` and `#Index` macros: iOS 18+.
- Model inheritance: iOS 26+ (June 2025 updates); always gate by deployment target.

## Release-Aware Recommendations

When advising changes:

- avoid recommending `#Unique` or `#Index` on iOS 17-only apps;
- avoid relying on history sorting (`HistoryDescriptor.sortBy`, iOS 26+) unless the deployment target allows it;
- provide fallback plans for older deployment targets.

## Primary Documentation

- https://developer.apple.com/documentation/swiftdata/swiftdataerror
- https://developer.apple.com/documentation/swiftdata/datastoreerror
- https://developer.apple.com/documentation/updates/swiftdata
