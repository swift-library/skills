# Swift API Design Guidelines

Use this when:

- Designing or reviewing public, package-internal, or reusable Swift APIs.
- Renaming declarations, argument labels, parameters, protocols, overloads, or
  documentation comments.
- Checking whether call sites read clearly.

Skip this file if:

- The API surface is private implementation detail with strong local precedent.
- The framework or domain in use has more precise naming rules for the task.

## Core Priority

Clarity at the point of use is more important than brevity. Review declarations
and call sites together; do not judge names only where they are declared.

## Clear Usage

- Include all words needed to avoid ambiguity at the call site.
- Omit words that repeat type information without adding semantic value.
- Name variables, parameters, and associated types by role, not by type.
- Add role nouns for weakly typed values such as `Any`, `NSObject`, `String`,
  `Int`, and unconstrained generics.

```swift
employees.remove(at: index)       // position-based removal
allViews.remove(cancelButton)     // role is clear from argument
func restock(from supplier: WidgetFactory)
```

## Fluent Usage

- Prefer names that form readable phrases at use sites.
- Start factory methods with `make`.
- Side-effect-free APIs should read as noun phrases or queries.
- Side-effecting APIs should read as imperative verbs.
- Mutating/nonmutating pairs should follow Swift precedent:
  `sort` / `sorted`, `reverse` / `reversed`, `formUnion` / `union`.
- Boolean APIs should read as assertions: `isEmpty`, `contains(_:)`,
  `intersects(_:)`.

## Argument Labels

- Omit all labels only when arguments cannot be usefully distinguished.
- Omit the first label for value-preserving conversion initializers.
- If the first argument is part of a prepositional phrase, usually include the
  preposition in the label.
- If the first argument forms a grammatical phrase with the base name, omit the
  first label and move leading words into the base name.
- Label remaining arguments unless a specific guideline justifies omission.
- Keep labels on defaulted arguments and place defaulted parameters near the
  end when possible.

```swift
view.dismiss(animated: false)
words.split(maxSplits: 12)
x.insert(y, at: z)
```

## Documentation Comments

- Every public or reusable declaration should have a useful summary comment.
- Summaries should describe what a function does and returns, what a subscript
  accesses, what an initializer creates, or what a type/property is.
- Use Swift Markdown symbol markup where helpful: `Parameter`, `Returns`,
  `Throws`, `Note`, `Warning`, `SeeAlso`.
- If a computed property is not `O(1)`, document the complexity.
- If a declaration is hard to summarize clearly, consider redesigning the API.

## Terminology

- Prefer common words unless a term of art provides needed precision.
- Preserve established meanings for terms of art.
- Avoid nonstandard abbreviations.
- Follow domain precedent when it improves shared understanding.
- Use standard Swift casing: types and protocols in `UpperCamelCase`, other
  declarations in `lowerCamelCase`, with consistent acronym handling.

## Overloads And Weak Types

- Overloads should share semantics or operate in clearly distinct domains.
- Avoid overloads that differ only by return type.
- Avoid weakly typed overload sets where the call-site meaning collapses.
- Label tuple members and name closure parameters in public API surfaces.

## Review Checklist

- [ ] Call sites are clear without reading implementation.
- [ ] Names include semantic words and omit type-repeating words.
- [ ] Side effects match verb/noun naming.
- [ ] Mutating/nonmutating pairs follow Swift precedent.
- [ ] Argument labels follow grammar and conversion rules.
- [ ] Default parameters simplify common use without creating ambiguity.
- [ ] Documentation summaries are useful and precise.
- [ ] Non-`O(1)` computed properties document complexity.
- [ ] Overloads are not ambiguous for weakly typed values.
