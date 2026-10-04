# Skill Authoring Architecture

This document defines the collection-level structure expected for skills in
this repository. It is the primary architecture reference for skill shape,
progressive disclosure, and trigger precision.

## Purpose

Skills should be cheap to discover, precise to trigger, and deep only after
selection. A skill must let Codex or Claude decide whether to use it from a
small trigger contract, then load only the workflow, rules, knowledge,
references, templates, or scripts needed for the current task.

## Ownership Model

- `AGENTS.md` routes work inside this repository and records durable operating
  notes. It should not duplicate full skill logic.
- `README.md` indexes the collection, available skills, and installation paths.
- `Documentation/Architecture/*` owns collection-level skill design rules.
- `skills/*/SKILL.md` owns the boundary, trigger contract, workflow, validation
  rules, and output format for one skill.
- `skills/*/rules/` owns stable skill-local invariants and decision rules.
- `skills/*/knowledge/` owns curated domain knowledge used by the skill.
- `skills/*/references/` owns long-form source material or topic depth that
  should not live in `SKILL.md`.
- `skills/*/profiles/` owns named composition variants when a skill emits or
  evaluates multiple output shapes.
- `skills/*/examples/` owns small examples and expected output samples.
- `skills/*/templates/` and `skills/*/assets/` own reusable output shapes,
  snippets, schemas, or fixtures.
- `skills/*/scripts/` owns internal deterministic helpers.
- `skills/*/cli/` owns a user-facing command surface when the skill provides
  one.
- `skills/*/agents/` is optional interface metadata for agent hosts. It is not
  the authoritative trigger or workflow source.
- `.claude-plugin/marketplace.json` is the Claude marketplace discovery
  registry for this collection. Each entry's `source` is `./skills/<name>`, so
  the plugin root is the skill folder and the plugin loads that one skill. A
  source at the repository root would make Claude Code scan the whole
  `skills/` directory for every plugin. Because the plugin root is the skill
  folder, a skill must not contain the plugin component locations
  `commands/`, `hooks/`, `output-styles/`, `.mcp.json`, or Markdown files in
  `agents/`.

## Directory Shape

Every skill must have:

```text
skills/<skill>/
└── SKILL.md
```

Published skills should also have:

```text
skills/<skill>/
└── agents/
    └── openai.yaml
```

Use optional layers only when they have real content:

```text
skills/<skill>/
├── rules/
├── knowledge/
├── references/
├── profiles/
├── templates/
├── assets/
├── examples/
├── scripts/
└── cli/
```

Do not create empty directories just to make every skill look identical. A
small skill with only `SKILL.md` and `agents/openai.yaml` is valid when the
workflow does not need deeper material.

When an optional layer exists, it should include a local index unless the layer
has only one self-explanatory file:

- Use `README.md` for structural layers such as `rules/`, `profiles/`,
  `templates/`, `examples/`, `scripts/`, or `cli/`.
- Use `_index.md` for topic catalogs under `references/`.
- Use `README.md` or an obvious catalog file for `knowledge/`.

## Skill Categories

Classify a skill first by its primary trigger and output, not only by
technology name. Use these primary categories to decide whether a capability
deserves a separate skill or belongs inside an existing skill.

`Automation-Backed` is a secondary tag, not a mutually exclusive category. A
skill can be both `Package Analysis` and `Automation-Backed`, or both `Domain
Pattern` and `Automation-Backed`.

### Repository Structure Skills

Use for repository-level scaffolding, documentation architecture, governance,
or layout normalization.

Expected traits:

- triggers on repository shape or documentation placement
- edits docs, templates, indexes, or governance files
- produces audits, normalized files, or scaffold output

Example: `swiftpm-docs`.

### Package Analysis Skills

Use for package-level evaluation where the output is a judgment, report,
candidate map, or evidence bundle.

Expected traits:

- inspects `Package.swift`, source, tests, docs, or local workspace context
- compares alternatives or ranks evidence
- produces an audit, recommendation, or review artifact

Examples: `swiftpm-index`, `swiftpm-architecture`.

### Domain Pattern Skills

Use for implementation and review guidance in a focused Swift or
Apple-platform domain.

Expected traits:

- triggers on code shape, diagnostics, API usage, or framework-specific work
- uses progressive disclosure into topic references
- produces implementation guidance, review findings, or small code changes
- prefers one framework or tightly bounded platform domain per skill

Examples: `swift-concurrency-patterns`, `swift-testings-patterns`,
`core-data-patterns`, and `swiftui-patterns`.

Default split rule: prefer one Apple / Swift framework or tightly bounded
platform domain per `Domain Pattern` skill. For example, SwiftUI, SwiftData,
Core Data, Swift Testing, and Swift Concurrency should remain separate because
their triggers, diagnostics, references, and safe implementation rules differ.

Merge framework topics only when their triggers and workflow are effectively
the same, or when the topic is too small to justify independent progressive
disclosure. In that case, keep it as a reference file inside the nearest
specific skill rather than creating a new top-level skill.

### Baseline Pattern Skills

Use for broad, lightweight review across Swift or Apple-platform code when a
deep domain skill is not warranted.

Expected traits:

- catches obvious outdated patterns or unsafe defaults
- routes deep work to a more specific skill
- should stay intentionally shallow

Example: `swift-programming-language`.

### Automation-Backed Skills

Use as a secondary classification when a skill has a stable mechanical step
worth exposing through `scripts/` or `cli/`.

Expected traits:

- automation supports scanning, fetching, rendering, validation, or export
- high-level judgment remains in `SKILL.md` and rules
- generated runtime output is not silently promoted to curated truth

Examples:

- `swiftpm-index`: Package Analysis + Automation-Backed.
- `swiftpm-architecture`: Package Analysis + Automation-Backed.
- `swiftui-patterns`: Domain Pattern + Automation-Backed.

## Split / Merge Rules

Create a separate skill when:

- the trigger can be stated precisely without relying on another skill
- the workflow, validation rules, or output format differs materially
- the skill needs its own references, knowledge, scripts, CLI, or templates
- using the capability automatically would be useful and low-noise

Do not create a separate skill when:

- the content is only a small topic reference inside an existing workflow
- the trigger would overlap heavily with an existing skill
- the new skill would mostly duplicate another skill's `SKILL.md`
- the capability is a one-off checklist without stable reuse

When two skills could trigger, route to the more specific one first. Keep
baseline skills shallow and make them hand off to domain skills for deep work.

## Naming Rules

Use lowercase kebab-case for skill names and directories.

Prefer names that combine platform/domain and a stable concern:

- `swiftpm-docs`
- `swiftpm-index`
- `swiftpm-architecture`
- `swift-concurrency-patterns`
- `swiftui-design`
- `widgetkit-design`

Use concern suffixes consistently:

- `*-patterns`: framework, API, Swift package, or tool usage patterns and
  implementation practice. These skills answer "how should this technology be
  used in code?" and cover correctness, API choices, idioms, migration,
  debugging, review, and refactoring within that domain.
- `*-design`: visual design, interaction quality, information hierarchy, and
  platform-native feel. These skills answer "does this interface or experience
  look and behave right for the platform?"
- `*-performance`: source-level performance concern for a specific framework or
  platform surface. These skills answer "will this code update, render, allocate,
  or scale efficiently?" and cover implementation guidance, review, diagnosis,
  remediation, and measurement handoff.
- Other concern names should describe the durable output or domain, such as
  `docs`, `index`, `architecture`, `instruments`, or `writing`.

Do not force every skill into `*-patterns`. Use `*-patterns` for code-facing
framework/API practice or concrete Swift package/tool practice. Use a direct
domain name when the skill's work is not primarily implementation patterns,
such as `interface-writing` for text shown inside product interfaces.

For concrete Swift package/tool skills, use the package/tool slug plus
`-patterns` for the directory and `SKILL.md` name. The display name should use
the project's official casing plus `Patterns` when official casing is clear.

Examples:

- `mlx-swift-patterns` with display name `MLX Swift Patterns`.
- `swiftlint-patterns` with display name `SwiftLint Patterns`.
- `swift-argument-parser-patterns` with display name
  `Swift Argument Parser Patterns`.

Use operation words such as `review`, `refactor`, `debug`, `migrate`, and
`implement` in `description`, `Workflow`, or `Output Format` for ordinary
domain skills. Avoid making a review or refactor mode the skill name when the
same knowledge system also applies during new work.

Avoid names that are too broad or ambiguous:

- `swift-helper`
- `docs`
- `review`
- `package-index` without the SwiftPM or official scope
- `swiftui-refactor` when the real concern is SwiftUI usage patterns
- review-suffixed SwiftUI performance names when the real concern is SwiftUI
  performance

The display name in `agents/openai.yaml` may be friendlier, but it must match
the same concept as the `SKILL.md` name and marketplace entry.

## Progressive Disclosure

Use this layer model:

1. Discovery layer: `name`, `description`, and skill path. This layer decides
   whether the skill should be selected.
2. Routing / workflow layer: `SKILL.md`. This layer defines when to use the
   skill, when not to use it, required workflow, decision rules, validation,
   output format, and uncertainty handling.
3. Rule / knowledge / reference layer: `rules/`, `knowledge/`, `references/`,
   and `profiles/`. This layer holds depth and should be read only when
   relevant.
4. Automation layer: `scripts/` or `cli/`. This layer handles repeatable
   mechanics and must not silently replace human or agent judgment.
5. Asset / template layer: `assets/`, `templates/`, or `examples/`. This layer
   holds reusable shapes, examples, fixtures, or expected outputs that the
   workflow can emit or adapt.

Do not put catalogs, long examples, source-doc dumps, or exhaustive
framework notes directly in `SKILL.md`. Move that depth into the proper
skill-local layer and point to it from `SKILL.md`.

## Variant Reference Splitting

When one skill covers a domain that has platform, framework, API-version, or
task-shape variants, split the depth into focused reference files instead of
putting every variant in `SKILL.md`.

Use separate references when:

- a task usually needs only one platform or variant
- guidance differs enough that combined rules would conflict
- a single reference is becoming a cross-platform checklist
- the same skill should still own the trigger and workflow

Examples:

- SwiftUI accessibility may use separate iOS and macOS references when platform
  behavior differs.
- Swift Charts accessibility belongs in the Charts skill because chart
  descriptors and Audio Graph are chart-specific.
- Swift Concurrency can keep actors, tasks, async sequences, `Sendable`, and
  testing guidance in separate references.
- Performance work can split source-level SwiftUI performance from Instruments
  trace capture and analysis.

Create a new top-level skill only when the variant has its own trigger,
workflow, validation rules, or output contract. Otherwise keep it as a
reference under the nearest specific skill.

## Skill Candidate Review

When evaluating any proposed skill input, run it through a small value-and-fit
review before changing this collection. A candidate may come from a user idea,
an existing local skill that might be split or merged, an observed repeated
task, or another public/local skill. The goal is to improve local trigger
precision, workflow quality, reference coverage, or mechanical reliability.
When the feed workflow routes a candidate here, this collection still owns the
local value, authority, information-conservation, and final shape decision.
Record those decisions in audit-ready rows: source item id/name, state, local
destination, local owner, reason, and authority status when the item depends on
mutable Apple, Swift, Xcode, package, or tool behavior.

Use candidate input only when it improves one of these surfaces:

- precise trigger phrases and negative boundaries
- compact workflow steps that change agent behavior
- decision rules, validation rules, and failure handling
- high-density reference guidance that is reusable after deduplication
- examples that define reusable patterns, validation fixtures, or expected
  output shapes after compression to the smallest useful form
- scripts or assets only when they provide stable mechanics the skill needs

Do not carry over content when it is:

- low-density explanations that repeat normal model knowledge
- long examples that do not define a reusable pattern, fixture, or output
  exemplar
- full catalogs that belong in narrower references or generated data
- host-specific metadata that conflicts with this collection's registry
- overlapping trigger contracts that would cause avoidable skill collisions
- source directory shape when it conflicts with this repository's skill
  architecture
- repository metadata, branding, funding files, host-specific setup, or
  legal/compliance files; these are non-capability material, and that status
  does not decide whether framework or workflow capability is retained

When the review finds value, translate it through the local architecture:
improve the nearest existing skill first, keep `description` compact, move
depth into focused references, and create a new top-level skill only when the
candidate exposes a distinct trigger, workflow, validation rule, or output
contract.

When a candidate has a named reference source, review source coverage before
and after the translation. Preserve task-relevant information value, not source
wording or structure. Keep useful capabilities, edge cases, tool assumptions,
troubleshooting paths, examples, and validation knowledge by placing them in
the right local layer: `SKILL.md` for trigger and workflow, `references/` for
depth, `scripts/` or `cli/` for repeatable mechanics, and `templates/` or
`examples/` for reusable output shapes.

For external skill sources, run an information-conservation check before
closing the change. Actionable source skill information should map to a local
skill, reference, script, template, example, or deferred row with a candidate
local owner. Compression is acceptable only when the local result can still
support the same useful API choice, architectural decision, safety stop,
validation check, failure diagnosis, or reusable artifact shape.

When a candidate or review includes Apple, Swift, Xcode, swiftlang, or
third-party package facts that may have changed, current primary-source
verification is a mandatory gate before turning them into local trigger,
workflow, validation, availability, API, tool, or platform rules. Primary
sources include official Apple documentation, Swift.org, docs.swift.org,
official Swift Forums announcements or proposals, the current local SDK/tool
output, and the package source for official packages. If verification is not
available, keep the note evidence-limited or marked as needing verification
and do not present it as current authority.

Compression is not permission to lose executable value. Any omitted source
material should fall into a clear category: duplicate, low-density explanation,
host-specific metadata, incompatible external structure, out-of-scope domain
coverage, or non-durable example material. The result should read like a
collection-native review outcome that retains the useful behavior and knowledge
needed to perform the same local task.

Information density should be consistent across skills: prefer rules that are
patch-ready, audit-ready, or routing-relevant. If a paragraph does not help the
agent decide, implement, validate, or report, remove it or move it to a
reference only when it has durable value.

Keep the retained information volume proportional to reuse. A small trigger
improvement may only need a one-line description change; a reusable pattern may
deserve a focused reference; a large example should survive only as a compact
snippet, fixture, or output exemplar.

## Description-Driven Disclosure

Progressive disclosure starts in the `description`, not in the `SKILL.md` body.
The description is always visible to the agent and should decide whether the
skill is worth loading at all.

Write each description as a compact trigger filter:

- name the highest-signal task or code shape first
- include the main positive trigger categories
- include negative boundaries when nearby skills could also match
- identify the output or judgment the skill produces
- avoid full package, framework, API, or topic catalogs

For collection domain skills, the description should be specific enough to
trigger without the user naming the skill. Explicit invocation may select a
review, refactor, audit, brief, or diagnostic mode, but it must use the same
knowledge system and boundary as automatic triggering. True root/meta
maintenance skills may be explicit-only; they do not belong in this collection.

When a skill has both automatic and manual entry modes, keep the automatic
trigger narrow and cheap. Put the full reading order, escalation path, and deep
catalog scope in `SKILL.md` or the referenced rule/knowledge files.

## Trigger Contract

The `description` frontmatter is a trigger contract, not a generic summary. It
should be compact, explicit, and action-oriented.

Every description should answer:

- what task should trigger this skill
- what user phrases or repo situations should match
- what domain the skill applies to
- what artifact or judgment the skill produces
- what should not trigger it

Put high-value trigger phrases early. Include negative boundaries. Avoid broad
names and descriptions such as "Swift helper", "docs", "review", or "utility".

Good descriptions name capability and boundary:

```yaml
description: Use for Swift Package architecture design, review, and diagnostics involving target graphs, module boundaries, dependency direction, composition roots, public API surfaces, source selection, or compact evidence briefs. Do not use for feature specs, roadmap planning, code rewrites, UI feature architecture, or full-repository concatenation.
```

Bad descriptions are too broad:

```yaml
description: Helps with Swift packages.
```

## Required SKILL.md Shape

Each skill should keep `SKILL.md` concise and operational. Prefer this section
shape unless the skill has a clear reason to vary:

- Purpose
- Entry Modes, when the skill has both automatic and manual paths
- When To Use
- When Not To Use
- Inputs To Inspect
- Workflow
- Reference Files To Consult
- Decision Rules
- Validation Rules
- Output Format
- Failure / Uncertainty Handling

`SKILL.md` should define reading order for deeper files. It should not require
loading every rule, reference, catalog, or template for ordinary use.

## Agents Metadata

`agents/openai.yaml` is optional but recommended for published skills. Use it
for display and manual-entry ergonomics:

- `display_name`
- `short_description`
- `icon_small`
- `icon_large`
- `brand_color`
- `default_prompt`

Keep it consistent with `SKILL.md`, but do not treat it as the source of truth.
Automatic progressive disclosure depends primarily on the `SKILL.md`
frontmatter description and then the workflow in `SKILL.md`.

For Codex UI icons, prefer checked-in skill-local files:

- `assets/icon-small.svg`
- `assets/icon-large.png`

Use `icon_small` as SVG and `icon_large` as PNG, matching bundled Codex
examples. Keep optional vector sources such as `assets/icon-large.svg` only
when they help regenerate the PNG. Do not use symlinked icon assets for skills
that may be copied, zipped, or installed independently.

## Automation Rules

Add scripts or CLIs only for stable, repeatable mechanics such as scanning,
fetching, rendering, validating, or exporting. Do not add automation just to
encode high-level judgment.

Generated or runtime artifacts should stay outside the skill directory unless
the skill explicitly defines a checked-in fixture or example.

## Create / Update Skill Loop

When creating, splitting, renaming, or materially changing a skill, use this
loop:

1. Classify the skill by primary category and any secondary tags.
2. Define the `SKILL.md` `name` and trigger-oriented `description` before
   adding deep material.
3. Choose the smallest directory shape that supports the workflow.
4. Put durable depth in the right optional layers and add local indexes when a
   layer has multiple files.
5. Add or update `agents/openai.yaml` only after `SKILL.md` is stable.
6. Apply the skill candidate review rules before adding, splitting, merging,
   adapting, incorporating, or registering a skill.
7. Update `README.md`, `AGENTS.md`, and `.claude-plugin/marketplace.json` only
   after the skill directory contains `SKILL.md`.
8. Reconcile every advertised path before commit:
   - every `skills/<name>` path in `README.md`, `AGENTS.md`, and
     `.claude-plugin/marketplace.json` exists
   - every advertised skill directory contains `SKILL.md`
   - every advertised skill directory is tracked or staged
   - every rename or split stages both the old-path deletion and new-path
     addition
   - no stale old skill names remain outside intentional migration notes
9. Keep `AGENTS.md` short. It may record durable conflict routing, but detailed
   trigger lists belong in each skill's `description` and `SKILL.md` body.
10. Validate before handoff.

## Validation Checklist

Before publishing or materially changing a skill, check:

- `SKILL.md` has valid frontmatter with a precise `name` and `description`.
- The description is trigger-oriented and includes negative boundaries.
- The description supports progressive disclosure: it can trigger the skill
  cheaply without becoming a full catalog.
- `SKILL.md` is a task protocol, not a catalog or long reference file.
- Candidate input has been normalized to this collection's information
  density and ownership model.
- Deeper material lives in `rules/`, `knowledge/`, `references/`,
  `profiles/`, `templates/`, `assets/`, `examples/`, `scripts/`, or `cli/` as
  appropriate.
- Platform, framework, API-version, or task-shape variants are split into
  focused references when they would otherwise bloat `SKILL.md` or conflict.
- Optional layers are not empty and have a local index when they contain
  multiple files.
- Automatic entry paths do not require network refreshes or full catalog loads
  unless that is the skill's explicit job.
- Manual entry paths remain available for full audits, maintenance, refresh, or
  export tasks when the skill supports them.
- `agents/openai.yaml`, if present, agrees with `SKILL.md`.
- Custom `icon_small` and `icon_large` paths, if present, point to real
  skill-local assets. SVG icons are square and XML-valid; PNG icons are square
  valid PNG files.
- `.claude-plugin/marketplace.json` points only to tracked skill directories.
- `README.md`, `AGENTS.md`, and `.claude-plugin/marketplace.json` do not point
  at untracked, missing, or partially renamed skill directories.
- Route guidance in `AGENTS.md` stays short and does not duplicate full skill
  workflows.
- Current-source verification is complete before Apple, Swift, Xcode,
  swiftlang, package, availability, or tool behavior that may have changed is
  promoted to a local rule. Otherwise it is explicitly marked evidence-limited
  or needing verification.

## Source Authority

- Repository-local deployment targets, package manifests, build settings, and
  code win for project-specific compatibility decisions.
- Official Apple, Swift.org, docs.swift.org, current local SDK/tool output,
  and official package sources win over memory, examples, and community
  material for API names, availability, command flags, and platform behavior.
- Community references can inform workflow and examples, but they must not
  become authority for current Apple or Swift behavior without current official
  or primary-source verification.
- If a local skill or reference conflicts with verified current sources,
  update the nearest existing skill/reference first; create a new skill only
  when the source change creates a distinct trigger, workflow, validation
  rule, or output contract.
