---
name: swiftpm-docs
description: Scaffold, audit, normalize, and export Swift package repository documentation structure. Use for repo docs baselines, documentation drift audits, Route/Index separation, Docs/Architecture current truth, Docs/Proposals design-in-progress, Docs/Decisions/Migrations/Archive history, Docs/Reference placement, GitHub/community-health docs, profile-based template output, and root PLANS.md execution aids for large docs migrations. Produces documentation findings, file edits, or target-repository template files. Do not use for general Swift coding, feature specs, product roadmaps, UI work, CI/release automation, or generic task orchestration.
---

# SwiftPM Docs

## Purpose

Shape Swift package repositories so documentation roles are explicit,
repo-native, and easy to maintain.

## When To Use

- Scaffold a docs-first or public-repo-complete documentation baseline.
- Audit an existing Swift package repo against the documentation role model.
- Normalize misplaced docs into route, index, proposal, truth, history,
  governance, or reference roles.
- Export target-repository documentation from skill-local template sources.
- Emit `templates/PLANS.md.tpl` to the target repository root as `PLANS.md`
  for large normalize, migration, or export work.

## When Not To Use

- Do not use for feature specification workflows.
- Do not use for product requirements, roadmap planning, or task management.
- Do not use for general Swift implementation, UI work, or runtime
  architecture changes.
- Do not use for release automation, CI workflow design, or general process
  frameworks.

## Inputs To Inspect

- Root docs: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`,
  `SECURITY.md`, `SUPPORT.md`, `LICENSE`, and `CODEOWNERS` when present.
- Docs tree: `Docs/README.md`, `Docs/Architecture/*`,
  `Docs/Proposals/*`, `Docs/Decisions/*`, `Docs/Migrations/*`,
  `Docs/Archive/*`, and `Docs/Reference/*`.
- GitHub surface: `.github/*`, issue templates, pull request templates, and
  GitHub-facing policy files.
- Skill internals when editing this collection:
  `rules/`, `templates/`, `profiles/`, `examples/`, and `references/`.

## Workflow

1. Start with an audit when a target repo already exists.
2. Classify files by role before editing content.
3. Normalize role collisions before exporting template output.
4. Choose the smallest profile that fits the requested baseline:
   `minimal` for docs-first, `standard` for public-repo-complete.
5. Compose scaffold and export outputs from explicit profile guidance, not
   ad-hoc file lists.
6. For long-running normalize, migration, or export work, create a root
   `PLANS.md` from `templates/PLANS.md.tpl` and keep it current.

## Role Model

- Route: `AGENTS.md`
- Index: `README`-class files
- Proposal: `Docs/Proposals/*`
- Truth: `Docs/Architecture/*`
- History: `Docs/Decisions/*`, `Docs/Migrations/*`, `Docs/Archive/*`
- Governance: `.github/*`
- Reference: `Docs/Reference/*`

## Reference Files To Consult

Read only the files relevant to the selected operation:

- `rules/route-vs-index.md`: route/index classification.
- `rules/proposal-vs-truth-vs-history.md`: proposal, truth, and history
  classification.
- `rules/architecture-description-primacy.md`: current architecture
  description ownership.
- `rules/architecture-doc-format.md`: lightweight arc42-style architecture
  document shape.
- `rules/decision-record-format.md`: lightweight ADR/MADR-style decision
  record shape.
- `rules/proposal-doc-format.md`: lightweight proposal document shape.
- `rules/governance-vs-docs-placement.md`: GitHub and governance placement.
- `rules/readme-layering.md`: root README, docs README, architecture README,
  and architecture-rule ownership.
- `profiles/minimal.md` and `profiles/standard.md`: profile composition.
- `examples/`: small reference previews and target-tree examples.
- `references/codex-exec-plans.md`: when deciding whether a task needs a
  durable `PLANS.md` execution aid.

External foundations:
[ISO/IEC/IEEE 42010](https://www.iso-architecture.org/ieee-1471/ads/),
[arc42](https://arc42.org/documentation/), [MADR/ADR](https://adr.github.io/madr/),
and [Diataxis](https://diataxis.fr/) inform the skill's semantics and boundary
rules. They do not directly dictate the repository tree.

## Decision Rules

- Keep Route and Index separate. `AGENTS.md` routes work; it does not explain
  the tree. `README` files explain the tree; they do not route work.
- Keep root `README.md` as the public landing page and concise entry index.
  Move documentation reading indexes to `Docs/README.md`, architecture indexes
  to `Docs/Architecture/README.md`, and current architecture rules to named
  files under `Docs/Architecture/`.
- Keep design-in-progress in `Docs/Proposals/*`. Proposal space is neither
  current truth nor historical record.
- Keep current truth in `Docs/Architecture/*`, not in decision logs, migration
  notes, archives, or proposals.
- Treat `Docs/Architecture/*` as the primary current architecture description.
  Proposal, history, and reference materials support that description; they do
  not replace it.
- Keep historical context in `Docs/Decisions/*`, `Docs/Migrations/*`, and
  `Docs/Archive/*`, not in current architecture files or proposal drafts.
- Keep GitHub-facing policy and templates in `.github/*`.
- Keep reference material in `Docs/Reference/*`.
- Treat exported output as downstream only. It must trace back to this skill
  and the normalized repo structure.
- Author template source files from the target repository's perspective, not
  from the `swift-skills` collection's perspective.
- Do not expose collection-internal production terminology in generated target
  templates.
- Treat `minimal` as the docs-first baseline: the smallest stable repo shape
  that makes Route, Index, Truth, and Governance explicit.
- Treat `standard` as the first public-repo-complete baseline: it extends
  beyond `minimal` with fuller proposal, history, reference, and
  GitHub/community-health coverage.
- Keep the `minimal` / `standard` distinction intentional unless product
  strategy changes deliberately.
- Favor crisp README indexes over long essays.
- Allow target trees to vary by profile. Minimal and standard trees are both
  valid when the role boundaries stay intact.

## Validation Rules

- The selected profile matches the emitted or changed file set.
- Route files do not become indexes, and README-class files do not become
  routing contracts.
- Root `README.md` stays outward-facing and does not restate detailed
  architecture rules that belong under `Docs/Architecture/*`.
- `Docs/Architecture/*` states current truth explicitly after proposal or
  decision changes.
- Proposal, decision, migration, archive, and reference materials do not
  redefine current truth on their own.
- Target-facing templates and exported files do not mention `swift-skills`,
  skill-local `rules/`, `examples/`, profile mechanics, or source/export
  internals.
- `PLANS.md`, when emitted, is treated as an execution aid only.

## Output Format

For audits or normalize/export slices, return:

1. Phase / stage judgment
2. Inputs inspected
3. Files changed
4. What changed
5. Findings or drift assessment
6. Validation performed
7. Risks / constraints
8. Recommended next steps
9. Code diff (key hunks), if files changed

## Failure / Uncertainty Handling

- Stop and ask when the requested work crosses into product planning,
  implementation workflow, release automation, or non-documentation
  architecture.
- If file ownership is ambiguous, classify by role before editing.
- If the current truth only appears in supporting artifacts, update or request
  an explicit `Docs/Architecture/*` source of truth.
- If a profile does not cover a requested output, call that out rather than
  silently expanding the profile.
