---
name: swiftpm-readme-design
description: Design, write, and audit the public face of Swift package repositories on GitHub. Use for README headers with an existing logo, badges derived from repository facts, manual-style README section structure, Install and Quick start snippets that must resolve and compile against published tags, GitHub About descriptions and topics, organization profile READMEs, social preview cards, logo-row banners, and terminal demo images rendered from real command output. Produces README edits, About and topics proposals, verification results, and generated SVG assets. Do not use for drawing or redesigning logos, documentation directory architecture, package API or module architecture, release tagging or publishing, or general Swift coding.
---

# SwiftPM README Design

## Purpose

Make a Swift package repository easy to evaluate and adopt from its GitHub
page: a recognizable header, accurate badges, a README that works as a short
manual, snippets that compile against what is actually published, and a
consistent About, topics, and preview image.

## When To Use

- A package README needs a header, badges, structure, or a full rewrite.
- Install or Quick start snippets need to be written or verified against the
  published repository and tags.
- A repository's About description, topics, or social preview needs to be set
  or made consistent with the README.
- An organization needs a profile README, a logo-row banner, or a consistent
  storefront across repositories.
- A command-line tool needs a terminal demo image built from real output.

## When Not To Use

- Drawing, redesigning, or generating a logo. This skill places an existing
  logo; when none exists it keeps a text header and reports the gap.
- Deciding the documentation tree, DocC catalog placement, or which documents
  own architecture and reference content.
- Designing package APIs, targets, or module boundaries.
- Creating tags, GitHub releases, release notes, or publish automation.
- Writing user interface text inside an app.

## Inputs To Inspect

- `Package.swift`: name, products, Swift tools version, and platforms.
- The `origin` remote, default branch, and released tags.
- Existing `README.md`, `.github/README.md`, `LICENSE`, `NOTICE`,
  `CHANGELOG.md`, `CONTRIBUTING.md`, `SECURITY.md`, and the documentation
  directory (`Documentation/` or `Docs/`).
- CI workflow files under `.github/workflows/`.
- Public source: every API named in the README must exist there.
- The existing logo file, if any, and the organization's other READMEs when
  the repository should match a family style.
- Current About description, topics, and homepage
  (`gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl`).

## Workflow

1. Collect facts with `scripts/readme_facts.py REPO`. Owner, name, default
   branch, latest tag, tools version, platforms, license, and CI workflow come
   from the repository, never from memory.
2. Read the public source and existing docs. List the products, their main
   entry points, and any behavior the README must state accurately.
3. Write or revise the README with `rules/readme-standard.md` and
   `templates/README.md.tpl`. Paste the badge block from
   `readme_facts.py REPO --badges` and the dependency line from
   `readme_facts.py REPO --install` unchanged.
4. Place the logo by following `rules/visual-assets.md`. Do not draw one.
5. Verify the README:
   - `scripts/check_readme.py REPO` for links, anchors, alt text, emoji,
     install facts, and a README that shadows the root one;
   - `scripts/quickstart_check.py REPO` to resolve the Install requirement
     from the published URL and build the Quick start in a scratch consumer.
6. Propose the About description, topics, and homepage with
   `rules/repository-surface.md`. Apply them only when asked.
7. Generate surface assets when requested:
   - `scripts/social_preview.py` for a 1280x640 card from the logo and the
     About sentence;
   - `scripts/logo_row.py` for an organization banner from existing logos;
   - `scripts/terminal_svg.py` for a terminal demo from a real transcript.
   Preview each in light and dark themes before use.
8. For an organization, write `profile/README.md` in the organization's
   `.github` repository from `templates/profile.README.md.tpl`, using each
   repository's About sentence.

## Reference Files To Consult

- `rules/readme-standard.md`: header, badges, section order, writing, and
  what belongs in a README. Read for any README work.
- `rules/repository-surface.md`: About, topics, homepage, social preview,
  organization profile, and banner. Read when touching GitHub settings or
  organization pages.
- `rules/visual-assets.md`: logo placement, theme checks, terminal demos, and
  licensing limits on fonts, symbols, and third-party marks. Read before
  adding or generating any image.
- `templates/README.md`: the template catalog.
- `scripts/README.md`: script usage, dependencies, and exit codes.

## Decision Rules

- Facts beat prose. When the README disagrees with the manifest, tags, CI, or
  source, fix the README.
- With no released tag, the Install snippet depends on the default branch and
  the status note says so. Never invent a version.
- For a 0.x tag, use `.upToNextMinor(from:)`; from 1.0, use `from:`.
- Only four badge kinds: CI, Swift, platforms, and license. Omit the CI badge
  when there is no CI workflow. Do not add download, star, or coverage badges
  that need third-party services the repository does not use.
- The README describes the current product. Roadmaps, internal process, agent
  or workspace wording, local paths, and comparisons with the project's
  sources stay out. Attribution goes in the License section and `NOTICE`.
- Keep the README a manual for the common path. Move exhaustive option
  tables, long troubleshooting, and architecture detail to the documentation
  directory and link to them.
- Generated images contain no live text that depends on installed fonts:
  convert text to outlines from a font whose license allows it.

## Validation Rules

- `check_readme.py` exits 0.
- `quickstart_check.py` resolves the published requirement and builds; any
  command the Quick start shows has been run with its output matching.
- Every API, product, command, and option named in the README exists in the
  public source at the referenced tag or default branch.
- Badge values equal `readme_facts.py` output.
- The About description and the README value sentence say the same thing.
- Images render on both a white and a dark background.

## Output Format

```text
Repository: <owner>/<name> @ <branch or tag>
Facts: tools <x>, platforms <list>, latest tag <tag or none>, license <id>
README: <created / revised / unchanged>, sections <list>
Checks: check_readme <pass / n findings>; quickstart <pass / fail: reason>
About: "<sentence>"; topics <list>; homepage <url or none>
Assets: <files generated or none>
Not verified: <items and why>
```

## Failure / Uncertainty Handling

- If the Quick start cannot build (missing tag, private dependency, platform
  SDK unavailable), report the exact failing command and error. Do not
  publish an unverified snippet as working.
- If a behavior cannot be confirmed from source or by running it, leave it
  out or mark it in the report as unverified.
- If the repository has no logo, keep the text header and report that a logo
  is missing.
- If GitHub settings cannot be changed with the available permissions,
  report the exact values to set.
