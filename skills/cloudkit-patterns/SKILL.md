---
name: cloudkit-patterns
description: Use this skill for CloudKit implementation and review across iCloud containers, public/private/shared databases, CKRecord modeling, custom zones, record queries, subscriptions, silent-change delivery, CKSyncEngine, server change tokens, CKShare, UICloudSharingController, CKAsset storage, account status, CKError handling, conflict resolution, CloudKit Dashboard workflows, NSUbiquitousKeyValueStore, and iCloud document coordination. Do not use for SwiftData/Core Data CloudKit sync unless direct CloudKit records, schema, sharing, subscriptions, or dashboard behavior is in scope.
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

## Validation

- Build the affected app and extension targets with the intended entitlements.
- Exercise create, fetch, update, delete, query, and asset paths against the
  intended CloudKit environment when feasible.
- Test signed-out, restricted, offline, quota, partial-failure, conflict, and
  change-token-reset states when they are relevant.
- Test subscription delivery, manual fetch, and sync-engine state restoration
  across relaunches when sync is in scope.
- Verify Dashboard schema/indexes and confirm logs redact record contents.

## Output

Return:

1. CloudKit ownership and persistence-framework boundary
2. Container/database/schema assessment
3. Record, sync, sharing, or iCloud coordination findings
4. Error, conflict, privacy, and recovery notes
5. Validation run or still needed
