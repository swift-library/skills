# SwiftUI Design Reference Index

- `visual-design-principles.md` - spacing, typography, color, sizing, grouped content, navigation chrome, SwiftUI control selection, controls, and checklist
- `anti-ai-ui-guardrails.md` - anti-AI-slop warning signs, design directions, brand asset protocol, five-part review, and code shape guidance
- `interactive-editor-design.md` - crop/collage/canvas editor presentation, geometry, gestures, safe areas, and settings surfaces
- `licenses.md` - license file locations

## Symptom Routing

- Generic, template-like, AI-looking, or visually vague SwiftUI screens:
  `anti-ai-ui-guardrails.md`.
- Branded UI without provided assets, or a request to choose visual direction:
  `anti-ai-ui-guardrails.md`.
- Arbitrary padding, inconsistent rhythm, oversized rows, or crowded controls:
  `visual-design-principles.md`.
- Too many font sizes, inconsistent weights, or mismatched font design:
  `visual-design-principles.md`.
- Hardcoded colors, many opacity values, or poor light/dark adaptation:
  `visual-design-principles.md`.
- Gradient cards, heavy borders, huge corner radii, or custom dividers:
  `anti-ai-ui-guardrails.md`, then `visual-design-principles.md`.
- Toggle labels, exclusive choices, low-contrast tints, or control affordance
  issues: `visual-design-principles.md`.
- SwiftUI primitive choice, settings rows, inspector rows, title-value rows,
  `Form`, `Section`, `LabeledContent`, `Label`, `Toggle`, `Picker`,
  `TextField`, `Button`, `Menu`, `List`, or `Table` visual semantics:
  `visual-design-principles.md`.
- Crop/collage/canvas editor state, gesture conflicts, safe-area gaps, preview
  vs export mismatch, or stacked settings: `interactive-editor-design.md`.
