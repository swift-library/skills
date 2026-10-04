---
name: pencilkit-patterns
description: Use this skill for PencilKit implementation and review across PKCanvasView, PKDrawing, PKToolPicker, inking/eraser/lasso tools, custom tool picker items, accessory items, Apple Pencil hover/squeeze/roll interactions, drawing policies, stroke inspection, serialization, image export, thumbnails, undo/redo, SwiftUI wrappers, and device testing. Do not use for PaperKit structured markup, PDFKit document semantics, generic vector drawing, or visual design polish alone.
---

# PencilKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for PencilKit drawing
experiences that capture Apple Pencil or finger input, manage drawing tools,
serialize drawings, and integrate with SwiftUI or UIKit/AppKit surfaces.

## When To Use

- Creating or reviewing `PKCanvasView`, `PKDrawing`, `PKToolPicker`, drawing
  policies, tools, and delegates.
- Adding inking, eraser, lasso, ruler, custom tool picker items, accessory
  items, or Apple Pencil hover/squeeze/roll behavior.
- Serializing drawings, exporting images, generating thumbnails, inspecting
  strokes, combining drawings, or preserving drawing versions.
- Wrapping PencilKit in SwiftUI and debugging coordinator, undo/redo, lifecycle,
  or tool picker state.
- Testing Apple Pencil behavior on device.

## When Not To Use

- Do not use for PaperKit structured markup.
- Do not use for PDF document semantics, forms, search, or PDF permissions.
- Do not use for generic vector drawing frameworks unless PencilKit is the
  capture surface.
- Do not use for visual design polish alone.
- Do not invent Apple Pencil hardware behavior or tool picker API availability.
  Verify current Apple documentation and device capability.

## Inputs To Inspect

- `PKCanvasView`, `PKDrawing`, `PKToolPicker`, tool configuration, and delegate
  code.
- SwiftUI wrappers, coordinator ownership, first responder handling, undo/redo,
  and tool picker visibility.
- Drawing serialization, image export, thumbnailing, stroke inspection, and
  versioning.
- Apple Pencil hover, squeeze, roll angle, and custom tool picker item logic.
- Device testing notes and simulator limitations.

## Workflow

1. Identify whether the feature needs freeform drawing, annotation, signature,
   stroke analysis, export, or Pencil-specific interactions.
2. Own `PKCanvasView`, `PKDrawing`, and `PKToolPicker` state outside transient
   SwiftUI body construction.
3. Configure drawing policy, first responder, tool picker visibility, and tool
   selection before adding product-specific UI.
4. Keep drawing persistence, undo/redo, image export, and thumbnail generation
   explicit.
5. Inspect stroke data only when the feature needs real stroke semantics.
6. Validate Apple Pencil hover, squeeze, roll, and custom tool picker behavior
   on compatible hardware.

## Review Rules

- Do not confuse `PKDrawing` freeform strokes with PaperKit structured markup.
- Do not drop drawing data when SwiftUI view identity changes.
- Do not assume simulator behavior covers Apple Pencil hardware interactions.
- Do not serialize drawings without versioning or migration thinking when the
  data is durable.
- Do not generate large images or thumbnails on the main actor when avoidable.
- Keep tool picker observers and first responder behavior cleaned up.

## Validation

- Build the affected app target.
- Test draw, erase, select, undo, redo, save, load, and export paths.
- Test SwiftUI wrapper lifecycle across navigation, resize, and scene changes.
- Test custom tool picker items and accessory actions when present.
- Test Apple Pencil-specific behavior on compatible hardware when in scope.

## Output

For implementation or review work, return:

1. Drawing surface and tool model
2. Persistence, export, and wrapper findings
3. Hardware-specific behavior and validation status
4. Boundary to PaperKit or PDFKit
5. Validation run or still needed
