<div align="center">

<p align="center">
  <a href="https://github.com/swift-library/skills"><img src="Documentation/Assets/Logo.svg" width="160" alt="skills logo"></a>
</p>

<h1 align="center">skills</h1>

<p align="center">
  Build and maintain Swift packages and Apple apps with agent skills in a single plugin.
</p>

<p align="center">
  <a href="https://github.com/swift-library/skills/actions/workflows/ci.yml"><img src="https://github.com/swift-library/skills/actions/workflows/ci.yml/badge.svg?branch=master" alt="CI"></a>
  <a href="LICENSE.txt"><img src="https://img.shields.io/badge/license-Apache--2.0-blue?style=flat" alt="License: Apache-2.0 WITH Swift-exception"></a>
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#quick-look">Quick look</a> ·
  <a href="#install">Install</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#documentation">Documentation</a> ·
  <a href="#contributing">Contributing</a> ·
  <a href="#license">License</a>
</p>

</div>

## Overview

The collection covers package architecture, Apple frameworks, interface design, developer tools, documentation, and release engineering. Each skill carries a focused trigger and supporting guidance; your agent selects it when a task matches, and the [catalog](Documentation/Catalog.md) helps you find the right workflow.

## Quick look

Install the collection in Claude Code:

```sh
claude plugin marketplace add swift-library/skills
claude plugin install swift-skills@swift-skills
```

## Install

The `swift-skills` plugin installs the whole collection in Claude Code or Codex. For Codex CLI 0.147.0 or later:

```sh
codex plugin marketplace add swift-library/skills --ref master
codex plugin add swift-skills@swift-skills
```

Restart your host after installing. The [installation guide](Documentation/Installation.md) covers updates and other hosts.

> [!NOTE]
> The collection has no tagged release. Installation uses the current `master` branch.

## Usage

Claude and Codex select a skill automatically when a request matches its
description. Name the skill to select it explicitly:

- "Audit this repository's documentation with swiftpm-docs."
- "Use swift-concurrency-patterns to fix these Sendable diagnostics."
- "Check this package's README and Quick start with swiftpm-readme."
- "Run the swiftpm-github-release checks before I make this repository public."

When two skills could apply, the more specific one should win: a SwiftUI
rendering question belongs to `swiftui-performance` rather than
`swiftui-patterns`, and a framework review belongs to that framework's skill
rather than `swift-programming-language`. [AGENTS.md](AGENTS.md) records the
routing for pairs that overlap.

Skills with scripts need the tools those scripts call, such as `git`, `swift`,
`xcodebuild`, or Python 3. The skill's `SKILL.md` or `scripts/README.md` names
them.

## Requirements

- An agent host that can load `SKILL.md` instructions, such as the hosts in the [installation guide](Documentation/Installation.md)
- The SDKs and tools named by the individual skill for its task; the collection itself declares no Swift compiler floor

## Documentation

- [Skill catalog](Documentation/Catalog.md)
- [Installation guide](Documentation/Installation.md)
- [Documentation index](Documentation/README.md)
- [Skill authoring architecture](Documentation/Architecture/skill-authoring.md)

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. Each
skill lives in `skills/<skill>/`:

- `SKILL.md`: the trigger description, scope, workflow, validation rules, and
  output format
- `agents/openai.yaml`: display name, short description, and default prompt
  for Codex
- optional `rules/`, `references/`, `knowledge/`, `profiles/`, `templates/`,
  `examples/`, `scripts/`, `cli/`, and `assets/`, each with an index when it
  holds more than one file

[Skill authoring](Documentation/Architecture/skill-authoring.md) defines the
structure, trigger contract, and validation checklist for new or changed
skills. The Claude and Codex marketplaces each publish the root `swift-skills`
plugin. Run `Scripts/check` before pushing; it validates both hosts' manifests,
distribution regression tests, and documentation template exports. Use the
[isolated installation checks](Documentation/Architecture/skill-authoring.md#plugin-distribution)
when changing plugin distribution.

Commit subjects and pull request titles follow Conventional Commits. The shared
policy checks pull request titles and added lines. [SUPPORT.md](SUPPORT.md) covers questions and bug reports, and
[GOVERNANCE.md](GOVERNANCE.md) describes how decisions are made. Report
vulnerabilities through the private route in [SECURITY.md](SECURITY.md).
Participation follows the [Code of Conduct](https://github.com/swift-library/.github/blob/master/CODE_OF_CONDUCT.md).

## License

The skills are licensed under the Apache License 2.0 with the Swift Runtime
Library Exception, so code copied from a skill into an app needs no
attribution. See [LICENSE.txt](LICENSE.txt) and [NOTICE](NOTICE). Material from other
authors keeps its own license, noted in the skill that includes it.
