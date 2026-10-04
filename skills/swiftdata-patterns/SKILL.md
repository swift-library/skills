---
name: swiftdata-patterns
description: 'Use this skill for any implementation, review, debugging, migration, or modernization change that touches SwiftData surfaces, including @Model, @Relationship, relationship append, inverse relationships, graph-root insertion, @Attribute, @Transient, #Predicate, @Query, FetchDescriptor, ModelContainer, ModelContext, context.insert, save/autosave, ModelConfiguration, ModelActor, SchemaMigrationPlan, VersionedSchema, persistent history, CloudKit sync, #Index, #Unique, inheritance, or Core Data coexistence. Also use alongside SwiftDataWritable when @Writable relationship chains raise persistence, insert, save, delete, or graph traversal questions. Do not use for Core Data-only stacks, deep SwiftUI UI design, broad Swift Concurrency migration, networking, package architecture, or repository documentation.'
---

# SwiftData Patterns

## Purpose

Guide SwiftData implementation, review, migration, and debugging with
project-compatible patterns for schema design, container/context lifecycle,
querying, relationships, migrations, CloudKit sync, and concurrency boundaries.

## When To Use

- Designing or reviewing `@Model` schemas, relationships, delete rules,
  attributes, transient data, uniqueness, indexes, or model inheritance.
- Reviewing relationship append, inverse relationship maintenance, graph-root
  insertion, `ModelContext.insert`, `context.save()`, context autosave, or delete
  behavior, including SwiftDataWritable relationship-chain call sites where the
  question is the underlying SwiftData persistence behavior.
- Fixing `#Predicate`, `@Query`, `FetchDescriptor`, filtering, sorting,
  dynamic query setup, or query performance.
- Setting up or reviewing `ModelContainer`, `ModelConfiguration`,
  `ModelContext`, autosave, undo, insert/update/delete lifecycle, or tests.
- Planning schema migrations with `VersionedSchema`, `SchemaMigrationPlan`,
  migration stages, persistent history, or release data compatibility.
- Reviewing CloudKit-backed SwiftData constraints and sync behavior.
- Handling SwiftData background persistence, `ModelActor`, context boundaries,
  or identifier-based model handoff.
- Migrating from or coexisting with Core Data while SwiftData is the target.

## When Not To Use

- Do not use for Core Data-only stacks.
- SwiftDataWritable package-specific `@Writable` projection shape, macro
  expansion, generated surface types, and ordinary/throws autosave API are out
  of scope. Still use this skill for the underlying SwiftData persistence
  truth: relationship graph traversal, graph-root insertion,
  `ModelContext.insert`, save/autosave, delete rules, and inverse relationship
  behavior.
- Do not use for deep SwiftUI layout, navigation, accessibility, or animation
  work.
- Do not use for source-level SwiftUI performance work.
- Do not use for broad Swift Concurrency migration, actor-isolation design,
  `Sendable` fixes, or data-race work unless the concrete problem is SwiftData
  context/model isolation.
- Do not use for networking architecture, package architecture, dependency
  replacement, or repository documentation.
- Do not suggest Core Data unless SwiftData cannot solve the concrete
  requirement or Core Data coexistence is already in scope.

## Inputs To Inspect

- Deployment targets and Swift/Xcode version before recommending availability
  sensitive APIs such as `#Index`, `#Unique`, `HistoryDescriptor`, `DataStore`,
  or inheritance patterns.
- `@Model`, `@Relationship`, `@Attribute`, `@Transient`, `#Predicate`,
  `#Index`, and `#Unique` definitions.
- `ModelContainer`, `.modelContainer(...)`, `ModelConfiguration`,
  `ModelContext`, `mainContext`, and custom context setup.
- SwiftDataWritable relationship-chain call sites only when the question depends
  on SwiftData relationship persistence, graph insertion, `context.insert`, or
  save/autosave behavior.
- `@Query`, `FetchDescriptor`, predicates, sort descriptors, fetch limits, and
  in-memory filtering.
- Migrations, `VersionedSchema`, `SchemaMigrationPlan`, persistent history
  token handling, and destructive operations.
- CloudKit capability setup, CloudKit database selection, optionality,
  uniqueness, relationship constraints, and sync error symptoms.
- Tests, preview/in-memory containers, widgets, intents, app extensions, and
  cross-process change handling when relevant.

## Workflow

1. Read local project truth first.
2. Classify the task: schema, container/context lifecycle, query/predicate,
   relationships/inheritance, migration/history, CloudKit, Core Data adoption,
   concurrency, testing, or troubleshooting.
3. Confirm deployment target before recommending version-gated APIs.
4. Verify real container wiring before debugging inserts, fetches, previews, or
   tests; missing container setup makes inserts fail and fetches empty.
5. Open only the smallest matching reference files. Open `references/_index.md`
   only if routing is unclear.
6. For reviews, run the high-signal checks in `references/review-rules.md` and
   `references/predicate-safety.md` after inspecting the broader project
   surface.
7. Prioritize data loss, migration safety, sync divergence, accidental mass
   deletion, predicate runtime crashes, and context-isolation bugs over style.
8. Prefer behavior-preserving fixes and validate with build, targeted tests,
   migration rehearsal, CloudKit dev-container checks, or representative data.

## Reference Files To Consult

- `references/modeling-and-schema.md`: model design, attributes, uniqueness,
  indexing, transient data, and schema planning.
- `references/model-context-and-lifecycle.md`: container setup, context roles,
  autosave, undo, insert/update/delete, selection, and identity.
- `references/querying-and-fetching.md`: `@Query`, `FetchDescriptor`,
  predicates, sorting, bounds, and performance.
- `references/relationships-and-inheritance.md`: relationship modeling, delete
  rules, inverses, inheritance, and hierarchy queries.
- `references/migrations-and-history.md`: schema evolution, migration plans,
  persistent history, tombstones, and release risks.
- `references/cloudkit-sync.md`: CloudKit capabilities, compatibility,
  container selection, dev schema, and sync verification.
- `references/core-data-adoption.md`: Core Data coexistence and incremental
  SwiftData adoption boundaries.
- `references/concurrency-and-actors.md`: `ModelActor`, context boundaries,
  background persistence, undo, and history with concurrent writers.
- `references/troubleshooting-and-updates.md`: frequent failures, debug
  sequence, and release-aware API availability.
- `references/implementation-playbooks.md`: end-to-end task playbooks.
- `references/review-rules.md`: high-signal review checks for autosave,
  relationships, delete rules, properties, and fetches.
- `references/predicate-safety.md`: predicate operations, unsupported methods,
  and dangerous runtime-crash patterns.
- `references/cloudkit-constraints.md`: concise SwiftData CloudKit constraints.
- `references/indexing-rules.md`: iOS 18+ database indexing patterns.
- `references/model-inheritance-rules.md`: iOS 26+ model subclassing.

## Decision Rules

- Repository-local truth wins over this skill.
- When SwiftDataWritable also applies, first use SwiftData rules to determine
  persistence behavior, graph-root insertion, relationship traversal,
  `ModelContext.insert`, save/autosave, delete, and inverse behavior; then
  choose the writable API surface separately.
- Do not require manual `context.insert(child)` solely because a newly created
  model is appended to an attached owner's relationship; first check whether the
  attached owner graph will be saved. Use explicit insert for independent graph
  roots or when local design requires a separate insertion boundary.
- Treat schema changes as migration changes. Rehearse on existing data before
  claiming safety.
- Review delete rules as business rules. Unbounded or broad deletes require
  explicit predicate review.
- Keep model/context isolation explicit. Do not pass mutable model instances
  across contexts, tasks, actors, widgets, or extensions; prefer persistent
  identifiers and refetching.
- Prefer deterministic store-backed predicates, explicit sort order, and
  bounded fetches over ad hoc filtering in views.
- For CloudKit-backed SwiftData, verify optionality, uniqueness, relationship,
  and production schema constraints before changing models.
- Gate new APIs by deployment target and provide compatible fallbacks.
- Use Core Data only for coexistence, migration, or requirements SwiftData does
  not currently satisfy.

## Review Checklist

- `ModelContainer` is wired at the correct app/window/test/preview boundary.
- Model definitions include deliberate relationships, delete rules, inverses,
  optionality, uniqueness, indexing, and transient data decisions.
- Predicates use supported operations and avoid known runtime-crash patterns.
- Queries are deterministic, sorted when needed, and bounded for scale.
- Saves, undo, and context roles match the UI/background workflow.
- Migration and history paths are tested against pre-existing user data.
- CloudKit constraints are satisfied before enabling sync.
- Background work uses safe context or model actor boundaries.

## Output Format

For reviews, report findings first by severity with exact files and lines when
available. For each finding, include the violated rule or risk, the likely
impact, and a concrete before/after or recommended change.

For implementation work, summarize:

1. SwiftData surface changed
2. Schema, container, context, query, migration, or sync impact
3. Compatibility and deployment-target impact
4. Validation performed
5. Remaining risks or follow-up checks

## Failure / Uncertainty Handling

- If deployment target, CloudKit usage, existing data compatibility, or
  container wiring is unknown, state the uncertainty before recommending
  version-gated or migration-sensitive APIs.
- If a change could delete data, break migration, or alter a production
  CloudKit schema, stop and request explicit confirmation before proposing an
  irreversible path.
- If the task becomes broad concurrency, SwiftUI, Core Data-only, or package
  architecture work, state that it is outside SwiftData persistence scope.
