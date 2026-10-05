---
name: gamekit-patterns
description: Use this skill for GameKit and Game Center implementation and review across Game Center entitlement setup, GKLocalPlayer authentication, authenticateHandler, scoped player identifiers, GKAccessPoint, Game Center dashboards, GKLeaderboard, GKAchievement, GKMatchmakerViewController, GKMatch, GKTurnBasedMatch, multiplayer matchmaking, saved games, challenges, friends, nearby discovery, and server identity verification. Do not use for SpriteKit/SceneKit/RealityKit rendering, browser games, generic networking, or StoreKit commerce.
---

# GameKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for GameKit and Game Center
features, including player identity, dashboards, leaderboards, achievements,
real-time multiplayer, turn-based matches, saved games, and social features.

## When To Use

- Enabling Game Center and authenticating `GKLocalPlayer`.
- Presenting `GKAccessPoint`, Game Center dashboards, leaderboards,
  achievements, or matchmaker UI.
- Submitting scores with `GKLeaderboard` or progress with `GKAchievement`.
- Building real-time matches with `GKMatchmakerViewController`, `GKMatch`, and
  match delegates.
- Building turn-based games with `GKTurnBasedMatch`, turn events, match data,
  exchanges, and participant outcomes.
- Handling saved games, challenges, friends, nearby players, scoped player
  identifiers, or server-side identity verification.

## When Not To Use

- Do not use for SpriteKit, SceneKit, or RealityKit rendering mechanics;
  rendering is out of scope.
- Do not use for browser games or web multiplayer.
- Do not use for generic socket/network transport unless GameKit owns the match.
- Do not use for purchases, subscriptions, or app commerce; StoreKit commerce is
  out of scope.

## Inputs To Inspect

- Game Center entitlement, App Store Connect/Xcode GameKit configuration, and
  platform targets.
- `GKLocalPlayer` authentication owner, `authenticateHandler`, and player state
  observation.
- Access point/dashboard presentation, view-controller delegates, and UI
  placement.
- Leaderboard and achievement identifiers, score/progress submission, and
  offline/error behavior.
- Real-time and turn-based match requests, delegates, data size, participant
  state, disconnects, and cleanup.
- Saved-game conflict handling, friend/challenge flows, and server identity
  verification.

## Workflow

1. Confirm the task is GameKit/Game Center rather than rendering, networking, or
   commerce.
2. Verify current GameKit availability, entitlement configuration, and service
   behavior before making platform claims.
3. Initialize and retain local-player authentication state before accessing Game
   Center data.
4. Keep dashboard/access-point presentation separated from game-loop rendering.
5. Treat leaderboard, achievement, saved-game, and match identifiers as durable
   product configuration that must match App Store Connect or Xcode setup.
6. For real-time matches, verify request limits, delegate lifetime, data
   transport, disconnects, and matchmaking cleanup.
7. For turn-based matches, preserve match data versioning, participant outcomes,
   turn ordering, exchange handling, and match removal behavior.
8. Validate with signed-in and signed-out player states and real Game Center
   service paths when possible.

## Review Rules

- Do not assume the local player is authenticated or allowed to use every Game
  Center feature.
- Do not store or transmit unscoped legacy player identifiers. Use
  `gamePlayerID` or `teamPlayerID` instead of the deprecated `playerID`.
- Submit and load scores with `GKLeaderboard` and `GKLeaderboard.Entry`, not
  the deprecated `GKScore` APIs.
- Verify identity on a server with
  `GKLocalPlayer.fetchItems(forIdentityVerificationSignature:)`, not the
  deprecated `generateIdentityVerificationSignature(completionHandler:)`.
- Do not treat GameKit match data as unlimited or durable app storage.
- Do not block the game loop on Game Center network calls.
- Treat Game Center service behavior, identity verification, matchmaking,
  leaderboard configuration, and platform-specific dashboard behavior as current
  Apple documentation and service gated.

## Validation

- Build the affected app target.
- Test signed-out, sign-in UI, authenticated, denied/unavailable, access point,
  dashboard, leaderboard, achievement, saved-game, and error paths.
- Test real-time or turn-based match flows with multiple players/devices when
  the feature depends on Game Center service behavior.
- Test server identity verification when the app trusts GameKit identity on a
  backend.

## Output

For implementation or review work, return:

1. GameKit versus rendering/networking/commerce boundary decision
2. Entitlement, local-player, and dashboard findings
3. Leaderboard, achievement, saved-game, and identity findings
4. Matchmaking or turn-based findings when applicable
5. Validation run or still needed
