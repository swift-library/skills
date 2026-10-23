---
name: swiftpm-readme
description: SwiftPM README fact checks and content for badge values, Install, compiling Quick start examples, Products, Usage and Requirements. Verify tags, Package.swift, topics and About claims. Not for README visual layout, GitHub settings changes or release tagging.
---

# SwiftPM README

## Purpose

Supply the Swift-specific facts and content of a Swift package repository's
README and GitHub metadata, each verified against the manifest, tags, CI,
public source, and the published package: badge values, the Install snippet
and build-from-source commands, a Quick start that builds as written, and
Products, Usage, and Requirements sections that name only what exists.

## When To Use

- Badge values for a Swift package need deriving or checking: Swift tools
  version, platforms, license, and CI workflow.
- Install or Quick start snippets need to be written or verified against the
  published repository and tags.
- Products, Usage, or Requirements sections need writing or a fact check
  against public source.
- A Swift package needs topic proposals, or its About sentence needs checking
  against what the package does.
- Checking SwiftPM dependency/product install lines and build-from-source commands, and resolving and compiling Quick start code against the published tag.

## When Not To Use

- README first-screen composition: header, logo placement, which badges
  appear and in what order and style, navigation, section skeleton, and
  section names. The repository's GitHub presentation owner decides these
  from the applicable design standard.
- Social preview cards, terminal demos, logo banners, organization profiles,
  and preview uploads.
- Install channels outside SwiftPM and Mint, such as Homebrew or release
  downloads, CLI command references, and MCP client configuration; their
  owners supply them.
- Applying About, topics, homepage, or other repository settings.
- Deciding what belongs in the README versus the documentation tree, or DocC
  catalog placement.
- Drawing logos, designing package APIs or module boundaries, creating tags
  or releases, or writing user interface text inside an app.

## Inputs To Inspect

- `Package.swift`: name, products, Swift tools version, and platforms.
- The `origin` remote, default branch, and released tags.
- Existing `README.md`, `.github/README.md`, `LICENSE`, `NOTICE`, and CI
  workflow files under `.github/workflows/`.
- Public source: every API named in the README must exist there.
- The section skeleton: which Swift sections the README has, their names
  (for example "Quick look" or "Quick start"), whether the snippet section
  holds Swift code or another demonstration such as a recorded terminal
  session, and whether it has a status note. It is the caller's decision, or
  the existing README's sections when revising.
- Documentation placement decisions: which content the documentation owner
  keeps in the README and which documents the README links to.
- Current About description and topics
  (`gh repo view OWNER/REPO --json description,repositoryTopics,homepageUrl`).

## Workflow

1. Collect facts with `scripts/readme_facts.py REPO`. Owner, name, default
   branch, latest tag, tools version, platforms, license, CI workflow, and
   badge values come from the repository, never from memory.
2. Read the public source and existing docs. List the products, their main
   entry points, and any behavior the README must state accurately.
3. Write or revise the Swift sections the skeleton names, following
   `rules/readme-sections.md` and `templates/sections.md.tpl`. Paste the
   dependency line from `readme_facts.py REPO --install` unchanged. Return the
   `badges` values for the presentation owner to compose into badge markup.
4. Verify:
   - `scripts/check_readme.py REPO` for a shadowing README, links and
     anchors, alt attributes, local paths, the install owner, version, and
     branch, and badge values;
   - when the snippet section holds Swift code,
     `scripts/quickstart_check.py REPO --section TITLE` to resolve the Install
     requirement from the published URL and build that code in a scratch
     consumer;
   - for a terminal demo, check it against the recording source and validation
     the repository declares, and leave rendering to the presentation owner
     (`github-readme-design` when installed). A repository whose CI implements
     a demo re-recording check, such as a shared workflow's `demo` option,
     re-records with that check.

   When the documentation owner surfaces `.github/README.md`, pass
   `--readme .github/README.md` to both checkers; the path is relative to
   `REPO`.
5. Propose Swift ecosystem topics and check the About sentence's claims with
   `rules/topics-and-about.md`. Report proposals; do not apply them.

## Reference Files To Consult

- `rules/readme-sections.md`: badge values, Install, Quick start, Products,
  Usage, Requirements, and fact rules. Read for any README work.
- `rules/topics-and-about.md`: Swift topics, About claim checks, and homepage
  candidates. Read when proposing repository metadata.
- `templates/README.md`: the template catalog.
- `scripts/README.md`: script usage, dependencies, and exit codes.

## Decision Rules

- Facts beat prose. When the README disagrees with the manifest, tags, CI, or
  source, fix the README.
- With no released tag, the Install snippet depends on the default branch and
  the README says so. Never invent a version.
- For a 0.x tag, use `.upToNextMinor(from:)`; from 1.0, use `from:`.
- A badge value equals the `readme_facts.py` value for its kind. A kind with
  no backing fact has no value to supply.

## Validation Rules

- `check_readme.py` exits 0.
- For a Swift snippet section, `quickstart_check.py` resolves the published
  requirement and builds; any command the section shows has been run with its
  output matching.
- Every API, product, command, and option named in the README exists in the
  public source at the referenced tag or default branch.
- The About sentence claims nothing the source does not support.

## Output Format

```text
Repository: <owner>/<name> @ <branch or tag>
Facts: tools <x>, platforms <list>, latest tag <tag or none>, license <id>
Badge values: <kind: value, ...>
Sections: <written / revised / unchanged>, <section names>
Checks: check_readme <pass / n findings>; quickstart <pass / fail: reason>
Topics: <proposed list>; About claims <consistent / findings>
Not verified: <items and why>
```

## Failure / Uncertainty Handling

- If the Quick start cannot build (missing tag, private dependency, platform
  SDK unavailable), report the exact failing command and error. Do not
  publish an unverified snippet as working.
- If a behavior cannot be confirmed from source or by running it, leave it
  out or mark it in the report as unverified.
- If there is neither an existing README nor a supplied skeleton, write no
  README sections, return the facts and check results, and report that the
  skeleton decision is needed.
