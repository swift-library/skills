# Accessibility QA Checklist

Use this checklist for manual accessibility testing. Adapt it to the reviewed
app, platform, device, and common tasks.

## Scope

- Build / version:
- Device / OS:
- Common tasks tested:
- Tester:
- Date:

## VoiceOver

- [ ] Every interactive element is reachable.
- [ ] Labels are concise and meaningful.
- [ ] Labels do not include redundant role words.
- [ ] State is exposed as value or trait.
- [ ] Decorative images are skipped.
- [ ] Reading order is logical.
- [ ] Focus moves correctly after navigation and modal presentation.
- [ ] Focus returns after dismissal.
- [ ] Adjustable controls can be changed.
- [ ] Dynamic updates are announced or focused when needed.
- [ ] A core task can be completed without sighted help.

## Voice Control

- [ ] "Show numbers" covers every interactive element.
- [ ] "Tap [number]" activates the expected element.
- [ ] "Show names" exposes visible labels.
- [ ] "Tap [visible label]" works where visible labels exist.
- [ ] Icon-only controls have speakable input labels.
- [ ] Text input and scrolling work.
- [ ] Hidden or custom actions are reachable.

## Switch Control

- [ ] Scan order reaches all interactive elements.
- [ ] Activation triggers the expected control.
- [ ] Custom or hidden actions appear in the action menu.
- [ ] Modals and popovers are reachable and dismissible.
- [ ] Primary tasks do not depend on timeouts.

## Keyboard

- [ ] Tab and Shift-Tab reach every interactive element.
- [ ] Arrow-key navigation works in lists, grids, menus, and tables.
- [ ] Space or Return activates focused controls.
- [ ] Escape dismisses modal or transient UI.
- [ ] Focus is visible and never trapped.

## Larger Text / Dynamic Type

- [ ] Text scales at the largest relevant size.
- [ ] No essential text clips, overlaps, or disappears.
- [ ] Layout adapts where horizontal space runs out.
- [ ] Fixed chrome uses Large Content Viewer where appropriate.
- [ ] Custom fonts scale through platform APIs.

## Display Settings

- [ ] Light and dark appearance are readable.
- [ ] Increase Contrast improves or preserves contrast.
- [ ] Color is not the only status signal.
- [ ] Reduce Motion removes or replaces large motion.
- [ ] Reduce Transparency does not make content unreadable.
- [ ] Bold Text and Button Shapes do not break hierarchy.

## Media

- [ ] Captions exist for meaningful speech and sound.
- [ ] Captions respect system settings where possible.
- [ ] Audio descriptions exist for meaningful visual-only video.
- [ ] Media controls are reachable with assistive technologies.
- [ ] Speech or app audio does not conflict with VoiceOver.

## Nutrition Label Summary

| Label | Status | Blocking issues |
|---|---|---|
| VoiceOver | Pass / Fail / N/A / Not tested | |
| Voice Control | Pass / Fail / N/A / Not tested | |
| Larger Text | Pass / Fail / N/A / Not tested | |
| Dark Interface | Pass / Fail / N/A / Not tested | |
| Differentiate Without Color Alone | Pass / Fail / N/A / Not tested | |
| Sufficient Contrast | Pass / Fail / N/A / Not tested | |
| Reduced Motion | Pass / Fail / N/A / Not tested | |
| Captions | Pass / Fail / N/A / Not tested | |
| Audio Descriptions | Pass / Fail / N/A / Not tested | |

Do not recommend a label when a common task fails for that feature.
