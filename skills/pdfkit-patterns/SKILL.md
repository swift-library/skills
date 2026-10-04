---
name: pdfkit-patterns
description: Use this skill for PDFKit implementation and review across PDFView, PDFDocument, PDFPage, PDFSelection, PDFAnnotation, navigation, search, thumbnails, forms, links, outlines, page manipulation, rendering, printing, password-protected documents, access permissions, annotation persistence, and SwiftUI wrappers. Do not use for PaperKit structured markup, PencilKit freeform drawing, generic document storage, or PDF generation unrelated to PDFKit behavior.
---

# PDFKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for PDF display, navigation,
search, annotation, form, rendering, page manipulation, and SwiftUI wrapping
using PDFKit.

## When To Use

- Displaying or reviewing PDFs with `PDFView`, `PDFDocument`, `PDFPage`, and
  page navigation.
- Implementing search, selection, highlights, annotations, links, forms,
  outlines, thumbnails, or permissions.
- Creating, merging, splitting, rotating, cropping, rendering, printing, or
  exporting PDF content with PDFKit.
- Wrapping PDFKit in SwiftUI and debugging coordinator, annotation hit testing,
  page state, or persistence behavior.

## When Not To Use

- Do not use for structured markup editing with PaperKit.
- Do not use for freeform Apple Pencil drawing mechanics with PencilKit.
- Do not use for generic document storage or file coordination unless PDFKit
  behavior is the main issue.
- Do not use for server-side PDF generation unrelated to Apple PDFKit APIs.
- Do not invent platform quirks, permission behavior, or annotation persistence
  rules. Verify current Apple documentation and local SDK behavior.

## Inputs To Inspect

- `PDFView`, `PDFDocument`, `PDFPage`, `PDFSelection`, `PDFAnnotation`, and
  SwiftUI wrapper code.
- Document loading, passwords, permissions, page navigation, notifications, and
  display modes.
- Search, selection, text extraction, annotations, widgets/forms, outlines, and
  links.
- Page manipulation, rendering, printing, save/export, and annotation
  persistence code.
- Test PDFs: encrypted, large, annotated, form-based, scanned, and malformed
  documents.

## Workflow

1. Identify the PDF workflow: read-only viewing, annotation, forms, search,
   page manipulation, rendering, printing, or export.
2. Choose `PDFView` display mode, scaling, page model, and document ownership
   before adding UI.
3. Handle loading errors, password prompts, permissions, page count, and
   malformed documents.
4. Keep annotations, selections, forms, and search results tied to page
   coordinates and document save behavior.
5. For SwiftUI wrappers, keep coordinator state explicit and avoid recreating
   `PDFDocument` or `PDFView` on every update.
6. Validate with representative PDFs, including large, encrypted, scanned,
   annotated, and form documents when those behaviors matter.

## Review Rules

- Do not assume all PDFs have selectable text.
- Do not mutate annotations or forms without a save/export path.
- Do not ignore document permissions or password-protected failures.
- Do not mix PDF page coordinates with SwiftUI view coordinates without clear
  conversion.
- Do not rebuild PDF views in SwiftUI updates without preserving page and zoom
  state.
- Keep PaperKit and PencilKit responsibilities separate unless the task is an
  explicit integration.

## Validation

- Build the affected app target.
- Test open, page navigation, zoom, search, annotation, save/export, and
  printing where applicable.
- Test encrypted, scanned, large, and malformed PDFs when in scope.
- Test SwiftUI wrapper update cycles, page restoration, and annotation hit
  testing.
- Verify annotation/form persistence by reopening the saved document.

## Output

For implementation or review work, return:

1. PDF workflow and document model
2. Display, navigation, search, and annotation findings
3. Save/export, permission, and wrapper findings
4. Boundary to PaperKit or PencilKit
5. Validation run or still needed
