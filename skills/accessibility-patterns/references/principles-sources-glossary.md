# Principles, Sources, And Glossary

Use this file when the task needs accessibility framing, source attribution, or
a short definition of common terms.

## Working Principles

- Shift accessibility left. Treat it as part of first-draft UI work and PR
  review, not only a release audit.
- Optimize for users, not checklists. Checklists catch issues, but the goal is
  completing real tasks with assistive technologies.
- Accessibility is contextual. There can be multiple valid fixes with
  different product, design, and technical tradeoffs.
- Prefer native controls and platform semantics. Custom controls should earn
  their complexity.
- Test as you go. Automated checks help, but manual testing with real
  assistive technologies is required.
- Fix design systems and reusable components when the issue is systemic.
- Preserve local product intent. Do not rewrite copy, layout, or architecture
  unless accessibility requires it.

## Glossary

| Term | Meaning |
|---|---|
| Accessible name | The name assistive technologies expose for a UI element. |
| Accessibility label | User-facing text for an element when visible text is absent or insufficient. |
| Accessibility value | Current state or data, such as "50 percent" or "3 selected". |
| Accessibility hint | Optional consequence or interaction guidance. |
| Trait / role | Semantic type or state, such as button, header, selected, disabled, adjustable. |
| Focus | Current assistive-technology or keyboard target. |
| Reading order | The order assistive technologies traverse content. |
| Dynamic Type | Apple text-size system for user-preferred readable text. |
| VoiceOver | Apple screen reader. |
| Voice Control | Voice-based interaction system. |
| Switch Control | Scanning-based interaction system for switch devices or equivalent input. |
| Full Keyboard Access | Keyboard-only navigation and activation path on supported platforms. |
| Nutrition Label | App Store accessibility support declaration for common tasks. |

## Source Policy

Prefer current Apple documentation for framework APIs and App Store
Accessibility Nutrition Label criteria. Use upstream community skills as
implementation pattern sources, not as final authority when Apple docs or local
project constraints differ.

Upstream skill sources synthesized into this skill:

- `dadederk/iOS-Accessibility-Agent-Skill`
- `PasqualeVittoriosi/swift-accessibility-skill`
- `rgmez/apple-accessibility-skills`

License notices are preserved in the skill root. See `licenses.md`.

## Useful Official Source Areas

- Apple Accessibility framework and accessibility API documentation.
- SwiftUI accessibility documentation.
- UIKit `UIAccessibility` documentation.
- AppKit `NSAccessibility` documentation.
- App Store Connect Accessibility Nutrition Label overview and evaluation
  criteria.
- Apple Human Interface Guidelines accessibility guidance.
- WCAG and WCAG2ICT when compliance mapping is explicitly requested.
