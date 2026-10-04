---
name: swiftpm-architecture
description: 'Use this skill for Swift Package architecture design, review, refactoring guidance, and package-structure diagnostics involving Package.swift target graphs, module boundaries, product/library/executable layout, dependency direction, public API surfaces, composition roots, cross-target test strategy, source selection, or compact evidence briefs. Auto-trigger for package-structure work during implementation or review; use manual mode for full architecture review, active/proactive review, context packaging, and reviewer handoff. Do not use for full-repository concatenation, standalone feature specs, roadmap work, code rewrites, strict Swift code-shape taste review, UI feature architecture, or package documentation migration.'
---

# SwiftPM Architecture

Input assumption: local filesystem path to a Swift Package repository.

## Positioning

This skill guides Swift Package architecture work and produces evidence-oriented
review artifacts when requested.

- Primary job: guide target graphs, module boundaries, product layout,
  dependency direction, composition roots, public API surfaces, test placement,
  and package-structure refactors.
- Review-mode job: review a local Swift Package architecture with progressive
  disclosure, choosing direct in-place review or brief output from the request.
- Manual brief job: turn a local Swift Package into a compact,
  evidence-oriented Markdown brief when the user explicitly asks for active,
  proactive, brief, bundle, context package, or reviewer handoff behavior.
- Not its job: produce a final architecture verdict, generate a full migration
  plan, rewrite code, rank community dependencies, run strict Swift code-shape
  taste review, or concatenate the whole repository.
- Review notes are prompts for deeper review. They must stay grounded in package
  layout, source names, public API, target graph, tests, and documentation.

## Entry Modes

- Automatic package architecture guidance: Use when implementation or review
  work touches `Package.swift`, target/module boundaries, product layout,
  dependency direction, composition roots, public API exposure, cross-target
  testing, or package-structure diagnostics. Answer in place with scoped
  guidance, findings, or small refactor recommendations.
- In-place review: If the user clearly asks to review a local Swift Package
  architecture, inspect the repository directly and answer with prioritized
  findings, evidence, and residual risks. Do not create a Markdown file unless
  requested.
- Active review: If the user explicitly asks for active or proactive review
  behavior, emit the fixed Markdown brief described under Output Contract. This
  is the active mode default.
- Brief/bundle: If the user asks for a brief, bundle, context pack, handoff, or
  Markdown output, emit the fixed Markdown brief described under Output
  Contract.
- Ambiguous mentions: If the request only names architecture or package shape
  without a concrete change or review ask, gather only enough context to clarify
  intent or provide a lightweight orientation.

## Progressive Disclosure

- Start with `Package.swift`, the target graph, top-level docs, and high-signal
  directories under `Sources/` and `Tests/`.
- Load full source only for files that explain architecture boundaries,
  composition, public API, state, services, persistence, parsing, networking, or
  test contracts.
- Run the helper script for active review and brief output, or when it materially
  speeds up file ranking. For direct in-place reviews, use the script output as
  internal evidence and keep the user-facing answer concise.
- Load `references/example-output.md` only when markdown brief shape is unclear
  or formatting needs calibration.

## Scope

- Treat a repository as small when it is roughly:
  - up to ~60 Swift source files, or
  - up to ~120 total text files across `Sources/`, `Tests/`, and key docs.
- If the repository is larger, keep the same output shape and reduce source inclusion aggressively.
- Preserve architecture understanding; do not switch to full-repo concatenation.

## Quick Start

For active review or Markdown brief output, run the helper script first.

```bash
python3 scripts/build_swift_package_bundle.py /path/to/swift-package-repo
```

Use flags only when needed.

```bash
python3 scripts/build_swift_package_bundle.py /path/to/repo --output /tmp/architecture-review-bundle.md --max-files 24 --max-bytes 80000 --max-file-lines 900 --include-tests
```

## Workflow

1. Choose mode.
- Use automatic package architecture guidance for implementation or review work
  touching package structure.
- Use in-place review for clear ordinary package architecture review requests.
- Use active review when explicitly asked for proactive review; active review
  produces a brief.
- Use brief/bundle mode only when the user asks for an artifact or handoff.

2. Inspect structure.
- Read `Package.swift` first.
- Walk `Sources/`, `Tests/`, manifest-declared custom target paths, root
  `README*`, and architecture-relevant docs.
- Ignore noise: `.build`, `DerivedData`, `xcuserdata`, generated artifacts, unrelated binaries, cache folders.

3. Build a repository map.
- Summarize meaningful directories.
- Identify targets/modules and dependencies. Prefer `swift package dump-package`
  when available, and fall back to conservative `Package.swift` text scanning.
- Identify files/docs that define architecture or conventions.

4. Extract architecture signals.
- Public types and protocols.
- Core models.
- State containers (`Store`, `ViewModel`, reducers, state structs/enums).
- Services/repositories/providers.
- Dependency injection/composition entrypoints.
- Rendering/navigation/composition boundaries.
- Persistence/network/parsing boundaries if present.

5. Select files by architectural value.
- Rank importance and include representative files, not duplicates.
- Keep architecture-first ordering.

6. Produce the requested output.
- For in-place review, answer in code-review posture: findings first, then open
  questions or assumptions, then a compact summary and test/review gaps.
- For active review or brief/bundle mode, assemble one markdown brief that
  follows the output contract exactly.

## Compression Policy

- Enforce token efficiency as a hard rule.
- Write summaries before source.
- Include representative files instead of repeated variants.
- Include full source only for selected files.
- Keep documentation on a budget: root README can anchor context, but nested
  usage README files must not crowd out source files.
- Keep large files on a budget: if a file is architecturally important but too
  large to embed, list it as omitted-but-important instead of including full
  source.
- If the bundle is too large:
  - raise the score threshold,
  - keep one representative per repeated pattern/feature area,
  - drop low-signal docs/tests/utilities first,
  - always keep `Package.swift` and composition/abstraction files.
- For very small repositories, include most source files only when the bundle stays structured and readable.

## File Selection Rules

Prioritize by default:
- `Package.swift`
- app/feature entrypoints
- public protocols
- core models
- state containers
- repositories/services/providers
- dependency injection and composition roots
- representative feature files

Exclude by default:
- previews
- mocks
- fixtures
- repetitive extensions
- generated files
- build outputs and derived artifacts
- trivial test data

Include tests only when they add architecture signal:
- contract/integration tests that define module boundaries,
- tests that clarify state transitions or dependency wiring,
- tests needed to understand non-obvious design decisions.

## Script-First Policy

Run `scripts/build_swift_package_bundle.py` first for active review and markdown
brief output. For in-place review, run it when useful for fast ranking or
static-scan cues.

Script responsibilities:
- scan files,
- filter noise,
- extract package/module structure,
- rank files,
- assemble markdown skeleton,
- embed selected source files.

Model responsibilities:
- explain architectural patterns,
- interpret key abstractions,
- identify risks and tradeoffs,
- add concise review commentary without turning static-scan cues into a final
  pass/fail assessment.

## Fallback Rules

- If `Package.swift` is missing or invalid, infer structure from layout and mark it as inferred.
- If the helper script fails, continue with manual inspection and keep the same output contract.
- Distinguish observed facts from inferred intent explicitly.
- Do not overclaim undocumented patterns.

## Output Contract

This contract applies only to active review and brief/bundle mode. Emit exactly
one markdown file. Use these headings exactly and in this order:
- `# Repository Overview`
- `# Directory Tree`
- `# Module Summary`
- `# Key Architectural Patterns`
- `# Key Abstractions`
- `# Important Files to Read First`
- `# Selected Source Files`
- `# Review Notes`

Under `# Selected Source Files`, emit one subsection per file using this exact shape:

````markdown
## `<relative/path/to/file>`
- file path: `<relative/path/to/file>`
- why it matters: `<concise architectural rationale>`

```<language>
<full source>
```
````

Do not reorder selected files alphabetically; order them by architecture-review priority.

Under `# Review Notes`, make the posture explicit: notes are static-scan cues
for review focus, not complete findings. Prefer evidence-backed observations
over broad recommendations.

When important files are excluded by byte, line, vendored/external, or source
selection budgets, list them under `# Important Files to Read First` using an
`Omitted but important:` paragraph rather than adding another top-level heading.

## Reference Loading

- Load `references/example-output.md` only when markdown brief shape is unclear
  or formatting needs calibration.
- Skip reference loading during normal in-place review, scanning, and ranking.

## Do Not

- Do not emit a raw unordered file dump.
- Do not prioritize completeness over learning value.
- Do not infer MVVM, TCA, Clean Architecture, or DI frameworks unless code/docs support it.
- Do not let `# Review Notes` exceed the combined prose in sections `# Repository Overview` through `# Important Files to Read First`.
- Do not create feature roadmaps, task plans, migration plans, or code changes
  unless the user asks for a separate follow-up outside this bundle contract.
