---
name: spritekit-patterns
description: Use this skill for SpriteKit implementation and review across SKScene, SKView, SpriteView, SKRenderer, SKNode, SKSpriteNode, SKAction, texture atlases, physics bodies, SKPhysicsWorld, contact delegates, touch input, SKCameraNode, particles, tile maps, shaders, constraints, frame-cycle callbacks, SwiftUI presentation, and 2D game performance. Do not use for Game Center services, SceneKit 3D, RealityKit/ARKit, browser games, or generic SwiftUI layout.
---

# SpriteKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for SpriteKit 2D game and
graphics work, including scenes, nodes, actions, physics, input, cameras,
particles, tile maps, shaders, SwiftUI presentation, and performance.

## When To Use

- Building or reviewing `SKScene`, `SKView`, `SpriteView`, or `SKRenderer`
  presentation.
- Structuring `SKNode`/`SKSpriteNode` hierarchies, z-ordering, names, and scene
  transitions.
- Implementing `SKAction` animation, custom frame-cycle updates, constraints,
  or GameplayKit-backed scene logic.
- Setting up physics bodies, `SKPhysicsWorld`, contact/collision masks, and
  contact delegates.
- Handling touches, camera/HUD behavior, particles, tile maps, audio nodes,
  texture atlases, shaders, or performance overlays.

## When Not To Use

- Do not use for Game Center identity, leaderboards, achievements, or
  matchmaking.
- Do not use for SceneKit 3D scene graphs.
- Do not use for RealityKit/ARKit spatial or AR scenes.
- Do not use for browser games or web canvas engines.
- Do not use for generic SwiftUI layout unless `SpriteView` is the problem.

## Inputs To Inspect

- Scene lifecycle, renderer choice, frame rate, pause/resume, and transition
  code.
- Node hierarchy, coordinate system usage, asset loading, texture atlas setup,
  and draw order.
- Actions, update loop, timers, constraints, camera, and HUD state.
- Physics bodies, categories, contact/collision masks, joints, fields, and
  delegate ownership.
- Touch input, gesture bridging, SwiftUI wrapper lifetime, and cleanup.
- Performance overlays, texture size, particle count, draw calls, and memory
  pressure.

## Workflow

1. Confirm the task is SpriteKit 2D rendering or game mechanics.
2. Verify current platform support and SpriteKit renderer behavior before
   making platform-specific claims.
3. Decide between `SKView`, `SpriteView`, and `SKRenderer` based on host UI and
   render-loop needs.
4. Keep scene lifecycle explicit: load, present, resize, pause, update, and
   teardown.
5. Separate `SKAction` animation from per-frame simulation logic when state
   needs deterministic control.
6. Model physics categories and contact masks deliberately; test contacts
   before tuning visuals.
7. Validate performance with debug overlays, texture/atlas checks, particle
   counts, and realistic device frame rates.

## Review Rules

- Do not rebuild scenes from transient SwiftUI view updates unless the lifecycle
  is intentional.
- Do not use physics contacts without deterministic category and collision-mask
  definitions.
- Do not let actions, timers, and update-loop state fight over the same node
  properties.
- Do not assume SpriteKit is the right owner for visionOS-native immersive 3D
  content.
- Treat renderer behavior, platform support, physics performance, and SwiftUI
  `SpriteView` integration as current Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test scene presentation, resize, pause/resume, transition, update loop, input,
  physics contacts, camera/HUD behavior, and teardown.
- Test representative devices or simulator frame rates, texture memory, and
  debug overlays for performance-sensitive work.

## Output

For implementation or review work, return:

1. SpriteKit versus GameKit/SceneKit/RealityKit boundary decision
2. Scene, renderer, node, action, and frame-loop findings
3. Physics, input, camera, and asset findings
4. Performance and lifecycle findings
5. Validation run or still needed
