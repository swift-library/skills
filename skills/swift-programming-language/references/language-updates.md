# Swift Language Updates

Keep the project's supported toolchain, language mode, SDK and deployment
target separate. New syntax requires a compiler that parses it; a newer
compiler does not by itself authorize raising the minimum OS or enabling every
upcoming feature. The existing baseline in `rules/baseline.md` remains
conditional on project facts.

## Swift 6.3 / 6.4

- Swift 6.3 module selectors such as `Swift::Int` disambiguate a module from a
  same-named type. Use them for real ambiguity; existing unambiguous qualified
  names need no blanket rewrite.
- Swift 6.4 permits optional opaque and existential spellings such as
  `some Value?` and `any Value?`, equivalent to `(some Value)?` and
  `(any Value)?`. Keep the parenthesized forms for older compiler compatibility.
  Protocol compositions still need parentheses: `any (Value & Named)?` is
  valid, while `any Value & Named?` is rejected. See SE-0521 in the source map.
- Swift 6.4 supports `anyAppleOS` in availability declarations, for example
  `@available(anyAppleOS 27.0, *)`. Continue to check each API's platform
  exclusions; a shared availability spelling does not make every Apple API
  available on every platform.

## Source-level warning control

Swift 6.4 adds `@diagnose` (SE-0522) for a specific compiler warning group in a
declaration's signature and lexical scope. Read the actual diagnostic group
before choosing a control; the behavior identifiers are `error`, `warning`,
and `ignored`, without a leading dot:

```swift
@diagnose(DeprecatedDeclaration, as: warning,
          reason: "Retained compatibility bridge")
func bridgeToLegacySystem() {
  oldAPI()
}
```

Here `oldAPI()` represents an existing deprecated API. The attribute can make
its warning remain a warning even under `-warnings-as-errors`; unrelated
declarations keep their configured policy. Nested declarations can refine the
enclosing control. It cannot downgrade a genuine compilation error.

Keep the project's warning policy. Use local control for a justified exception,
not as a replacement for diagnosing the underlying problem. `reason:` is an
optional string literal, not interpolated text. Older compilers need their
existing supported diagnostic path; do not insert the new attribute
unconditionally.

Async cleanup, isolation and task cancellation changes, and Swift Testing
assertions, interoperability and test-runner behavior, are out of scope for this
reference. Session examples are leads until the current declaration
and a small compiler probe confirm the exact shape. In particular, do not
promote a `mapKeyedValues` spelling solely from a session mention when it cannot
be found in the selected standard library.

Use `official-sources.md` for source verification. Record compiler and runtime
results in the calling repository's evidence, not as a universal readiness
claim in this reference.
