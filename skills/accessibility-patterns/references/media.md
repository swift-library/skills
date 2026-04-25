# Media Accessibility

Use this file for captions, audio descriptions, speech, Smart Invert, media
playback, and routing chart-specific accessibility.

## Prefer System Media Controls

Prefer platform media players when they meet product requirements. System
players provide caption, subtitle, audio route, playback, and accessibility
behavior that custom players must recreate.

For UIKit video playback, `AVPlayerViewController` usually provides the safest
baseline. For SwiftUI, wrap or use platform-native playback APIs according to
the app's target and existing stack.

## Captions And Subtitles

Provide captions for dialogue and meaningful sound in video or audio-only
content when the app's common tasks depend on that media.

For custom media UI:

- expose a visible way to choose captions where product requirements allow it
- respect system caption preferences where possible
- test caption appearance with user settings
- verify captions stay synchronized and visible in light/dark appearance

Do not use subtitles as a substitute for captions when important non-speech
audio is part of comprehension.

## Audio Descriptions

Provide audio descriptions when visual-only video content is necessary to
understand or complete a common task.

For custom media UI:

- detect and expose available audio description tracks
- respect system audio description preferences where possible
- make track selection reachable with VoiceOver, Voice Control, Switch Control,
  and keyboard where applicable

## Speech

For speech synthesis or spoken content:

- respect audio session behavior and user expectations around spoken audio
- avoid overlapping system VoiceOver speech with app speech
- provide visible alternatives where speech conveys essential information
- localize spoken text and pronunciation where needed

## Smart Invert And Image-Like Content

Use Smart Invert protection for photos, videos, maps, artwork, and other media
whose meaning depends on original colors:

```swift
Image("MapSnapshot")
    .accessibilityIgnoresInvertColors()
```

Use this sparingly. Do not protect ordinary UI chrome that should adapt to
accessibility display settings.

## Charts

Chart accessibility belongs primarily in `swift-charts-patterns`. Route
Swift Charts work involving `AXChartDescriptorRepresentable`, Audio Graph,
`.accessibilityChartDescriptor`, mark labels, chart summaries, or custom chart
fallbacks to that skill.

For non-chart accessibility audits, note chart blockers and then hand off
chart-specific implementation to `swift-charts-patterns`.

## Checklist

- [ ] Captions are available for meaningful speech and sound.
- [ ] Audio descriptions are available for meaningful visual-only video.
- [ ] Media controls are reachable with assistive technologies.
- [ ] Caption and audio-description settings respect system preferences where
      possible.
- [ ] Speech does not conflict with VoiceOver.
- [ ] Photos, videos, and maps protect original colors only when needed.
- [ ] Chart-specific work routes to `swift-charts-patterns`.
