# Core Haptics Validation

Use this reference for validation plans, failure diagnosis, and authority
checks.

## Physical Device Required

Simulator and static code review cannot prove haptic feel, timing, intensity,
hardware support, or user settings behavior. Use a physical device for final
validation whenever haptic behavior matters.

## Minimum Validation Pass

- Build the affected app target.
- Confirm target resources include any `.ahap` and referenced audio files.
- Run on representative physical hardware.
- Test supported and unsupported custom haptics paths.
- Test app background/foreground if the engine lives across lifecycle changes.
- Trigger interruption or reset-sensitive paths when practical.
- Verify visual/audio/haptic timing together.
- Verify the feature still communicates state without haptics.
- Inspect logs for swallowed Core Haptics errors.

## Failure Diagnosis

If haptics are not felt:

- Check `CHHapticEngine.capabilitiesForHardware().supportsHaptics`.
- Check that the engine was started and kept alive.
- Check that the pattern player was created from the current engine.
- Check reset/stopped handlers for stale players.
- Check muted audio/haptic engine properties if the code changes them.
- Increase intensity only after confirming the event is actually playing.
- Test on a physical device before changing pattern values.

If AHAP playback fails:

- Validate JSON syntax.
- Confirm the `.ahap` file is in the app target bundle.
- Confirm referenced audio files are in the bundle.
- Replace `try?` with error reporting while diagnosing.
- Load the AHAP through `CHHapticPattern(contentsOf:)`.
- Confirm exact numeric file limits from current Apple documentation before
  treating them as a rule.

If timing feels wrong:

- Check whether the haptic starts after an async operation rather than with the
  visible event.
- Check whether `prepare()` or engine start happens too late.
- Check whether a looping or continuous player has startup latency after idle
  shutdown.
- Align animation, audio, and haptic start times.

## Authority Checks

Verify these facts before writing them as rules:

- platform and OS availability
- hardware support matrix
- Low Power Mode behavior
- system haptic settings behavior
- AHAP audio file size, duration, and format limits
- newly added UIKit/SwiftUI feedback APIs

Prefer official Apple documentation, current local SDK headers or
swiftinterfaces, and direct device behavior over memory or secondary sources.
