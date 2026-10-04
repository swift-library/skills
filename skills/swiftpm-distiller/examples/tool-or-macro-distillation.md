# Tool Or Macro Distillation

## Prompt Shape

Prepare a skill-creation handoff from `/path/to/swift-formatting-plugin`.

## Evidence To Prefer

- `Package.swift`: executable targets, plugins, macros, products, toolchain
  constraints, and command/plugin names.
- README/DocC: invocation commands, package-plugin setup, macro annotations,
  diagnostics, and generated output examples.
- Tests: diagnostic assertions, command output, plugin fixtures, expansion
  fixtures, or integration tests.
- Public source: macro declarations, command entrypoints, plugin permissions,
  and result-builder or DSL entrypoints.

## Expected Handoff Shape

```markdown
Package identity:
- Root: `/path/to/swift-formatting-plugin`
- Package surface type: CLI / plugin / macro / result-builder.
- Invocation surface:
- Package identity: `swift-formatting-plugin` (from manifest and resolved pin).

Evidence inspected:

| Evidence | Source/path | Used for | Notes |
|---|---|---|---|
| Manifest | `Package.swift` | tools, products, plugin/macro targets | includes command/plugin names |
| Docs | `README.md`, DocC | invocation and setup | command flags and macro annotations |
| Tests | `Tests/*` | diagnostics and output expectations | expansion and fixture checks |
| Interface output | `.distill/Interface/*.md` | public declarations | generated during session |
| Resolved deps | `Package.resolved` | SwiftSyntax pin | maps macro imports to package identity |

Generated interface evidence:
- Availability: generated.
- Command: `swift-interface-distiller generate --output-dir .distill/Interface`
- Working directory: `/path/to/swift-formatting-plugin`
- Exit code/status: 0
- Output path: `.distill/Interface`
- Notes: no missing public targets reported.

Commands:

| Command | Working directory | Exit code/status | Purpose | Notes |
|---|---|---|---|---|
| `swift-interface-distiller generate --output-dir .distill/Interface` | `/path/to/swift-formatting-plugin` | 0 | public interface evidence | output in `.distill/Interface` |

Public capabilities:

| Claim | Evidence source | Caveat / uncertainty |
|---|---|---|
| Package exposes a SwiftPM command plugin backed by an executable formatter tool. | `Package.swift`, generated interface output, README invocation docs | Exact supported flags should stay copied from README/tests. |

Dependency and import mapping:

| Import/module | Target | Product | Package identity | Location | Resolved state | Evidence | Notes |
|---|---|---|---|---|---|---|---|
| `SwiftFormattingPlugin` | `SwiftFormattingPlugin` | plugin product | `swift-formatting-plugin` | local package root | local checkout | `Package.swift` | Plugin entrypoint. |
| `SwiftSyntax` | external target/product | `SwiftSyntax` | `swift-syntax` | Git URL from manifest | version from `Package.resolved` | `Package.swift`, `Package.resolved` | Confirm exact product names from manifest before final authoring. |

Candidate skill boundary:
- Candidate trigger when the user asks to operate this tool or author code that
  uses its package-specific API.
- Suggested non-goals: generic Swift formatting, macro design, or package
  architecture review unless this package's API is the concrete subject.

Suggested supported tasks:
- Run the package tool with documented flags.
- Add the documented plugin or macro to a SwiftPM target.
- Interpret known diagnostics and generated output.

Suggested workflows:
- Confirm toolchain/platform constraints from `Package.swift`.
- Use README/test-backed command or annotation forms.
- Suggested validation commands: package documented command, `swift test`, or a
  fixture expansion test when present.

Handoff notes for skill creator:
- Candidate `SKILL.md`: trigger, invocation workflow, diagnostics, validation.
- `references/diagnostics.md`: only if diagnostics are numerous and stable.
- `examples/`: only for short command/macro before-after cases.
- `scripts/`: only if invocation requires repeatable wrapper logic.
- Open questions: final author should decide whether CLI, plugin, and macro
  surfaces belong in one skill or separate references.

Authoring handoff:
- Leave final `SKILL.md` and `agents/openai.yaml` shaping to the authoring
  workflow; keep this distillation focused on package-specific commands, APIs,
  diagnostics, and evidence.
```

## Robustness Checks

- Are CLI/plugin/macro surfaces separated instead of collapsed into one generic
  "library usage" section?
- Are commands and diagnostics copied from evidence, not invented?
- Is architecture review routed away unless package structure is the actual ask?
