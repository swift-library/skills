# Working with predicates

SwiftData predicates support only a subset of Swift functionality. Some things are marked as being unsupported, meaning that they will not build. Other things are *not* marked as unsupported and yet are still not supported, meaning that they will build but crash at runtime.

This guide contains specific guidance on what to use and when.


## String matching

When writing a query predicate to perform string matching, always use `localizedStandardContains()` rather than trying to use `lowercased().contains()` or similar.

For example, this is correct:

```swift
@Query(filter: #Predicate<Movie> {
    $0.name.localizedStandardContains("titanic")
}) private var movies: [Movie]
```


## hasPrefix()

`hasPrefix()` and `hasSuffix()` are not supported in SwiftData predicates. If you want to use `hasPrefix()`, you should use `starts(with:)` instead, like this:

```swift
@Query(filter: #Predicate<Website> {
    $0.type.starts(with: "https://apple.com")
}) private var appleLinks: [Website]
```


## Unsupported predicates

Many common methods have no equivalent in SwiftData, and will not compile. For example, all these common operations are not supported:

- `String.hasSuffix()`
- `String.lowercased()`
- `Sequence.map()`
- `Sequence.reduce()`
- `Sequence.count(where:)`
- `Collection.first`

Custom operators are also not allowed.


## Captured custom value types

Do not compare custom value objects directly against captured constants in a
SwiftData predicate, even when the value type is `Codable`, `Hashable`, or a
small nested wrapper around a primitive. SwiftData can reject the predicate at
runtime because it cannot translate the captured custom value into a store
query.

For example, this model-level type is useful domain modeling:

```swift
@Model
final class Item {
    struct Identifier: Codable, Hashable {
        var rawValue: String
    }

    var id: Identifier
}
```

But this predicate is not safe:

```swift
let itemID = Item.Identifier(rawValue: "abc")

let predicate = #Predicate<Item> { item in
    item.id == itemID
}
```

It can fail with an error such as:

```text
Unsupported Predicate: Captured/constant values of type 'Identifier' are not supported
```

Keep the semantic API typed outside the query layer, then compare a
predicate-supported primitive member at the SwiftData boundary:

```swift
let rawItemID = itemID.rawValue

let predicate = #Predicate<Item> { item in
    item.id.rawValue == rawItemID
}
```

This member-access pattern is valid when `id` is a stored SwiftData property
and `rawValue` is a stored primitive value SwiftData can translate. If the typed
identifier is exposed through a computed property, `@Transient` property, or
other non-store-backed API, query the stored primitive backing column instead:

```swift
let rawItemID = itemID.rawValue

let predicate = #Predicate<Item> { item in
    item.identifier == rawItemID
}
```

The captured-value limitation is not specific to nested types. A top-level
custom struct has the same direct-comparison problem. Inline construction inside
the predicate is not a workaround either, because predicate macros do not
support arbitrary initializer calls.


## Dangerous predicates

Some SwiftData predicates will compile cleanly then fail or even crash at runtime.

For example, this is a valid predicate designed to show only movies that have a non-empty cast list:

```swift
@Query(filter: #Predicate<Movie> { !$0.cast.isEmpty }, sort: \Movie.name) private var movies: [Movie]
```

However, *this* query looks like it does the same thing, but will crash at runtime:

```swift
@Query(filter: #Predicate<Movie> { $0.cast.isEmpty == false }, sort: \Movie.name) private var movies: [Movie]
```

Never attempt to create query predicates that use computed properties or
`@Transient` properties. Avoid querying whole custom `Codable` values directly;
compare a stored primitive member or a stored primitive backing column instead.
Unsupported shapes might compile cleanly, but they can crash at runtime.

All predicates must rely on data that is actually stored in the database as `@Model` classes.

Never attempt to use regular expressions in predicates. They will compile cleanly then fail at runtime. So, this is *not* allowed:

```swift
@Query(filter: #Predicate<Movie> {
    $0.name.contains(/Titanic/)
}, sort: \Movie.name)
private var movies: [Movie]
```
