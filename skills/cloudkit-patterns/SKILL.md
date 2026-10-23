---
name: cloudkit-patterns
description: CloudKit record, sync and sharing implementation with CKRecord, CKSyncEngine, CKShare, subscriptions, change tokens and conflict recovery. Inspect containers, zones and account state. Not for SwiftData/Core Data sync without a direct CloudKit concern.
---

# CloudKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for direct CloudKit and
adjacent iCloud data workflows. Use this skill when the task is about CloudKit
containers, records, sync, sharing, subscriptions, account state, or iCloud data
coordination, not when CloudKit is only an implementation detail of a local
persistence framework.

## When To Use

- Configuring iCloud containers, entitlements, public/private/shared databases,
  development/production environments, or CloudKit Dashboard schema.
- Modeling `CKRecord` types, fields, references, assets, custom zones, and
  indexes.
- Implementing record CRUD, queries, batch operations, subscriptions, silent
  change delivery, or operation retry behavior.
- Building sync with `CKSyncEngine`, incremental zone/database changes, server
  change tokens, local state persistence, and conflict resolution.
- Implementing record or zone sharing with `CKShare` and
  `UICloudSharingController`.
- Handling account status, unavailable iCloud, quota, partial failures,
  server-side errors, and user-visible recovery.
- Reviewing `NSUbiquitousKeyValueStore` or iCloud document coordination when it
  is part of an iCloud data feature.

## When Not To Use

- Do not use for ordinary SwiftData or Core Data model work unless direct
  CloudKit schema, sharing, or sync diagnostics are part of the task.
- Do not use for Keychain credential storage or system authentication flows.
- Do not use for generic push notification handling unless the push is a
  CloudKit subscription/change-delivery concern.
- Do not use for market, account, or support messaging about iCloud.

## Inputs To Inspect

- Entitlements, iCloud container identifiers, target capabilities, provisioning
  state, and CloudKit Dashboard environment/schema.
- Record types, fields, references, assets, indexes, custom zones, database
  choice, and sharing model.
- Operation code, async CloudKit API usage, retry/backoff handling, QoS,
  batching, and partial failure handling.
- Subscription registration, remote notification handling, sync engine state,
  server change tokens, and local persistence of sync metadata.
- Account-status UI, conflict resolution, quota handling, logging, privacy, and
  tests using real or isolated containers.
- Check `com.apple.developer.icloud-container-identifiers` for the selected container and `com.apple.developer.icloud-container-environment` for Development/Production.
- For `CKSyncEngine`, check CloudKit and Remote notifications capabilities; its SDK contract requires both.

## Workflow

1. Confirm whether the task is direct CloudKit/iCloud data work or a
   persistence-framework sync slice.
2. Check entitlement, container, environment, and dashboard/schema readiness
   before reviewing code behavior.
3. Choose the correct database and zone shape: public, private, shared, default
   zone, or custom zone.
4. Review record modeling for stable record IDs, references, assets, encrypted
   fields where appropriate, indexes, and server-side query needs.
5. Review writes and reads for batching, partial failures, retries, cancellation,
   main-thread boundaries, and user-visible progress.
6. For sync, verify local persistence of change tokens and `CKSyncEngine` state,
   zone recovery, push-triggered fetches, and conflict handling.
   - Gate `CKSyncEngine` to iOS 17/macOS 14/tvOS 17/watchOS 10 or later; initialize `Configuration(database:stateSerialization:delegate:)` for a private or shared database, never the public database.
   - Persist each `.stateUpdate` serialization from `CKSyncEngineDelegate.handleEvent(_:syncEngine:)` alongside app data and restore the latest state on initialization across launches.
   - Automatic sync timing is indeterminate; use `fetchChanges()` / `sendChanges()` for an explicit sync request.
7. For sharing, verify records live in a shareable zone, `CKShare` setup,
   share acceptance, participant permissions, and owner/participant semantics.
8. For iCloud key-value or document coordination, keep the workflow clearly
   scoped and avoid mixing it with record sync unless the feature needs both.
9. Validate with the smallest real-container or dashboard-backed path that can
   prove the behavior.

## Review Rules

- Do not hide direct CloudKit failure modes behind generic persistence advice.
- Do not assume an iCloud account, network, quota, dashboard schema, or push
  delivery is available.
- Do not discard server change tokens or sync engine state without a rebuild
  plan.
- Do not store sensitive record payloads, account identifiers, or assets in logs
  or review output.
- Treat `CKSyncEngine`, sharing, account-state, dashboard, and environment
  behavior as current-documentation and local-SDK gated.
- Limit each sync-engine record batch to 250 saves plus deletes; `RecordZoneChangeBatch(pendingChanges:recordProvider:)` stops at the limit and leaves remaining changes pending.
- Replace deprecated `CKQueryOperation.recordFetchedBlock` / `queryCompletionBlock` with `recordMatchedBlock` / `queryResultBlock` on iOS 15/macOS 12/tvOS 15/watchOS 8 or later; handle per-record failures and returned cursors.
- Move fetched `CKAsset.fileURL` data into app-owned storage promptly; the system deletes staged files, and filenames/metadata need separate record fields.
- Inspect `CKPartialErrorsByItemIDKey` per item and honor `CKErrorRetryAfterKey` as seconds before retrying.
- For `serverRecordChanged`, merge client/ancestor changes into the server record and retry that record; reusing the stale client record repeats the conflict.

## Validation

- Build the affected app and extension targets with the intended entitlements.
- Exercise create, fetch, update, delete, query, and asset paths against the
  intended CloudKit environment when feasible.
- Test signed-out, restricted, offline, quota, partial-failure, conflict, and
  change-token-reset states when they are relevant.
- Test subscription delivery, manual fetch, and sync-engine state restoration
  across relaunches when sync is in scope.
- Verify Dashboard schema/indexes and confirm logs redact record contents.
- Test signed-out public reads separately from writes: public fetch/query can work without an iCloud account, but public saves and private access require one.
- In sync-engine tests, set `Configuration.automaticallySync = false` and invoke fetch/send explicitly for deterministic scheduling.

## Output

Return:

1. CloudKit ownership and persistence-framework boundary
2. Container/database/schema assessment
3. Record, sync, sharing, or iCloud coordination findings
4. Error, conflict, privacy, and recovery notes
5. Validation run or still needed
