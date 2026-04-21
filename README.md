# swift-skills

`swift-skills` is a skill collection for repository-native Swift documentation
work. The repo holds skill definitions, rules, examples, and skill-local
template source material.

## Current Focus

The collection currently centers on one flagship skill:
`skills/swift-package-docs/`.

`swift-package-docs` is limited to Swift package documentation architecture. It
supports:

- scaffold
- audit
- normalize
- export template

For larger normalize, migration, or export work, it may also use a durable
`PLANS.md` scaffold as an execution aid. That does not expand the skill into
product specs, roadmap planning, or workflow orchestration.

## Repo Shape

- `.claude-plugin/`: Claude Code marketplace metadata for the collection
- `skills/`: authoritative skill source material, including skill-local
  template sources

## Install In Claude

Install a specific skill directory rather than the repository root.

For the current flagship skill:

- source directory: `skills/swift-package-docs/`

### Claude Apps

Zip the `skills/swift-package-docs/` directory and upload that skill in Claude:

1. Open Claude.
2. Go to `Settings > Capabilities > Skills`.
3. Click upload.
4. Select the zipped `swift-package-docs/` skill folder.

### Claude Code

Place the skill directory in `~/.claude/skills`:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/swift-package-docs" \
  ~/.claude/skills/swift-package-docs
```

If you prefer a copy instead of a symlink:

```bash
mkdir -p ~/.claude/skills
cp -R "$(pwd)/skills/swift-package-docs" \
  ~/.claude/skills/swift-package-docs
```

### Claude Code Marketplace

For local testing from this repository:

```bash
claude plugin marketplace add .
claude plugin install swift-package-docs@swift-skills
```

After publishing the repository to GitHub:

```bash
claude plugin marketplace add swift-library/skills
claude plugin install swift-package-docs@swift-skills
```

This uses `/.claude-plugin/marketplace.json` as the marketplace catalog.

## Install In Codex

Install a specific skill directory into `$CODEX_HOME/skills` rather than
linking the repository root.

For the current flagship skill:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/skills/swift-package-docs" \
  "${CODEX_HOME:-$HOME/.codex}/skills/swift-package-docs"
```

If you prefer a copy instead of a symlink:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R "$(pwd)/skills/swift-package-docs" \
  "${CODEX_HOME:-$HOME/.codex}/skills/swift-package-docs"
```

Restart Codex after installing so it picks up the new skill.

## Current Skill Design

The current skill design centers on `swift-package-docs/`.

- `AGENTS.md` is the collection route and operational contract.
- `README`-class files index the collection tree, scope, ownership, and
  placement.
- `skills/` is the authoritative source for skill definitions, rules,
  templates, examples, and profiles.
- `.github/*` is repo-local GitHub governance for `swift-skills`.

For the target-repository role model and detailed documentation semantics, see
`skills/swift-package-docs/SKILL.md`.

Route and index are separate on purpose. Do not turn `AGENTS.md` into a tree
index, and do not turn `README` files into routing contracts.
