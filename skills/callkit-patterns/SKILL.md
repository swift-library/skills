---
name: callkit-patterns
description: Use this skill for CallKit and PushKit VoIP implementation and review across CXProviderConfiguration, CXProvider, CXCallController, CXCallUpdate, incoming and outgoing calls, provider delegates, answer/end/mute/hold actions, VoIP push token and push handling, audio-session coordination, and Call Directory extensions. Do not use for generic notifications, AVKit playback, ordinary audio sessions, or app architecture without CallKit lifecycle work.
---

# CallKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for CallKit system call
integration, PushKit VoIP call delivery, and Call Directory extensions.

## When To Use

- Reporting incoming calls or starting outgoing calls through CallKit.
- Configuring `CXProviderConfiguration`, `CXProvider`, `CXCallController`,
  `CXCallUpdate`, transactions, and provider delegate methods.
- Handling `CXAnswerCallAction`, `CXEndCallAction`, mute, hold, group, DTMF, or
  call-translation actions.
- Registering PushKit VoIP tokens and reporting calls promptly after VoIP push
  receipt.
- Coordinating CallKit lifecycle with audio-session activation and call
  connection state.
- Building or reviewing a Call Directory extension for caller identification or
  blocking.

## When Not To Use

- Do not use for generic UserNotifications/APNs behavior; use
  `user-notifications-patterns`.
- Do not use for media playback or Picture in Picture; use `avkit-patterns`.
- Do not use for ordinary app navigation or architecture without CallKit state.
- Do not use for generic `AVAudioSession` routing unless CallKit activates it.

## Inputs To Inspect

- CallKit capability setup, PushKit registration, and app lifecycle code.
- `CXProvider` ownership, provider configuration, delegate implementation, and
  action fulfillment/failure paths.
- Incoming-call reporting, outgoing transaction submission, and call UUID
  mapping.
- VoIP push token refresh, push handling, server correlation, and error
  recovery.
- Audio-session activation/deactivation and Call Directory extension loading.

## Workflow

1. Confirm the feature is system call integration rather than a notification or
   media feature.
2. Verify current platform support, entitlement/capability requirements, and
   VoIP push behavior before making API claims.
3. Keep `CXProvider` and call UUID ownership explicit and durable.
4. Report incoming calls with `CXCallUpdate`, and keep delayed network
   connection state separate from CallKit action completion.
5. Submit outgoing calls through `CXCallController` transactions.
6. Fulfill or fail every action after the telephony work reaches the matching
   state.
7. Coordinate audio session activation from provider delegate callbacks.
8. Validate PushKit token refresh, push receipt, immediate call reporting, and
   Call Directory extension error handling when those surfaces are present.

## Review Rules

- Do not treat PushKit VoIP pushes as ordinary background notifications.
- Do not create multiple unrelated `CXProvider` owners for the same call
  service.
- Do not fulfill CallKit actions before the app has reached the required call
  state.
- Do not leak phone numbers, handles, or caller metadata in unnecessary logs.
- Treat VoIP push policy, default-calling behavior, Call Directory limits, and
  platform support as current Apple documentation and SDK gated.

## Validation

- Build the app and any Call Directory extension target.
- Test incoming call, answer, end, outgoing start, mute/hold where supported,
  audio-session activation/deactivation, token refresh, push receipt, and call
  failure paths.
- Test device behavior for VoIP pushes and call UI; simulator-only evidence is
  not enough for delivery claims.

## Output

For implementation or review work, return:

1. CallKit versus notification/audio boundary decision
2. Provider, call UUID, and action lifecycle findings
3. PushKit and audio-session coordination findings
4. Call Directory findings when applicable
5. Validation run or still needed
