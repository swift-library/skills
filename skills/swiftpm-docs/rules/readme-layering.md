# README Layering

Use this rule when deciding how much responsibility a `README` file should
carry.

## Principle

`README` files are entry points, but not all entry points have the same
audience.

- Root `README.md` is the GitHub-facing landing manual and entry index.
- `Documentation/README.md` is the documentation reading index.
- `Documentation/Architecture/README.md` is the architecture reading index.
- `Documentation/Architecture/*.md` owns current architecture rules and descriptions.
- `Sources/<Target>/<Target>.docc/` owns target-level API documentation for
  Swift modules when DocC is present.

GitHub recognizes README files in `.github`, root, and `docs` directories. For
ordinary Swift package repositories, default to the root `README.md` as the
surfaced repository landing page. Use `.github/README.md` only for special
GitHub profile or default community-health repositories, or when the target
explicitly wants that file to be surfaced.

## Root README

Root `README.md` should answer:

- what this repository is
- what it is for
- how to install, run, or enter the project
- the common happy-path usage or commands for the primary audience
- the most important output, artifacts, or integration points
- where to read next

It may link to target-level DocC catalogs, but should not duplicate
symbol-level API reference content.

For a user-facing package, CLI, tool, app, or library, do not reduce root
`README.md` to a documentation-tree directory. Keep the install/setup/manual
surface that a GitHub reader needs to try or evaluate the project. Concise
means summarize and link out, not delete common usage.

Root `README.md` may link to architecture, governance, and documentation
indexes, but should not restate detailed architecture rules or internal
ownership models. Full option tables, long troubleshooting catalogs,
architecture truth, and symbol-level API reference should move to
`Documentation/Reference/*`, `Documentation/Architecture/*`, or target-level
DocC as appropriate, with a short summary retained in the root README.

## Documentation README

`Documentation/README.md` should answer:

- what documentation areas exist
- where each documentation category belongs
- which subtree to read for deeper context

It may point readers to DocC catalogs under `Sources/<Target>/`, but DocC
catalogs are not part of the `Documentation/` tree by default.

It is the reading index for documentation, not the public landing page.

## Architecture README

`Documentation/Architecture/README.md` should answer:

- what architecture documents exist
- which file owns each current architecture concern
- where to read current truth

It is an index for architecture files, not the architecture description itself.

## Normalization Guidance

- Move public overview, install/setup instructions, quick start, common usage,
  and representative examples to root `README.md`.
- Remove `.github/README.md` from ordinary repositories when it collides with
  the root landing manual.
- Move documentation-tree navigation to `Documentation/README.md`.
- Move architecture-file navigation to `Documentation/Architecture/README.md`.
- Move current architecture rules into named files under
  `Documentation/Architecture/`.
- Preserve canonical documentation path casing such as
  `Documentation/Architecture/` and `Documentation/Reference/` during tree
  normalization, and use PascalCase Markdown document names for non-README
  documentation in those role directories.
- Move exhaustive CLI option tables, output contracts, and troubleshooting
  catalogs to `Documentation/Reference/*`, while keeping a common-case summary
  in root `README.md`.
- Keep module API DocC catalogs colocated with SwiftPM targets, normally under
  `Sources/<Target>/<Target>.docc/`.
- Prefer a short link over duplicating architecture rules in root `README.md`.
