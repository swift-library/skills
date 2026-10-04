---
name: swiftpm-distiller
description: Distill known SwiftPM package or Swift library evidence into a normalized, evidence-backed handoff report for a separate skill-creation workflow. Use when asked to turn SwiftPM/library evidence into candidate skill boundaries, candidate triggers, suggested tasks, workflows, suggested validation commands, risks, uncertainty, or import/dependency mapping. Do not use for final SKILL.md authoring, final skill metadata, collection placement, package architecture review, dependency recommendation, generic docs migration, code rewrites, or non-Swift package analysis.
---

# SwiftPM Distiller

## Purpose

Turn a local SwiftPM package or Swift library source tree into a compact,
evidence-backed handoff report for a separate skill-creation workflow. The
report should explain what the package does, what evidence was inspected, what
public capabilities and dependencies were found, and which candidate skill
boundaries, triggers, tasks, workflows, suggested validation commands, risks,
and open questions should be handed to the skill creator.

## Positioning

- Primary job: inspect SwiftPM/library evidence, summarize package
  capabilities, identify public interface evidence, map imports and
  dependencies, and surface constraints, risks, and uncertainty.
- Advisory job: recommend candidate skill names, candidate triggers, candidate
  skill boundaries, suggested supported tasks, suggested non-goals, suggested
  workflows, suggested validation commands, and handoff notes for the skill
  creator. These recommendations are evidence-backed input, not final authoring.
- Project-local job: when the source is an in-repository SwiftPM package,
  distill package/module/path-scoped evidence and candidate operating guidance
  for a separate project-local skill authoring workflow.
- Not its job: review package architecture or produce architecture handoff
  briefs, recommend whether to adopt a dependency, normalize repository
  documentation structure, rewrite source, or produce a full repository
  evidence bundle.
- Skill creation boundary: final `SKILL.md` authoring, final metadata,
  repository or collection placement, marketplace/package conventions,
  cross-skill deduplication, collection-level validation, packaging conventions,
  and the final decision on whether a candidate capability should become a skill
  belong to the separate skill creator / authoring workflow.

## When To Use

- Known package distillation: the user provides a SwiftPM package, Swift
  library, local checkout, or library source tree and asks for new skill
  handoff material, an agent usage guide, or incremental evidence for an
  existing skill.
  This includes extracting tasks, entrypoints, public API flows, examples,
  constraints, validation commands, failure handling, candidate trigger
  boundaries, suggested non-goals, and handoff notes.
- Project-local package distillation: the request asks for skills for
  in-repository SwiftPM packages such as `Packages/*` or `*/Packages/*`. Use
  this skill to extract package-specific evidence, candidate triggers, and
  operating guidance for a separate project-local skill authoring workflow.
- Unfamiliar import distillation: the request starts from `import X`, a
  dependency module, or "what does X do?" Resolve the module to package and
  interface evidence first, then distill agent-operational guidance rather than
  guessing from the import name.

## When Not To Use

- Do not use for package target graphs, module-boundary review, composition-root
  review, or active/proactive architecture briefs.
- Do not use to decide whether a package should be adopted, wrapped, referenced,
  or replaced.
- Do not use for generic README summaries, DocC migration, governance docs, or
  repository documentation role cleanup.
- Do not use for final `SKILL.md` authoring, final skill metadata, repository or
  collection placement, marketplace/package conventions, cross-skill
  deduplication, collection-level validation, final skill adoption decisions, or
  non-Swift package analysis.

## Inputs To Inspect

- `Package.swift`, products, targets, plugins, macros, executable targets, and
  declared platform/toolchain constraints.
- `Package.resolved`, SwiftPM metadata, explicit checkout paths, `.build`
  checkouts, or Xcode `DerivedData/SourcePackages/checkouts` only when the
  package has to be resolved from an import/module name first.
- Compiler-derived interface evidence when available, such as
  `swift-interface-distiller` output or equivalent Swift symbol graph output.
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
2. If the request starts from an unfamiliar `import`, resolve module to package
   identity first using `Package.resolved`, SwiftPM metadata, or an explicit
   checkout. Do not infer package identity or behavior from the import name
   alone.
3. Inspect `Package.swift` first to identify products, modules, tools,
   platforms, plugins, macros, and test targets.
4. When available and cheap, generate or consult compiler-derived interface
   evidence before treating source text as the public API shape:
   `swift-interface-distiller generate --output-dir <scratch-dir>` or an
   equivalent symbol graph flow. Record the command, working directory, exit
   code/status, output path, and notable missing targets or failures.
5. Read public API and high-signal docs before implementation details.
6. Prefer examples, tests, DocC tutorials, and README quick starts as usage
   evidence; use source internals only to clarify missing behavior.
7. Synthesize candidate trigger semantics before listing APIs:
   - identify the host framework, tool, or user workflow the package improves;
   - phrase candidate triggers around that user-facing task or pain point first;
   - treat package names, imports, macros, types, and methods as evidence
     anchors, not as the default trigger subject;
   - when the package augments SwiftUI, SwiftData, UIKit, SwiftPM, or another
     host surface, make the host workflow explicit before package symbols.
8. Extract the candidate agent boundary:
   - candidate triggers and user phrasing,
   - suggested supported operations,
   - suggested non-goals and sibling skill handoffs,
   - required inputs and expected outputs.
9. Extract suggested operational guidance:
   - minimal correct setup and imports,
   - common workflows and API sequences,
   - suggested validation commands,
   - common diagnostics or failure modes,
   - version, platform, or toolchain constraints when evidenced.
10. Add handoff notes for the skill creator:
    - candidate `SKILL.md` scope and content split;
    - supporting files that may be useful, such as references, examples,
      templates, or scripts;
    - collection-placement constraints observed in local instructions;
    - cross-skill or final validation questions that remain outside this skill.
11. For project-local evidence, read the target project's placement policy when
    relevant and report it as context for the separate authoring workflow. Do
    not make the final placement decision in this distillation report.
12. If the user also wants actual skill files created or updated, produce the
    normalized handoff first, then use or route to the separate skill creator /
    authoring workflow for final file authoring and validation.
13. Produce the requested handoff without changing files unless the current user
    explicitly asks for edits outside the default distillation role.

## Evidence Layers

- Interface evidence: SwiftPM metadata and compiler symbol graph output. Use it
  to anchor public modules, public declarations, access levels, generated
  signatures, and symbol availability. `swift-interface-distiller` belongs in
  this layer.
- Intent evidence: README, DocC, Docs, tutorials, examples, tests, changelogs,
  and issue notes. Use it to recover workflows, good/bad usage, migration
  hazards, validation commands, diagnostics, and human guardrails.
- Source evidence: implementation details under `Sources/` and tests. Use it to
  resolve disagreements, verify behavior, and find edge cases not described by
  docs.

Do not collapse these layers. Interface tools should not read README, Docs,
DocC prose, or other human-authored guidance. This skill composes those
materials after the interface evidence is collected.

## Evidence Provenance

- Important claims in the handoff report must include the claim, evidence
  source, and any uncertainty or caveat.
- Record what was inspected, including `Package.swift`, `Package.resolved`,
  source tree layout, tests, docs, examples, existing generated artifacts, and
  generated interface output when available.
- Use generated interface evidence when available, including output from
  `swift-interface-distiller generate`.
- If generated interface evidence is produced during the session, record the
  exact command, working directory, exit code/status, relevant output path, and
  notable failures or missing targets.
- If generated interface evidence is unavailable, record the reason and rely on
  static package, source, docs, and test evidence while stating what remains
  uncertain.

## Dependency Interface Evidence

Use this mode when package evidence begins as an unfamiliar import or dependency
module in a host app:

1. Resolve the module to the package before reading or generating docs.
   Prefer `Package.resolved`, SwiftPM metadata, explicit checkout paths, or
   checked-out package `Package.swift` over name guessing.
2. Locate package source from a user-supplied root, `.build/checkouts`, or Xcode
   `DerivedData/SourcePackages/checkouts`. If using DerivedData, verify the host
   project has been built at least once before treating a missing checkout as a
   real absence.
3. Generate compiler-derived interface evidence into scratch or runtime storage.
   If caching is used, record package identity, version or revision, and the
   fact that generated interface evidence is staleable.
4. If a tool emits generated interface Markdown and README content in one
   artifact, split the provenance before distilling: generated declarations stay
   interface evidence; README or quick-start content stays intent evidence.
5. Use the evidence to answer what the dependency can do, then distill only the
   agent-operational parts into handoff material. Do not turn the whole
   generated API reference into a candidate skill handoff unless explicitly
   requested.

## Dependency And Import Mapping

Distinguish these names and locations in the handoff report; do not assume they
are identical:

- import module name;
- target name;
- product name;
- package display/name field in `Package.swift`;
- package identity;
- repository URL or registry location;
- `Package.resolved` pin identity;
- resolved version, branch, or revision;
- local path dependencies;
- renamed package identities;
- conditional or platform-specific dependencies.

When mapping imports to packages, include the evidence source and call out
ambiguous or unresolved mappings in plain language when evidence is incomplete.
Do not guess silently.

## Invocation Boundary

This skill does not self-initiate broad import scans or decide that dependency
evidence should be generated just because a Swift file contains external
imports. The request must provide a package, module, source root, import, or
existing skill update target before this skill begins distillation.

For project-local output, the target project's own `AGENTS.md` or local
instructions may define durable placement for evidence bundles, generated
interface evidence, skill candidates, or incremental update proposals. Read that
project-local policy when relevant and include it as handoff context. Final
durable placement and file creation belong to the separate skill creator /
authoring workflow.

The request context owns discovery breadth and report shape. This skill owns
package evidence distillation and the handoff report.

Distill dependency/import evidence when:

1. the current task is modifying or reviewing code that uses import/module `X`;
2. `X` is not the Swift standard library or Apple SDK. It may be an external
   dependency or a local package target when the current task needs local-target
   usage evidence;
3. no existing local skill or current evidence bundle already covers `X` well
   enough for the task;
4. `X` can be resolved through `Package.resolved`, SwiftPM metadata, local
   target metadata, or a checkout to a package identity, version, revision, or
   source root;
5. the agent is about to call, explain, modify, or review `X`'s API.

If these conditions are not satisfied, report the missing evidence or scope
mismatch instead of producing a speculative skill handoff. If only interface
evidence is missing, call the interface evidence backend first and stop at an
evidence bundle unless the request asks for a skill-creation handoff.

## Distillation Rules

- Treat local source and tests as highest authority for actual behavior.
- Treat README, DocC, and examples as highest authority for intended usage when
  they agree with source and tests.
- Treat compiler-derived interface evidence as the highest authority for public
  API shape when it is available and current.
- Do not use generated interface evidence as a substitute for human usage
  guidance; it cannot provide good design / bad design, anti-patterns,
  ownership boundaries, tradeoffs, migration hazards, or failure diagnosis by
  itself.
- For unfamiliar imports, generate or inspect dependency interface evidence
  instead of confidently explaining package APIs from symbol names or nearby
  call sites alone.
- Preserve executable knowledge: command sequences, required imports, setup
  steps, API ordering, diagnostics, edge cases, and known unsafe defaults.
- Preserve source-specific human guardrails. Code-related package distillation
  must not collapse into API lookup; keep good design / bad design, warning
  signs, anti-patterns, ownership decisions, tradeoffs, migration hazards,
  compatibility constraints, tests, validation commands, failure diagnosis, and
  useful code example shapes when package evidence provides them.
- Compress broad API surfaces into task-oriented workflows. Do not mirror a
  full API reference unless the user explicitly asks for one.
- Produce a self-contained suggested skill name. For Swift package/tool skill
  material, default to the package or tool slug plus `-patterns`, with official
  project casing in the display name when clear. If the target collection has a
  stricter naming contract, record it as a handoff constraint. Final collection
  placement, merge target, or adoption decision belongs to the separate
  authoring workflow.
- Do not let README installation sections, API catalogs, macro declarations, or
  symbol names become the trigger subject by default. Derive the trigger subject
  from the quick-start's underlying user intent, then add package/API symbols as
  precision anchors.
- For framework-augmentation packages, name the improved host workflow first
  and the package mechanism second. Example: "writable SwiftData `@Query`
  collection editing through `@Writable`" is better than "SwiftDataWritable
  package usage" when that is the evidenced user value.
- Do not invent support for platforms, products, APIs, or workflows not shown by
  package evidence.
- Treat host metadata such as `agents/openai.yaml` as handoff context, not final
  metadata authored by this skill.
- Keep the first pass handoff-only unless deterministic evidence tooling is
  clearly useful.
- Do not duplicate generic skill-authoring guidance inside the handoff. Include
  only package-specific operating knowledge and evidence that a separate author
  would not infer from generic skill authoring rules.

## Examples

Load files under `examples/` only when calibrating output shape, checking
whether a distillation is too generic, or deciding how to separate package
evidence from generic skill-authoring guidance.

- `examples/library-only-distillation.md`: compact library package calibration.
- `examples/tool-or-macro-distillation.md`: CLI, plugin, macro, or result-builder
  calibration.
- `examples/framework-augmentation-distillation.md`: package that improves a
  host framework workflow, where trigger wording must lead with the host task
  rather than the package's symbol list.

## Output Formats

For a default normalized handoff report, return these sections or equivalent
fields. Keep the report compact: use bullets for small packages, and use tables
when they make evidence, commands, dependencies, or ambiguity easier to scan.

1. Package identity: root path, `Package.swift` package name, package identity,
   location, tools version, and platform constraints when evidenced.
2. Evidence inspected, using compact bullets or this table shape when useful:

   | Evidence | Source/path | Used for | Notes |
   |---|---|---|---|
3. Generated interface evidence availability: available/generated/unavailable,
   output path if present, and reason if unavailable.
4. Commands run, unavailable, or skipped when relevant, using bullets or this
   table shape. If no commands were run, say so explicitly.

   | Command | Working directory | Exit code/status | Purpose | Notes |
   |---|---|---|---|---|

5. Products and targets: product names, target names, target types, test targets,
   executable/plugin/macro surfaces, and platform/toolchain constraints.
6. Public capabilities, including evidence and any uncertainty for important
   claims. Use this table shape only when it helps:

   | Claim | Evidence source | Caveat / uncertainty |
   |---|---|---|

7. Dependency and import mapping, or an explicit note when not applicable. Use a
   table for complex dependencies or ambiguous import mappings:

   | Import/module | Target | Product | Package identity | Location | Resolved state | Evidence | Notes |
   |---|---|---|---|---|---|---|---|

8. Candidate skill boundary: advisory scope and sibling-skill handoffs.
9. Candidate triggers: advisory trigger phrasing anchored in user workflows and
   package/API evidence.
10. Suggested supported tasks.
11. Suggested non-goals.
12. Suggested workflows and suggested validation commands.
13. Uncertainty and open questions for the skill creator.

When the request ultimately wants a skill created or updated, include handoff
notes for the skill creator instead of authoring final files:

1. candidate skill name and display-name evidence;
2. candidate `SKILL.md` sections and supporting-file ideas;
3. package-specific examples or references worth preserving;
4. `agents/openai.yaml` metadata hints when evidenced;
5. collection or project-local placement constraints found in local policy;
6. validation evidence and remaining open questions.

## Failure / Uncertainty Handling

- If `Package.swift` is missing, state that SwiftPM shape is inferred and avoid
  package-specific claims.
- If docs and tests disagree, prefer tests/source for behavior and flag the docs
  drift.
- If public API is too broad, distill around user-relevant tasks and list the
  omitted areas as evidence gaps.
- If module-to-package resolution fails, report the missing evidence path:
  absent `Package.resolved`, missing checkout, missing `Package.swift`, or no
  matching exported module. Do not guess the package from the import spelling.
- If an Xcode DerivedData checkout is expected but missing, treat it as host
  state first: verify the host project was built at least once and that
  `Package.resolved` plus `SourcePackages/checkouts` exist before concluding the
  package is unavailable.
- If interface generation fails, preserve the stderr/command, state whether the
  failure is tool availability, build artifacts, symbol graph generation, or
  package compilation, then fall back to source/docs and state what remains
  uncertain.
- If the package is mostly architecture or dependency-selection context, say
  that it is outside distillation scope instead of forcing a distillation.
- If the request is generic skill creation without SwiftPM source evidence, use
  the separate skill creator / authoring workflow instead of this skill.
