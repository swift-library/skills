# AHAP Files

Use this reference for Apple Haptic and Audio Pattern files used with Core
Haptics.

## Authority

- Apple AHAP documentation:
  <https://developer.apple.com/documentation/corehaptics/representing-haptic-patterns-in-ahap-files>
- Local SDK headers confirm `CHHapticPattern(contentsOf:)` / URL loading and
  AHAP-related pattern keys.

AHAP is a JSON-like file format for haptic and audio patterns. Add `.ahap`
files to the app bundle as resources and load them through Core Haptics.

## Artifact Shape

Keep examples small. The important shape is:

- top-level version
- pattern array
- haptic or audio events
- event time
- event parameters
- optional parameter curves

```json
{
  "Version": 1.0,
  "Pattern": [
    {
      "Event": {
        "Time": 0.0,
        "EventType": "HapticTransient",
        "EventParameters": [
          { "ParameterID": "HapticIntensity", "ParameterValue": 0.8 },
          { "ParameterID": "HapticSharpness", "ParameterValue": 0.5 }
        ]
      }
    }
  ]
}
```

Use larger AHAP examples only when they teach structure: crescendo, parameter
curve, synchronized audio, or repeated tactile texture.

## Loading

```swift
func loadPattern(named name: String, bundle: Bundle = .main) throws -> CHHapticPattern {
  guard let url = bundle.url(forResource: name, withExtension: "ahap") else {
    throw HapticPatternError.missingResource(name)
  }
  return try CHHapticPattern(contentsOf: url)
}
```

Do not silently return `nil` for production behavior. Missing or invalid AHAP
files should be diagnosable.

## Parameter Curves

Use parameter curves when the haptic should ramp, fade, pulse, or follow an
animation over time. A continuous event with a curve often feels more coherent
than several unrelated transients.

Guardrails:

- Match the curve to the visual/audio timeline.
- Avoid long continuous curves without a stop/cancel path.
- Test subtle values on hardware; static review cannot prove feel.

## Audio-Haptic Files

AHAP can reference audio events. Treat audio file limits, codecs, and duration
requirements as current-source facts. Verify against current Apple
documentation or local tooling before writing exact numeric constraints into a
skill or product rule.

## Validation

- Validate JSON syntax.
- Confirm the `.ahap` file is in the app target's resources.
- Confirm referenced audio files are in the bundle and named correctly.
- Load the pattern in code and surface thrown errors.
- Test on a physical device.
- Check audio-haptic sync against the animation or interaction.

## Review Smells

- AHAP file copied into the repo but not bundled in the app target.
- Pattern load uses `try?` and fails without diagnostics.
- Audio file path works in the editor but not in the app bundle.
- Long JSON example is copied without preserving the design reason.
- Numeric audio file requirements are repeated without current authority.
