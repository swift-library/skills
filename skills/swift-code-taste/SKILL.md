---
name: swift-code-taste
description: Use this skill when implementing, editing, refactoring, reviewing, or auditing Swift code where the user cares about Swift code taste, code elegance, code shape cleanliness, semantic naming, comment quality, abstraction quality, ownership boundaries, public API hygiene, semantic duplication, AI-shaped code, and Apple, Swift, and reference-project semantic alignment. Also use for questions like whether an abstraction earns its existence, whether code is too wrapped or only forwards calls, whether public/package-facing extensions pollute Apple/Swift/third-party type namespaces, or Chinese requests about 代码优雅, 抽象是否赚到存在, 不要为了抽象而抽象, 只包一层, or 代码味道. Do not use for SwiftPM target graph, product layout, or dependency direction alone; framework-specific API correctness; SwiftLint configuration; documentation structure; or generic style linting.
---

# Swift Code Taste

## Purpose

Apply the user's Swift engineering taste as an overlay while writing,
refactoring, or reviewing Swift code. The taste is:

> clean, direct, semantic, well-named, boundary-real, Apple/reference-aware,
> minimal, auditable Swift code.

This is not generic linting, generic architecture selection, planning, or
documentation structure. It is a code-shape and ownership-quality lens that can
combine with framework- or domain-specific guidance.

In this skill, a reference project is a codebase that the current project has
explicitly adopted as its semantic model. Do not treat every external
repository as a reference project.

## Taste Principles

- Local truth beats generic architecture. Preserve a repo's authored API
  philosophy unless the user approves a redesign.
- Keep one semantic owner. Renderers, registries, caches, indexes, and bridges
  may derive, dispatch, or adapt, but they should not become truth by accident.
- Public API is a contract, not a convenience. Expose only authored user
  surface, stable package concepts, real external consumption, or deliberate
  Apple, Swift, or reference-project parity.
- Explicit user scope gates are part of the design. Do not widen a review or
  refactor into Swift source, public API, package graph, or behavior changes
  the user excluded.
- Prefer direct concrete code until an abstraction proves boundary value.
  Future flexibility is not enough.
- Every abstraction must earn its existence by removing real complexity,
  protecting a real boundary, preserving a contract, or naming a stable
  semantic concept. A layer that only wraps and forwards is usually worse than
  direct code.
- Diagnose before patching when behavior is unclear. A low-visibility or weak
  patch should be replaced by evidence, rollback, or a clearer intervention.
- Reference-project alignment calibrates semantics; it does not require
  copying the reference project's directory shape, helper types, or implementation scaffolding.
- Final surface should not keep stale compatibility aliases, forwarding shells,
  or migration leftovers unless they are an explicit contract.
- Tests, examples, migration helpers, and host glue must not define production
  architecture.

## Canonical Change Shape

Treat conversation and review feedback as inputs to the edit. Before finalizing
Swift code, recompute the accepted design and make the implementation read as
if that design had been chosen directly.

Two editing paths that end at the same accepted design should produce
semantically equivalent active code, tests, configuration, examples, and
comments.

If an intermediate implementation contains `A + B` and the accepted result is
`A`, remove `B` together with its names, branches, wrappers, configuration,
tests, examples, and comments. Do not preserve the correction as `AWithoutB`,
an "intentionally no B" comment, or a permanent prohibition unless excluding
`B` is itself a current compatibility, safety, or architectural invariant.

Normalize by semantic identity and ownership, not by matching words. Removing a
current symbol or branch does not invalidate a distinct migration reader,
compatibility adapter, ownership boundary, or regression fixture that happens
to use the same domain term. Keep it only when its independent current role is
real, and name that role directly.

If a role-owned migration, compatibility, ownership, safety, or regression
artifact is already correct and the task does not change its facts, leave it
unchanged. Do not create diff noise by restating it merely because it is
relevant to the current edit.

A disabled flag, skipped test, dead branch, retained fixture, or "do not add"
rule created by the rejected implementation is still residue. Disabled state
alone does not make the artifact a compatibility, safety, ownership, or
regression invariant.

Pull requests and commits may explain the delta. Production code and comments
describe the current contract.

Add comments where a critical type, property, or method carries semantics that
names and types cannot express clearly. Useful comments define domain meaning,
units, valid ranges, identity, ownership, lifecycle, invariants, side effects,
failure semantics, or concurrency requirements. Public or package-facing APIs
with non-obvious contracts deserve documentation; obvious private code does not
need ceremonial comments.

Comments must be standalone and current. Do not restate names or types, narrate
prior implementations, quote review feedback, or explain that a discarded
approach is absent.

## Use When

- Implementing or refactoring Swift code where type, function, file, ownership,
  or public API shape is part of the work.
- Reviewing Swift code for dirty shape, weak naming, unnecessary wrappers,
  fake architecture, vague abstraction, semantic duplication, or AI-shaped
  scaffolding.
- Checking whether semantic truth, mutation, derived state, rendering, caching,
  indexing, host bridging, and public API ownership are in the right place.
- Checking whether custom Swift APIs align with Apple, SwiftLang, project-local,
  or adopted reference-project semantics.
- Reviewing public API surface cleanliness in Swift packages or app modules.

## When Not To Use

- SwiftPM target graphs, product layout, module dependency direction, package
  structure, or architecture briefs by themselves.
- SwiftUI or UIKit architecture pattern selection by itself.
- Framework/API correctness inside a focused Apple or Swift package domain.
- SwiftLint setup, rule governance, analyzer runs, or enforcement wiring.
- Repository documentation structure, README layering, or DocC placement.
- Broad Swift modernization or API guideline baseline work with no ownership or
  code-shape concern.

## Workflow

1. Read local truth first: user request, nearby code, `AGENTS.md`, `README.md`,
   `Package.swift`, project files, and architecture docs when present.
2. Honor explicit scope gates before forming fixes. If the user constrained the
   round to diagnosis, docs, no source edits, no public API changes, no package
   graph changes, or no behavior changes, keep recommendations inside that
   boundary.
3. Identify the review surface:
   - code shape and naming
   - architecture ownership and mutation boundaries
   - public API surface
   - semantic duplication
   - Apple, SwiftLang, project-local, or reference-project alignment
   - AI-shaped or generated-looking scaffolding
4. Prefer the local style that already has semantic weight. Do not force Clean
   Architecture, MVVM, VIPER, Redux, service layers, factories, coordinators,
   registries, or protocols by default.
5. For mutable Apple, Swift, Xcode, SDK, or package facts, verify against
   current official docs, local SDK/tool output, or verified package source
   before treating the fact as authoritative.
6. Report findings only when they have concrete evidence and a cleaner expected
   shape. Prefer deletion, narrowing, or direct concrete implementation when
   code does not earn its place.
7. Finish with a canonicalization sweep across code, comments, tests, examples,
   and configuration so rejected intermediate concepts leave no residual
   vocabulary or behavior.

Read `examples/review-cues.md` when applying this skill feels too abstract.
Read `examples/review-output.md` when a review needs a compact sample of the
expected output shape.

## Code Shape Rules

Ask whether every type, function, file, wrapper, helper, adapter, protocol,
extension, abstraction, and public symbol earns its existence.

For each abstraction, identify what it owns, protects, simplifies, or makes
harder to misuse. If the answer is only "it makes the design look layered" or
"it may be useful later", prefer deleting it or folding it into the caller.

When adding public or package-facing package-specific APIs to Apple, Swift, or
third-party owned types, check whether the package is polluting an official host
namespace. A semantic namespace can earn its existence when it groups a stable
family of package-owned modifiers or helpers; do not add a namespace just to
hide one thin forwarding method. For private or narrowly local helpers, prefer
direct, clear code over namespace ceremony.

Prefer code that is clean, direct, compact but not cryptic, semantic,
well-named, easy to audit, easy to delete, low-boilerplate, low-noise, and
hand-shaped rather than generated-looking.

Flag aggressively:

- verbose code with low information density
- repeated boilerplate or template-shaped implementation
- comments that restate obvious code
- comments, names, or tests that narrate a correction instead of expressing
  the current contract
- unnecessary wrappers or redundant forwarding methods
- single-use abstractions
- single-implementation protocols without boundary value
- types that only hold one trivial method
- weak type identity or files that do not earn their existence
- stale names, stale files, and stale compatibility surfaces
- public API noise
- complete-framework shapes around small capabilities

Do not automatically penalize direct implementation, concrete types,
fat-but-coherent domain models, explicit APIs, local specialized mechanisms,
lack of protocols, simple directory structure, or package-internal concrete
implementation when they are clean and semantic.

## Naming Rules

Treat vague names as suspicious unless local architecture gives them real
meaning:

- `Manager`
- `Helper`
- `Service`
- `Utility`
- `Engine`
- `Context`
- `Coordinator`
- `Provider`
- `Resolver`
- `Factory`
- `Registry`

Prefer names that express domain role, architectural role, stable package
concept, Swift/Apple semantic alignment, or concrete responsibility. A good
name explains what the type is, not merely that it manages, provides,
coordinates, or resolves something.

## Ownership Rules

Review architecture by asking:

- Who owns semantic truth?
- Who is allowed to mutate?
- Who only derives data?
- Who only indexes or caches?
- Who only renders?
- Who only bridges to host or external systems?
- What is the real source of authority?
- Is the boundary real, or only decorative?

Flag hard:

- renderer, registry, cache, index, or ViewModel becoming authoritative truth
- package/module dependency direction violations
- UI or host integration leaking into package core
- examples or tests influencing production architecture
- multiple places owning the same semantic concept
- fake layers where ownership remains unclear
- public API added only for tests or unstable implementation details

An abstraction is justified only when it protects a stable public API, isolates
an external dependency, supports multiple real implementations, enables
meaningful test substitution, represents a real boundary, encodes a stable
domain concept, or aligns with Apple, Swift, or reference-project semantics.

## Apple / Swift / Reference Project Alignment

Before approving a custom concept, ask:

- Does this resemble an Apple API, a SwiftLang package capability, a
  project-local concept, or an adopted reference-project contract?
- Does naming match the expected Swift or Apple semantic?
- Does behavior match platform expectations?
- Is this reinventing an official or already-adopted capability?
- If it diverges, is the divergence explicit and justified?

Prefer alignment in this order:

1. Semantic model.
2. Naming where appropriate.
3. Default behavior where appropriate.
4. Lifecycle boundaries where appropriate.
5. Public surface shape where appropriate.
6. Local package architecture cleanliness.

Do not blindly copy reference-project code. Extract the contract and keep the local shape
clean.

## Severity

- `Hard`: block or strongly reject semantic truth ownership violations,
  dependency direction violations, renderer/cache/registry truth ownership,
  unjustified public API expansion, duplicated official/project capability,
  production architecture polluted by tests/examples, large fake frameworks
  around small capabilities, or major Apple/Swift semantic mismatch.
- `Should`: fix vague names, unnecessary wrapper chains, single-use
  abstractions, single-implementation protocols without boundary value,
  semantic duplication, redundant forwarding, weak file/type identity,
  low-density comments, speculative hooks, or stale names.
- `Optional`: non-blocking local readability, minor naming, small duplication,
  or small organization cleanup.

## Output Format

For code review, use this shape:

```text
1. Architecture verdict
Pass / Soft fail / Hard fail

2. Findings
[Hard|Should|Optional] <Title>
Evidence:
- <file / symbol / behavior>
Why this is a smell:
- <code shape, ownership, abstraction value, public API hygiene, reference-project alignment, or AI-shaped smell>
Expected shape:
- <cleaner architecture/code shape>
Minimal fix:
- <smallest viable correction>

3. Public API surface impact
- Added public API:
- Removed public API:
- Public API concerns:

4. Code shape impact
- Unnecessary wrappers:
- Weak names:
- Semantic duplication:
- Stale leftovers:
- AI-shaped smell:

5. Swift / Apple / reference-project alignment
- Relevant reference-project or platform semantic:
- Alignment concern:
- Suggested correction:

6. Recommended next step
Merge / merge after cleanup / block until fixed.

7. Code diff (key hunks)
Show focused git-style unified diff hunks for the recommended fix when applicable.
```

For implementation or refactoring, apply the same rules silently while editing,
then summarize only the meaningful code-shape, ownership, public API, or
alignment choices.
