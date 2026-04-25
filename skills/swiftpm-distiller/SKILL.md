---
name: swiftpm-distiller
description: Distill a SwiftPM package or Swift library source into agent-operational skill material, including trigger contracts, supported tasks, API usage workflows, minimal examples, validation commands, failure modes, and SKILL.md versus references/examples/scripts placement. Use when asked to turn a Swift library into a skill, make agent usage guidance from a package, extract workflows or API usage from SwiftPM source, or generate/update skill material from library evidence. Do not use for package architecture review, dependency recommendation, generic docs migration, code rewrites, or non-Swift package distillation.
---

# SwiftPM Distiller

## Purpose

Turn a local SwiftPM package or Swift library source tree into skill-ready
agent guidance. The output should teach an agent when to use the library, how to
use it correctly, what not to use it for, and how to validate work that depends
on it.

## Positioning

- Primary job: extract agent-operational knowledge from package evidence:
  trigger boundary, supported tasks, non-goals, key APIs, workflows, examples,
  validation commands, and failure modes.
- Skill-authoring job: recommend or draft the `SKILL.md` body and optional
  `references/`, `examples/`, `templates/`, or `scripts/` placement when the
  user asks to create or update a skill.
- Not its job: review package architecture, recommend whether to adopt a
  dependency, normalize repository documentation, rewrite source, or produce a
  full repository evidence bundle.
- Neighboring skills: use `swiftpm-architecture` for architecture review or
  handoff briefs, `swiftpm-index` for dependency/candidate decisions, and
  `swiftpm-docs` for repository documentation structure.

## When To Use

- The user asks to distill a SwiftPM package, Swift library, local checkout, or
  library source tree into a skill or agent usage guide.
- The task is to extract how an agent should use a library: tasks, entrypoints,
  public API flows, examples, constraints, validation commands, or failure
  handling.
- The requested output is skill material, a skill skeleton, a skill update plan,
  or a concise distillation report for later skill authoring.

## When Not To Use

- Do not use for package target graphs, module-boundary review, composition-root
  review, or active/proactive architecture briefs.
- Do not use to decide whether a package should be adopted, wrapped, referenced,
  or replaced.
- Do not use for generic README summaries, DocC migration, governance docs, or
  repository documentation role cleanup.
- Do not use for non-Swift packages unless the user explicitly asks for a Swift
  collection skill that wraps a non-Swift tool used by Swift workflows.

## Inputs To Inspect

- `Package.swift`, products, targets, plugins, macros, executable targets, and
  declared platform/toolchain constraints.
- Public API source under `Sources/`, especially public types, protocols,
  initializers, result builders, property wrappers, macros, commands, and
  composition helpers.
- `README*`, DocC catalogs, `Docs/`, `Documentation/`, examples, sample apps,
  tutorials, and quick-start sections.
- Tests that demonstrate real usage, edge cases, diagnostics, command output,
  fixtures, or validation expectations.
- Existing `AGENTS.md`, contribution notes, scripts, or CI commands only when
  they affect how an agent should operate the library.

## Workflow

1. Confirm the target is a SwiftPM package or Swift library source tree.
2. Inspect `Package.swift` first to identify products, modules, tools,
   platforms, plugins, macros, and test targets.
3. Read public API and high-signal docs before implementation details.
4. Prefer examples, tests, DocC tutorials, and README quick starts as usage
   evidence; use source internals only to clarify missing behavior.
5. Extract the agent boundary:
   - trigger conditions and user phrasing,
   - supported operations,
   - explicit non-goals and sibling skill handoffs,
   - required inputs and expected outputs.
6. Extract operational guidance:
   - minimal correct setup and imports,
   - common workflows and API sequences,
   - validation commands,
   - common diagnostics or failure modes,
   - version, platform, or toolchain constraints when evidenced.
7. Decide material placement:
   - keep concise trigger, workflow, validation, and output rules in
     `SKILL.md`;
   - move long API catalogs, extended examples, troubleshooting matrices, or
     source-derived references into optional supporting files;
   - add scripts only for deterministic repeated operations, not for one-off
     scanning.
8. Produce the requested output without changing files unless the user asks to
   create or update the skill.

## Distillation Rules

- Treat local source and tests as highest authority for actual behavior.
- Treat README, DocC, and examples as highest authority for intended usage when
  they agree with source and tests.
- Preserve executable knowledge: command sequences, required imports, setup
  steps, API ordering, diagnostics, edge cases, and known unsafe defaults.
- Compress broad API surfaces into task-oriented workflows. Do not mirror a
  full API reference unless the user explicitly asks for one.
- Do not invent support for platforms, products, APIs, or workflows not shown by
  package evidence.
- Keep host metadata such as `agents/openai.yaml` secondary to `SKILL.md`.
- Keep the first pass documentation-only unless deterministic tooling is clearly
  necessary.

## Output Formats

For a default distillation report, return:

1. Package summary
2. Recommended skill boundary
3. Supported tasks
4. Non-goals and handoffs
5. Core usage workflows
6. Validation commands
7. Failure modes / constraints
8. Recommended skill file layout
9. Open questions or evidence gaps

When asked to create or update a skill, return or edit material with:

1. `SKILL.md` frontmatter description
2. `SKILL.md` body structure
3. Optional supporting-file placement
4. `agents/openai.yaml` values when needed
5. Validation checklist

## Failure / Uncertainty Handling

- If `Package.swift` is missing, state that SwiftPM shape is inferred and avoid
  package-specific claims.
- If docs and tests disagree, prefer tests/source for behavior and flag the docs
  drift.
- If public API is too broad, distill around user-relevant tasks and list the
  omitted areas as evidence gaps.
- If the package is mostly architecture or dependency-selection context, route
  to the neighboring skill instead of forcing a distillation.
