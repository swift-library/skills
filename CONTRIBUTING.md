# Contributing

Keep changes small, boundary-first, and tied to the existing collection model.

## Change Surfaces

- Update `skills/<skill>/SKILL.md` when changing a skill's purpose, scope,
  supported operations, or role model.
- Update `skills/<skill>/rules/` when changing stable invariants.
- Update `skills/<skill>/templates/` for skill-local template source material
  and scaffold fragments.
- Update `skills/<skill>/examples/` for small reference examples and target
  trees.
- Update root `README.md` only when the top-level collection shape changes.

## Expectations

- Keep route language in `AGENTS.md`.
- Keep tree, placement, and ownership language in `README`-class files.
- Keep `skills/<skill>/templates/` upstream and keep exported output
  downstream from rule authority.
- If a template change alters intended structure, update rules or `SKILL.md`
  first.
- Prefer minimal edits over speculative expansion.
