# README Standard

Use this rule for the root `README.md` of a Swift package, tool, or plugin
repository.

## Scope

The README is the landing page and a short manual. A reader should be able
to decide whether the package fits, install it, run the smallest example, and
find each product's main entry points without leaving the page.

Keep in the README:

- what the package does and for whom;
- install and quick start;
- common usage organized by task;
- requirements, links to deeper docs, contribution and license pointers.

Move out of the README and link instead:

- exhaustive option and flag tables;
- long troubleshooting catalogs;
- architecture rules and internal ownership;
- symbol-level API reference (DocC);
- change history (`CHANGELOG.md`).

Only one README is surfaced on the repository home page. GitHub picks
`.github/README.md` before the root file, so an ordinary repository must not
have `.github/README.md`.

## Header

Centered, in this shape:

```html
<p align="center">
  <img src="Documentation/Assets/Logo.svg" width="160" alt="swift-example logo">
</p>

<h1 align="center">swift-example</h1>

<p align="center">
  One sentence that says what the package does, in user terms.
</p>

<p align="center">
  <!-- badge block from readme_facts.py --badges -->
</p>
```

- Use the repository's existing documentation directory for assets
  (`Documentation/Assets/` or `Docs/Assets/`).
- Without a logo, drop the image paragraph and keep the rest.
- The value sentence matches the GitHub About description.

## Body Order

1. Anchor navigation: `[Overview](#overview) · [Install](#install) · ...`,
   one entry per level-2 section that follows.
2. Status note as a GitHub alert (`> [!NOTE]`), one or two sentences of real
   status: pre-1.0 source stability, or no tagged release yet and how to
   depend on the default branch.
3. `## Overview`: what it does and why, then a short capability list.
4. `## Install`: the SwiftPM dependency from `readme_facts.py --install` and
   the `.product(name:package:)` lines the reader needs. Tools add their
   install commands (Homebrew, Mint, release download) only when those
   channels exist.
5. `## Quick start`: the smallest complete example that builds as written.
6. `## Products`: a table of product and purpose, when there is more than one
   product.
7. `## Usage`: task-oriented `###` subsections covering every product's main
   entry points.
8. `## Requirements`: Swift version and platforms, consistent with the badges.
9. `## Documentation`: links to files and DocC catalogs that exist.
10. `## Contributing`: links to `CONTRIBUTING.md` and `SECURITY.md` when they
    exist.
11. `## License`: license name, links to `LICENSE` and `NOTICE`, and any
    attribution such as "adapted from" or "derived from".

Omit a section that would be empty. Add a section such as `## Command-line
usage` or `## Configuration` when the package has that surface.

## Badges

- CI: the workflow badge for the default branch, linking to the workflow.
- Swift: the minimum tools version.
- Platforms: declared platforms, plus Linux only when CI builds on Linux.
- License: SPDX identifier, linking to the license file.

Generate them; never type badge values by hand.

## Writing

- English, present tense, current user-facing facts.
- Complete sentences and plain words; serial comma; consistent spelling.
- Analogies to well-known Swift or Apple APIs are welcome when accurate.
- Compatibility notes go next to the behavior they qualify.
- Code fences carry a language tag (`swift`, `bash`, `text`, `json`).
- Every API, product, command, and flag shown exists in public source.
- Command output shown in the README is real output.
- No emoji, no marketing superlatives, no "simply" or "just".

## Public Content

The README, its images, and the About text are public. Keep out:

- absolute local paths, usernames, and machine names;
- agent state, workspace notes, task logs, and local evidence;
- internal tool, team, or process names;
- statements about how the project compares with the projects it was
  derived from, other than attribution.
