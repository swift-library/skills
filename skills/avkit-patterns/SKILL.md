---
name: avkit-patterns
description: Use this skill for AVKit and AVFoundation playback implementation and review across AVPlayer, AVPlayerViewController, SwiftUI VideoPlayer, Picture in Picture, AirPlay, subtitles, playback controls, player observation, HLS buffering, audio session/background playback, Now Playing, lifecycle cleanup, and playback error handling. Do not use for photo picking/capture, MusicKit catalog playback, generic audio DSP, or visual design polish.
---

# AVKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for media playback UI and
playback state using AVKit, AVFoundation players, Picture in Picture, AirPlay,
and related system playback surfaces.

## When To Use

- Implementing or reviewing `AVPlayer`, `AVPlayerViewController`,
  `VideoPlayer`, `AVPlayerLayer`, or `AVQueuePlayer` playback.
- Adding Picture in Picture, AirPlay, subtitles, captions, playback controls,
  speed, HLS, buffering, or interstitial behavior.
- Wiring audio sessions, background playback, Now Playing metadata, or remote
  command handling for playback features.
- Debugging black frames, readiness, lifecycle cleanup, time observation,
  errors, buffering, or route changes.

## When Not To Use

- Do not use for photo picking, photo capture, or photo-library workflows; use
  `photokit-patterns`.
- Do not use for Apple Music catalog, MusicKit authorization, or subscription
  playback; use `musickit-patterns`.
- Do not use for generic audio DSP, recording, or synthesis without AVKit
  playback UI.
- Do not use for visual polish only.
- Do not invent platform-specific PiP, HDR, AirPlay, or frame-analysis
  behavior. Verify current Apple documentation and local SDK symbols.

## Inputs To Inspect

- Player ownership, item loading, player view/controller setup, and SwiftUI
  lifecycle.
- Audio session category/options, background modes, route changes, interruption
  handling, and Now Playing integration.
- PiP controller, restore callbacks, AirPlay route handling, subtitles,
  captions, and media selection code.
- HLS, buffering, readiness, error handling, retry, and analytics/progress
  observation.
- Device/simulator behavior, playback URLs, assets, and repro steps.

## Workflow

1. Identify playback surface: standard system UI, SwiftUI `VideoPlayer`, custom
   player layer, audio-only playback, or PiP.
2. Choose `AVPlayerViewController` or system playback UI when possible. Use
   custom layers only when the product needs custom controls.
3. Own the player outside transient SwiftUI body creation and clean up observers
   and items deliberately.
4. Configure audio session, background modes, interruptions, route changes, and
   Now Playing only when required by the feature.
5. Handle readiness, buffering, stalled playback, failed items, unavailable
   captions, and network failures.
6. Validate PiP, AirPlay, subtitles, background playback, and route changes on
   hardware when the feature depends on system behavior.

## Review Rules

- Do not subclass `AVPlayerViewController`.
- Do not create new players repeatedly from SwiftUI `body`.
- Do not leak time observers, KVO/observation tokens, items, or PiP controllers.
- Do not assume media is ready when a URL exists.
- Do not hide playback errors or buffering states.
- Do not claim PiP support without checking device support and restore flows.

## Validation

- Build the affected app target.
- Test initial load, play, pause, seek, failure, and app lifecycle transitions.
- Test PiP, AirPlay, background playback, subtitles, and route changes when in
  scope.
- Test poor network or stalled HLS behavior for streaming media.
- Verify observer cleanup with repeated presentation/dismissal.

## Output

For implementation or review work, return:

1. Playback surface and player ownership
2. Audio session, PiP, AirPlay, and lifecycle findings
3. Buffering, subtitle, error, and cleanup findings
4. Boundary to PhotoKit or MusicKit
5. Validation run or still needed
