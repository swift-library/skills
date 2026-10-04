---
name: app-intents-patterns
description: Use this skill for App Intents implementation and review across AppIntent actions, parameters, AppEntity/AppEnum modeling, entity queries, App Shortcuts, Siri and Shortcuts integration, Spotlight indexing, widgets, controls, Live Activity interactivity, Focus filters, assistant schemas, URL representation, and SiriKit migration. Do not use for visual widget design, broad SwiftUI architecture, App Store metadata, market messaging, or standalone Core Spotlight work with no App Intents surface.
---

# App Intents Patterns

## Purpose

Guide implementation, review, and troubleshooting for App Intents features that
expose app actions and app data to system experiences such as Siri, Shortcuts,
Spotlight, widgets, controls, Focus, and Live Activities.

## When To Use

- Creating or reviewing `AppIntent` actions, `@Parameter` values, result
  dialogs, snippets, confirmations, or intent errors.
- Modeling app data with `AppEntity`, `AppEnum`, static options, or entity
  query protocols.
- Adding App Shortcuts, Siri phrases, Spotlight indexing, assistant schemas, or
  system discovery surfaces.
- Wiring App Intents into widgets, controls, Live Activities, Focus filters, or
  Action button flows.
- Migrating relevant SiriKit custom intent behavior to App Intents.
- Debugging intent discovery, parameter resolution, app launch/navigation,
  authentication, or missing entity results.

## When Not To Use

- Do not use for widget visual layout only.
- Do not use for general SwiftUI architecture or navigation without an App
  Intents surface.
- Do not use for App Store metadata, pricing, release operations, or market
  copy.
- Do not use for standalone Core Spotlight indexing unless App Intents entities
  or system experiences are part of the task.
- Do not invent version-specific Siri, Apple Intelligence, or assistant schema
  behavior. Verify current Apple documentation and the local SDK before relying
  on new surfaces.

## Inputs To Inspect

- App, extension, and package targets that contain App Intents code.
- Intent, entity, enum, query, shortcut, and app-dependency types.
- WidgetKit, control, Live Activity, Spotlight, Focus, or Siri integration
  points that call into App Intents.
- Navigation, authentication, deep-link, and app-launch code reached from an
  intent.
- Tests, sample shortcuts, simulator/device runs, and Shortcuts or Spotlight
  validation evidence.

## Workflow

1. Identify the system surfaces in scope: Shortcuts, Siri, Spotlight, widgets,
   controls, Live Activities, Focus, Action button, or app launch.
2. Confirm platform, target, and module placement before changing public
   intent types.
3. Model each intent around one user action. Keep title, description,
   parameters, dialog, result type, and error behavior explicit.
4. Model app data as entities only when the system needs to search, choose,
   display, index, or pass that data across experiences.
5. Implement entity queries with predictable identifiers, display
   representations, property matching, paging or narrowing where needed, and
   safe empty-result behavior.
6. Add shortcuts and phrases only after the action and entity model are stable.
7. Review app launch, scene routing, authentication, confirmation, undo, and
   URL representation paths for predictable behavior.
8. Validate the actual system surface, not just compilation.

## Review Rules

- Keep App Intents code small, deterministic, and independent of view state.
- Do not expose sensitive data through display representations, dialogs,
  snippets, donated entities, or logs.
- Do not use App Intents as a generic background job runner.
- Avoid duplicate intent names, vague parameter names, and entities without
  stable identifiers.
- Keep widgets and controls thin: route their App Intent work to reusable app
  services instead of embedding business logic in UI configuration code.
- Treat Siri and assistant-facing behavior as current-source gated whenever the
  API or platform claim is new or version-specific.

## Validation

- Build the affected app and extension targets.
- Run a representative shortcut or App Shortcut from the Shortcuts app when
  feasible.
- Test Spotlight or entity discovery when entities are indexed or searchable.
- Test widget, control, or Live Activity interaction when the intent is invoked
  from that surface.
- Exercise denied authentication, missing entity, cancellation, and validation
  failure paths.

## Output

For implementation or review work, return:

1. System surfaces inspected
2. Intent and entity model judgment
3. Routing, authentication, confirmation, and error handling notes
4. Validation run or still needed
5. Current-source assumptions for version-specific behavior
