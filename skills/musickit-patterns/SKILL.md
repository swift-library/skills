---
name: musickit-patterns
description: Use this skill for MusicKit and Apple Music implementation and review across MusicAuthorization, catalog and library access, Apple Music subscription checks and offers, ApplicationMusicPlayer/SystemMusicPlayer, playback queues, artwork, charts, playlists, user tokens, MediaPlayer integration, Now Playing, remote commands, background audio, interruptions, and route changes. Do not use for generic AVKit video playback, StoreKit purchases, non-Apple streaming services, or music marketing copy.
---

# MusicKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for Apple Music features that
use MusicKit, MediaPlayer, subscription state, catalog/library data, and music
playback queues.

## When To Use

- Requesting or reviewing `MusicAuthorization` and Apple Music capability
  setup.
- Searching or displaying catalog, artwork, charts, genres, albums, songs,
  artists, playlists, or library content.
- Checking `MusicSubscription`, presenting subscription offers, or handling
  unavailable catalog playback.
- Using `ApplicationMusicPlayer`, `SystemMusicPlayer`, queues, playback state,
  Now Playing metadata, or remote commands.
- Debugging Apple Music user-token, region, library, playback, or background
  audio behavior.

## When Not To Use

- Do not use for generic video playback or AVKit player UI; use
  `avkit-patterns`.
- Do not use for StoreKit purchases or in-app subscriptions.
- Do not use for non-Apple streaming services unless an Apple-platform app also
  uses MusicKit.
- Do not use for music marketing copy, App Store metadata, or playlist strategy
  alone.
- Do not invent catalog availability, subscription offer, token, or regional
  behavior. Verify current Apple documentation and live platform behavior.

## Inputs To Inspect

- MusicKit capability, usage descriptions, authorization requests, and
  subscription checks.
- Catalog/library queries, artwork loading, playlist modification, and user data
  access.
- Player choice, queue construction, playback commands, playback-state
  observation, Now Playing, and MediaPlayer integration.
- Background audio mode, audio session, interruptions, route changes, and remote
  command handling.
- Region/subscription test accounts, device behavior, and fallback UI.

## Workflow

1. Identify whether the feature needs catalog browsing, library access,
   subscription playback, queue control, or MediaPlayer integration.
2. Request MusicKit authorization only for user data access or playback
   features that require it.
3. Check subscription and catalog playback capability before starting playback
   or showing subscription offers.
4. Choose `ApplicationMusicPlayer` for app-owned playback state and
   `SystemMusicPlayer` only when controlling the Music app's state is intended.
5. Keep catalog/library fetches, artwork loading, player queue state, and UI
   state separate.
6. Configure background audio, interruptions, route changes, Now Playing, and
   remote commands only when the app owns playback.
7. Validate with authorized, denied, no-subscription, region-unavailable, and
   background playback cases.

## Review Rules

- Do not assume authorization means the user can play catalog content.
- Do not hard-code catalog availability or subscription offer behavior.
- Do not mix StoreKit purchase flows with MusicKit subscription state.
- Do not mutate a user's library without explicit user intent.
- Do not block UI on large catalog or artwork requests.
- Keep app-owned playback distinct from Music app system playback.

## Validation

- Build the affected app target.
- Test authorization status transitions and denied behavior.
- Test subscription unavailable and catalog unavailable states.
- Test queue updates, play/pause/skip, interruption, route change, and
  background playback when in scope.
- Test artwork and library access with real account/device coverage when
  platform behavior matters.

## Output

For implementation or review work, return:

1. MusicKit capability and authorization model
2. Catalog/library/subscription findings
3. Player, queue, background, and MediaPlayer findings
4. Boundary to AVKit or StoreKit
5. Validation run or still needed
