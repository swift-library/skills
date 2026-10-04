---
name: scenekit-patterns
description: Use this skill for SceneKit implementation, migration review, and maintenance across SCNView, SceneView, SCNScene, SCNNode, transforms, SCNGeometry, SCNMaterial, PBR materials, lights, cameras, SCNAction, SCNTransaction, animations, physics, particles, model loading, shader modifiers, SCNProgram, hit testing, render delegates, and SpriteKit overlays. Do not use for new RealityKit/ARKit-first work, SpriteKit 2D, low-level Metal rendering, or browser 3D.
---

# SceneKit Patterns

## Purpose

Guide implementation, review, maintenance, and migration-sensitive work for
SceneKit 3D scene graphs, including nodes, geometry, materials, lighting,
animation, physics, particles, asset loading, shaders, hit testing, and SwiftUI
embedding.

## When To Use

- Maintaining or reviewing existing `SCNView`, `SceneView`, `SCNScene`, or
  `SCNNode` code.
- Working with SceneKit geometry, materials, physically based rendering,
  lighting, cameras, transforms, or constraints.
- Implementing `SCNAction`, `SCNTransaction`, explicit animations, morphs,
  skeletons, or imported animation data.
- Adding physics, particles, hit testing, SpriteKit overlays, custom geometry,
  shader modifiers, `SCNProgram`, or renderer delegates.
- Reviewing SceneKit-to-RealityKit migration boundaries for an existing app.

## When Not To Use

- Do not use for new RealityKit/ARKit-first spatial or AR scene construction.
- Do not use for SpriteKit 2D scene work.
- Do not use for low-level Metal rendering unless SceneKit shader integration
  is the actual issue.
- Do not use for browser 3D or web rendering.

## Inputs To Inspect

- `SCNView`/`SceneView` setup, scene loading, camera, lighting, and render-loop
  configuration.
- Node hierarchy, transforms, constraints, asset formats, and scene references.
- Materials, textures, transparency, PBR settings, shadows, and environment
  lighting.
- Actions, transactions, animations, physics bodies, collision categories, and
  particles.
- Hit testing, gestures, SwiftUI wrapper lifecycle, custom geometry/shaders, and
  render delegate code.
- Migration notes when RealityKit is the likely replacement for new work.

## Workflow

1. Confirm the task is existing SceneKit implementation, maintenance, or
   migration review.
2. Check current Apple documentation and SDK status before making lifecycle,
   availability, or migration claims.
3. Inspect the scene graph and asset-loading path before tuning rendering or
   interaction.
4. Keep transforms, pivots, coordinate conversions, and hit-test spaces explicit.
5. Separate animation mechanisms: actions, transactions, imported animations,
   and frame delegate updates.
6. Treat materials, lighting, transparency, shadows, and shader customization as
   performance-sensitive.
7. When a new feature is better served by RealityKit, state the migration
   boundary and avoid expanding SceneKit unnecessarily.

## Review Rules

- Do not promote SceneKit as the default owner for new spatial or AR work when
  RealityKit is the better current API.
- Do not make deprecation, platform, or migration claims without current Apple
  documentation or SDK verification.
- Do not mix coordinate spaces, pivots, or model scale without explicit
  conversion.
- Do not run heavy asset loading or texture work on interactive frame paths.
- Treat shader, Metal, render-loop, asset-loading, and SwiftUI embedding
  behavior as current Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test scene load, camera, lighting, materials, animations, physics, hit tests,
  SwiftUI embedding, pause/resume, memory, and teardown.
- Profile frame time and asset load behavior when scene complexity or shader
  work is in scope.
- Validate migration claims against a RealityKit prototype or current docs when
  the review recommends migration.

## Output

For implementation or review work, return:

1. SceneKit versus RealityKit/SpriteKit/Metal boundary decision
2. Scene graph, asset, transform, and rendering findings
3. Animation, physics, shader, and interaction findings
4. Migration or maintenance recommendation when applicable
5. Validation run or still needed
