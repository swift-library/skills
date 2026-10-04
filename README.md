<p align="center">
  <img src="Documentation/Assets/Logo.svg" width="160" alt="skills logo">
</p>

<h1 align="center">skills</h1>

<p align="center">
  Skills for Claude and Codex that organize the documentation of Swift package repositories.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"></a>
</p>

[Overview](#overview) · [Install](#install) · [Skills](#skills) ·
[Usage](#usage) · [Contributing](#contributing) · [License](#license)

> [!NOTE]
> The collection has no tagged release yet. Every install method below uses
> the current `master` branch.

## Overview

A skill is a folder with a `SKILL.md` file and supporting material that Claude
or Codex loads when a request matches the skill's description. This collection
currently provides `swift-package-docs`, which gives each kind of documentation
in a Swift package repository one clear home: routing instructions in
`AGENTS.md`, indexes in `README` files, and proposals, current architecture,
history, governance, and reference material in their own directories.

- Scaffold the smallest documentation layout that makes these roles explicit.
- Audit an existing repository, map each file to a role, and flag misplaced or
  missing documents.
- Normalize documentation so that each file has one role and one authority.
- Export reusable repository documentation from the skill's templates.
- Choose between a `minimal` docs-first profile and a `standard` profile for a
  complete public repository.

The skill's semantics draw on
[ISO/IEC/IEEE 42010](https://www.iso-architecture.org/ieee-1471/ads/),
[arc42](https://arc42.org/documentation/), [MADR](https://adr.github.io/madr/),
and [Diataxis](https://diataxis.fr/).

## Install

The plugin marketplace installs skills by name. The other methods install a
single skill directory; do not install the repository root as a skill.

### Claude Code plugin marketplace

The repository is a Claude Code plugin marketplace named `swift-skills`. Add it
and install the skill as a plugin:

```bash
claude plugin marketplace add swift-library/skills
claude plugin install swift-package-docs@swift-skills
```

Inside Claude Code, run the same commands as `/plugin marketplace add` and
`/plugin install`.

### Claude Code skills directory

Clone the repository and copy the skill into `~/.claude/skills`:

```bash
git clone https://github.com/swift-library/skills.git
cd skills
mkdir -p ~/.claude/skills
cp -R skills/swift-package-docs ~/.claude/skills/swift-package-docs
```

To follow updates with `git pull`, link the directory instead of copying it:

```bash
ln -s "$(pwd)/skills/swift-package-docs" ~/.claude/skills/swift-package-docs
```

### Claude apps

From the root of the cloned repository, zip the skill folder:

```bash
cd skills
zip -r ../swift-package-docs.zip swift-package-docs
```

In Claude, open **Settings > Capabilities > Skills**, choose upload, and select
`swift-package-docs.zip`.

### Codex

From the root of the cloned repository, copy the skill into the `skills`
directory under `CODEX_HOME`, which defaults to `~/.codex`:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/swift-package-docs "${CODEX_HOME:-$HOME/.codex}/skills/swift-package-docs"
```

Use `ln -s "$(pwd)/skills/swift-package-docs"` with the same destination to
link the directory instead. Restart Codex after installing so that it loads the
new skill.

## Skills

| Skill | Description |
| --- | --- |
| [`swift-package-docs`](skills/swift-package-docs/SKILL.md) | Scaffold, audit, normalize, and export repository-native documentation architecture for Swift package repositories. |

## Usage

### Ask for an operation

Claude and Codex load `swift-package-docs` when a request is about the
documentation structure of a Swift package repository. Name the skill to
select it explicitly:

- "Audit this repository's documentation with swift-package-docs."
- "Use swift-package-docs to scaffold the minimal documentation layout."
- "Normalize these docs to the swift-package-docs standard profile."

The skill supports four operations:

| Operation | What it does |
| --- | --- |
| scaffold | Creates the minimum route, index, proposal, truth, history, governance, and reference layout |
| audit | Maps existing files to documentation roles, flags collisions, and identifies missing boundaries |
| normalize | Moves or rewrites documentation so that each file has one clear role and authority |
| export template | Produces repository documentation from the normalized model and the skill's templates |

For an existing repository, the skill starts with an audit and normalizes
before it exports. For large normalize, migration, or export work, it can keep
a self-contained plan based on its `assets/PLANS.md` scaffold.

### Role model

Each documentation role has one location in the target repository:

| Role | Location |
| --- | --- |
| Route | `AGENTS.md` |
| Index | `README` files |
| Proposal | `Docs/Proposals/` |
| Truth | `Docs/Architecture/` |
| History | `Docs/Decisions/`, `Docs/Migrations/`, and `Docs/Archive/` |
| Governance | `.github/` |
| Reference | `Docs/Reference/` |

`AGENTS.md` routes work and does not describe the tree. `README` files describe
the tree and do not route work. Current architecture lives only in
`Docs/Architecture/`. Proposals and history support it without replacing it.

### Profiles

- [`minimal`](skills/swift-package-docs/profiles/minimal.md): the smallest
  docs-first baseline, with `AGENTS.md`, `README.md`, `CONTRIBUTING.md`,
  `Docs/README.md`, `Docs/Architecture/README.md`, and `.github/README.md`.
- [`standard`](skills/swift-package-docs/profiles/standard.md): the minimal
  files plus proposals, decisions, migrations, archive, reference, a license,
  and the community health files and templates a public repository needs.

The [examples](skills/swift-package-docs/examples/README.md) show target trees,
export previews, and before-and-after normalizations.

### Scope

`swift-package-docs` covers documentation architecture only. It does not write
feature specifications, product requirements, or roadmaps, and it does not
orchestrate tasks, manage releases, or automate general workflows.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Each
skill lives in `skills/<skill>/`:

- `SKILL.md`: the name, description, scope, and supported operations
- `rules/`: stable invariants
- `templates/`: template sources for generated repository files
- `profiles/`: which templates each profile produces
- `examples/`: small reference examples
- `references/` and `assets/`: supporting material the skill reads

`.claude-plugin/marketplace.json` lists the skills that the Claude Code
marketplace publishes. To test changes, validate the catalog and add your
clone as a local marketplace:

```bash
claude plugin validate .
claude plugin marketplace add ./
```

Commit subjects follow Conventional Commits, and a pull request check enforces
them. [SUPPORT.md](SUPPORT.md) covers questions and bug reports, and
[GOVERNANCE.md](GOVERNANCE.md) describes how decisions are made. Report
vulnerabilities through the private route in [SECURITY.md](SECURITY.md).
Participation follows the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

The skills are available under the MIT License. See [LICENSE](LICENSE).
