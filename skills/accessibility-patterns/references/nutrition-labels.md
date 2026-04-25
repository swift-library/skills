# Accessibility Nutrition Labels And WCAG Mapping

Use this file when preparing an App Store Accessibility Nutrition Label
recommendation, evaluating common tasks, or mapping findings to WCAG. This is
not a legal compliance or certification workflow.

## Source Of Truth

Apple's current App Store Connect guidance is the source of truth for
Accessibility Nutrition Labels. Check current App Store Connect documentation
before final submission.

Apple's public App Store Connect help currently describes these label
categories:

- VoiceOver
- Voice Control
- Larger Text
- Dark Interface
- Differentiate Without Color Alone
- Sufficient Contrast
- Reduced Motion
- Captions
- Audio Descriptions

The labels are evaluated per supported device family and common tasks. Device
applicability can vary, so preserve App Store Connect's current wording when
preparing final submission text.

## Evaluation Principle

Recommend a label only when reviewed evidence shows users can complete all
common tasks for the evaluated device using that accessibility feature.

Common tasks normally include:

- primary app functionality
- first launch or onboarding
- login or account creation when present
- purchase or subscription flows when present
- settings and account management
- default, empty, loading, and error states that users encounter in common
  flows

If a single common task is blocked for a feature, do not recommend claiming
that label for the reviewed scope.

## Recommended Output

```text
Accessibility Nutrition Label recommendation

Scope reviewed:
- App version / build:
- Devices:
- Common tasks:

Could recommend:
- Label: reason tied to common-task evidence

Should not recommend:
- Label: blocker or missing evidence

Common-task matrix:
| Task | VoiceOver | Voice Control | Larger Text | Dark Interface | No Color | Contrast | Motion | Captions | Audio Desc |
|---|---|---|---|---|---|---|---|---|---|
| ... | pass / fail / not applicable / not reviewed |

Required verification:
- ...
```

Use "could recommend" and "should not recommend" rather than absolute claims.
State whether each conclusion is based on code review, manual testing, device
testing, automated audit, or provided evidence.

## Label-Specific Checks

VoiceOver:

- all common tasks are perceivable, operable, and understandable
- controls expose labels, values, traits, grouping, actions, and focus
- visual-only information has text alternatives
- focus order follows the task
- modals and alerts keep focus in context and can be dismissed
- dynamic changes are announced or focused when needed

Voice Control:

- controls can be discovered and activated by voice
- visible labels match spoken commands where practical
- gesture-only flows have alternatives
- icon-only controls expose input labels
- duplicate labels are disambiguated by visible context
- text entry, scrolling, and custom actions work by voice

Larger Text:

- text scales to the required range for the platform
- content does not clip, overlap, or lose essential meaning
- custom fonts and non-text measurements scale appropriately
- layouts reflow or scroll at large sizes
- fixed chrome uses Large Content Viewer or equivalent support when appropriate

Dark Interface:

- screens support dark appearance or an equivalent dark interface
- text, controls, media, and custom surfaces remain legible
- no bright flash or light-only surface breaks common tasks
- custom colors provide dark variants or dynamic behavior

Differentiate Without Color Alone:

- color-coded state also has text, icon, shape, pattern, or semantic state
- grayscale testing leaves status, links, charts, and validation understandable

Sufficient Contrast:

- text and meaningful icons meet the contrast target for the evaluated UI
- contrast is checked in both light and dark appearance when applicable
- non-text controls, focus rings, borders, placeholders, and status indicators
  are checked

Reduced Motion:

- decorative motion is removed or reduced
- meaningful motion has a lower-motion alternative
- auto-playing or auto-advancing content can be paused, stopped, or controlled

Captions:

- video and audio content with dialogue or meaningful sounds has captions when
  applicable
- custom media respects system caption preferences where possible
- captions are synchronized and include meaningful non-speech audio when needed
- transcripts are available for audio-only content when the task depends on it

Audio Descriptions:

- video with meaningful visual-only content has audio descriptions when
  applicable
- custom media can select or expose audio description tracks
- audio description can follow system preference where possible
- visual-only instructions, text, or action in media are described

## API Hints

| Label | SwiftUI / UIKit / AppKit hints |
|---|---|
| VoiceOver | `.accessibilityLabel`, `.accessibilityValue`, traits, grouping, custom actions, focus APIs, `UIAccessibility.post`, `NSAccessibility.post` |
| Voice Control | `.accessibilityInputLabels`, `accessibilityUserInputLabels`, visible labels, custom actions |
| Larger Text | text styles, `@ScaledMetric`, `UIFontMetrics`, Large Content Viewer |
| Dark Interface | semantic colors, dynamic colors, color scheme testing |
| Differentiate Without Color Alone | shape, text, icon, pattern, chart symbols, semantic state |
| Sufficient Contrast | semantic colors, increased contrast settings, Accessibility Inspector contrast checks |
| Reduced Motion | `accessibilityReduceMotion`, `UIAccessibility.isReduceMotionEnabled`, WatchKit equivalent |
| Captions | system media player controls, caption tracks, caption appearance settings |
| Audio Descriptions | audio description media tracks, system audio description preference, spoken audio sessions |

## WCAG Mapping

WCAG mapping is useful for explaining risk and evidence, but do not treat a
short code review as a complete WCAG conformance audit.

Common mappings:

- labels, names, and roles: name/role/value success criteria
- keyboard access: keyboard operability and focus order
- Dynamic Type and Larger Text: resize text and reflow concerns
- contrast and color-only state: contrast and use-of-color criteria
- captions and audio descriptions: time-based media criteria
- motion gating: animation and motion-triggered interaction concerns

When mapping to WCAG, include:

- the success criterion or category
- evidence reviewed
- pass/fail/unknown
- required manual test
- product or design dependency

## Boundaries

- Do not claim legal compliance.
- Do not recommend a label from a single screen if common tasks are broader.
- Do not ignore ads, web views, media, onboarding, login, purchase, settings,
  or error flows if they are part of common tasks.
- Preserve local product scope and App Store Connect platform-specific
  applicability.
