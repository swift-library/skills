---
name: swiftpm-distiller
description: SwiftPM package or Swift library distillation into a skill-authoring handoff with candidate triggers, API workflows, validation commands and risks. Resolve unfamiliar imports to their packages first. Not for final SKILL.md authoring or adoption decisions.
---

# SwiftPM Distiller

## Purpose And Boundary

Distill a local SwiftPM package or Swift library into a compact skill-authoring
handoff with cited sources: capabilities, dependencies, candidate names,
triggers, boundaries, tasks, workflows, validation commands, risks and open
questions. Recommendations are advisory; the request owns discovery breadth
and report shape.

Use for a known package, checkout or source tree, an agent usage guide,
incremental material for an existing skill, or project-local packages such as
`Packages/*` and `*/Packages/*`. For an unfamiliar `import X`, dependency module
or “what does X do?” request, resolve the package and public interface first.
The request must supply a package, module, source root, import or existing skill
update target; external imports alone do not authorize broad scans.

For dependency/import distillation during code work, require all of:

- the task modifies or reviews code using `X` and is about to call, explain,
  modify or review its API;
- `X` is outside the Swift standard library and Apple SDK; external dependencies
  and local package targets needing usage guidance qualify;
- no local skill or current report bundle covers `X` sufficiently;
- manifest, pin, SwiftPM/local-target metadata or checkout resolves `X` to a
  package identity, version, revision or source root.

Report missing inputs or scope mismatches instead of speculating. If only a
public interface is needed, use the interface collector and stop at its output
unless the request asks for a skill-creation handoff.

This skill does not own architecture review (target graphs, module boundaries,
composition roots or active/proactive briefs), adoption/wrapping/reference/
replacement decisions, generic README summaries, DocC migration, governance or
repository documentation cleanup, source rewriting, full repository report
bundles, or non-Swift analysis. Final `SKILL.md` and host metadata authoring,
repository/collection placement, marketplace and packaging conventions,
cross-skill deduplication, collection validation and skill adoption belong to
the separate authoring workflow. Produce the handoff first when final skill
files are requested, then route to that workflow. Keep the first pass
handoff-only unless deterministic collection tooling is useful; other file
edits require an explicit user request.

## Inputs, Layers And Provenance

Keep three layers distinct and apply their respective authority:

- **Public API:** `Package.swift`, SwiftPM metadata and current compiler-derived
  snapshots, rendered views or equivalent symbol graphs anchor modules,
  declarations, access levels, generated signatures and availability. Current
  compiler output is the highest authority for public API shape.
- **Docs, examples and tests:** `README*`, DocC, `Docs/`, `Documentation/`,
  tutorials, quick starts, sample apps, examples, tests, changelogs and issue
  notes supply intended workflows, good/bad usage, migration hazards,
  diagnostics, validation commands and human guardrails. README, DocC and
  examples govern intended usage when they agree with source and tests.
- **Source code:** public APIs and internals under `Sources/`, plus tests, are
  the highest authority for actual behavior, disagreements and undocumented
  edge cases. Inspect types, protocols, initializers, result builders, property
  wrappers, macros, commands and composition helpers; tests also expose command
  output, fixtures and validation expectations.

Interface tools collect declarations, not README, Docs, DocC prose or other
human-authored guidance. Compose those materials afterward. If a tool emits
interface Markdown and README content together, distinguish the generated
declarations from the README/quick-start provenance. A snapshot alone cannot
supply design judgment, ownership, tradeoffs, migration hazards or diagnosis.

Record inspected manifests, pins, source layout, docs, tests, examples, existing
generated artifacts and interface output. Keep canonical snapshots and rendered
views distinct, carrying configuration, scope and collection gaps with every
selected view; command success does not establish complete API coverage. For
generated output record exact commands, working directories, exit codes/status,
paths, failures and missing targets. Keep outputs in the target's ignored
producer directory. Cached snapshots need package identity, version/revision
and a staleness caveat. If unavailable, record why, use static manifests,
source, docs and tests, and state remaining uncertainty. Every important claim
needs supporting evidence and a caveat where applicable.

## Workflow

1. Confirm a SwiftPM package or Swift library source tree. Inspect
   `Package.swift` first for products, modules, tools, platforms, plugins,
   macros, executables, tests and toolchain constraints.
2. For unfamiliar imports, resolve identity before reading or generating docs:
   inspect `Package.resolved`, SwiftPM/local-target metadata, explicit checkouts
   or the checked-out manifest. Locate source in the supplied root,
   `.build/checkouts` or Xcode `DerivedData/SourcePackages/checkouts`. Do not
   infer identity or behavior from import spelling or nearby call sites.
3. When available and cheap, generate or consult a compiler-derived API
   snapshot before treating source text as public API shape. Use
   `interface-distiller collect package`, `render` to read the interface, and
   `query` to select declarations. Use `swift-interface-distiller-patterns`
   for installation, configuration, scope, budgets and completeness. Check
   expected/collected modules and gaps; support executable/plugin behavior
   with manifest, docs and tests rather than library declarations alone.
4. Read public APIs and high-signal docs before internals. Prefer examples,
   tests, DocC tutorials and README quick starts for usage; consult internals
   to clarify missing behavior. Read `AGENTS.md`, contribution notes, scripts
   and CI commands when they affect library operation. For project-local
   packages, report local placement policy for report bundles, API snapshots,
   skill candidates and incremental proposals as authoring context.
5. Derive candidate triggers before listing APIs: name the host framework,
   tool, workflow or pain point improved, then package names, imports, macros,
   types and methods as precision anchors. Use the quick-start's user intent,
   not installation prose or API catalogs, as the subject. For augmentation
   packages, lead with the host workflow (SwiftUI, SwiftData, UIKit, SwiftPM,
   etc.): “writable SwiftData `@Query` collection editing through `@Writable`”
   rather than “SwiftDataWritable package usage,” when supported by the sources.
6. Extract candidate user phrasing, supported operations, non-goals, sibling
   handoffs, required inputs and expected outputs. Suggest correct setup and
   imports, API sequences, workflows, validation commands, diagnostics,
   failure modes and verified version/platform/toolchain constraints.
7. Recommend a self-contained skill name: package/tool slug plus `-patterns`,
   with official project casing for the display name when clear. Report any
   stricter collection naming contract as a constraint. Add candidate
   `SKILL.md` scope/content split, useful references/examples/templates/scripts,
   supported `agents/openai.yaml` hints, local placement constraints and final
   validation or cross-skill questions for the author.

## Dependency And Import Mapping

Distinguish import module, target, product, `Package.swift` display/name field,
package identity, repository URL/registry location, `Package.resolved` pin
identity, resolved version/branch/revision, local path dependencies, renamed
identities and conditional/platform-specific dependencies. Do not assume these
names coincide. Cite the source for each mapping and flag ambiguous or
unresolved mappings explicitly.

## Distillation Rules

- Preserve executable knowledge: commands, imports, setup, API ordering,
  diagnostics, edge cases and unsafe defaults.
- Preserve source-specific human guardrails: good/bad design, warning signs,
  anti-patterns, ownership decisions, tradeoffs, migration hazards,
  compatibility constraints, tests, validation commands, failure diagnosis
  and useful code-example shapes.
- Compress broad API surfaces into user-relevant operational workflows;
  include a full API reference only when explicitly requested. Include only
  package-specific knowledge an author would not infer from generic
  skill-authoring guidance.
- Do not invent support for platforms, products, APIs or workflows absent from
  the inspected sources.

## Examples

Use these only to calibrate output shape, specificity and the separation of
package knowledge from generic skill authoring:

- `examples/library-only-distillation.md`: compact library handoff.
- `examples/tool-or-macro-distillation.md`: CLI/plugin/macro/result-builder
  surfaces.
- `examples/framework-augmentation-distillation.md`: host-workflow-first
  triggers.

## Output Formats

Return these sections or equivalent fields. Use compact bullets for small
packages and tables when sources, commands, dependencies or ambiguity benefit.

1. Package identity: root path, `Package.swift` package name, package identity,
   location, tools version and verified platform constraints.
2. Inspected materials, as bullets or:

   | Material | Source/path | Used for | Notes |
   |---|---|---|---|

3. API snapshot availability: available/generated/unavailable, output path if
   present and reason if unavailable.
4. Commands run, unavailable or skipped. Explicitly say if none were run. Use
   bullets or:

   | Command | Working directory | Exit code/status | Purpose | Notes |
   |---|---|---|---|---|

5. Products and targets: names, target types, test targets,
   executable/plugin/macro surfaces and platform/toolchain constraints.
6. Public capabilities with supporting evidence and uncertainty for important
   claims, optionally:

   | Claim | Evidence source | Caveat / uncertainty |
   |---|---|---|

7. Dependency/import mapping, or an explicit not-applicable note. For complex
   or ambiguous mappings:

   | Import/module | Target | Product | Package identity | Location | Resolved state | Evidence | Notes |
   |---|---|---|---|---|---|---|---|

8. Candidate skill boundary: advisory scope and sibling-skill handoffs.
9. Candidate triggers: advisory phrasing anchored in user workflows and
   supported package/API capabilities.
10. Suggested supported tasks.
11. Suggested non-goals.
12. Suggested workflows and validation commands.
13. Uncertainty and open questions for the skill creator.

For skill creation/update requests, include authoring handoff notes:

1. candidate skill name and sources supporting the display name;
2. candidate `SKILL.md` sections and supporting-file ideas;
3. package-specific examples or references worth preserving;
4. supported `agents/openai.yaml` metadata hints;
5. collection/project-local placement constraints found in local policy;
6. check results and remaining open questions.

## Failure / Uncertainty Handling

- Missing `Package.swift`: state that SwiftPM shape is inferred; avoid
  package-specific claims.
- Docs/tests disagreement: prefer tests/source for behavior and flag docs drift.
- Excessively broad API: focus on user-relevant tasks and list omitted areas
  as coverage gaps.
- Failed module resolution: identify absent `Package.resolved`, missing
  checkout/manifest or no matching exported module; never guess from spelling.
- Missing Xcode DerivedData checkout: verify the host project was built at
  least once and check `Package.resolved` and `SourcePackages/checkouts` before
  concluding the package is unavailable.
- Failed interface generation: preserve stderr and command; classify tool
  availability, build artifacts, symbol graph generation or package compilation
  failures, then fall back to source/docs and state uncertainty.
- Architecture or dependency-selection requests: report the scope mismatch.
  Generic skill creation without SwiftPM source belongs to the authoring
  workflow.
