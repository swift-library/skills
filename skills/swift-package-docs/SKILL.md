---
name: swift-package-docs
description: Scaffold, audit, normalize, and export repository-native documentation architecture for Swift package repositories. Use this skill for Route/Index/Proposal/Truth/History/Governance/Reference shaping. For larger normalize or export work, it may also use a PLANS.md scaffold as an execution aid. Do not use it for feature specs, product planning, task orchestration, release management, or general workflow automation.
---

# Swift Package Docs

## Purpose

Shape Swift package repositories so documentation roles are explicit,
repo-native, and easy to maintain.

## Scope

In scope:

- scaffold a minimal documentation architecture
- audit an existing repo against the role model
- normalize misplaced documentation into the right role
- export target-repository docs after normalization

Out of scope:

- feature specification workflows
- product requirements or roadmap planning
- task orchestration
- release process management
- general engineering workflow automation

## External Foundations

This skill draws on a few established documentation frameworks:

- [ISO/IEC/IEEE 42010: Architecture Descriptions](https://www.iso-architecture.org/ieee-1471/ads/)
  for architecture-description semantics
- [arc42 Documentation](https://arc42.org/documentation/) for architecture
  documentation coverage
- [MADR](https://adr.github.io/madr/) for decision-record structure
- [Diataxis](https://diataxis.fr/) for documentation type separation

These references inform the skill's semantics and boundary rules. They do not
directly dictate the repository tree.

## Supported Operations

### scaffold

Create the minimum route, index, proposal, truth, history, governance, and
reference layout for a Swift package repository.

### audit

Map existing files to documentation roles, flag collisions, and identify
missing boundaries.

### normalize

Move or rewrite documentation so each file has one clear role and authority.

### export template

Produce target-repository docs from the normalized source model and skill-local
template sources. The export is a copy for reuse, not the authority.

## Execution Plans

For large normalize, migration, or export work, use `assets/PLANS.md` as a
durable execution-plan scaffold.

- Keep the plan self-contained so another session can resume from it.
- Update discoveries, decisions, validation, and next actions as work
  progresses.
- Treat the plan as an execution aid only. It does not replace architecture
  truth, proposal docs, or decision records.
- Read `references/codex-exec-plans.md` when deciding how much structure to
  use.

## Role Model

- Route: `AGENTS.md`
- Index: `README`-class files
- Proposal: `Docs/Proposals/*`
- Truth: `Docs/Architecture/*`
- History: `Docs/Decisions/*`, `Docs/Migrations/*`, `Docs/Archive/*`
- Governance: `.github/*`
- Reference: `Docs/Reference/*`

## Hard Boundaries

- Keep Route and Index separate. `AGENTS.md` routes work; it does not explain
  the tree. `README` files explain the tree; they do not route work.
- Keep design-in-progress in `Docs/Proposals/*`. Proposal space is neither
  current truth nor historical record.
- Keep current truth in `Docs/Architecture/*`, not in decision logs, migration
  notes, archives, or proposals.
- Treat `Docs/Architecture/*` as the primary current architecture description.
  Proposal, history, and reference materials support that description; they do
  not replace it.
- Keep historical context in `Docs/Decisions/*`, `Docs/Migrations/*`, and
  `Docs/Archive/*`, not in current architecture files or proposal drafts.
- Keep GitHub-facing policy and templates in `.github/*`.
- Keep reference material in `Docs/Reference/*`.
- Treat exported output as downstream only. It must trace back to this skill
  and the normalized repo structure.
- Author template source files from the target repository's perspective, not
  from the `swift-skills` collection's perspective.
- Do not expose collection-internal production terminology in generated target
  templates.

## Operating Defaults

- Start with audit when a repo already exists.
- Prefer the smallest real skeleton that makes the boundaries obvious.
- Normalize before exporting any template.
- Compose scaffold and export outputs from explicit profile guidance, not
  ad-hoc file lists.
- Treat `minimal` as the docs-first baseline: the smallest stable repo shape
  that makes Route, Index, Truth, and Governance explicit.
- Treat `standard` as the first public-repo-complete baseline: it extends
  beyond `minimal` with fuller proposal, history, reference, and
  GitHub/community-health coverage.
- Keep the `minimal` / `standard` distinction intentional unless product
  strategy changes deliberately.
- Favor crisp README indexes over long essays.
- Allow target trees to vary by profile. Minimal and standard trees are both
  valid when the role boundaries stay intact.

## Minimal Example Target Tree

```text
<swift-package-repo>/
  AGENTS.md
  README.md
  CONTRIBUTING.md
  Package.swift
  Sources/
  Tests/
  Docs/
    README.md
    Architecture/
      README.md
  .github/
    README.md
```

## Standard Example Target Tree

Use the standard profile when normalizing a more established package repo. See
`profiles/standard.md` and `examples/standard-target-tree.md`.
