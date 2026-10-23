---
name: swift-interface-distiller-patterns
description: swift-interface-distiller public API inspection and revision comparison from packages, symbol graphs, binary modules or C/Objective-C headers. Produce budgeted interface queries and slices with completeness notes. Not for runtime behavior or SemVer policy.
---

# Interface Distiller Patterns

## Purpose

Use swift-interface-distiller to turn compiler observations into public API
context an agent can read, query and compare. Own the collection choices,
interface selection and interpretation of evidence. Preserve configuration,
scope, provenance and gaps alongside the selected declarations.

The command examples follow the v0.3.1 CLI contract. Confirm the executable's
version and help before use; read the matching upstream documentation when
using another version.

## When To Use

- Understand an unfamiliar dependency's types, members, protocol requirements
  or construction API without walking its implementation.
- Give an agent a focused public interface under a symbol or byte budget.
- Review additions, removals and field changes between package revisions or
  releases collected under the same configuration and scope.
- Inspect an existing snapshot or normalize producer-supplied symbol graphs.
- Collecting local packages, symbol graphs, binary modules, or C/Objective-C headers into interface views, queries, slices, and comparisons with explicit configuration and completeness.

## When Not To Use

- Choosing a SemVer bump, enforcing a release gate or governing baselines.
- Finding implementation usages, navigating source files or answering index
  questions.
- Explaining runtime behavior, hidden defaults, macro expansion or which
  protocol implementation the compiler selects as a witness.
- Treating an interface projection as compilable replacement source.

## Inputs To Inspect

- The API question, input kind, package/revision identity and selected modules.
- Available snapshots and their collector, toolchain, SDK, target,
  configuration and scope identities.
- For collection: the actual compiler/SDK, deployment target, build and
  language modes, conditions, traits and declared environment.
- For graphs or binary modules: the producer's configuration and content
  roots. The current machine's detected configuration cannot reconstruct them.
- Desired format, documentation depth, roots, byte/symbol budgets and whether
  the limit covers the payload or the entire delivered artifact.
- The target repository's ignored output location, normally under `.build/`.

## Workflow

1. Bound the task to observed public API. Prefer a usable existing snapshot
   when compilation is unnecessary. Read
   [commands](references/commands.md) for installation and the selected input
   path; package collection may build code and run package plugins.
2. Verify `interface-distiller --version` and `--help`. Install through
   Homebrew or build a selected release with SwiftPM when needed. Keep the
   tool checkout and outputs in their owning workspace locations.
3. Select the collection configuration explicitly. Generate detected settings
   only for a build performed here, review them, then pass `--configuration`.
   For externally produced inputs, use the producer's recorded settings.
   Record source/revision and dependency identities; no build matrix is
   inferred. SDK path and identity must agree, and the triple must carry the
   deployment floor recorded by `deploymentTarget`.
4. Collect the selected package, normalize graphs, collect a binary module or
   collect headers. Default package scope is public/open library products;
   `--module` replaces that set and `--dependency-module` adds explicitly
   selected modules from the resolved graph. Do not infer a module name from
   a repository's display name. Exclusion globs win over inclusion.
5. Read the snapshot header and gaps before the declarations. Render the
   default interface with summary docs, then use `--docs full`, `--docs none`,
   `--show-implied` or `--view evidence` according to the question. The evidence
   view and canonical JSON retain details collapsed in the readable view.
6. Query a type or symbol, then slice only the needed reference closure. Choose
   JSON, Swift or Markdown before setting the budget. Read
   [interpretation](references/interpretation.md) for budget accounting,
   external references and truncation. Measure the entire output when the
   consumer has a hard total byte limit.
7. To review changes, collect both revisions with one collector and matching
   build configuration and scope. Compare the snapshots and report interface,
   documentation, availability and provenance observations separately. Use
   baseline write/check only when baseline management is part of the task.
8. Return the selected context or comparison with its source identity,
   configuration/scope, actual size, collection gaps and selection state.
   State what the observations cannot answer.

## Reference Files To Consult

- [Command recipes](references/commands.md): installation, input adapters,
  rendering, queries, budgets, comparison and baseline operations.
- [Interpretation](references/interpretation.md): completeness, presentation,
  size accounting and failure handling.
- [Eval fixtures](references/eval-fixtures.md): realistic tasks and acceptance
  checks for the skill's boundaries.
- [Reference index](references/_index.md): upstream command and evidence
  authorities.

## Decision Rules

- Unknown is never "no". Unreported isolation or conformance information
  cannot prove a negative fact.
- A complete slice closes over in-snapshot references. It does not prove that
  collection observed every platform, module or condition.
- External references are out-of-scope observations. Budget omissions are
  in-snapshot declarations excluded by selection. Preserve both categories.
- A readable interface can exceed tracked source size when build plugins
  generate public declarations. Use actual measurements; no compression ratio
  is promised by the tool.
- Source navigation, runtime semantics and version policy remain outside this
  evidence workflow. Release decisions follow the repository's VERSIONING
  authority.

## Validation Rules

- Bind results to the exact snapshot and full configuration identity. Short
  header IDs are display labels.
- Check expected versus collected modules, gaps and conflicts independently
  from query/slice state and omissions.
- Verify every command against the installed CLI. Check real output and exit
  codes; a help listing alone does not demonstrate a successful collection.
- When changing this skill, exercise the applicable eval fixtures with the
  matching released CLI and run the collection's declared checks.

## Output Format

Return only the context needed for the question, with:

- input/revision and snapshot identity, collector and configuration/scope;
- selected declarations, view/format and documentation choice;
- payload and total bytes when budgeted, selection state, omissions and
  external references;
- expected/collected modules, collection gaps and unresolved questions;
- comparison categories or command failure evidence when applicable.

## Failure / Uncertainty Handling

Report an unavailable compiler, producer configuration or module as missing
evidence. An import or process failure is not an empty successful interface.
Never replace a valid baseline with incomplete collection. Preserve diagnostics
separately from contract data and keep run reports with execution paths local.
