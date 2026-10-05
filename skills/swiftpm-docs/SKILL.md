---
name: swiftpm-docs
description: Scaffold, audit, normalize, and export Swift package repository documentation structure. Use for repository documentation baselines, documentation drift audits, Route/Index separation, Documentation/Architecture current truth, DocC target catalog placement, Documentation/Proposals design-in-progress, Documentation/Decisions/Migrations/Archive history, Documentation/Reference placement, GitHub/community-health documentation, profile-based template output, and .agent/PLANS.md execution-state aids for large documentation migrations. Produces documentation findings, file edits, or target-repository template files. Do not use for general Swift coding, feature specs, product roadmaps, UI work, CI/release automation, or generic task orchestration.
---

# SwiftPM Documentation

## Purpose

Shape Swift package repositories so documentation roles are explicit,
repo-native, and easy to maintain.

## When To Use

- Scaffold a documentation-first or public-repo-complete documentation baseline.
- Audit an existing Swift package repo against the documentation role model.
- Normalize misplaced documentation into route, index, proposal, truth, history,
  governance, or reference roles.
- Export target-repository documentation from skill-local template sources.
- Emit `templates/.agent.PLANS.md.tpl` to the target repository as
  `.agent/PLANS.md` for large normalize, migration, or export work.

## When Not To Use

- Do not use for feature specification workflows.
- Do not use for product requirements, roadmap planning, or task management.
- Do not use for general Swift implementation, UI work, or runtime
  architecture changes.
- Do not use for release automation, CI workflow design, or general process
  frameworks.

## Inputs To Inspect

- Root documentation: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`,
  `SECURITY.md`, `SUPPORT.md`, `LICENSE`, and `CODEOWNERS` when present.
- Documentation tree: `Documentation/README.md`,
  `Documentation/Architecture/*`, `Documentation/Proposals/*`,
  `Documentation/Decisions/*`, `Documentation/Migrations/*`,
  `Documentation/Archive/*`, and `Documentation/Reference/*`.
- DocC catalogs and generated archives: `Sources/<Target>/<Target>.docc/*`,
  package-level `.docc` catalogs when intentionally used, and
  `.doccarchive` outputs.
- Agent temporary state: `.agent/PLANS.md` and task-scoped `.agent/*` artifacts
  when present. Do not treat `.codex/*` capability or skill configuration as
  temporary execution state.
- GitHub surface: `.github/*`, issue templates, pull request templates, and
  GitHub-facing policy files.
- Skill internals when editing this collection:
  `rules/`, `templates/`, `profiles/`, `examples/`, and `references/`.

## Workflow

Both existing profiles include one compact version and release policy scaffold:
`Documentation/Architecture/VersioningAndRelease.md`, from
`templates/Documentation.Architecture.VersioningAndRelease.md.tpl`. Populate it from actual project declarations,
build configuration, scripts and accepted rules. Include component version
authority, derived fields, dependency compatibility, candidate acceptance,
evidence reuse/invalidation, real entry points and artifact retention.

For an existing repository, find the document already owning these rules first.
Complete that document and adjust the profile target, indexes and AGENTS route
to that single entry. Do not generate a competing policy. Distinguish implemented
automation from manual procedures and missing release capability. Unknown
commands remain explicitly unestablished; the scaffold does not create them.
This is documentation work; changes to release implementation belong to the
project's release owner.

1. Start with an audit when a target repo already exists.
2. Classify files by role before editing content.
3. Normalize role collisions before exporting template output.
4. Choose the smallest profile that fits the requested baseline:
   `minimal` for documentation-first, `standard` for public-repo-complete.
5. Compose scaffold and export outputs from explicit profile guidance, not
   ad-hoc file lists.
6. For long-running normalize, migration, or export work, create
   `.agent/PLANS.md` from `templates/.agent.PLANS.md.tpl` and keep it current.
   Before writing it, run `git check-ignore -q .agent/PLANS.md` in the target
   repository; when that fails, append `.agent/` to the repository's local
   `.git/info/exclude`, not to the shared `.gitignore`.
7. When iterative feedback or a rejected implementation is part of the input,
   read `rules/canonical-artifacts.md` before editing. If `AGENTS.md` is in
   scope, also read `templates/AGENTS.md.tpl`, merge its complete canonical
   artifact contract with valid repository routes, and run
   `scripts/validate_canonical_target.py` before handoff.
8. Inventory every conflicting implementation, option, test, fixture,
   snapshot, configuration, schema, generated source, and example found
   outside documentation ownership. Report each remaining file or category;
   do not reduce the handoff to representative examples.

## Role Model

- Agent Guide: `AGENTS.md`
- Index: `README`-class files
- Proposal: `Documentation/Proposals/*`
- Truth: `Documentation/Architecture/*`
- History: `Documentation/Decisions/*`, `Documentation/Migrations/*`,
  `Documentation/Archive/*`
- Governance: `.github/*`
- Reference: `Documentation/Reference/*`
- DocC Source: `Sources/<Target>/<Target>.docc/*`
- Generated DocC Output: `.doccarchive` directories
- Agent Temporary State: `.agent/*`, especially `.agent/PLANS.md`

## Reference Files To Consult

Read only the files relevant to the selected operation:

- `rules/route-vs-index.md`: agent guide versus index
  classification, including product-state documentation boundaries.
- `rules/proposal-vs-truth-vs-history.md`: proposal, truth, and history
  classification.
- `rules/architecture-description-primacy.md`: current architecture
  description ownership.
- `rules/canonical-artifacts.md`: current-artifact normalization after
  iterative feedback or superseded implementation attempts.
- `rules/architecture-doc-format.md`: lightweight arc42-style architecture
  document shape.
- `rules/decision-record-format.md`: lightweight ADR/MADR-style decision
  record shape.
- `rules/proposal-doc-format.md`: lightweight proposal document shape.
- `rules/governance-vs-documentation-placement.md`: GitHub and governance
  placement.
- `rules/path-casing.md`: canonical documentation path casing for scaffold,
  normalize, and export work.
- `rules/readme-layering.md`: root README, documentation README, architecture
  README, and architecture-rule ownership.
- `rules/docc-placement.md`: target-level DocC catalog placement, generated
  archive boundaries, and DocC build expectations.
- `rules/docc-landing-identity.md`: package icon and page color on DocC
  landing pages.
- `profiles/minimal.md` and `profiles/standard.md`: profile composition.
- `examples/`: small reference previews and target-tree examples.
- `references/codex-exec-plans.md`: when deciding whether a task needs a
  session-spanning `.agent/PLANS.md` execution aid.
- `scripts/validate_template_exports.py`: materialize the `minimal` and
  `standard` output maps and verify target `AGENTS.md` invariants.
- `scripts/validate_canonical_target.py`: verify an edited target `AGENTS.md`
  carries the complete contract and flag correction-shaped prose in active
  documentation roles and DocC source.

External foundations:
[ISO/IEC/IEEE 42010](https://www.iso-architecture.org/ieee-1471/ads/),
[arc42](https://arc42.org/documentation/), [MADR/ADR](https://adr.github.io/madr/),
and [Diataxis](https://diataxis.fr/) inform the skill's semantics and boundary
rules. They do not directly dictate the repository tree.

## Decision Rules

- Keep Agent Guide and README entry roles separate. `AGENTS.md`
  carries first-principles work, task route, authority boundaries, and boundary
  guardrails; it does not explain the tree or serve as a user manual. `README`
  files explain public entry points, documentation indexes, and placement; they
  do not route agent work.
- Keep root `README.md` as the GitHub-facing landing manual and entry index.
  GitHub can recognize README files in `.github`, root, and `docs`, but
  ordinary Swift package repositories should default to root `README.md`. Emit
  `.github/README.md` only for special GitHub profile or default
  community-health repositories, or when the target explicitly chooses that
  surfaced README behavior.
  For a user-facing package, CLI, tool, app, or library, preserve the public
  manual essentials: what it does, requirements, installation or setup, quick
  start, common commands or examples, expected output, and links to deeper
  documentation. Move documentation reading indexes to `Documentation/README.md`,
  architecture indexes to `Documentation/Architecture/README.md`, exhaustive
  reference material to `Documentation/Reference/*`, and current architecture
  rules to named files under `Documentation/Architecture/`.
- Keep shipped documentation focused on current product facts, supported
  behavior, and operating guidance. Keep temporary implementation notes,
  local evidence, local paths, run-specific artifacts, and historical comparison
  notes out of README files, reference docs, API docs, and bundled user-facing
  skills. Promote only accepted decision records into
  `Documentation/Decisions/*` and durable transition or cutover records into
  `Documentation/Migrations/*`.
- Normalize accepted feedback across the complete active documentation
  surface. Rejected intermediate concepts must not survive as labels,
  qualifiers, examples, or explanatory prose unless their exclusion is a
  current compatibility, safety, or ownership invariant.
- Normalize by semantic identity and role, not by matching text. A rejected
  current capability does not invalidate a distinct released-format history,
  migration, ownership fact, or safety boundary that uses the same term.
  Preserve those artifacts unless separate evidence changes their facts. If
  they are already correct and the task does not change their facts, leave
  their contents unchanged rather than polishing or restating them.
- When canonicalizing an existing `AGENTS.md`, replace correction-shaped
  feature guidance with the self-contained canonical-artifact contract carried
  by `templates/AGENTS.md.tpl`; do not treat a feature bullet such as
  `A without B` as already current.
- Inspect code, tests, configuration, schemas, generated sources, and examples
  for contract drift that would make normalized documentation false. Report
  that drift as a blocking handoff to its implementation owner; do not mutate
  non-documentation artifacts unless the user separately requests that work
  and the applicable implementation owner is active.
- Treat a disabled option, skipped test, dead branch, retained fixture, or
  feature-specific prohibition as drift when it exists only because the
  rejected capability was attempted. Disabled state alone is not a reason to
  preserve or document it as a current invariant.
- Keep DocC catalogs with the SwiftPM target they document, normally at
  `Sources/<Target>/<Target>.docc/`. Root `Documentation/` is repository-level
  documentation; it is not the default home for module API DocC catalogs.
- Treat `.doccarchive` directories as generated output unless the repository
  explicitly has a checked-in publishing artifact policy.
- Keep design-in-progress in `Documentation/Proposals/*`. Proposal space is
  neither current truth nor historical record.
- Keep current truth in `Documentation/Architecture/*`, not in decision logs,
  migration notes, archives, or proposals.
- Treat `Documentation/Architecture/*` as the primary current architecture
  description. Proposal, history, and reference materials support that
  description; they do not replace it.
- Keep historical context in `Documentation/Decisions/*`,
  `Documentation/Migrations/*`, and `Documentation/Archive/*`, not in current
  architecture files or proposal drafts.
- Keep GitHub-facing policy and templates in `.github/*`.
- Keep CODEOWNERS at `.github/CODEOWNERS` in generated defaults.
- Keep reference material in `Documentation/Reference/*`.
- Keep agent temporary execution artifacts in `.agent/*`. The standard active
  plan surface is `.agent/PLANS.md`. Do not place agent plans at repository root,
  in `Documentation/*`, or in `.github/*`, and do not use `.agent/*` for
  `.codex` responsibilities such as skills or capability configuration.
- Preserve canonical documentation path casing. Use the PascalCase-style role
  directory segments shown by this skill, such as
  `Documentation/Architecture`, `Documentation/Proposals`,
  `Documentation/Decisions`, `Documentation/Migrations`,
  `Documentation/Archive`, and `Documentation/Reference`, and use PascalCase
  Markdown document names under those role directories, except for `README.md`
  indexes and explicitly conventional external files.
- Treat exported output as downstream only. It must trace back to this skill
  and the normalized repo structure.
- Author template source files from the target repository's perspective, not
  from the `swift-skills` collection's perspective.
- Do not expose collection-internal production terminology in generated target
  templates.
- Treat `minimal` as the documentation-first baseline: the smallest stable repo
  shape that makes Agent Guide, Index, Truth, and Governance explicit.
- Treat `standard` as the first public-repo-complete baseline: it extends
  beyond `minimal` with fuller proposal, history, reference, and
  GitHub/community-health coverage.
- Keep the `minimal` / `standard` distinction intentional unless product
  strategy changes deliberately.
- Favor crisp README navigation over long essays, but do not collapse the root
  README into a pure documentation-tree directory. Summarize common public
  usage in the root README and link to deeper reference documentation for
  exhaustive option tables, architecture details, or failure catalogs.
- Allow target trees to vary by profile. Minimal and standard trees are both
  valid when the role boundaries stay intact.

## Validation Rules

- The selected profile matches the emitted or changed file set.
- Agent guides do not become indexes, and README-class files do not
  become routing contracts.
- Root `README.md` stays outward-facing, keeps public manual essentials for the
  repository's primary audience, and does not restate detailed architecture
  rules that belong under `Documentation/Architecture/*`.
- Shipped documentation states current product facts and usage without
  temporary implementation notes, run-specific artifacts, or historical
  comparison notes.
- Current docs stand alone without the editing conversation and contain no
  residual names, examples, or correction narratives for rejected intermediate
  concepts.
- Current docs have the same meaning as a direct accepted design and do not use
  `only`, `without`, `removed`, `rejected`, `legacy`, `deprecated`, or
  `no longer supported` merely to narrate the editing path.
- Existing history, migration, ownership, and safety artifacts remain
  unchanged unless task-specific evidence independently changes their facts.
- An unchanged role-owned artifact has no content diff; mentioning it in the
  handoff does not justify editing it.
- Generated schemas, help, DocC output, and metadata are regenerated by their
  owner or reported as blocking drift; they are not hand-edited.
- Ordinary Swift package repositories do not emit `.github/README.md` by
  default, and GitHub's surfaced repository README resolves to root
  `README.md`.
- Public SwiftPM targets with user-facing APIs have DocC catalogs colocated
  with the target, or the absence of DocC is called out as an intentional gap.
- Generated `.doccarchive` output is not mixed into source documentation.
- `Documentation/Architecture/*` states current truth explicitly after proposal
  or decision changes.
- Proposal, decision, migration, archive, and reference materials do not
  redefine current truth on their own.
- Canonical documentation paths and Markdown document filenames keep the casing
  used by the selected profile, templates, and path-casing rule.
- Target-facing templates and exported files do not mention `swift-skills`,
  skill-local `rules/`, `examples/`, profile mechanics, or source/export
  internals.
- `python3 scripts/validate_template_exports.py` materializes both profiles and
  verifies that each exported `AGENTS.md` carries the complete path-independent
  canonical-artifact contract.
- After canonicalizing an existing repository, run
  `python3 scripts/validate_canonical_target.py <repository>`. Use
  `--allow-path` only for a reviewed active file whose negative wording is
  independently required by a current compatibility, safety, or ownership
  invariant, and state that rationale in the handoff.
- `.agent/PLANS.md`, when emitted, is treated as temporary execution state only.
  It is not architecture truth, a proposal, a decision record, a migration
  record, reference material, GitHub governance, or `.codex` skill material.
  `git check-ignore -q .agent/PLANS.md` succeeds, and `git ls-files .agent`
  prints nothing.

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
- If current-capability feedback appears to contradict a historical or
  ownership artifact, do not infer that the artifact is false. Preserve it and
  report the semantic distinction or request implementation-owner resolution.
- If an existing root `PLAN.md` or `PLANS.md` appears, treat it as legacy or
  ambiguous execution state; preserve active content before normalizing the
  active plan surface to `.agent/PLANS.md`.
- If the current truth only appears in supporting artifacts, update or request
  an explicit `Documentation/Architecture/*` source of truth.
- If a profile does not cover a requested output, call that out rather than
  silently expanding the profile.
