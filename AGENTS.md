# swift-skills Agent Route

Read `README.md` first for the collection shape and authority model.

## Route

- Enter `skills/swift-package-docs/` when the task is about repository-native
  documentation architecture for a Swift package repository.
- Stay within that skill when the requested work is scaffold, audit, normalize,
  or export template.
- For large multi-step documentation migrations or normalize/export work inside
  that skill, use its `assets/PLANS.md` scaffold and keep the plan updated as
  work proceeds.
- Stop and clarify if the task drifts into feature specs, roadmap planning,
  task orchestration, release automation, or general workflow systems.

## Authority

- `AGENTS.md` files route work and define operational handling.
- `README`-class files index scope, placement, and ownership.
- `skills/*/SKILL.md` defines the skill boundary and supported operations.
- `skills/*/rules/` holds stable documentation-role invariants.
- `skills/*/templates/` holds upstream skill-local template source material and
  scaffold fragments.
- `skills/*/examples/` holds small reference examples.
- `.claude-plugin/marketplace.json` is the discovery registry for the
  collection.

## Operating Notes

- When editing `skills/*/templates/`, write for the generated target
  repository, not for the `swift-skills` collection.
- Do not leak collection-internal production terms into target templates. Keep
  out references to skill-local template source material, source-versus-export
  distinctions, and collection `rules/` or
  `examples/` directories.
- Keep target templates focused on the generated repository's roles,
  placement, scope, and contributor expectations.
- Keep changes minimal and boundary-first.
- Do not turn this file into a directory catalog.
