---
name: vision-patterns
description: Use this skill for Apple Vision and VisionKit implementation and review across OCR, barcode recognition, face detection, face landmarks, image classification, rectangle and horizon detection, document recognition, segmentation, tracking, video-frame processing, coordinate conversion, VNCoreMLModel requests, DataScannerViewController, ImageAnalyzer, VNDocumentCameraViewController, camera permission, overlays, and SwiftUI wrappers. Do not use for Core ML model lifecycle without Vision requests, PhotoKit library workflows, generic camera capture, or visual design.
---

# Vision Patterns

## Purpose

Guide implementation, review, and troubleshooting for Vision and VisionKit
features that recognize, scan, analyze, segment, track, or interact with image
and camera content.

## When To Use

- Implementing OCR, barcode recognition, face detection/landmarks, rectangles,
  horizon detection, image classification, saliency, document recognition, or
  segmentation.
- Processing images, video frames, `CMSampleBuffer` values, orientations,
  normalized coordinates, and bounding boxes.
- Integrating a Core ML model through `VNCoreMLModel` or Vision request
  pipelines.
- Using VisionKit `DataScannerViewController`, `ImageAnalyzer`,
  `ImageAnalysisInteraction`, or `VNDocumentCameraViewController`.
- Reviewing camera permission, availability, overlays, SwiftUI wrappers,
  threading, memory, and device testing for Vision workflows.

## When Not To Use

- Do not use for Core ML model loading or deployment without Vision request
  semantics.
- Do not use for Photos library access or media picking.
- Do not use for generic AVFoundation capture setup unless Vision frame
  analysis is the primary task.
- Do not use for pure visual design, image editing, or product copy.
- Do not invent Vision or VisionKit availability, typed API, or recognition
  behavior. Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- Vision imports, request types, request handlers, image/frame inputs,
  orientation handling, and request reuse.
- OCR languages, recognition levels, custom words, confidence thresholds, and
  text bounding-box mapping.
- Face, barcode, segmentation, tracking, classification, document, and Core ML
  request configuration.
- VisionKit controllers, delegates, async streams, overlays, camera permission,
  and SwiftUI wrappers.
- Sample images/videos, UI coordinate conversion, threading, memory, and tests.

## Workflow

1. Identify whether the feature uses static images, live camera scanning, video
   frames, document capture, or Vision plus Core ML.
2. Confirm platform availability and camera/photo permissions before designing
   user-visible scanning behavior.
3. Normalize image orientation, scale, color space, and coordinate systems at
   the boundary. Keep conversion helpers tested.
4. Configure requests explicitly: language, recognition level, symbologies,
   confidence thresholds, region of interest, revision, and batching when
   applicable.
5. Keep live scanning cancellable and throttled. Avoid retaining frame buffers
   or request results longer than needed.
6. For VisionKit, test `isSupported`, `isAvailable`, delegate events, async
   recognized items, overlays, and camera-denied states.
7. Treat model loading and performance tuning beyond the Vision request as
   general Core ML work once the Vision request integration is stable.

## Review Rules

- Do not trust normalized Vision coordinates without proving the conversion to
  the displayed image or overlay.
- Do not run heavy Vision work on the main actor unless the API requires it and
  the work is trivial.
- Do not assume VisionKit scanning is available on every device or simulator.
- Do not use one request configuration for every document, language, barcode,
  or video-framerate case.
- Treat new Vision request names, typed APIs, and VisionKit behavior as
  current-source gated.

## Validation

- Build the affected app/package against the local SDK.
- Test representative sample images or videos, including rotated, low-light,
  low-resolution, and negative cases.
- Test coordinate overlays visually or with fixture assertions.
- Test camera permission denied/restricted, unsupported device, unavailable
  scanner, and cancellation states when VisionKit is in scope.
- Measure latency, frame rate, memory, and battery impact for live recognition.

## Output

For implementation or review work, return:

1. Vision or VisionKit surface and availability assumptions
2. Request configuration, input handling, and coordinate findings
3. Camera, memory, threading, and Core ML integration boundaries
4. Validation run or still needed
5. Current-source assumptions for version-specific behavior
