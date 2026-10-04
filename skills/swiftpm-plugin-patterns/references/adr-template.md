# ADR Template For Plugin Build Graph Decisions

Use this when a plugin architecture or toolchain decision needs to survive the
current implementation session.

```markdown
# <Decision Title>

Status: Accepted | Superseded | Revisit

Date: YYYY-MM-DD

## Context

Describe the plugin topology, client package shape, relevant dependencies, and
why the decision matters.

## Decision

State the chosen architecture or fallback. Include the exact boundary:
plugin target, executable tool, core target, generated files, and public user
workflow.

## Reproduction

- Swift toolchain:
- SwiftPM source revision or Xcode version:
- Dependency versions:
- Direct imports and declared target/product dependencies:
- Direct build command:
- Explicit target dependency import check command/result:
- Real plugin command:
- `--disable-experimental-prebuilts` command, if SwiftSyntax is involved:
- Result:

## Observed Build Graph

Record the important `debug.yaml` or verbose-log facts:

- Host module path:
- Tool module compile inputs:
- Tool link inputs:
- Missing or stale module:
- Whether the missing module is a direct import without a direct dependency:
- Relevant `*-tool.build` directories:

## Upstream Evidence

- SwiftPM / SwiftSyntax / forum links:
- Whether upstream has fixed, partially fixed, or documented workarounds:
- Local repros that pass:
- Local repros that still fail:

## Consequences

Explain what remains supported, what is deferred, and which user workflow is
kept production-safe.

## Revisit Trigger

Name the event that should reopen this decision, such as a SwiftPM version
upgrade, SwiftSyntax package change, or a successful minimal repro under the
real plugin path.
```
