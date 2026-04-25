# README Layering

Use this rule when deciding how much responsibility a `README` file should
carry.

## Principle

`README` files are indexes, but not all indexes have the same audience.

- Root `README.md` is the public landing page.
- `Docs/README.md` is the documentation reading index.
- `Docs/Architecture/README.md` is the architecture reading index.
- `Docs/Architecture/*.md` owns current architecture rules and descriptions.

## Root README

Root `README.md` should answer:

- what this repository is
- what it is for
- how to install, run, or enter the project
- where to read next

Keep root `README.md` concise and outward-facing. It may link to architecture,
governance, and docs indexes, but should not restate detailed architecture
rules or internal ownership models.

## Docs README

`Docs/README.md` should answer:

- what documentation areas exist
- where each documentation category belongs
- which subtree to read for deeper context

It is the reading index for documentation, not the public landing page.

## Architecture README

`Docs/Architecture/README.md` should answer:

- what architecture documents exist
- which file owns each current architecture concern
- where to read current truth

It is an index for architecture files, not the architecture description itself.

## Normalization Guidance

- Move public overview and install/setup instructions to root `README.md`.
- Move docs-tree navigation to `Docs/README.md`.
- Move architecture-file navigation to `Docs/Architecture/README.md`.
- Move current architecture rules into named files under `Docs/Architecture/`.
- Prefer a short link over duplicating architecture rules in root `README.md`.
