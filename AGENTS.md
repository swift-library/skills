# swift-skills Agent Guide

Read `README.md` first for the collection shape and authority model.

## First-Principles Work

- Name the behavior, root cause, invariant, owner, data flow, and validation
  before changing reusable skill files.
- Change the owning skill or collection layer, not the nearest convenient file.
- Keep changes traceable to the request, a cited source, or the owning invariant.
- Do not promote one fixture, one source run, or local execution state into
  reusable skill contracts.
- Keep skill docs focused on current reusable capabilities, trigger conditions,
  workflows, validation, and resource navigation. Keep creation notes, one-run
  validation logs, transitional explanations, retired-version notes, and source
  comparison narratives out of reusable skill instructions.
- Validate collection changes with the collection's declared checks.

## Canonical Artifacts

- Treat conversation, review, and intermediate attempts as editing input.
  Recompute the complete accepted contract before finalizing reusable skill
  material.
- Active skill artifacts depend only on that contract and their owned role,
  not on the editing path. Apply this to metadata, instructions, names,
  branches, configuration, schemas, scripts, templates, comments, tests,
  fixtures, examples, assets, and normative docs.
- If an intermediate result is `A + B` and the accepted result is `A`, express
  `A` directly. Remove `B` and its residual surface rather than naming the
  result `A without B` or documenting the correction.
- Normalize by semantic identity and artifact role, not by token. A rejected
  current capability does not invalidate a distinct historical fact,
  migration, provenance record, ownership boundary, or safety rule that uses
  the same term.
- Retain a negative rule only when exclusion is independently required by a
  current compatibility, safety, ownership, or regression invariant.
- A disabled flag, skipped test, dead branch, retained fixture, or prohibition
  created by the rejected attempt is residue, not an invariant. Remove it or
  route it to its owner; do not promote its disabled state into policy.
- Keep history only in artifacts that explicitly own provenance or history and
  still have durable value. Do not create one merely to preserve a correction.
- Preserve role-owned facts unless separate evidence changes them; do not
  rewrite history or ownership merely to make a rejected term disappear.
- Leave an already-correct history, migration, provenance, ownership, or safety
  artifact unchanged when the task does not change its facts. Do not polish or
  restate it merely because it is relevant to the current edit.
- Before handoff, verify that a reader without the editing conversation can use
  the current skill without mentally subtracting a rejected concept.

## Maintenance Route

- For a skill's trigger, workflow, or resources, edit that skill's directory
  following [skill authoring](docs/architecture/skill-authoring.md). Read that
  architecture before changing collection naming or authoring rules.
- For adding, renaming, or retiring a skill, follow the create/update loop in
  [skill authoring](docs/architecture/skill-authoring.md#create--update-skill-loop)
  and update [discovery](docs/catalog.md).
- For plugin distribution or versions, edit the plugin and marketplace
  manifests and `VERSION`; follow [release](docs/reference/release.md) and run
  `scripts/check`.
- For Swift package target-repository templates, edit
  `skills/swiftpm-docs/templates/` with the owning profiles and rules; run
  `scripts/check`. A template change merges here on its own. After a release,
  the organization's
  [template publisher](https://github.com/swift-library/github-workflows#package-template-publication)
  re-exports it into swift-library/swift-package-template.
- For the reader manual or documentation index, edit `README.md` or
  `docs/README.md`; keep detailed architecture and reference content in their
  named documents.
- Run `scripts/check` before handing off collection changes.
- Stop and clarify if collection maintenance expands into feature specs,
  roadmap planning, task orchestration, live release publishing, or general
  workflow systems.

## Authority

- `README.md` is the reader manual and discovery entry for scope, installation, usage, and requirements.
- `AGENTS.md` guides collection maintenance and cross-cutting edit guardrails.
- `docs/` holds collection documentation, indexed by `docs/README.md`; `docs/catalog.md` owns skill discovery and `docs/architecture/skill-authoring.md` owns authoring rules.
- `skills/*/SKILL.md` owns each skill's trigger, overlap boundaries, workflow, validation, and output.
- `skills/*/rules/` holds stable documentation-role invariants.
- `skills/*/knowledge/` holds curated skill-local domain knowledge when a skill
  needs a catalog or reusable basis.
- `skills/*/templates/` holds skill-local template source material, report
  shapes, and scaffold fragments.
- `skills/*/examples/` holds small reference examples.
- `.claude-plugin/plugin.json` and the root `plugin.json` own the plugin
  manifests for Claude Code and Codex.
  `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`
  publish the collection for their hosts.

## Boundary Guardrails

- Do not put single-skill workflow detail in this collection guide unless the
  collection itself owns the route.
- Do not hardcode downstream commands, sibling skill names, source paths, or
  fixture values into reusable guidance unless routing is the artifact being
  edited.
- If a value changes by source, package, skill, fixture, or runtime run, keep
  it in the owning artifact and route to it from here.

## Operating Notes

- When editing target-repository templates, write for the generated target
  repository, not for the `swift-skills` collection.
- Do not leak collection-internal production terms into target-repository
  templates. Keep out references to skill-local template source material,
  source-versus-export distinctions, and collection `rules/` or `examples/`
  directories.
- Keep report templates focused on the user-facing audit or review output they
  produce.
- When creating or materially changing a skill, follow
  `docs/architecture/skill-authoring.md`: keep `SKILL.md` trigger-oriented,
  preserve progressive disclosure, and keep host-specific `agents/` metadata
  secondary to the skill frontmatter and workflow.
- When a skill is based on a named reference source, preserve source coverage
  for task-relevant capabilities and executable knowledge while translating it
  into this collection's structure.
- For code-related upstream absorption, do not reduce source material to an API
  guide. Preserve Swift engineering judgment: good and bad design shapes,
  ownership boundaries, anti-patterns, tradeoffs, migration hazards,
  validation commands, tests, and failure diagnosis when the source carries
  that knowledge.
- Preserve source-specific human guardrails during Swift upstream absorption.
  If a source uses a named pattern, checklist, warning sign, negative example,
  or preferred implementation shape to prevent AI-shaped Swift, keep a concrete
  local equivalent in the owning skill/reference or record why it is
  compressed, deferred, or dropped.
- For Apple, Swift, Xcode, and swiftlang API facts that may have changed, use
  official documentation, the current local SDK/tool output, or verified
  package source before treating memory or skill references as authoritative.
- Keep changes minimal and boundary-first.
- Do not turn this file into a directory catalog.

## Code Review Rules

### Trigger and ownership

- Flag a skill description that promises work outside the skill's documented
  boundary; it can route a request to the wrong owner. Safe path: align the
  description, supported workflow and resource routes.

### Reusable guidance

- Flag guidance that turns a single organization's choices or one execution's
  inputs into a reusable requirement. Safe path: accept the value as an input
  or keep it in the example or owner that supplies it.

### Evidence and coverage

- Flag a capability claim without source support or an executable check where
  one is available, and a changed workflow without an eval that distinguishes
  the intended behavior. Safe path: verify the claim and add focused coverage
  in the owning skill.
