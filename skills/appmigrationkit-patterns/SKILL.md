---
name: appmigrationkit-patterns
description: Use this skill for AppMigrationKit implementation and review across migration extensions, source and destination apps, data-container access, export property declarations, ResourcesExporting, resource import, MigrationStatus, progress, App Group recovery, AppMigrationTester, versioned migration, cancellation, and first-launch import UX. Do not use for generic persistence migration, CloudKit sync, or package architecture unless AppMigrationKit owns the transfer.
---

# AppMigrationKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for AppMigrationKit
cross-device or cross-platform app data transfer, including migration extension
setup, resource export/import, and first-launch recovery.

## When To Use

- Adding or reviewing an AppMigrationKit extension target.
- Exporting transportable resources with `ResourcesExporting` or
  `ResourcesExportingWithOptions`.
- Importing migrated resources into a destination app and checking
  `MigrationStatus`.
- Handling migration progress, cancellation, App Group recovery, versioned
  migration, selective export, and error recovery.
- Testing migration code with AppMigrationKit testing tools.

## When Not To Use

- Do not use for ordinary Core Data or SwiftData schema migration; in-store
  model migration is out of scope.
- Do not use for CloudKit sync or account-based restore; leave those to the
  owning persistence or CloudKit code.
- Do not use for package architecture unless the target graph is the only issue.
- Do not treat AppMigrationKit as a general backup/export feature.

## Inputs To Inspect

- Source app, destination app, extension targets, app identifiers, entitlements,
  and data-container access.
- Export declarations, resource enumeration, archive format assumptions, and
  file-size estimates.
- Import code, first-launch migration status handling, clearing status, and
  user-facing recovery.
- App Group sharing, version mapping, cancellation, progress reporting, and
  test fixtures.

## Workflow

1. Confirm AppMigrationKit is the transfer owner rather than a generic storage
   migration.
2. Verify current platform support, entitlement access, and testing tool
   behavior before making API claims.
3. Separate source-app export, destination-app import, and user-facing recovery
   responsibilities.
4. Make resource enumeration deterministic and version-aware.
5. Preserve transportable resources without assuming direct database reuse is
   safe.
6. Use `MigrationStatus.importStatus` and `clearImportStatus()` intentionally on
   first launch.
7. Test success, cancellation, partial failure, unsupported version, missing
   resource, and retry paths.

## Review Rules

- Do not blur AppMigrationKit handoff with app-internal schema migration.
- Do not assume the source and destination have the same file layout or model
  version.
- Do not leave successful migration status uncleared after notifying the user.
- Do not log private migrated resource contents.
- Treat entitlement access, extension lifecycle, archive behavior, and platform
  coverage as current Apple documentation and SDK gated.

## Validation

- Build source app, destination app, and migration extension targets.
- Run AppMigrationKit tests or local migration fixtures when available.
- Test no-migration, successful import, failed import, cancellation, status
  clearing, App Group recovery, and version mismatch paths.

## Output

For implementation or review work, return:

1. AppMigrationKit versus persistence/sync boundary decision
2. Source/export and destination/import findings
3. Migration status, progress, and recovery findings
4. Entitlement and platform assumptions
5. Validation run or still needed
