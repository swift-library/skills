<!-- Derived from repository-docs rules/readme-layering.md. Edit the source and run its scripts/derive_rules.py. -->
# README Layering

Use this rule for repository landing manuals, directory indexes, and links to
deeper documentation. Choose layers by audience and purpose. Preserve the
target's established paths, casing, and intentionally surfaced entry files.

## Root README

A root README should help the intended reader understand and enter the
repository:

- identity, audience, purpose, and scope;
- what capabilities or artifacts it provides and their supported limits;
- requirements, installation/setup, and a representative happy path;
- common commands, examples, outputs, or integration points;
- the repository and documentation index, with ownership where helpful;
- links to deeper development, architecture, reference, and governance docs.

Adapt these questions to the repository. A workspace needs navigation and
operation entry points; a skill collection needs discovery, installation, and
use; an app, library, plugin, or tool needs its supported entry surface.
Do not invent an installation flow for a repository that does not have one.

Keep common usage, concise development commands, and public safety guidance.
A short architecture overview is useful when it helps readers understand the
product or choose an integration. Root README can summarize and link to the
current architecture without becoming its exhaustive specification.

## Directory And Documentation Indexes

A directory README explains the local area:

- what it contains and the area's scope;
- where its components or documents live;
- which owner or document carries each concern;
- where a reader should go next.

A documentation index explains available document categories. An architecture
index maps concerns to named current architecture documents. A reference index
maps commands, APIs, schemas, and deeper manuals to their owners.

Put the actual architecture and reference content in named documents. A
directory README may include necessary local usage; an index-only document
should not acquire the agent's task workflow or stop conditions.

## Detailed Content And Other Owners

| Content | Destination |
| --- | --- |
| Full module model, dependency direction, architecture contracts and rationale | Current architecture documents |
| Exhaustive CLI flags, output schemas, long examples and troubleshooting catalogs | Reference/manual documents |
| Authored or generated API reference | The project's established API documentation owner |
| Contribution process, security reporting, release policy | Existing governance owners |
| Agent edit route, required checks by change type, edit escalation | AGENTS.md |
| Future design options | Existing proposal owner |
| Accepted decisions, migrations, source attribution, release facts | Relevant durable history/provenance owner |
| Local plans, raw run evidence and authoring iterations | Declared task-state owner |

Keep a common-case summary and a link in README when extracting detailed
manual content. Generic layering does not choose a language-specific API
generator, build workflow, naming convention, or new architecture.

## Missing Or Multiple Entry Files

Report missing files in an audit. During authorized normalization, create a
minimal README when real manual/index content needs an owner; create AGENTS
when actual agent routes or guardrails need one. Missing files alone do not
require boilerplate creation.

When several README files exist, establish their audience and published role
before merging or removing them. Profile, community-health, package, and
directory entry points can have distinct purposes. Preserve intentional
surfaces and repair a genuine duplicated or competing landing manual with
evidence. File location alone does not justify deletion.

## Verification

- Confirm relocated content remains reachable from the appropriate entry.
- Preserve common installation and usage commands, supported limits, safety,
  attribution, and useful architecture summaries.
- Check links using the target's actual file locations and anchors.
- Check documented command existence and relevant manifest/configuration
  facts; do not run live operations merely to verify documentation.
- Compare current statements across manuals, routes, and architecture owners.
  Resolve contradictions from evidence or report the specific uncertainty.
- For templates, inspect their emitted content and links using the target's
  conventions. Template variables should supply target-dependent values.
