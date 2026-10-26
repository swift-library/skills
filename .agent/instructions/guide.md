---
description: Route swift-skills collection maintenance and keep templates, skill guidance and upstream absorption reusable.
---
# swift-skills Agent Guide

Read `README.md` first for the collection shape and authority model.

## Maintenance Route

- For a skill's trigger, workflow, or resources, edit that skill's directory
  following [skill authoring](docs/architecture/skill-authoring.md). Read that
  architecture before changing collection naming or authoring rules.
- For adding, renaming, or retiring a skill, follow the create/update loop in
  [skill authoring](docs/architecture/skill-authoring.md#create--update-skill-loop)
  and update [discovery](docs/catalog.md).
- For plugin distribution or versions, edit the plugin manifests
  (`.claude-plugin/plugin.json`, `plugin.json`), the marketplace manifests
  (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`) and
  `VERSION`; follow [release](docs/reference/release.md).
- For Swift package target-repository templates, edit
  `skills/swiftpm-docs/templates/` with the owning profiles and rules. A
  template change merges here on its own. After a release, the organization's
  [template publisher](https://github.com/swift-library/github-workflows#package-template-publication)
  re-exports it into swift-library/swift-package-template.
- Run `scripts/check` before handing off collection changes.
- Stop and clarify if collection maintenance expands into feature specs,
  roadmap planning, task orchestration, live release publishing, or general
  workflow systems.

## Authoring Guardrails

- Write target-repository templates for the generated repository. Keep out
  collection-internal terms: skill-local template sources, source-versus-export
  distinctions, and collection `rules/` or `examples/` directories.
- Keep skill docs to current reusable capabilities, triggers, workflows,
  validation and resource navigation. Creation notes, one-run validation logs,
  transitional explanations, retired-version notes and source comparisons stay
  out of reusable skill instructions.
- Do not hardcode downstream commands, sibling skill names, source paths, or
  fixture values into reusable guidance unless routing is the artifact being
  edited.
- When a skill is based on a named reference source, preserve source coverage
  for task-relevant capabilities and executable knowledge while translating it
  into this collection's structure.
- For code-related upstream absorption, do not reduce source material to an API
  guide. Preserve Swift engineering judgment: good and bad design shapes,
  ownership boundaries, anti-patterns, tradeoffs, migration hazards, validation
  commands, tests, and failure diagnosis when the source carries that knowledge.
- Preserve source-specific human guardrails during Swift upstream absorption.
  If a source uses a named pattern, checklist, warning sign, negative example,
  or preferred implementation shape to prevent AI-shaped Swift, keep a concrete
  local equivalent in the owning skill or reference, or record why it is
  compressed, deferred, or dropped.
- For Apple, Swift, Xcode, and swiftlang API facts that may have changed, use
  official documentation, the current local SDK or tool output, or verified
  package source before treating memory or skill references as authoritative.
