---
name: swiftlint-patterns
description: Use this skill for SwiftLint setup, configuration governance, rule selection, .swiftlint.yml, disabled_rules, opt_in_rules, only_rules, analyzer_rules, included/excluded paths, suppressions, baselines, autocorrection, reporters, build tool plugins, command plugins, Xcode run scripts, CI/pre-commit wiring, custom regex rules, Swift custom rules, swiftlint analyze, toolchain selection, and rollout strategy. Do not use for ordinary Swift style review, broad Swift API design, formatting-only work, or package architecture unless SwiftLint enforcement/configuration is the task.
---

# SwiftLint Patterns

## Purpose

Guide SwiftLint setup, review, troubleshooting, and rollout for Swift and
Apple-platform repositories. Use this skill when the task is about enforcing
SwiftLint behavior, not when the task is only general Swift style judgment.

## When To Use

- Creating, reviewing, or refactoring `.swiftlint.yml`.
- Choosing `disabled_rules`, `opt_in_rules`, `only_rules`, `analyzer_rules`,
  severities, reporters, included paths, excluded paths, or nested configs.
- Reviewing suppressions, baselines, generated-code exclusions, or rollout
  plans for existing codebases.
- Wiring SwiftLint through an Xcode run script, Swift Package plugin,
  command plugin, build tool plugin, CI job, pre-commit hook, or local script.
- Troubleshooting `swiftlint lint`, `swiftlint analyze`, autocorrection,
  reporter output, rule availability, plugin working directories, or
  toolchain-version behavior.
- Designing custom regex rules or evaluating whether Swift custom rules are
  justified.

## When Not To Use

- Ordinary Swift code review where SwiftLint is not part of the request.
- Broad Swift language, API, or style guidance.
- Package graph or target-boundary design unless SwiftLint plugin wiring is
  the package issue.
- General build, release, or App Store workflows unless they are directly
  enforcing SwiftLint.
- Formatter-only work unless SwiftLint is part of the enforcement surface.

## Inputs To Inspect

- `.swiftlint.yml`, nested configs, parent/child config references, and any
  path-specific overrides.
- `Package.swift`, Xcode project build phases, plugin declarations, local
  scripts, CI workflows, pre-commit hooks, Fastlane lanes, or Docker/Mint/Homebrew
  setup that installs or runs SwiftLint.
- Suppression comments, baseline files, generated code directories, test
  target boundaries, and current lint output.
- Current SwiftLint project documentation, local `swiftlint help`,
  `swiftlint rules`, and `swiftlint version` output before relying on mutable
  command, rule, reporter, plugin, or analyzer behavior.

## Workflow

1. Confirm the task is about SwiftLint enforcement or configuration. If it is
   only ordinary Swift style review, it is out of scope.
2. Identify the runner: CLI, Xcode run script, SwiftPM command plugin, build
   tool plugin, CI, pre-commit, or another wrapper. Note working directory and
   config file discovery.
3. Inspect `.swiftlint.yml` and any nested, parent, or child configs. Check
   `included`/`excluded` paths against the repository layout, generated code,
   fixtures, tests, and vendored dependencies.
4. Review rule governance. Prefer explicit rationale for rule families, severity
   changes, opt-in adoption, analyzer rules, and any `only_rules` mode.
5. Review suppressions and baselines. Suppressions should be local and explained
   when practical; baselines should be a migration aid, not a permanent hiding
   place for new violations.
6. For analyzer rules, verify that the workflow produces a clean compiler log
   and runs `swiftlint analyze` separately from normal linting.
7. For autocorrection, review the expected diff after running SwiftLint. Treat
   disk edits from autocorrection as code changes that still need normal review.
8. For custom rules, choose regex rules only when syntax kinds and false
   positives are acceptable. Treat Swift custom rules as a heavier project
   investment that needs current build and distribution evidence.
9. Propose the smallest enforcement change that improves signal without
   flooding the repository with noisy churn.

## Review Rules

- Do not route ordinary Swift style disagreement to this skill unless SwiftLint
  configuration or enforcement is being changed.
- Do not enable broad new rule sets on a legacy codebase without a rollout
  strategy, baseline, or scoped path plan.
- Do not use path exclusions to hide first-party code without calling out the
  reason and the re-entry condition.
- Do not treat rule names, reporter names, analyzer behavior, plugin behavior,
  or installation paths as stable without checking current primary
  documentation or local tool output.
- Keep Xcode build scripts deterministic: fail clearly when SwiftLint is
  expected, or intentionally warn and skip only when the repository has chosen
  that mode.

## Validation

Use the narrowest commands that match the repository:

```bash
swiftlint version
swiftlint rules
swiftlint lint --config .swiftlint.yml
swiftlint lint --strict --config .swiftlint.yml
swiftlint analyze --config .swiftlint.yml --compiler-log-path xcodebuild.log
```

When SwiftLint is wired into Xcode, SwiftPM plugins, CI, or pre-commit, also
run the configured integration command or build path that exercises that wiring.

## Output

Return a compact review or implementation note covering:

- SwiftLint trigger boundary and runner choice.
- Config and rule-governance changes.
- Suppression, baseline, and rollout handling.
- Integration wiring and expected failure mode.
- Validation commands run, skipped, or still needed.
