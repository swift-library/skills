<!-- Derived from repository-docs rules/code-review-rules.md. Edit the source and run its scripts/derive_rules.py. -->
# Code Review Rules

Use this rule when writing, auditing, or templating the review instructions an
automatic or human reviewer applies to pull requests, and the tool entry files
that carry them to a specific reviewer.

## Placement

- Repository-wide rules live in a `## Code Review Rules` section of the root
  AGENTS.md. Rules for one area live in the AGENTS.md nearest to that area; a
  changed file gets the root rules plus those of its nearest nested file.
- Group related rules under `###` headings, for example compatibility, claims,
  documentation, and tests.
- AGENTS.md stays the single source. A reviewer that reads another file gets
  an import of AGENTS.md or content derived from it, never a second
  hand-maintained copy.

## What Belongs

A review rule describes a consequential judgment specific to this repository:

- the behavior a reviewer should flag;
- why it matters here;
- the safe path or accepted exception.

Phrase rules as durable outcomes, not as names of functions or files that are
likely to move. "Flag a public API change without a changelog entry; add the
entry under the next version" survives refactoring. "Check `parseHeader()`"
does not.

## What Does Not Belong

- Anything a tool decides deterministically: formatting, linting, spelling,
  type or availability errors, forbidden paths or names in a diff, required
  files. Those are CI checks; a review rule restating them adds noise.
- Index content, ownership catalogs, architecture explanations, and process
  or history notes. Link to their owner instead.
- Generic coding advice that applies to any repository.

## Size

Review rules are loaded with every review, so each one costs attention. Keep
the section short and specific enough to verify. Codex reads at most 32 KiB of
combined AGENTS.md instructions by default; Anthropic recommends keeping each
CLAUDE.md under 200 lines. Move detail to the linked owner and keep only the
judgment in the rule.

## Reviewer And Tool Files

- **Codex** reads AGENTS.md files from the repository root down to the working
  directory, and its code review applies the `## Code Review Rules` section.
  Automatic review is turned on per repository in Codex settings.
- **Claude Code** supports native AGENTS.md loading from v2.1.277 when its
  built-in instruction reader is enabled. The default reads AGENTS.md when
  no CLAUDE.md or CLAUDE.local.md exists in the working directory or above it.
  Check Project instructions in `/config`: `claude-md-and-agents-md` loads
  both, while `claude-md` or `managed-only` can exclude AGENTS.md.
  Before v2.1.281, some Bedrock or telemetry-disabled sessions lack native
  support; the first session after upgrading from v2.1.276 or earlier may
  also need a new session. Where native loading is unavailable, or CLAUDE.md
  is also needed, retain an `@AGENTS.md` import followed by Claude-specific
  instructions. Check loaded memory with `/context` before removing an
  existing entry file.
- **Claude Code Review** reads CLAUDE.md files at every level as project
  context and reports newly introduced violations as nits. Review-only
  instructions go in a root `REVIEW.md`: severity, nit volume, skip rules,
  repository checks, and the evidence a finding needs. Its rules are written
  directly in the file, so a repository that enables it derives `REVIEW.md`
  from the AGENTS.md section plus Claude-only severity and skip lines, and
  checks the derived text for drift. Its findings do not block merging.
- Other reviewers with their own instruction files, such as Cursor Bugbot
  (`.cursor/BUGBOT.md`) and GitHub Copilot (`.github/copilot-instructions.md`),
  follow the same import-or-derive rule.

Add a tool entry file only when a reviewer or tool in actual use needs it.

## Audit Checks

- The root AGENTS.md has a `## Code Review Rules` section when the repository
  uses automatic review.
- Every rule names the behavior, the reason, and the safe path.
- No rule duplicates a CI check, formatter, linter, or compiler diagnostic.
- Nested rules apply only to their area and do not repeat root rules.
- Each tool entry file imports or derives from AGENTS.md; a copied or diverged
  rule is a finding.

## Sources

- OpenAI: [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md),
  [Codex code review in GitHub](https://learn.chatgpt.com/docs/third-party/github),
  [Custom code review rules for Codex](https://developers.openai.com/blog/custom-code-review-rules-for-codex).
- Anthropic: [Claude Code memory and AGENTS.md](https://code.claude.com/docs/en/memory),
  [Claude Code Review](https://code.claude.com/docs/en/code-review).
