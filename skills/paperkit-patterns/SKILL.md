---
name: paperkit-patterns
description: Use this skill for PaperKit implementation and review across PaperMarkupViewController, PaperMarkup, structured markup elements, feature sets, insertion UI, toolbar/controller integration, PencilKit coexistence, markup persistence, thumbnails, rendering, SwiftUI/UIKit/AppKit wrapping, undo, document-based apps, and compatibility handling. Do not use for freeform PencilKit-only drawing, PDFKit document semantics, or stable production claims without current SDK verification.
---

# PaperKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for PaperKit structured markup
experiences, including markup controllers, persistence, PencilKit coexistence,
rendering, insertion UI, and compatibility handling.

## When To Use

- Creating or reviewing `PaperMarkupViewController`, `PaperMarkup`, supported
  feature sets, markup editing, or structured annotation elements.
- Integrating PaperKit with PencilKit drawing, tool pickers, document viewers,
  note-taking surfaces, or document-based apps.
- Persisting, loading, rendering, thumbnailing, indexing, or migrating PaperKit
  markup data.
- Debugging unsupported content, feature-set compatibility, autosave, undo, or
  SwiftUI/UIKit/AppKit wrapper behavior.

## When Not To Use

- Do not use for freeform drawing with PencilKit only; use
  `pencilkit-patterns`.
- Do not use for PDF document display, forms, search, or PDF permissions; use
  `pdfkit-patterns`.
- Do not use for generic document storage unless PaperKit markup is the main
  data.
- Do not present beta/new API behavior as stable. Verify current Apple
  documentation, Xcode, and SDK symbols before relying on PaperKit API names,
  availability, feature sets, or persistence formats.

## Inputs To Inspect

- `PaperMarkupViewController`, `PaperMarkup`, feature-set configuration, and
  wrapper code.
- Tool, insertion, toolbar, responder, delegate, undo, autosave, and document
  integration.
- PencilKit tool picker and drawing coexistence.
- Persistence, thumbnails, rendering, indexing/search, and compatibility
  handling.
- Test documents, unsupported-content cases, and SDK availability checks.

## Workflow

1. Confirm the current SDK exposes the PaperKit APIs the task needs.
2. Identify whether the feature needs structured markup, freeform drawing,
   document annotation, or a PaperKit/PencilKit mix.
3. Create and retain the markup data model deliberately. Do not let wrapper
   updates recreate it unexpectedly.
4. Configure supported feature sets, tool picker integration, insertion UI, and
   responder behavior before adding product UI.
5. Design persistence, autosave, rendering, thumbnails, undo, and compatibility
   fallback before treating markup as durable app data.
6. Validate unsupported-content and SDK-availability behavior explicitly.

## Review Rules

- Keep every PaperKit API claim current-SDK gated.
- Do not confuse structured markup with PencilKit strokes.
- Do not assume markup persistence is forward/backward compatible without a
  migration and unsupported-content policy.
- Do not rebuild markup controllers in SwiftUI updates without preserving
  document state.
- Do not strip unsupported markup silently.
- Keep PDFKit document semantics separate unless the task is explicit PDF
  annotation integration.

## Validation

- Build with the intended Xcode and platform SDK.
- Test create, edit, save, load, render, and thumbnail paths.
- Test tool picker, insertion UI, undo, and PencilKit coexistence when in scope.
- Reopen saved documents and inspect unsupported-content behavior.
- Test wrapper lifecycle across navigation, resizing, and document reload.

## Output

For implementation or review work, return:

1. SDK/API availability status
2. Markup model and controller ownership
3. Tooling, persistence, rendering, and compatibility findings
4. Boundary to PencilKit or PDFKit
5. Validation run or still needed
