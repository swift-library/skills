---
name: tabletopkit-patterns
description: Use this skill for TabletopKit implementation and review across visionOS tabletop games, TabletopGame, TableSetup, Tabletop, EntityTabletop, equipment protocols, seats, TableState, TabletopAction, move/update equipment actions, turns, score counters, state bookmarks, interactions, gestures, dice, RealityKit rendering, GroupActivities synchronization, and multiplayer table state. Do not use for generic board-game rules, GameKit matchmaking, RealityKit-only rendering, or browser games without TabletopKit.
---

# TabletopKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for TabletopKit spatial
tabletop games, including table setup, equipment, seats, turns, actions,
bookmarks, interactions, RealityKit rendering, and group-session state.

## When To Use

- Building or reviewing a TabletopKit game on visionOS.
- Creating `TabletopGame`, `TableSetup`, `Tabletop`/`EntityTabletop`, equipment,
  cards, pieces, dice, counters, or seats.
- Managing `TableState`, `TabletopAction`, move/update equipment actions,
  turn-setting, score counters, bookmarks, or custom actions.
- Handling table interactions, gestures, dice tossing, seat ownership, arbiter
  behavior, or multiplayer state.
- Rendering table, equipment, or seats through RealityKit entities.
- Synchronizing tabletop state through GroupActivities.

## When Not To Use

- Do not use for generic board-game rules or AI that do not touch TabletopKit.
- Do not use for Game Center matchmaking, leaderboards, or achievements;
  GameKit services are out of scope.
- Do not use for RealityKit-only rendering without TabletopKit game state;
  standalone RealityKit work is out of scope.
- Do not use for browser tabletop games.

## Inputs To Inspect

- visionOS target setup, TabletopKit imports, and GroupActivities/RealityKit
  dependencies.
- `TabletopGame`, `TableSetup`, tabletop shape, table entity, equipment IDs,
  equipment state, and seat definitions.
- Turn logic, controlling seats, score counters, bookmarks, custom actions, and
  undo/replay assumptions.
- Interaction delegates, gestures, dice/card/piece layouts, and RealityKit
  entity mapping.
- Multiplayer/session coordination, arbiter ownership, state snapshots, and
  debug logs.

## Workflow

1. Confirm the task is TabletopKit state and interaction, not generic board-game
   logic or RealityKit rendering alone.
2. Verify current visionOS, GroupActivities, RealityKit, and TabletopKit API
   behavior before making platform claims.
3. Model the table setup first: tabletop, equipment, seats, identifiers, and
   initial state.
4. Keep game rules, visual state, and synchronized table state separate.
5. Use TabletopKit actions for state changes that need to sync or replay.
6. Validate seat control, turn progression, interaction lifecycle, dice/card
   mechanics, bookmarks, and score counters.
7. Inspect multiplayer and arbiter behavior before assuming deterministic state
   across participants.

## Review Rules

- Do not hide table-state mutations behind visual-only RealityKit code.
- Do not treat arbitrary game logic as synced unless TabletopKit or the session
  layer owns it.
- Do not assume all players have seats, controls, or the same local view state.
- Do not overuse GameKit when GroupActivities/TabletopKit owns the table state.
- Treat visionOS requirements, GroupActivities behavior, RealityKit rendering,
  and multiplayer synchronization as current Apple documentation and SDK gated.

## Validation

- Build the visionOS app target.
- Test table setup, equipment lookup, seat claim/release, actions, turns, score
  counters, bookmarks, interactions, dice/card behavior, and state snapshots.
- Test multiplayer/group-session behavior with multiple participants when
  synchronization is in scope.
- Validate RealityKit entity mapping and interaction hit targets in device or
  simulator conditions appropriate to the feature.

## Output

For implementation or review work, return:

1. TabletopKit versus GameKit/RealityKit/browser boundary decision
2. Table setup, equipment, seat, and identifier findings
3. Action, turn, interaction, bookmark, and score findings
4. RealityKit rendering and GroupActivities synchronization findings
5. Validation run or still needed
