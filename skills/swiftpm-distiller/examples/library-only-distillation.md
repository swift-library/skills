# Library-Only Distillation

## Prompt Shape

Distill `/path/to/swift-validation` into a skill-creation handoff.

## Evidence To Prefer

- `Package.swift`: products, target names, platforms, test targets.
- `README.md` and DocC quick starts: intended imports and common flows.
- Public types in `Sources/`: builders, validators, errors, result models.
- Tests: real call sequences and edge cases.

## Expected Handoff Shape

```markdown
Package identity:
- Root: `/path/to/swift-validation`
- Package name: `SwiftValidation`
- Package identity: `swift-validation` (inferred from local root and manifest)
- Products and targets: `SwiftValidation` library product, `SwiftValidation`
  target, `SwiftValidationTests` test target.

Evidence inspected:

| Evidence | Source/path | Used for | Notes |
|---|---|---|---|
| Manifest | `Package.swift` | products, targets, platforms | tools version and target list |
| Docs | `README.md` | intended workflows | quick-start API sequence |
| Source layout | `Sources/SwiftValidation` | public capabilities | validators and result types |
| Tests | `Tests/SwiftValidationTests` | usage and edge cases | invalid input cases |
| Resolved deps | `Package.resolved` | dependency pins | file not present; no external pins found |
| Interface output | `swift-interface-distiller` | public API shape | not generated in this sample |

Generated interface evidence:
- Availability: unavailable.
- Reason: not generated for this lightweight sample; static source/docs/tests
  evidence is enough for this candidate handoff.

Commands:

| Command | Working directory | Exit code/status | Purpose | Notes |
|---|---|---|---|---|
| none | `/path/to/swift-validation` | not run | sample stays static | No commands were run. |

Public capabilities:

| Claim | Evidence source | Caveat / uncertainty |
|---|---|---|
| Package supports model validation workflows with structured failures. | README quick start, `Sources/SwiftValidation`, validation tests | Exact API names should be confirmed if interface output is later generated. |

Dependency and import mapping:

| Import/module | Target | Product | Package identity | Location | Resolved state | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| `SwiftValidation` | `SwiftValidation` | `SwiftValidation` | `swift-validation` | local package root | not applicable | `Package.swift`, source layout | Local package; no external dependency mapping needed. |

Candidate skill boundary:
- Candidate trigger when code adds validation rules, handles validation results,
  or tests invalid input with this package.
- Suggested non-goals: generic form validation UX, unrelated model-layer design,
  or validation libraries not backed by this package evidence.
- Neighbor handoffs: broader Swift architecture or interface copy work once the
  issue leaves this package's API.

Suggested supported tasks:
- Add validation rules to a model.
- Parse validation failures into user-facing diagnostics.
- Write tests around invalid input cases.

Suggested workflows:
- Import the product module.
- Build a validator with the public builder/API shown in README/tests.
- Run validation and handle the documented result/error type.
- Suggested validation commands: package tests or the target repo tests that
  exercise the package integration.

Handoff notes for skill creator:
- Candidate `SKILL.md`: trigger, workflow, validation, failure handling.
- `references/api-workflows.md`: only if the package has multiple independent
  validation workflows.
- `examples/`: only for compact before/after snippets.
- Open questions: confirm exact public API names with generated interface output
  if the final skill will quote declarations.

Authoring handoff:
- Keep generic skill anatomy in the authoring workflow; this distillation
  contributes only package-specific evidence and workflows.
```

## Robustness Checks

- Does every workflow cite package evidence instead of inferred API behavior?
- Are generic skill-writing rules kept out of the handoff?
- Are unsupported package surfaces listed as evidence gaps instead of invented?
