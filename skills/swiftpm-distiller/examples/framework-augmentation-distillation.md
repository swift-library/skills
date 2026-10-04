# Framework Augmentation Distillation

## Prompt Shape

Distill `/path/to/swift-data-writable` into a Swift collection skill-creation
handoff.

## Evidence To Prefer

- README and DocC quick starts: the host framework workflow being improved.
- Public macro/property-wrapper declarations: the package mechanism and
  supported attachment shapes.
- Runtime projection types and tests: supported operations, save behavior,
  diagnostics, and validation commands.
- Negative diagnostics: unsupported host surfaces and sibling skill handoffs.

## Expected Handoff Shape

```markdown
Package identity:
- Root: `/path/to/swift-data-writable`
- Package identity: `swift-data-writable`
- Host workflow improved: writable SwiftData `@Query` collection editing in
  SwiftUI.
- Package mechanism: SwiftDataWritable's `@Writable` macro generates a
  `$property` projection backed by `ModelContext`.

Evidence inspected:

| Evidence | Source/path | Used for | Notes |
|---|---|---|---|
| Manifest | `Package.swift` | macro/runtime targets and platforms | confirms SwiftPM shape |
| Docs | README, DocC quick starts | host workflow and intended usage | SwiftData query-editing examples |
| Source | macro declarations, runtime projection types | public capability claims | `@Writable` and projection API |
| Tests | macro/runtime/usage tests | supported operations and diagnostics | append/delete/save/reorder cases |
| Interface output | `Docs/Generated/SwiftDataWritable.md` | public declaration check | pre-existing generated artifact |

Generated interface evidence:
- Availability: available.
- Artifact source: `Docs/Generated/SwiftDataWritable.md`
- Command provenance: not produced during this session.
- Notes: use static source/tests if the generated artifact appears stale.

Commands:

| Command | Working directory | Exit code/status | Purpose | Notes |
|---|---|---|---|---|
| none | `/path/to/swift-data-writable` | not run | sample uses existing generated artifact | No commands were run. |

Public capabilities:

| Claim | Evidence source | Caveat / uncertainty |
|---|---|---|
| `@Writable` improves SwiftData `@Query` collection editing by exposing a mutable projection. | README quick start, macro declarations, runtime projection tests | Final author should preserve unsupported-shape diagnostics. |

Dependency and import mapping:

| Import/module | Target | Product | Package identity | Location | Resolved state | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| `SwiftDataWritable` | runtime target | `SwiftDataWritable` | `swift-data-writable` | local package root | local checkout | `Package.swift`, source layout | Public runtime import. |
| `SwiftData` | Apple SDK | Apple SDK | not applicable | Apple SDK | not applicable | README/source imports | Host framework, not a SwiftPM package dependency. |
| `SwiftSyntax` | macro support target | `SwiftSyntax` product | `swift-syntax` | manifest URL or registry | resolved pin if present | `Package.swift`, `Package.resolved` | Exact pin depends on resolved file availability. |

Candidate skill boundary:
- Candidate trigger when a SwiftData or SwiftUI/SwiftData task wants `@Query`
  collection add/delete/save/reorder ergonomics through `@Writable`.
- Also consider triggering when code imports `SwiftDataWritable` or references
  `WritableCollection`, `MutableWritableCollection`, or generated `$items`
  projections.
- Suggested non-goal: generic SwiftData schema/container/query work without
  `@Writable` or SwiftDataWritable evidence.
- Suggested non-goal: generic SwiftUI `List` editing after the writable query
  projection is no longer the issue.

Suggested supported tasks:
- Add `@Writable` to explicit SwiftData `@Query` array properties.
- Use generated `$property` projections for append, insert, remove, delete,
  save, and transaction writes.
- Integrate projections with SwiftUI `.onDelete` and `.onMove`.
- Choose autosave or explicit save behavior.
- Interpret SwiftDataWritable macro diagnostics.

Candidate trigger wording:
- Good: Use this skill when a SwiftData or SwiftUI/SwiftData task wants
  writable `@Query` collection ergonomics through SwiftDataWritable's
  `@Writable` macro.
- Bad: Use this skill for SwiftDataWritable package usage involving
  `WritableCollection` and generated projections.

Handoff notes for skill creator:
- Candidate `SKILL.md`: trigger boundary, host workflow, core projection
  workflows, diagnostics, validation.
- `references/diagnostics.md`: only if diagnostics grow beyond a compact list.
- `examples/`: only for short before/after SwiftUI query-editing snippets.
- Suggested validation commands: package macro tests, runtime tests, and a
  SwiftUI integration test if the final skill includes UI workflow examples.
- Open questions: confirm supported SwiftData platform/tools versions and exact
  behavior for autosave versus explicit save.
```

## Robustness Checks

- Does the trigger lead with the host workflow users will ask for?
- Are package symbols used as precision anchors instead of the main subject?
- Are generic host-framework tasks routed to sibling skills when the package is
  not the concrete mechanism?
- Does the skill avoid becoming a full package API manual?
