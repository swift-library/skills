# Route In README

## Problem

`Docs/README.md` contains:

```md
If the task is a docs normalization pass, read `Docs/Architecture/` first and
stop if release automation is requested.
```

## Why It Is Misclassified

- the sentence is task-driven
- the sentence tells an agent when to read and when to stop
- `README` files are for index, scope, and placement guidance

## Applicable Rules

- `rules/route-vs-index.md`

## Normalized Outcome

- move the task-driven sentence into `AGENTS.md`
- keep `Docs/README.md` focused on tree and placement

Example normalized index:

```md
`Docs/Architecture/` holds current truth.
`Docs/Proposals/` holds design-in-progress.
```
