# Manual Testing

Use this file for practical device and simulator verification steps. Manual
testing is required for meaningful accessibility claims.

## Test Planning

Test the common tasks that matter to the product:

- launch and onboarding
- login or account setup
- primary feature flow
- search, browse, create, edit, or purchase flows when present
- settings and account management
- loading, empty, error, and permission states
- media playback when present

Use a real device for final VoiceOver, Voice Control, Switch Control, media,
audio, haptics, camera, and hardware input checks. Use Simulator and previews
for early layout, Dynamic Type, color scheme, and Accessibility Inspector work.

## VoiceOver

Enable VoiceOver from Settings > Accessibility > VoiceOver or through the
Accessibility Shortcut.

Verify:

- every interactive element is reachable
- labels are concise and do not include role words
- values and traits describe state
- decorative images are skipped
- reading order matches task order
- focus moves after navigation and modal presentation
- focus returns after dismissal
- adjustable controls change with VoiceOver gestures
- dynamic content updates are announced or focused appropriately
- at least one complete core flow can be completed without sighted help

## Voice Control

Enable Voice Control from Settings > Accessibility > Voice Control.

Verify:

- "Show numbers" covers every interactive element
- "Tap [number]" activates the correct element
- "Show names" exposes visible control names
- "Tap [visible label]" works where visible labels exist
- icon-only controls have speakable input labels
- text input works with dictation commands
- scrolling and custom actions are reachable

## Switch Control

Enable Switch Control from Settings > Accessibility > Switch Control.

Verify:

- scan order reaches every interactive element
- custom actions appear where gesture-only actions exist
- modals and popovers are reachable and dismissible
- no primary task depends on a timeout
- grouped content reduces scan burden without hiding controls

## Full Keyboard Access

Enable Full Keyboard Access on iPadOS where applicable. On macOS, keyboard
navigation is a first-class path.

Verify:

- Tab and Shift-Tab reach all interactive elements
- arrow-key navigation works in lists, grids, tables, menus, and segmented
  controls where expected
- Space or Return activates focused controls
- Escape dismisses modals, sheets, popovers, or panels
- focus never disappears or gets trapped

## Dynamic Type And Display Settings

Test:

- largest accessibility text size
- smallest text size if compact layouts are important
- Bold Text
- Increase Contrast
- Reduce Transparency
- Differentiate Without Color / grayscale
- Reduce Motion
- light and dark appearance

Verify:

- text does not clip, overlap, or lose essential meaning
- layout adapts instead of relying on tiny scale factors
- status is not color-only
- focus and borders remain visible
- meaningful motion has a low-motion alternative

## Accessibility Inspector

Use Xcode > Open Developer Tool > Accessibility Inspector for:

- labels, traits, values, and frame inspection
- hierarchy and hit-region checks
- contrast checks
- notification inspection
- simulated display settings

Inspector findings are useful evidence, but passing an Inspector audit does not
prove the flow works with real assistive technologies.

## Reporting Template

```text
Accessibility manual test summary

Build / device:
Common tasks tested:

VoiceOver:
- Pass / fail / not tested:
- Notes:

Voice Control:
- Pass / fail / not tested:
- Notes:

Switch Control:
- Pass / fail / not tested:
- Notes:

Keyboard:
- Pass / fail / not tested:
- Notes:

Dynamic Type / display:
- Pass / fail / not tested:
- Notes:

Blockers:
- ...

Recommended follow-up:
- ...
```
