# Core Haptics Engine Lifecycle

Use this reference for `CHHapticEngine` setup, capability checks, lifecycle,
reset/stopped recovery, shutdown, and fallback decisions.

## Authority

- Apple `CHHapticEngine` documentation:
  <https://developer.apple.com/documentation/corehaptics/chhapticengine>
- Apple `resetHandler` documentation:
  <https://developer.apple.com/documentation/corehaptics/chhapticengine/resethandler-swift.property>
- Local SDK headers confirm `capabilitiesForHardware()`, `stoppedHandler`,
  `resetHandler`, `isAutoShutdownEnabled`, `playsHapticsOnly`,
  `playsAudioOnly`, `isMutedForAudio`, and `isMutedForHaptics`.

## Lifecycle Shape

Keep engine ownership explicit and long-lived enough for playback. A local
manager, feature dependency, or app service can own the engine; a transient
view body should not.

```swift
import CoreHaptics

final class HapticEngineController {
  private var engine: CHHapticEngine?
  private var players: [String: any CHHapticPatternPlayer] = [:]

  var supportsCustomHaptics: Bool {
    CHHapticEngine.capabilitiesForHardware().supportsHaptics
  }

  func prepare() throws {
    guard supportsCustomHaptics else { return }

    let engine = try CHHapticEngine()
    engine.stoppedHandler = { [weak self] reason in
      self?.handleStopped(reason)
    }
    engine.resetHandler = { [weak self] in
      self?.handleReset()
    }
    try engine.start()
    self.engine = engine
  }

  private func handleStopped(_ reason: CHHapticEngine.StoppedReason) {
    players.removeAll()
  }

  private func handleReset() {
    players.removeAll()
    do {
      try engine?.start()
    } catch {
      // Surface this through the app's logging or diagnostics boundary.
    }
  }
}
```

The exact owner is project-specific. Preserve these mechanics:

- engine has a stable owner
- hardware capability is checked
- start failure is handled
- stopped/reset handlers are registered
- pattern players are recreated after reset
- diagnostics do not disappear into `try?` when behavior matters

## Reset And Stopped Handling

`stoppedHandler` is for external stop causes such as interruption, suspension,
idle timeout, engine destruction, game-controller disconnect, or system error.
Do not assume it runs for explicit `stop` calls.

`resetHandler` is recovery after a haptic server failure. Treat existing pattern
players as invalid and recreate them. Apple documentation says pattern objects
and engine properties are preserved; players still need a new lifecycle.

Callbacks can arrive away from the main thread. Hop to the correct actor or
queue before touching UI state.

## Shutdown And Power

Stop the engine when custom haptic playback is no longer needed. Consider
`isAutoShutdownEnabled` only when the feature can tolerate extra startup
latency after idle shutdown.

Continuous haptic texture is expensive enough to need an explicit stop path.
Do not use continuous patterns for generic loading states or scrolling.

## Fallback Boundary

Fallback is a product/design decision, not a Core Haptics API trick:

- If custom haptics are unsupported, keep the UI fully functional.
- For simple confirmations, use SwiftUI sensory feedback or a simple feedback
  generator rather than reimplementing a custom engine.
- UIKit has no `UIFeedbackGenerator.isHapticFeedbackEnabled`; do not gate
  fallback on it.

## Review Smells

- Engine is created inside a SwiftUI `body` or repeatedly in a button closure.
- Code checks Core Haptics support but has no fallback behavior.
- `resetHandler` only restarts the engine and leaves stale players around.
- `stoppedHandler` mutates UI state without actor/queue control.
- Long-running haptics have no explicit stop/cancel path.
- Errors are swallowed even though the user-visible experience depends on the
  haptic.
