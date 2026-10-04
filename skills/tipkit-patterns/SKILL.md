---
name: tipkit-patterns
description: Use this skill for TipKit implementation and review across Tips.configure, Tip definitions, TipView, popoverTip, TipUIView, TipNSView, TipGroup, Rule, Parameter, Event, display frequency, datastore location, CloudKit tip sync, tip actions, custom TipViewStyle, invalidation, eligibility reset, testing helpers, and onboarding/discovery boundaries. Do not use for generic onboarding copy, marketing prompts, ordinary SwiftUI layout, or interface wording unless TipKit behavior is in scope.
---

# TipKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for TipKit feature-discovery
surfaces. Use this skill when the task is about TipKit eligibility, display,
persistence, testing, or placement behavior, not when the task is only writing
product copy or designing an onboarding flow.

## When To Use

- Configuring TipKit with `Tips.configure`, datastore location, display
  frequency, or optional CloudKit-backed tip state.
- Defining `Tip` types with title, message, image, actions, rules, options,
  identifiers, and status monitoring.
- Displaying tips with SwiftUI `TipView`, `.popoverTip`, UIKit `TipUIView`, or
  AppKit `TipNSView`.
- Sequencing tips with `TipGroup`, invalidating tips after feature use, or
  resetting eligibility for re-display.
- Implementing rules with `Parameter` and `Event`, display-count/duration
  options, or custom `TipViewStyle`.
- Testing tip visibility with TipKit testing helpers and datastore reset paths.

## When Not To Use

- Do not use for generic onboarding, walkthroughs, empty states, or promotional
  prompts that do not use TipKit.
- Do not use for interface wording only.
- Do not use for ordinary SwiftUI layout or architecture unless TipKit
  placement, task timing, or view lifecycle is the issue.
- Do not use tips for critical instructions, consent, errors, or required task
  completion.

## Inputs To Inspect

- App launch/init path where `Tips.configure` is called.
- `Tip` conformances, identifiers, rules, options, actions, invalidation, and
  status or display updates.
- SwiftUI, UIKit, or AppKit presentation code: `TipView`, `.popoverTip`,
  `TipUIView`, `TipUIPopoverViewController`, `TipNSView`, or `TipNSPopover`.
- Datastore configuration, CloudKit tip sync setup, preview/test setup, and UI
  tests.
- Product context: what feature the tip teaches, when it appears, and how it
  stops appearing.

## Workflow

1. Confirm the task is TipKit behavior, not general onboarding or interface
   text.
2. Verify `Tips.configure` runs once early enough and handles thrown errors.
3. Review each tip for a stable identity, concise user value, optional action,
   and a clear invalidation path after the feature is learned or used.
4. Review rules and events for eligibility precision. Avoid showing tips on
   every launch or before the highlighted feature is visible.
5. Choose inline versus popover presentation based on layout impact and whether
   the highlighted control can be obscured safely.
6. Keep sequencing explicit with `TipGroup` when multiple tips can compete.
7. For datastore or CloudKit tip sync, verify current Apple documentation and
   local SDK behavior before making platform claims.
8. Add testing controls for deterministic previews, UI tests, and re-testing
   eligibility without contaminating production state.

## Review Rules

- Do not use TipKit as advertising, feature tours, or blocking guidance.
- Do not leave tips without invalidation, maximum display policy, or a product
  reason for repeated display.
- Do not couple tip eligibility directly to transient view recomputation.
- Do not assume datastore, CloudKit sync, testing helper, or display-frequency
  behavior without current documentation or local SDK verification.
- Leave text quality review to general UI copy guidance when wording is the
  main task.

## Validation

- Build the affected app target.
- Exercise first-run, already-viewed, invalidated, reset, and feature-used
  states.
- Run UI tests or previews with deterministic test helpers when tip visibility
  matters.
- Verify tips do not appear on unrelated screens, repeatedly interrupt normal
  work, or block accessibility flows.

## Output

Return:

1. TipKit trigger boundary and presentation choice
2. Configuration, rule, event, and invalidation findings
3. Datastore/sync/testing notes
4. User-impact and non-TipKit routing concerns
5. Validation run or still needed
