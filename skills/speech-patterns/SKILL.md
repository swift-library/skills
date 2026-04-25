---
name: speech-patterns
description: Use this skill for Speech framework implementation and review across speech authorization, microphone permission, NSSpeechRecognitionUsageDescription, NSMicrophoneUsageDescription, SpeechAnalyzer, SpeechTranscriber, AssetInventory, AnalyzerInput streams, SFSpeechRecognizer, SFSpeechAudioBufferRecognitionRequest, SFSpeechURLRecognitionRequest, AVAudioEngine taps, live transcription, file transcription, on-device/server recognition decisions, partial/final results, cancellation, and recognition cleanup. Do not use for Natural Language post-processing alone, AVKit playback, server transcription APIs, or generic permission copy.
---

# Speech Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple's Speech framework
when transcribing live or prerecorded audio, managing speech assets, and
coordinating microphone/audio pipeline state.

## When To Use

- Requesting speech recognition authorization, microphone permission, and
  required usage-description keys.
- Implementing live transcription, file transcription, partial/final results,
  alternative transcriptions, confidence handling, or punctuation behavior.
- Using `SpeechAnalyzer`, `SpeechTranscriber`, `AssetInventory`,
  `AnalyzerInput`, or related modern Speech modules.
- Maintaining legacy `SFSpeechRecognizer`, audio-buffer requests, URL requests,
  delegates, and recognition task lifecycle.
- Debugging `AVAudioEngine` taps, audio session category, on-device versus
  server recognition, cancellation, cleanup, and unavailable locales.

## When Not To Use

- Do not use for Natural Language post-processing unless Speech transcription
  is also in scope; use `natural-language-patterns`.
- Do not use for AVKit playback or media-player UI; use `avkit-patterns`.
- Do not use for server transcription APIs, voice AI products, or prompt
  marketing.
- Do not use for generic permission dialog text only; use `interface-writing`.
- Do not invent recognition limits, locale support, asset behavior, or modern
  Speech API availability. Verify current Apple documentation and the local
  SDK.

## Inputs To Inspect

- Speech and microphone usage-description keys, target capabilities, and
  authorization flow.
- `SpeechAnalyzer`, modules, `SpeechTranscriber`, assets, input streams, and
  result-consumption code.
- `SFSpeechRecognizer`, recognition requests, tasks, delegates, locales,
  on-device flags, contextual strings, and availability delegates.
- `AVAudioSession`, `AVAudioEngine`, input node taps, file input, sample format,
  cancellation, cleanup, and UI state.
- Tests, device runs, audio fixtures, privacy/logging, and unavailable-state
  behavior.

## Workflow

1. Confirm whether the feature uses modern Speech modules, legacy
   `SFSpeechRecognizer`, live microphone audio, file audio, or both.
2. Check speech authorization, microphone permission, usage-description keys,
   locale support, and asset availability before starting audio capture.
3. Keep audio session, engine, tap, request, task, and analyzer lifecycle
   explicit. Pair every start path with stop, cancel, finalize, and cleanup.
4. Make partial, final, failure, denied, unavailable, cancelled, and timeout
   states visible in app state.
5. For file transcription, validate audio format compatibility and avoid
   treating long-file behavior as equivalent to live dictation.
6. For on-device recognition, verify support for the locale and API path rather
   than assuming it from device class.
7. Keep transcript post-processing separate from recognition lifecycle and route
   deterministic text analysis to `natural-language-patterns` when needed.

## Review Rules

- Do not start microphone capture before both product intent and permissions are
  clear.
- Do not leave audio taps, recognition tasks, or analyzer input streams active
  after cancellation or finalization.
- Do not assume every locale supports on-device recognition or required assets.
- Do not log raw audio, raw transcripts, or alternatives unless the feature has
  an explicit retention need.
- Treat `SpeechAnalyzer`, `SpeechTranscriber`, asset inventory, recognition
  limits, and modern locale support as current-source gated.

## Validation

- Build the affected app/package against the local SDK.
- Test authorized, denied, restricted, unavailable, and revoked permission
  states.
- Test live transcription and file transcription with representative audio,
  silence, noisy input, and cancellation.
- Test locale unavailable, asset missing/downloading, network unavailable when
  server recognition is possible, and on-device unsupported states.
- Inspect audio engine cleanup, task cancellation, and transcript privacy in
  logs, analytics, and screenshots.

## Output

For implementation or review work, return:

1. Speech surface, permission, locale, and asset assumptions
2. Audio pipeline, recognition lifecycle, and transcript findings
3. On-device/server, cleanup, privacy, and post-processing boundaries
4. Validation run or still needed
5. Current-source assumptions for version-specific behavior
