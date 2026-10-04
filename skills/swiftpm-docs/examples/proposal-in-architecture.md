# Proposal In Architecture

## Problem

`Documentation/Architecture/Package.md` contains:

```md
## Candidate Layout

Option A keeps proposals under `Documentation/Architecture/`.
Option B creates `Documentation/Proposals/`.
We should decide after the next refactor.
```

## Why It Is Misclassified

- the content compares unresolved options
- the content does not state the current canonical layout
- `Documentation/Architecture/*` is for current truth, not design-in-progress

## Applicable Rules

- `rules/proposal-vs-truth-vs-history.md`

## Normalized Outcome

- move the unresolved options into `Documentation/Proposals/PackageDocsLayout.md`
- leave only the current accepted structure in `Documentation/Architecture/Package.md`

Example normalized truth:

```md
Package documentation roles are defined under `Documentation/Architecture/`.
Design alternatives are kept under `Documentation/Proposals/`.
```
