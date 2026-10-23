# Changelog

## Unreleased

### Breaking changes

- `swift-scripts-patterns` is renamed `swift-sh-patterns`, and
  `swift-testings-patterns` is renamed `swift-testing-patterns`. Update prompts
  and configurations that name them; installations that link skill directories
  directly must link the new directory names.
- The Codex plugin manifest is the portable Agent Plugins `plugin.json` at the
  repository root, with the Codex interface under `extensions.com.openai`;
  `.codex-plugin/plugin.json` is removed. Codex needs CLI 0.147.0 or later to
  install the plugin.

### Discovery and collection

- Skill descriptions lead with the framework or task and keep only adjacent
  boundaries; triggers outside a description stay in the skill's When To Use
  section. The whole listing fits the Claude Code and Codex listing budgets,
  enforced by `scripts/check`.
- `scripts/check` validates skill frontmatter, host metadata, links, reference
  cycles and organization-neutral content, and reports listing sizes per host.
- Collection documentation lives under `docs/`, indexed by `docs/README.md`.
  `AGENTS.md` guides collection maintenance; each skill's description and
  `SKILL.md` state its boundaries.
- Repository automation uses lowercase `scripts/`.
- Skill outputs scale with the task: direct answers for questions, short
  summaries for small edits, full reports for audits and reviews.
- Skills name concrete artifacts, such as API snapshots, check results, logs or
  traces, where they named an artifact "evidence".

### Skills

- `swiftpm-github-release` judges readiness from the repository's own CI,
  required checks and adopted VERSIONING. The shared CI specification applies to
  callers of a workflow that implements it. `check_repo_facts.py` checks AI
  attribution trailers with `--forbid-ai-trailers` and enforces breaking bumps
  for deployment-target or tools-version raises with `--breaking-floor-raise`;
  otherwise it reports those raises as notes.
- `swiftpm-readme` takes the default branch and tags from the published remote
  and reports them as unknown when the remote cannot be read. Terminal demos are
  rendered by the presentation owner, with `github-readme-design` when installed.
- `swiftpm-docs` exports a documentation profile into a package with
  `scripts/export_profile.py`, taking identity values from arguments and build
  and test commands from the package directory, including the one declared in
  `.github/swift-package.json`. The Canonical Artifacts contract is an optional
  module (`--module canonical-artifacts`). Rules cover the document lifecycle
  from proposal to accepted decision and current architecture, decision
  statuses and supersession. VERSIONING goes to the repository steward when it
  is installed; work its owner does stays in the task plan, and only handed-off
  or public work goes to GitHub issues.
- `swiftpm-macos-app-packaging` writes the notarization key and archive into a
  private temporary directory, merges every architecture of embedded frameworks
  in universal builds, and reads versions from `version.env` in both packaging
  and notarization.
- `ios-simulator` keeps build state in a per-project user cache, overridable
  with `--state-dir` or `IOS_SIMULATOR_STATE_DIR`.
- `keychain-patterns` and `cryptokit-patterns` each keep their own domain's
  references, with one Secure Enclave rule: exclude Simulator at compile time
  and check availability at runtime.
- The Swift Charts accessibility example and the SwiftUI `@Entry` guidance use
  APIs from the current SDKs.
- CloudKit, App Intents, WidgetKit, UserNotifications, BackgroundTasks,
  EnergyKit, StoreKit and HealthKit skills add SDK-verified API, entitlement and
  availability facts.
- `swiftpm-distiller` states its boundary and source layers once.

### Automation

- CI checks that `swift-library/swift-package-template` carries the minimal
  documentation export with the Canonical Artifacts module.

## 0.1.0

- First release of the `swift-skills` plugin for Claude Code and Codex, with skills for:
  - Swift language and packages.
  - Repository documentation and release.
  - SwiftUI, UIKit, and interface.
  - Data, storage, and sync.
  - Security, identity, and privacy.
  - App services and system integration.
  - Commerce, wallet, and attribution.
  - Personal data and location.
  - Media, graphics, and games.
  - Machine learning and language.
  - Networking and the web.
  - Devices, sensors, and accessories.
  - Diagnostics and simulators.
- `swiftpm-docs` keeps version rules in VERSIONING and writes the release reference
  `Documentation/Reference/Release.md`, with a compatibility surface section,
  in place of `Documentation/Architecture/VersioningAndRelease.md`.
