---
name: swift-data-writable-patterns
description: "Use when SwiftUI or package APIs may fit SwiftDataWritable @Writable surfaces: @Query add/delete/save/reorder, @Writable autosave/throwing/mutableBy variants, single or optional PersistentModel mutation, @Bindable bridge via $model.writable or $model.throwsWritable, domain save/writeback hooks, WritableTransaction runtime bridges, Writable*/ThrowsWritable* domain extensions, or relationship chains such as $book.tags.append(tag). Also use for SwiftDataWritable review of graph-root relationship persistence, context.insert, save/autosave choices, or relationship append semantics; let SwiftData's own persistence, schema, migration, CloudKit, predicate, and custom-store rules govern underlying behavior. Do not use for SwiftData-only schema/container/query work unless @Writable surfaces are concrete."
---

# SwiftDataWritable Patterns

## Purpose

Guide use, review, and debugging of SwiftDataWritable's write surfaces for
SwiftUI + SwiftData apps and downstream package APIs. The package adds a
write-side companion to observed SwiftData query collections and model values
while leaving SwiftData's `ModelContext`, `@Query`, `@Bindable`, schema
attributes, relationship graph traversal, context autosave, and query refresh
behavior in charge.

## Trigger Discipline

For SwiftData read/write/edit work that mentions `@Writable`,
SwiftDataWritable, writable projections, package/domain write extensions, or
relationship chains, check this skill before adding manual `ModelContext`
helpers, custom binding glue, or local collection mutation code.

Use it when the task involves:

- Adding, deleting, batch-writing, saving, or reordering `@Query` results from a
  view.
- Wiring SwiftUI `.onDelete` or `.onMove` to SwiftData model collections.
- Mutating a single `PersistentModel` from a view.
- Keeping `@Bindable` field bindings while adding model-aware write helpers.
- Mutating relationship membership through owner-aware chains such as
  `$book.tags.append(tag)` or `$book.tags[0].documents.append(document)`.
- Designing downstream package/domain APIs that extend `WritableModel`,
  `ThrowsWritableModel`, `WritableRelationshipCollection`, or
  `ThrowsWritableRelationshipCollection`.
- Choosing between mutate-only, best-effort autosave, and throwing autosave.
- Wrapping autosave in a domain transaction function through `transaction:` or
  passing `WritableTransaction` to a manual runtime bridge.
- Reviewing code that imports `SwiftDataWritable` or references
  `Writable*` / `ThrowsWritable*` surface types.

SwiftDataWritable defines the API surface, not the persistence truth. When the
task asks whether a relationship append persists a new model, whether
`context.insert` is required, or what save/delete/autosave does, let
SwiftData's graph-root and `ModelContext` rules set the underlying behavior.

Do not use this skill when the request is only about SwiftData schema design,
migrations, containers, CloudKit, predicates, custom stores, or query behavior
and does not involve a SwiftDataWritable surface.

## Surface Matrix

Use the source property shape to pick the surface.

| Source shape | Generated surface | Meaning |
| --- | --- | --- |
| `@Writable @Query var items: [Model]` | `WritableModelCollection<[Model]>` | Query snapshot mutation through `ModelContext`. |
| `@Writable(autosave: true) @Query var items: [Model]` | `WritableModelCollection<[Model]>` | Query mutation plus best-effort autosave. |
| `@Writable(autosave: true, throws: true) @Query var items: [Model]` | `ThrowsWritableModelCollection<[Model]>` | Query mutation plus throwing autosave. |
| `@Writable(autosave: true, throws: true, transaction: Domain.save) @Query var items: [Model]` | `ThrowsWritableModelCollection<[Model]>` | Query mutation wrapped by a domain-owned autosave transaction. |
| `@Writable(mutableBy:) @Query var items: [Model]` | `KeyPathWritableModelCollection<[Model]>` | Query snapshot mutation plus persisted reorder. |
| `@Writable(autosave: true, throws: true, mutableBy:) @Query var items: [Model]` | `KeyPathThrowsWritableModelCollection<[Model]>` | Reorder/query mutation plus throwing autosave. |
| `@Writable var model: Model` | `WritableModel<Model>` | Single model write helper and relationship-chain entry point. |
| `@Writable(autosave: true, throws: true) var model: Model` | `ThrowsWritableModel<Model>` | Single model write plus throwing autosave. |
| `@Writable(autosave: true, transaction: Domain.save) var model: Model` | `WritableModel<Model>` | Single model mutation wrapped by a domain-owned best-effort autosave transaction. |
| `@Writable var model: Model?` | `WritableModel<Model>?` | Optional single model write helper; use optional chaining. |
| `@Writable @Bindable var model: Model` | SwiftUI keeps `$model` | Bridge with `try $model.writable(...)` or `try $model.throwsWritable(...)`. |
| `$model.relationship` | `WritableRelationshipCollection<Root, [Child]>` | Root model relationship membership mutation. |
| `ThrowsWritableModel.relationship` | `ThrowsWritableRelationshipCollection<Root, [Child]>` | Relationship membership mutation plus throwing autosave. |

Reject or redirect these shapes:

- Plain arrays without `@Query`: no SwiftData query source of truth.
- `@Bindable @Query`: SwiftUI does not combine those roles here.
- `@Writable(mutableBy:)` on a single model: reordering is query-only.
- Direct `@Writable @Relationship`, `@Writable @Attribute`, or
  `@Writable @Transient`: schema fields stay normal model properties.
- Query collections not spelled `[Model]` or `Array<Model>`.

## Save Boundary

SwiftDataWritable has one macro and two error policies.

- `autosave: false`: mutate the current `ModelContext` or owner relationship;
  do not call `context.save()`.
- `autosave: true`: after successful mutation, attempt `context.save()`.
- `transaction:` with `autosave: true`: invoke the supplied domain function
  around the mutation instead of also calling `context.save()`.
- `throws: false`: automatic save failures are swallowed by ordinary
  `Writable*` surfaces.
- `throws: true`: generated `ThrowsWritable*` surfaces throw automatic save
  failures.
- Explicit `save()` always throws on failure.

Examples:

```swift
$persons.append(Person(name: "Draft"))
try $persons.save()

@Writable(autosave: true)
private var book: Book
$book.tags.append(tag) // best-effort autosave

@Writable(autosave: true, throws: true)
private var person: Person
try $person.write { person, _ in
  person.name = "Saved"
}

@Writable(autosave: true, throws: true, transaction: Book.writeback)
private var document: Document
```

`write` follows the same rule: ordinary `write` rethrows closure errors and
best-effort autosaves; `ThrowsWritable*` `write` throws either closure errors or
autosave errors.

Transaction functions receive the active `ModelContext`, the projected model or
collection value, and a mutation closure. Pass a non-overloaded function
directly. If one public name must support multiple source shapes, expose a
function-like value with `callAsFunction` overloads, because macro attribute
arguments are type-checked before expansion.

## Query Collection Workflow

Use `@Writable` with an explicit SwiftData `@Query` array property.

```swift
import SwiftData
import SwiftDataWritable
import SwiftUI

struct PeopleView: View {
  @Writable
  @Query(sort: \Person.name)
  private var persons: [Person]

  var body: some View {
    List {
      ForEach(persons) { person in
        Text(person.name)
      }
      .onDelete(perform: $persons.remove)
    }

    Button("Add") {
      $persons.append(Person(name: "New"))
    }
  }
}
```

`$items` is `WritableModelCollection<[Model]>`.

- `append(_:)`, `insert(_:)`, and `append(contentsOf:)` call
  `context.insert`.
- `delete(_:)`, `deleteAll()`, and `remove(atOffsets:)` call
  `context.delete` for models in the current query snapshot.
- This is query insertion/deletion, not local array mutation and not owner
  relationship mutation.
- `$items.remove` is the SwiftUI `.onDelete` function value.
- `save()` explicitly calls `context.save()` and throws save failures.
- `write { context in ... }` and `write { snapshot, context in ... }` run
  write closures and autosave according to the surface.

## Persisted Reordering

Use `@Writable(mutableBy:)` only when the model has a reference-writable
`Comparable` stored order field.

```swift
@Writable(mutableBy: \Person.priority)
@Query(sort: \Person.priority)
private var persons: [Person]
```

Then wire SwiftUI reordering through:

```swift
.onMove(perform: $persons.move)
```

`move(fromOffsets:toOffset:)` reorders the current query snapshot and reassigns
the existing ordering-key values to moved models. It does not synthesize dense
integer order values. Keep the `@Query(sort:)` key path and `mutableBy` key path
aligned unless local source proves a different intent.

## Single Model Workflow

Use `@Writable` directly on a single model when the view already has the model.

```swift
@Writable
private var person: Person

$person.write { person, _ in
  person.name = "Updated"
}
```

`$model` is `WritableModel<Model>`.

- `write { model, context in ... }` gives downstream extensions a uniform
  model-aware mutation boundary.
- `write { context in ... }` is available for context-only writes.
- `save()` explicitly calls `context.save()`.
- `$model.relationship` projects writable relationship collections when the key
  path is a writable relationship array.

Optional model properties generate optional writable surfaces:

```swift
@Writable
private var person: Person?

$person?.write { person, _ in
  person.name = "Updated"
}
```

Domain commands such as rename, move, archive, trash, or ownership validation
should be downstream extensions on `WritableModel` or `ThrowsWritableModel`, not
built into the package.

## Bindable Compatibility

Use `@Writable @Bindable` when a view needs SwiftUI field bindings and model
write helpers.

```swift
@Writable
@Bindable
private var person: Person

TextField("Name", text: $person.name)

try $person.writable(autosave: true).write { person, _ in
  person.name = "Updated"
}
try $person.throwsWritable(autosave: true).write { person, _ in
  person.name = "Updated"
}
```

`@Writable` does not generate a second `$person`; SwiftUI keeps
`Bindable<Person>`. The bridge reads `person.modelContext`; detached models
throw `WritableModelError.detachedModel`.

Manual bridge calls do not go through macro expansion. When a bridge needs a
custom save/writeback boundary, pass an explicit runtime transaction:

```swift
let transaction = WritableTransaction<Person>(body: PeopleDomain.save)

try $person.throwsWritable(
  autosave: true,
  transaction: transaction
).write { person, _ in
  person.name = "Updated"
}
```

## Relationship Chain Workflow

Relationship collections are projected from a writable owner model.

```swift
@Writable
private var book: Book

$book.tags.append(tag)
$book.tags[0].documents.append(document)
$book.tags[0].documents[0].write { document, _ in
  document.title = "Updated"
}
```

`$book.tags` is `WritableRelationshipCollection<Book, [Tag]>`.

- `append(_:)` and `append(contentsOf:)` mutate the owner relationship array.
- `remove(_:)`, `remove(atOffsets:)`, `$book.tags.remove`, and `removeAll()`
  remove relationship membership.
- These methods do not call `context.insert` or `context.delete`.
- Follow SwiftData's graph-root rule: insert/save the attached owner graph, and
  SwiftData traverses related models automatically. If the owner model is
  already attached to a `ModelContext`, a newly related model can be persisted
  by relationship mutation plus save. This is still SwiftData relationship
  behavior, not a query insertion API owned by SwiftDataWritable.
- Do not recommend manual `context.insert(child)` merely because `child` is
  new; only add explicit `ModelContext` work for an independent graph root,
  deletes, validation, inverse ownership, ordering, or side effects.
- If this behavior matters to the answer, verify SwiftData's documented
  behavior before making claims about `ModelContext.insert`, graph traversal,
  or persistence on save.
- Subscripts return `WritableModel<Element>` or `ThrowsWritableModel<Element>`
  so multi-level relationship chains stay writable.

Use explicit `ModelContext` code or downstream model extensions when a
relationship operation also needs an independent graph-root insert/delete,
inverse ownership fields, validation, ordering, or side effects.

## Extension Guidance

Do not create thin wrappers around projection operations. This is a smell:

```swift
extension WritableModel where Model == Book {
  func addTag(_ tag: Tag) {
    self[dynamicMember: \Book.tags].append(tag)
  }
}
```

Use the projection directly:

```swift
$book.tags.append(tag)
try $book.save()
```

Add an extension only when it carries domain behavior: creating related models,
deduplicating, updating inverse relationships, maintaining ordering, validating
ownership, or running side effects.

```swift
extension ThrowsWritableModel where Model == Book {
  @discardableResult
  func createTag(named name: String) throws -> Tag {
    try write { book, _ in
      let tag = Tag(name: name)
      book.tags.append(tag)
      return tag
    }
  }
}
```

For collection helpers, extend the concrete surface whose semantics match the
operation. Do not use query collections as local arrays; they are snapshots and
should write through `ModelContext`.

## Review Smells

- Answering a SwiftDataWritable relationship question without checking
  SwiftData's graph-root, relationship, and save rules.
- `$queryItems.append` expected to mutate the local array instead of inserting
  into `ModelContext`.
- `$owner.children.append(child)` treated as a query insertion API;
  relationship surfaces only mutate membership. SwiftData persists related
  models through an attached owner graph on save, but SwiftDataWritable does
  not call `context.insert`.
- Missing manual `context.insert(child)` flagged solely because `child` is new.
  That violates SwiftData's graph-root rule; first check whether the attached
  owner graph is saved.
- Immediate persistence expected from `@Writable` without `autosave: true`,
  `save()`, or SwiftData context autosave.
- Autosave failure expected to throw from ordinary `Writable*`; use
  `throws: true` / `ThrowsWritable*` for that.
- Expecting `transaction:` to run when `autosave` is false. Transactions are
  autosave hooks; without autosave, mutation runs directly.
- Passing an overloaded bare function name to `transaction:` and expecting the
  macro to infer the overload from the property. Use a non-overloaded function
  or a function-like value with `callAsFunction` overloads.
- Thin domain wrappers that only forward to an existing projection, for example
  `addTag` that only calls `$book.tags.append(tag)`.
- `@Writable(mutableBy:)` key path not aligned with the query sort key path.
- Domain commands forced into SwiftDataWritable instead of downstream
  `WritableModel` / `ThrowsWritableModel` extensions.

## Package Work Validation

When changing the SwiftDataWritable package, run:

```bash
swift test
swift package dump-package
```

Also grep for stale vocabulary when doing API renames:

```bash
rg -n "MutableModel|MutableRelationship|KeyPathMutable|ThrowingWritable" Sources Tests Docs README.md
```
