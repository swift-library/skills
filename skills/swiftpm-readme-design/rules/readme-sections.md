# README Sections

Use this rule for the Swift-specific sections of a Swift package, tool, or
plugin repository's root `README.md`. The header, badge selection, order and
styling, navigation, section skeleton, and section names come from the
repository's presentation decisions; this rule fills the sections that
skeleton contains.

## Scope

A reader should be able to install the package, build the smallest example,
and find each product's main entry points from these sections:

- Install: the SwiftPM dependency and the products a target needs.
- Quick start, or the skeleton's equivalent such as Quick look, when it holds
  Swift code: the smallest complete example that builds as written. A recorded
  terminal session in that section belongs to the presentation owner.
- Products: each product and its purpose, when there is more than one.
- Usage: task-oriented subsections covering every product's main entry
  points.
- Requirements: Swift version and platforms.

The documentation owner decides which content stays in the README and which
documents it links to. Link only to documents that exist.

GitHub surfaces `.github/README.md` before the root file. Whether one is
intended is the documentation owner's decision. `check_readme.py` checks the
root README by default and reports a `.github/README.md` that shadows it; when
the documentation owner surfaces `.github/README.md`, pass
`--readme .github/README.md` (relative to the repository) to both
`check_readme.py` and `quickstart_check.py`.

## Badge Values

`readme_facts.py` reports a value for each kind that a repository fact backs:

- `ci`: the CI workflow file on the default branch.
- `swift`: the minimum tools version, as `X.Y+`.
- `platforms`: declared platforms, plus Linux only when CI builds on Linux.
- `license`: the SPDX identifier and the license file it links to.

The presentation owner composes the markup, colors, order, and labels. Do not
type badge values by hand. Do not add the Swift bird or Apple logos to a badge,
for example with a shields.io `logo=swift` parameter, unless the owner has
accepted those trademarks' terms for this use.

## Install

- Paste the dependency line from `readme_facts.py --install` unchanged, and
  add the `.product(name:package:)` lines the reader needs.
- With no released tag, depend on the default branch and say so next to the
  snippet or in the skeleton's status note. Never invent a version.
- For a 0.x tag, use `.upToNextMinor(from:)`; from 1.0, use `from:`.
- Tools add their install commands (Homebrew, Mint, release download) only
  when those channels exist.

## Quick Start

- When the section holds Swift code, it is the smallest complete example that
  builds as written against the published requirement; `quickstart_check.py`
  builds it.
- Keep imports meaningful and match the current public API.
- Command output shown next to it is real output from the documented version.

## Products, Usage, and Requirements

- Products: a table of product and purpose when there is more than one.
- Usage: `###` subsections by task, each with a short explanation and a
  `swift` snippet that uses public API.
- Requirements: the Swift version and platforms, equal to the badge values.

Omit a section the skeleton does not contain or that would be empty. A Swift
surface the package actually has, such as command-line usage or
configuration, gets a section only when the skeleton names one.

## Facts

- Every API, product, command, and flag shown exists in public source at the
  referenced tag or default branch.
- Code fences carry a language tag (`swift`, `bash`, `text`, `json`).
- Compatibility notes go next to the behavior they qualify.
- Analogies to well-known Swift or Apple APIs are welcome when accurate.

## Public Content

The README is public. Keep out absolute local paths, usernames, and machine
names; agent state, workspace notes, task logs, and local evidence; and
internal tool, team, or process names.
