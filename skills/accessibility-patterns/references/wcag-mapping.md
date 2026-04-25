# WCAG Mapping

Use this file when the user asks to map Apple-platform findings to WCAG or
when an audit needs compliance-oriented language. This is not a complete legal
conformance audit.

## Scope

Map findings to WCAG 2.2 Level A/AA concepts when useful for risk and
prioritization. Keep the primary output grounded in Apple-platform behavior
and common tasks.

Include for each mapping:

- WCAG success criterion or category
- affected user task
- Apple-platform evidence
- pass / fail / unknown
- required manual verification

## Perceivable

| WCAG concept | Apple-platform checks |
|---|---|
| Non-text content | Meaningful images, icons, charts, and media have labels or alternatives; decorative content is hidden. |
| Captions and audio descriptions | Dialogue, relevant sounds, and meaningful visual-only video content have synchronized alternatives. |
| Info and relationships | Headings, sections, groups, rows, controls, and state are programmatically represented. |
| Meaningful sequence | Reading and focus order match the intended task order. |
| Use of color | Color-coded information also has text, shape, icon, pattern, or semantic state. |
| Contrast | Text, icons, borders, and focus indicators meet contrast expectations in light/dark modes. |
| Resize text / reflow | Dynamic Type and layout adaptation preserve content at large sizes. |

## Operable

| WCAG concept | Apple-platform checks |
|---|---|
| Keyboard accessible | Full Keyboard Access, macOS keyboard navigation, and tvOS focus can complete the task. |
| No keyboard trap | Modals, popovers, panels, and custom overlays have escape/dismiss paths. |
| Enough time | Users can pause, stop, extend, or avoid time-limited interactions. |
| Pause, stop, hide | Auto-updating, moving, blinking, or scrolling content has controls. |
| Focus order | Focus moves predictably through the task. |
| Focus visible | Focus rings or focused states are visible where applicable. |
| Pointer gestures | Multi-touch, drag, swipe, hover, or long-press actions have single-pointer or accessibility alternatives. |
| Label in name | Voice Control names match or include visible labels. |
| Target size | Interactive targets are large enough; use 44x44pt as the Apple-platform baseline unless local platform rules differ. |

## Understandable

| WCAG concept | Apple-platform checks |
|---|---|
| Language | Localized content, speech language, and text direction are handled where relevant. |
| Predictable behavior | Focus, selection, picker changes, and validation do not unexpectedly navigate or submit. |
| Consistent navigation | Common actions keep consistent labels and placement. |
| Error identification | Errors are visible, announced or focused, and tied to the relevant field. |
| Error prevention | Destructive, legal, financial, or irreversible actions have confirmation, review, or undo. |
| Accessible authentication | Passkeys, biometrics, password managers, or non-cognitive alternatives are available when authentication is in scope. |

## Robust

| WCAG concept | Apple-platform checks |
|---|---|
| Name, role, value | Controls expose accurate labels, traits/roles, values, and states. |
| Status messages | Dynamic status changes are announced without stealing focus unless focus movement is needed. |

## Nutrition Label Mapping

| App Store label | Closest WCAG areas |
|---|---|
| VoiceOver | Non-text content, relationships, sequence, headings/labels, name/role/value |
| Voice Control | Keyboard/input accessibility, label in name, target size |
| Larger Text | Resize text, reflow, text spacing |
| Dark Interface | Contrast, visual presentation |
| Differentiate Without Color Alone | Use of color, non-text contrast |
| Sufficient Contrast | Text and non-text contrast |
| Reduced Motion | Pause/stop/hide, flashing, motion effects |
| Captions | Time-based media captions |
| Audio Descriptions | Time-based media audio description |

## Boundaries

- Do not claim WCAG conformance from a static code review.
- Do not map every issue if the user asked for implementation rather than
  compliance language.
- Do not use WCAG references to override Apple-platform behavior; use them to
  explain impact and verification needs.
