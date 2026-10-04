---
name: realitykit-patterns
description: Use this skill for RealityKit and ARKit implementation and review across RealityView, ARView, Entity, Component, System, AnchorEntity, AnchoringComponent, ModelEntity, USDZ/Reality Composer Pro assets, materials, lighting, physics, collision and input targets, gestures, raycasting, scene understanding, ARKit sessions and anchors, hand/world tracking, spatial audio, SharePlay synchronization, and spatial performance. Do not use for SceneKit-only maintenance, SpriteKit 2D, TabletopKit game-state mechanics, or Focus Engine-only selection.
---

# RealityKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for RealityKit and ARKit 3D,
AR, and spatial experiences, including entities, components, systems, anchors,
assets, materials, physics, gestures, AR sessions, scene understanding, and
performance.

## When To Use

- Building or reviewing `RealityView`, `ARView`, entities, components, systems,
  or anchors.
- Loading USDZ, Reality Composer Pro, or bundled RealityKit assets.
- Creating programmatic meshes, `ModelEntity` content, materials, lighting,
  physics, collision shapes, input targets, gestures, or spatial audio.
- Integrating ARKit sessions, anchors, raycasting, plane/image/object/body/hand
  tracking, scene understanding, camera permission, or device support checks.
- Synchronizing RealityKit content across devices or SharePlay sessions.
- Reviewing RealityKit performance, entity lifecycle, pooling, draw calls, and
  memory pressure.

## When Not To Use

- Do not use for SceneKit-only maintenance unless migration to RealityKit is the
  task.
- Do not use for SpriteKit 2D scenes.
- Do not use for TabletopKit game-state semantics.
- Do not use for Focus Engine-only focus movement.
- Do not use for low-level Metal rendering unless RealityKit integration is the
  issue.

## Inputs To Inspect

- `RealityView` make/update closures, `ARView` setup, ARKit session or provider
  configuration, and permission checks.
- Entity hierarchy, component storage, systems, anchors, transforms, and update
  ownership.
- Asset-loading paths, USDZ/Reality Composer Pro content, async loading, and
  memory behavior.
- Materials, lights, physics, collisions, input targets, gestures, raycasting,
  and hit testing.
- ARKit anchors, scene understanding, tracking state, camera/session lifecycle,
  and device capability checks.
- Performance diagnostics, entity pooling, draw calls, accessibility, and
  synchronization behavior.

## Workflow

1. Confirm the task is RealityKit/ARKit scene construction, not SceneKit,
   SpriteKit, TabletopKit state, or focus-only work.
2. Verify current platform, device capability, permission, and SDK behavior
   before making spatial/AR claims.
3. Choose presentation surface deliberately: `RealityView`, `ARView`, or a
   renderer path.
4. Keep entity creation, component mutation, and system updates out of
   accidental SwiftUI update churn.
5. Anchor content explicitly and handle tracking loss, relocalization, and
   unsupported devices.
6. Generate collision shapes and input targets before relying on gestures or
   hit testing.
7. Load heavy assets asynchronously and validate memory, draw calls, and frame
   timing on representative devices.

## Review Rules

- Do not mutate RealityKit entities from transient SwiftUI closures without a
  stable owner.
- Do not assume ARKit data, camera access, or scene understanding is available
  without capability and permission checks.
- Do not use RealityKit to own TabletopKit turn/equipment state.
- Do not mix SceneKit migration claims into new RealityKit architecture without
  current docs or prototype evidence.
- Treat RealityKit API additions, visionOS differences, ARKit tracking
  providers, asset-loading behavior, and performance characteristics as current
  Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test entity creation, asset loading, anchors, tracking state, gestures,
  collisions, physics, materials, lighting, cleanup, and unsupported-device
  paths.
- Test ARKit permission, session start/stop, relocalization, raycasting, and
  scene-understanding behavior when AR is in scope.
- Profile frame time, draw calls, memory, and asset load latency for complex
  scenes.

## Output

For implementation or review work, return:

1. RealityKit/ARKit versus SceneKit/SpriteKit/TabletopKit boundary decision
2. Presentation, entity, component, system, and anchor findings
3. Asset, material, physics, input, and ARKit findings
4. Performance, accessibility, and synchronization findings
5. Validation run or still needed
