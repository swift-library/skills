# Changelog

## Unreleased

- Breaking: rename `swift-scripts-patterns` to `swift-sh-patterns` (`swift-sh Patterns`).
- Breaking: rename `swift-testings-patterns` to `swift-testing-patterns` (`Swift Testing Patterns`).
- Collection documentation lives under `docs/`, indexed by `docs/README.md`.
- Skill descriptions lead with the framework or task and keep only adjacent
  boundaries; the whole collection listing fits Claude Code and Codex listing
  budgets, enforced by `scripts/check`.
- CloudKit, App Intents, WidgetKit, UserNotifications, BackgroundTasks,
  EnergyKit, StoreKit and HealthKit skills add SDK-verified API, entitlement
  and availability facts.
- `scripts/check` validates skill contracts, metadata, links, reference cycles,
  and organization-neutral content, and reports host listing sizes.
- Repository automation uses lowercase `scripts/`, including the macOS app
  packaging scaffold and templates.
- `swiftpm-github-release` audits readiness against the shared CI contract:
  formatting, tests and a release build, plus declared jobs and repository
  commands, with `policy / policy` and `validate / result` as required checks.
- Documentation exports derive local `swift build` and `swift test` commands
  from the package directory declared in `.github/swift-package.json`.
- Terminal demos use the `github-readme-design` toolchain for local rendering
  and the validation workflow's demo switch for re-recording.
- `swiftpm-docs` exports a documentation profile into a package with
  `scripts/export_profile.py`, filling identity values from arguments and the
  build command, test command and requirement from the package's own files.
- `swiftpm-docs` hands VERSIONING to the repository steward only when it is
  installed.
- CI checks that `swift-library/swift-package-template` carries the minimal
  export unchanged.
- `swiftpm-docs` keeps work its owner does in place in the task plan and sends
  only handed-off or public work to GitHub issues.
- The `swift-skills` plugin manifest for Codex is the portable Agent Plugins
  `plugin.json` at the repository root, with the Codex interface under
  `extensions.com.openai`; `.codex-plugin/plugin.json` is removed. Codex needs
  CLI 0.147.0 or later to install the plugin.

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
