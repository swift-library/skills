# Proposal In Architecture

## Problem

`Docs/Architecture/Package.md` contains:

```md
## Candidate Layout

Option A keeps proposals under `Docs/Architecture/`.
Option B creates `Docs/Proposals/`.
We should decide after the next refactor.
```

## Why It Is Misclassified

- the content compares unresolved options
- the content does not state the current canonical layout
- `Docs/Architecture/*` is for current truth, not design-in-progress

## Applicable Rules

- `rules/proposal-vs-truth-vs-history.md`

## Normalized Outcome

- move the unresolved options into `Docs/Proposals/package-docs-layout.md`
- leave only the current accepted structure in `Docs/Architecture/Package.md`

Example normalized truth:

```md
Package documentation roles are defined under `Docs/Architecture/`.
Design alternatives are kept under `Docs/Proposals/`.
```
