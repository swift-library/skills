# Core Haptics Pattern Authoring

Use this reference for programmatic patterns, event choice, players, advanced
players, timing, looping, and dynamic parameters.

## Simple Before Custom

Before authoring a custom pattern, ask whether the interaction is only:

- button press
- toggle or picker selection
- success, warning, or error confirmation
- ordinary SwiftUI state transition

If yes, use SwiftUI sensory feedback or a simple feedback generator. Core
Haptics is for custom tactile texture, precise sequencing, audio-haptic sync,
advanced timing, or dynamic playback control.

## Event Choice

Use transient events for short impacts. Use continuous events for sustained
texture. Treat intensity and sharpness as design parameters, not magic
constants.

```swift
let tap = CHHapticEvent(
  eventType: .hapticTransient,
  parameters: [
    CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.7),
    CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.45),
  ],
  relativeTime: 0
)

let texture = CHHapticEvent(
  eventType: .hapticContinuous,
  parameters: [
    CHHapticEventParameter(parameterID: .hapticIntensity, value: 0.35),
    CHHapticEventParameter(parameterID: .hapticSharpness, value: 0.2),
  ],
  relativeTime: 0,
  duration: 0.6
)
```

Review the feel on hardware. Values below a useful threshold may disappear;
values near the maximum may feel harsh or spammy.

## Standard Player Shape

```swift
func play(_ events: [CHHapticEvent], on engine: CHHapticEngine) throws {
  let pattern = try CHHapticPattern(events: events, parameters: [])
  let player = try engine.makePlayer(with: pattern)
  try player.start(atTime: CHHapticTimeImmediate)
}
```

Keep creation failures observable. In production code, surface them through the
project's diagnostics boundary instead of defaulting to `try?`.

## Advanced Players

Use an advanced player when the feature needs pause/resume, seek, completion
handling, looping, or dynamic parameter updates.

```swift
func startLoop(
  pattern: CHHapticPattern,
  engine: CHHapticEngine
) throws -> any CHHapticAdvancedPatternPlayer {
  let player = try engine.makeAdvancedPlayer(with: pattern)
  player.loopEnabled = true
  try player.start(atTime: CHHapticTimeImmediate)
  return player
}

func updateIntensity(
  _ player: any CHHapticAdvancedPatternPlayer,
  value: Float
) throws {
  let parameter = CHHapticDynamicParameter(
    parameterID: .hapticIntensityControl,
    value: value,
    relativeTime: 0
  )
  try player.sendParameters([parameter], atTime: CHHapticTimeImmediate)
}
```

Guardrails:

- Clamp user-driven values before sending dynamic parameters.
- Stop looping players when the gesture or state ends.
- Do not update player parameters from high-frequency UI callbacks without
  throttling or a product need.
- Recreate advanced players after engine reset.

## Timing

Causality matters. Start the haptic at the same moment as the visual or audio
event it represents. Delayed haptics make the user feel a disconnected buzz,
even when the code is technically correct.

Bad shape:

```swift
performVisualChange()
Task {
  try await Task.sleep(for: .milliseconds(150))
  try player.start(atTime: CHHapticTimeImmediate)
}
```

Good shape:

```swift
try player.start(atTime: CHHapticTimeImmediate)
performVisualChange()
```

## Review Smells

- Custom pattern used for a plain button tap.
- Transient/continuous choice does not match the visual event.
- Pattern values are copied without a hardware test.
- Looping player has no stop path.
- Dynamic parameters are sent from every drag tick without restraint.
- Haptic timing follows async completion rather than the user-visible event.
