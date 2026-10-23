---
name: relevancekit-patterns
description: RelevanceKit implementation and review for watchOS Smart Stack surfacing, RelevantContext, widget relevance donation, contextual clues, and permission/SDK gating. Not for widget timelines, visual polish, or underlying HealthKit/Core Location data access.
---

# RelevanceKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for RelevanceKit context
signals that improve widget visibility in the watchOS Smart Stack. Use this
skill when the task is about relevance signals, not generic widget UI or
timeline implementation.

## When To Use

- Adding RelevanceKit context to WidgetKit widgets for Smart Stack surfacing.
- Reviewing `RelevantContext` usage for time/date, location/place, fitness,
  sleep, hardware, or related contextual clues.
- Connecting RelevanceKit with WidgetKit configuration and App Intents donation
  where relevance behavior depends on both.
- Testing relevance on watchOS and handling unsupported platforms gracefully.
- Reviewing permission boundaries for location, fitness, sleep, or other
  sensitive contextual signals used to influence widget visibility.
- Grouping relevance signals and checking current SDK availability gates.

## When Not To Use

- Do not use for visual-only WidgetKit review.
- Do not use for generic widget extension, timeline, reload, or App Group data
  work.
- Do not use for HealthKit or Core Location implementation unless the issue is
  specifically how those signals feed RelevanceKit.
- Do not use for App Intent action/entity design unless the intent is part of
  relevance donation.

## Inputs To Inspect

- WidgetKit widget configuration, relevant widget code, App Intents donation,
  and platform availability checks.
- `RelevantContext` construction for date/time ranges, location or place
  contexts, fitness, sleep, hardware, and combined clues.
- Permission requests, fallback behavior, and privacy-sensitive contextual data
  handling.
- watchOS test plan, previews, logs, device state assumptions, and unsupported
  iOS/iPadOS/macOS behavior.

## Workflow

1. Confirm the task is RelevanceKit relevance behavior rather than ordinary
   widget implementation or visual polish.
2. Verify the supported platform and current SDK symbols before relying on any
   RelevanceKit API shape.
3. Choose the minimal contextual clues needed for the widget to be useful in the
   Smart Stack.
4. Keep relevance signals truthful, bounded in time, and tied to real user
   context rather than constant promotion.
5. Review permission-sensitive clues for user value, fallback behavior, and data
   minimization.
6. Coordinate with WidgetKit configuration and App Intents only where they
   directly affect relevance donation or surfacing.
7. Test on watchOS or clearly report when only static review was possible.

## Review Rules

- Do not treat RelevanceKit as a ranking override or marketing promotion tool.
- Do not use broad always-on relevance contexts when a narrower date, location,
  fitness, sleep, or hardware clue is available.
- Do not request sensitive permissions solely to improve widget visibility.
- Do not assume RelevanceKit affects non-watchOS platforms unless current
  documentation and local SDK behavior prove it.
- Leave visual widget review and timeline mechanics to general WidgetKit
  guidance.

## Validation

- Build the app and widget extension targets with the intended SDK.
- Test supported, unsupported, permission-denied, no-signal, and relevant-signal
  states.
- Verify relevance donation changes widget surfacing only under the intended
  context when device testing is feasible.
- Check logs and previews for stale, overbroad, or privacy-sensitive relevance
  data.

## Output

Return:

1. RelevanceKit trigger boundary and platform status
2. RelevantContext and donation findings
3. Permission, privacy, and fallback notes
4. WidgetKit/App Intents integration boundary
5. Validation run or still needed
