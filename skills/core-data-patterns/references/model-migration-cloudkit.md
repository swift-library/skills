# Model, Migration, And CloudKit

## Model Configuration

- Use constraints only when the product needs uniqueness semantics.
- Pair constraints with a deliberate merge policy.
- Prefer model validation for persistent invariants, and keep UI validation for
  user guidance.
- Use derived attributes when stored aggregates avoid expensive relationship
  traversal and the deployment target supports the feature.
- Treat transformables as a compatibility and migration risk. Prefer simple
  attribute types unless custom storage is justified.

## Lightweight Migration

Prefer lightweight migration when changes are compatible:

- add or remove attributes,
- make an attribute optional,
- make an optional attribute required when a default value exists,
- rename entities, attributes, or relationships with renaming identifiers,
- add or remove entities or relationships when mapping can be inferred.

Before recommending migration, inspect current model versions and renaming
identifiers.

## Staged And Deferred Migration

- Use staged migration for multi-step or complex migrations only when the
  deployment target supports it.
- Use deferred migration when expensive cleanup can happen after the store
  opens and the deployment target supports it.
- Keep production migrations reversible in planning even when the store
  migration itself is not reversible.

## CloudKit-Backed Core Data

When `NSPersistentCloudKitContainer` is used:

- Confirm CloudKit capability, container identifier, and store description
  configuration.
- Respect CloudKit schema limits such as optional relationships and supported
  attribute types.
- Avoid assuming unique constraints or model relationships behave like a local
  SQLite-only store.
- Treat production CloudKit schema changes as high risk. Once deployed,
  production schema changes are constrained and require careful planning.

## Debugging

- For migration errors, capture the exact Core Data error code and failing
  source/destination model versions.
- For CloudKit sync, inspect Core Data event notifications, device logs,
  account status, entitlements, and whether the issue reproduces in development
  or production containers.
