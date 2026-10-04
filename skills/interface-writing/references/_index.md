# Interface Writing Reference Index

Use this index only when `SKILL.md` routing is not enough.

## Read Order

- `voice-and-tone.md`: read when product voice, tone, terminology, or copy
  consistency is unclear.
- `interface-patterns.md`: read the section that matches the interface surface:
  alert, error, empty state, onboarding, notification, accessibility label,
  button, instruction, setting, or CLI output.
- `apple-sources.md`: read when official Apple writing, style-guide,
  accessibility-label, or freshness basis matters.

## Routing

- Voice definition, tone adjustment, product personality, or terminology drift:
  `voice-and-tone.md`.
- Alert, dialog, confirmation, destructive action, or permission prompt:
  `interface-patterns.md`.
- Error, validation message, empty state, onboarding, setting, tooltip,
  notification, or CLI output: `interface-patterns.md`.
- Accessibility label wording only: `interface-patterns.md`.
- Source strings, SwiftUI `Text`, CLI output, localization-risk notes,
  placeholders, terminology drift in implemented UI, or design-copy handoff:
  `interface-patterns.md`, then `voice-and-tone.md`.
- Official Apple writing, terminology, style-guide, or freshness checks:
  `apple-sources.md`.
- Assistive-technology behavior, Accessibility Inspector, WCAG, or Nutrition
  Label work: out of scope.
- Visual design, spacing, typography, or native UI polish: out of scope.
