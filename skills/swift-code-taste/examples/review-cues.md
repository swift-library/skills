# Swift Code Taste Review Cues

Use these as compact judgment examples, not as mandatory output.

## Flatten Thin Abstractions

- Smell: a small mode switch grows an engine enum, storage wrapper, and several
  factory helpers.
- Better shape: one public toggle, one internal state value, and one concrete
  factory.
- Why: the extra layers do not protect a boundary or reduce meaningful
  duplication.

## Make Abstractions Pay Rent

- Smell: a protocol, adapter, or helper only wraps one concrete type and forwards
  calls.
- Better shape: use the concrete type directly until the abstraction protects a
  contract, isolates a dependency, removes duplication, or names a real domain
  concept.
- Why: abstraction that does not buy boundary value is noise with a nicer name.

## Keep Public Namespaced Surface When It Owns A Domain

- Smell avoided: many package-specific modifiers or helpers are added directly
  to an Apple, Swift, or third-party owned public/package-facing type namespace
  such as `View`, `String`, `URL`, or `Data`.
- Better shape: expose one semantic namespace property, then keep the package's
  related modifiers or configuration under that namespace.
- Why: this abstraction earns its existence by protecting the host namespace,
  grouping a stable package-owned surface, and preserving fluent Swift-style
  call sites without scattering global symbols.
- Boundary: do this for a real family of package-owned APIs on an official or
  external host type. Do not namespace APIs on types the package already owns
  unless the namespace itself carries a real domain boundary. Do not add this
  ceremony for private or narrowly local helpers.

## Keep Public Surface Narrow

- Smell: internal strategy selection becomes a public type because it is easy
  to expose.
- Better shape: expose a small semantic command and keep strategy details
  internal.
- Why: public API should be a stable contract, not an implementation handle.

## Preserve The Real Owner

- Smell: a dispatcher, bridge, registry, cache, or renderer starts owning
  semantic state.
- Better shape: keep semantic state with the domain owner; let the adapter
  dispatch, translate, or publish.
- Why: boundary confusion is harder to repair than local boilerplate.

## Use Reference-Project Semantics Without Copying Shape

- Smell: local code claims reference-project parity because helper names look similar.
- Better shape: verify the reference project's interface, keep the semantic model, and narrow
  the local naming or hooks to the package's actual domain.
- Why: alignment is about behavior and vocabulary, not directory or helper
  cloning.

## Honor Explicit Scope Gates

- Smell: a docs-only, diagnosis-only, or no-public-API round grows source,
  package graph, behavior, or surface changes.
- Better shape: state the out-of-scope fix separately and keep the current
  patch inside the user's boundary.
- Why: uncontrolled widening is an architecture smell, not diligence.

## Diagnose Before Patch

- Smell: a weak patch lands because the visible behavior delta is hard to
  explain.
- Better shape: return to evidence, isolate the failure mode, then choose a
  clearer change or roll the weak patch back.
- Why: low-confidence fixes create stale code paths and hide the real boundary.

## Respect Authored API Philosophy

- Smell: a review rewrites a terse authored API into a more generic shape just
  because it looks unusual.
- Better shape: critique risks separately and preserve the public syntax unless
  the user approves the redesign.
- Why: intentional surface design is not boilerplate.

## Treat Code Elegance As Structure

- Smell: a review focuses on formatting while identity, reflection, route data,
  or erased views carry the real risk.
- Better shape: report the structural issue, its owner, and the smallest
  corrective shape.
- Why: clean Swift taste is about semantic shape before cosmetic polish.

## Remove Stale Compatibility Surface

- Smell: renamed APIs keep old aliases, forwarding wrappers, or migration
  shells after the final surface is chosen.
- Better shape: expose the final semantic name and delete stale public or
  package-visible leftovers unless migration compatibility is an explicit
  contract.
- Why: stale surface makes the package harder to audit and easier to misuse.
