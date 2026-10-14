# Installation

The plugin marketplace installs skills by name. The other methods install a
single skill directory; do not install the repository root as a skill. The
examples use `swiftpm-docs`; replace it with any name from the
[catalog](Catalog.md).

### Claude Code plugin marketplace

The repository is a Claude Code plugin marketplace named `swift-skills`, with
one plugin per skill. Add it and install the skills you want:

```bash
claude plugin marketplace add swift-library/skills
claude plugin install swiftpm-docs@swift-skills
```

Inside Claude Code, run the same commands as `/plugin marketplace add` and
`/plugin install`.

### Claude Code skills directory

Clone the repository and copy a skill into `~/.claude/skills`:

```bash
git clone https://github.com/swift-library/skills.git
cd skills
mkdir -p ~/.claude/skills
cp -R skills/swiftpm-docs ~/.claude/skills/swiftpm-docs
```

To follow updates with `git pull`, link the directory instead of copying it:

```bash
ln -s "$(pwd)/skills/swiftpm-docs" ~/.claude/skills/swiftpm-docs
```

### Claude apps

From the root of the cloned repository, zip the skill folder:

```bash
cd skills
zip -r ../swiftpm-docs.zip swiftpm-docs
```

In Claude, open **Settings > Capabilities > Skills**, choose upload, and select
`swiftpm-docs.zip`.

### Codex

From the root of the cloned repository, copy the skill into the `skills`
directory under `CODEX_HOME`, which defaults to `~/.codex`:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/swiftpm-docs "${CODEX_HOME:-$HOME/.codex}/skills/swiftpm-docs"
```

Use `ln -s "$(pwd)/skills/swiftpm-docs"` with the same destination to link the
directory instead. Restart Codex after installing so that it loads the new
skill.
