# Google Swift Style Guide Reference

## Contents

- [Authority](#authority)
- [Source Files](#source-files)
- [Formatting Overlay](#formatting-overlay)
- [Construct-Level Checks](#construct-level-checks)
- [Naming And API Shape](#naming-and-api-shape)
- [Programming Practices](#programming-practices)
- [Documentation Comments](#documentation-comments)
- [Review Checklist](#review-checklist)

Use this when:

- The repository explicitly adopts Google Swift style.
- The user asks for Google Swift style guidance.
- Reviewing source-file structure, formatting, import layout, documentation
  comments, or stricter Swift style details not covered by the local baseline.

Skip this file if:

- The repository has no stated Google style adoption.
- The question is only API naming; start with
  `api-design-guidelines.md` instead.
- A formatter or linter already owns the mechanical decision.

## Authority

- Repository-local style, configured formatters, and explicit user
  instructions win.
- Treat Google Swift style as an optional overlay, not universal Swift truth.
- Do not create broad reformat-only diffs unless the user asked for formatting
  or the repository is already enforcing the same style.
- Apple API Design Guidelines remain the default API naming baseline; Google
  style incorporates them and adds stricter source layout and formatting rules.

## Source Files

- Name a file after the primary type it contains.
- For protocol-conformance extensions, prefer `Type+Protocol.swift`.
- Use UTF-8 source.
- Avoid tab indentation and unexpected invisible characters.
- Import exactly the modules a file needs; do not rely on transitive imports.
- Prefer whole-module imports unless an individual import avoids meaningful
  namespace pollution.
- Sort imports within their groups and keep test-only `@testable` imports in a
  separate group.
- A file usually has one primary top-level type, with exceptions for tightly
  related declarations.
- Keep member order logical and reviewable; use `// MARK:` for meaningful
  groups when it helps navigation.
- Keep overloads adjacent when they share the same base name in the same scope.

## Formatting Overlay

Use these only when Google style is the target:

- Use the repository's configured line length; Google style uses 100 columns.
- Use K&R-style braces for non-empty blocks.
- Do not use semicolons to terminate or separate statements.
- Keep at most one statement per line, except for simple single-statement
  blocks where local style accepts it.
- When a comma-delimited list wraps, orient it consistently: all on one line or
  one element per line.
- Avoid decorative horizontal alignment except for genuinely tabular data.
- Prefer a single blank line between members and logical statement groups.
- Do not wrap import statements.
- Avoid unnecessary parentheses around top-level `if`, `guard`, `while`, and
  `switch` conditions.

## Construct-Level Checks

- Use `//` for non-documentation comments, not block comments.
- Declare one `let` or `var` per statement, except tuple destructuring.
- Put `switch` cases at the same indentation level as the `switch`.
- Prefer one enum case per line when cases have associated values, raw values,
  or documentation needs.
- Use trailing closures only where the call-site remains clear.
- Use trailing commas only if local tooling and style accept them.
- Group long numeric literals with underscores when grouping communicates
  numeric meaning; do not group opaque identifiers.
- Put parameterized attributes such as `@available(...)` on their own lines.

## Naming And API Shape

- Use access control, not leading underscores, to hide implementation details.
- Prefer ASCII identifiers unless Unicode identifiers are meaningful in the
  domain and well understood by the team.
- Initializer parameters that map directly to stored properties should use the
  same names as those properties.
- Static or class properties returning the declaring type should not repeat the
  type name in the property name.
- Global constants use `lowerCamelCase`; avoid Hungarian-style prefixes.
- Delegate-style APIs should keep the source object as the first argument and
  follow established Cocoa/Swift call-site grammar.

## Programming Practices

- Treat warnings as work to resolve.
- Use `Optional` for expected absence or a single obvious failure state.
- Use typed errors when an operation has multiple meaningful failure cases.
- Avoid force unwraps, force casts, and `try!` unless the invariant is
  obvious; otherwise document the invariant close to the operation.
- Keep implicitly unwrapped optionals narrow; acceptable cases are typically
  UI lifecycle wiring, Objective-C nullability boundaries, or test fixtures.
- Prefer member-level access control in extensions over `public extension`.
- Use nested types or case-less enums for real namespacing relationships.
- Prefer `guard` for early exits that keep the main path flush-left.
- Prefer `for ... where` when filtering inside a loop body would only add a
  nested `if`.
- Avoid `fallthrough` unless it clearly expresses the intended control flow.
- Avoid custom operators unless the domain meaning is strong and readability is
  materially better than named functions.

## Documentation Comments

- Use triple-slash `///` documentation comments.
- Start with a concise summary that describes the declaration at the point of
  use.
- Document parameters, return values, and thrown errors when the summary does
  not fully explain them.
- Prefer Swift Markdown markup that works with Xcode and DocC.
- Document public and reusable declarations; avoid comments that merely repeat
  the declaration name or type.

## Review Checklist

- [ ] The repository actually wants Google Swift style for this code.
- [ ] The finding is not already owned by formatter/linter configuration.
- [ ] Local style was checked before applying this overlay.
- [ ] Suggested changes avoid reformat-only churn unless requested.
- [ ] API naming findings are reconciled with Apple API Design Guidelines.
