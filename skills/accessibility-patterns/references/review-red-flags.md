# Accessibility Review Red Flags

Use this file during PR review or accessibility audit triage when you need to
separate real user-impact issues from noisy checklist output.

## High-Risk Review Patterns

- The review says "looks accessible" with no VoiceOver, keyboard, or device
  evidence.
- The change adds labels everywhere without checking for duplicate or
  overridden native labels.
- The fix changes architecture, navigation, or product copy when a local
  semantic fix would solve the issue.
- Color remains the only signal for status, selection, error, or progress.
- User-facing text uses fixed fonts or fixed-height containers.
- Hints repeat labels instead of adding useful consequence or interaction
  context.
- Custom controls work by touch or mouse only.
- Modal, popover, or overlay focus can escape to content behind it.
- Swipe-only, drag-only, long-press-only, or hover-only actions have no
  accessible alternative.
- The audit treats `accessibilityIdentifier` as user-facing accessibility text.
- Automated audit output is treated as proof that the flow is accessible.

## Reviewer Questions

- What concrete user task is blocked or degraded?
- Which assistive technology is affected?
- Can a keyboard-only user complete the flow?
- Is VoiceOver output understandable, ordered, and non-duplicated?
- Does Voice Control "Show Names" or "Show Numbers" expose the control?
- Does the fix preserve behavior while improving semantics?
- Is there a smaller local fix than the proposed refactor?
- What manual test proves the fix?

## Severity Guide

P0:

- a core task is unreachable
- a control cannot be discovered or activated
- modal focus escapes or traps the user
- text or media needed for the task has no accessible equivalent

P1:

- task is possible but confusing, slow, or fragile
- labels, grouping, reading order, or state are misleading
- large text or contrast breaks important screens
- hidden gestures or row actions lack alternatives

P2:

- consistency, polish, or completeness issue
- Nutrition Label readiness gap outside the current flow
- manual verification missing for a non-blocking concern

## Fast Pass Checklist

- [ ] Findings are grouped by P0/P1/P2.
- [ ] Every finding states user impact.
- [ ] Every fix is patch-ready or has an explicit product/design dependency.
- [ ] No speculative APIs are recommended without availability checks.
- [ ] Manual verification steps are included.
- [ ] Automated audit results are not the only evidence.
