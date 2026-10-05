<!-- Derived from repository-docs rules/route-vs-index.md. Edit the source and run its scripts/derive_rules.py. -->
# Route vs Index

Use this rule to assign repository documentation by audience, purpose, and
authority. Apply it to prose and to templates that emit that prose. Repository
type and programming language do not change these responsibilities.

## Document Roles

| Role | Purpose | Owner |
| --- | --- | --- |
| Agent route | What to read, when to act, what to verify, when to stop | AGENTS.md |
| Edit guardrail | A concise instruction that prevents a concrete incorrect or mis-scoped edit | AGENTS.md |
| Review rule | A consequential judgment a reviewer applies to a change, with its reason and safe path | The `## Code Review Rules` section of the root or nearest nested AGENTS.md |
| Tool entry file | A file a specific coding or review tool loads instead of AGENTS.md | CLAUDE.md, REVIEW.md, and similar files, which import or derive from AGENTS.md |
| Reader manual | Purpose, scope, installation, configuration, common use, supported limits | Root or appropriate product/directory README |
| Index | What exists, where it lives, and who owns each area | Root or directory README, or an existing dedicated index |
| Current architecture | Accepted structure, detailed contracts, invariants, and design rationale | Named architecture documents |
| Reference | Exhaustive API/command/schema details, long examples, topic depth | Named reference documents or the project's API documentation |
| Durable history | Accepted decisions with lasting rationale, migrations, provenance, releases | Existing history or provenance owners |
| Task state | Plans, raw evidence, run logs, intermediate attempts | The declared task-state owner |

Use the target's actual documentation locations and casing. These are roles,
not a prescribed directory tree.

## Decision Test

Ask what the sentence helps its reader do:

- Select a document, edit workflow, check, or escalation for a task: route.
- Avoid a specific incorrect edit, ownership violation, or compatibility
  break: a possible edit guardrail.
- Judge whether a proposed change is acceptable: a possible review rule. If a
  tool can decide it deterministically, it is a CI check, not a review rule.
- Understand the product or perform its supported operations: manual.
- Discover contents, locations, or descriptive ownership: index.
- Understand detailed current structure or rationale: architecture/reference.

Apply the test to clauses when a paragraph combines several roles. Words such
as "must", "before", "owns", or a directory name are clues, not verdicts.
Document length alone is not a finding.

## Ownership And Authority

A descriptive ownership table belongs in an index. A short boundary that
directly prevents editing the wrong owner may remain in AGENTS.

Examples:

- "The transport module lives under src/transport and owns wire encoding."
  is descriptive index content.
- "Before changing wire encoding, read the protocol contract; change the
  transport owner rather than adding a second encoder in the UI." is an agent
  route and edit guardrail.
- "The current protocol design is documented in docs/protocol.md." is an
  index entry.
- "Before changing protocol fields, read docs/protocol.md and verify peer
  compatibility." is an agent route.

Keep long ownership models and architectural explanations in their named
owner. AGENTS can link to that owner and retain only the boundary needed while
editing. Repeating the complete model weakens the guide.

## Reader Operations And Agent Instructions

Public operational instructions belong in the manual even when imperative:

- "Set the access token before running the CLI."
- "Run the test command to check a local development build."
- "Disconnect the device before replacing the cable."

Agent-specific editing and escalation belong in AGENTS:

- "Before changing authentication, read the security contract and run its
  focused tests."
- "Stop if a proposed migration would alter a schema owned by another repo."

Preserve user safety instructions and common development commands in README.
The same command can have distinct roles: its invocation may be described in
the development manual while AGENTS specifies which changes require it.

## Review Rules And Tool Entry Files

Review rules are agent instructions for one audience, the reviewer. Keep them
in their AGENTS.md section and follow [Code Review Rules](code-review-rules.md)
for their shape. A tool entry file carries only an import of AGENTS.md or
content derived from it, plus instructions that apply to that tool alone. A
hand-maintained copy of AGENTS.md content in a tool entry file is a duplicate.

## Skill Collections

- Collection README or discovery metadata indexes available skills and their
  purpose. It may summarize capabilities for readers.
- Each SKILL.md owns its trigger contract, supported workflow, validation,
  and output. Detailed per-skill trigger lists belong with that skill.
- Collection AGENTS routes maintenance of the collection and keeps necessary
  cross-cutting edit guardrails. A catalog of individual task triggers repeats
  the skill contracts and should be removed or replaced with index navigation.
- Collection-level naming and authoring specifications belong in their
  maintained design document. Link to it before naming/authoring work rather
  than copying its full rules into AGENTS.

The compact AGENTS role does not impose a compact-route-only shape on SKILL.md.
Skill-specific knowledge and workflows retain their own resource hierarchy.

## Minimal Normalization

1. Identify the canonical owner and preserve every unique current fact.
2. Move misplaced unique content to an existing suitable document. Keep a
   short route or link at the original entry when useful.
3. Delete a duplicate only after confirming a correct maintained copy exists.
   Summaries and purpose-specific routes need not duplicate the full contract.
4. Preserve factual ownership boundaries, licensing, migration facts, and
   current safety/compatibility constraints. Shared words do not make them
   duplicates or obsolete.
5. Make shipped documentation describe current supported behavior. Keep
   authoring corrections, local evidence, and run chronology with their task;
   preserve history only where it has durable value and an explicit owner.
6. Fix an in-scope producer as well as its affected generated outputs. Do not
   manually rewrite generated API or schema content when its source owns it.

If document statements conflict, inspect their declared authority and the
relevant implementation/configuration. Report unresolved facts and pause the
affected correction. Do not guess from file type, copy one statement over the
other, or request approval for a placement decision already covered by scope.
