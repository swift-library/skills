# Haptic Design Guardrails

Use this reference when reviewing whether a haptic pattern should exist and
whether its timing, intensity, and modality make sense.

## Causality / Harmony / Utility

Apply this named framework as a checklist, not as "use haptics tastefully". It
prevents the common AI failure mode of adding haptics everywhere just because
the API is available.

- Causality: the haptic must feel caused by the visible or interactive event.
- Harmony: haptic, audio, and visual feedback should feel like one event.
- Utility: the haptic should give the user value, not decoration.

## Causality

The haptic should happen at the moment the event happens. A delayed buzz breaks
the user's sense of cause and effect.

Good shape:

```swift
try player.start(atTime: CHHapticTimeImmediate)
commitVisualStateChange()
```

Bad shape:

```swift
commitVisualStateChange()
DispatchQueue.main.asyncAfter(deadline: .now() + 0.2) {
  try? player.start(atTime: CHHapticTimeImmediate)
}
```

## Harmony

Match haptic intensity and texture to the visual/audio object:

- small/light object: lighter or sharper transient
- heavy/large object: stronger or lower-feeling impact
- continuous transformation: continuous haptic and audio can be more coherent
  than unrelated pulses

This is a design judgment. Validate it by feel, not by code shape alone.

## Utility

Prefer haptics for:

- important confirmations
- error, warning, or success outcomes
- meaningful selection changes
- tactile texture that improves manipulation or game feel
- audio-haptic moments where the haptic carries product value

Avoid haptics for:

- every tap
- ordinary scrolling
- background events with no visible cause
- decorative animation with no user value
- loading or progress states without a clear stop and user benefit

## Accessibility Boundary

Never make haptics the only feedback for important state. Pair haptics with a
visible or audible cue when the state matters. Dedicated accessibility audits
are out of scope.

## Simple Before Custom

If the interaction is an ordinary SwiftUI state change, prefer SwiftUI
`.sensoryFeedback`. Use Core Haptics only when the
interaction needs custom tactile structure, audio-haptic sync, dynamic
parameters, or a pattern asset.

## Review Checklist

- Does the haptic fire at the same moment as the visual or audio event?
- Does the haptic match the size, intensity, and rhythm of the visible event?
- Does the haptic provide user value?
- Is there a non-haptic feedback path for important state?
- Is the pattern restrained enough to avoid fatigue or battery waste?
- Is the design tested on physical hardware?
