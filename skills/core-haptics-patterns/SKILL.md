---
name: core-haptics-patterns
description: 'Use this skill for Core Haptics implementation, review, debugging, and validation in Swift or Apple-platform code: CHHapticEngine, CHHapticPattern, CHHapticEvent, CHHapticPatternPlayer, CHHapticAdvancedPatternPlayer, AHAP files, haptic/audio patterns, dynamic parameters, capability checks, engine start/stop lifecycle, stoppedHandler, resetHandler, interruption recovery, real-device validation, and haptic failure diagnosis. Do not use for simple SwiftUI sensoryFeedback, ordinary UIFeedbackGenerator feedback, or accessibility-only haptic audits.'
---

# Core Haptics Patterns

## Purpose

Guide custom haptic and audio-haptic work built on Core Haptics. This skill
owns engine lifecycle, pattern authoring, AHAP resources, advanced players,
dynamic parameters, interruption/reset recovery, validation, and failure
diagnosis. It does not own ordinary button, toggle, picker, or SwiftUI
state-trigger feedback unless that UI action starts a Core Haptics pattern.

## When To Use

- Creating or reviewing `CHHapticEngine`, `CHHapticPattern`,
  `CHHapticEvent`, haptic/audio pattern players, advanced players, or dynamic
  parameters.
- Loading, validating, exporting, or debugging `.ahap` resources.
- Building custom haptic textures, continuous patterns, synchronized
  audio-haptic moments, or tactile feedback with precise timing.
- Debugging missing haptics, engine stoppages, reset recovery, unsupported
  hardware, muted playback, idle shutdown, or physical-device behavior.
- Reviewing whether a custom haptic pattern is warranted instead of simple
  SwiftUI or UIKit feedback.

## When Not To Use

- Do not use for simple SwiftUI `.sensoryFeedback`.
- Do not use for ordinary `UIImpactFeedbackGenerator`,
  `UISelectionFeedbackGenerator`, or `UINotificationFeedbackGenerator`
  feedback unless the task is deciding whether to escalate to Core Haptics.
- Do not use for haptic-only accessibility audits.
- Do not use for general audio playback, AVFoundation, or MusicKit behavior
  unless the audio is part of a Core Haptics pattern.
- Do not promote hardware support, settings behavior, Low Power Mode behavior,
  or AHAP audio-size limits from memory; verify current Apple documentation or
  local SDK headers first.

## Workflow

1. Classify the job: custom engine lifecycle, programmatic pattern, AHAP
   resource, advanced player, dynamic update, design review, or validation.
2. Apply the simple-before-custom gate. If declarative SwiftUI feedback or a
   basic feedback generator carries the interaction, use that instead of
   adding Core Haptics engine code.
3. Load only the matching reference:
   - `references/engine-lifecycle.md` for `CHHapticEngine`, capability checks,
     start/stop, stopped/reset handlers, shutdown, fallback, and thread safety.
   - `references/pattern-authoring.md` for transient/continuous events,
     intensity/sharpness, players, advanced players, looping, timing, and
     dynamic parameters.
   - `references/ahap-files.md` for `.ahap` resource shape, loading,
     validation, audio-haptic files, parameter curves, and artifact review.
   - `references/design-guardrails.md` for Causality / Harmony / Utility,
     overuse, accessibility, timing, and good/bad haptic design review.
   - `references/validation.md` for physical-device checks, simulator limits,
     failure diagnosis, and authority checks.
4. Verify current API facts against the local SDK or official Apple
   documentation when the claim affects availability, platform behavior,
   hardware support, settings behavior, or validation rules.
5. Apply the guardrails: simple-before-custom, Causality / Harmony / Utility,
   no decorative/every-tap haptics, no haptic-only feedback,
   continuous-pattern restraint, AHAP validation, and engine reset/stopped
   recovery.
6. Validate on physical hardware when behavior matters. Static code review and
   Simulator checks are not enough for haptic feel, timing, or device support.

## Core Checks

- Keep a strong reference to the haptic engine while pattern playback is
  expected.
- Check `CHHapticEngine.capabilitiesForHardware().supportsHaptics` before
  assuming custom haptic playback.
- Handle `stoppedHandler` and `resetHandler`; recreate players after reset and
  restart the engine when the feature should recover.
- Do not start a custom engine for ordinary button taps, toggles, picker
  changes, or success/error signals when SwiftUI sensory feedback or a simple
  generator is enough.
- UIKit has no `UIFeedbackGenerator.isHapticFeedbackEnabled`; do not gate
  feedback on it. Degrade respectfully by keeping the UI fully functional
  without haptics.
- Pair haptics with visible or audible feedback for important state changes.
- Avoid continuous haptics for loading states, scrolling, or decoration unless
  the feature has a clear user value and a stop/cancel path.
- Keep AHAP files in the app bundle and validate them on device before
  shipping.

## Output

For implementation, include the engine/pattern shape, fallback behavior,
validation path, and any physical-device checks still needed. For review, lead
with findings that name the broken boundary: unnecessary custom haptics,
missing capability/lifecycle handling, poor causality, haptic-only feedback,
AHAP artifact risk, or missing real-device validation.
