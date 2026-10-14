<div align="center">

<p align="center">
  <a href="https://github.com/swift-library/skills"><img src="Documentation/Assets/Logo.svg" width="160" alt="skills logo"></a>
</p>

<h1 align="center">skills</h1>

<p align="center">
  Agent skills for Swift packages and Apple platforms, installable individually.
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

Each skill packages its trigger, instructions, and supporting files in its own directory. Your agent host loads it when a task matches the trigger; the [catalog](Documentation/Catalog.md) helps you choose.

## Quick look

Add the marketplace and install the documentation skill:

```sh
claude plugin marketplace add swift-library/skills
claude plugin install swiftpm-docs@swift-skills
```

## Install

Choose the [installation method](Documentation/Installation.md) for your agent host. Install an individual skill directory rather than the repository root.

> [!NOTE]
> The collection has no tagged release. Installation uses the current `master` branch.

## Usage

Claude and Codex select a skill automatically when a request matches its
description. Name the skill to select it explicitly:

- "Audit this repository's documentation with swiftpm-docs."
- "Use swift-concurrency-patterns to fix these Sendable diagnostics."
- "Check this package's README and Quick start with swiftpm-readme-design."
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
skills. `.claude-plugin/marketplace.json` lists the skills that the Claude Code
marketplace publishes. To test changes, validate the catalog and add your
clone as a local marketplace:

```bash
claude plugin validate .
claude plugin marketplace add ./
```

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
