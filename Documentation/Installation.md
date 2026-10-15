# Installation

The `swift-skills` marketplace publishes the `swift-skills` plugin for Claude
Code and Codex. Installing it loads every skill under `skills/`. The
[catalog](Catalog.md) describes the workflows available to your agent.

## Claude Code

```bash
claude plugin marketplace add swift-library/skills
claude plugin install swift-skills@swift-skills
```

Inside Claude Code, use `/plugin marketplace add` and `/plugin install` with
the same arguments. Restart Claude Code after installing. To update:

```bash
claude plugin marketplace update swift-skills
claude plugin update swift-skills@swift-skills
```

## Codex

```bash
codex plugin marketplace add swift-library/skills --ref master
codex plugin add swift-skills@swift-skills
```

Restart Codex after installing. To refresh the marketplace:

```bash
codex plugin marketplace upgrade swift-skills
```

Check the installed version afterward. Marketplace refresh and installed-plugin
activation depend on the host version.

## Other hosts and local authoring

Agents without plugin support may copy or link individual `skills/<name>/`
directories into their skill search path. For example, from the cloned
repository root, choose an unused destination in your host's skills directory:

```bash
ln -s "$PWD/skills/swiftpm-docs" /path/to/host/skills/swiftpm-docs
```

Use either the plugin or a direct copy/link for a skill; overlapping installs
can load the same instructions twice. Remove overlapping installations when
switching methods, then restart the host. Consult each skill's `SKILL.md` for
the tools its workflow needs.

## Claude apps

From the cloned repository root, create an upload archive:

```bash
mkdir -p .build/uploads
(cd skills && zip -r ../.build/uploads/swiftpm-docs.zip swiftpm-docs)
```

In Claude, open **Settings > Capabilities > Skills**, choose upload, and select
`.build/uploads/swiftpm-docs.zip`. Use any skill name from the catalog.
