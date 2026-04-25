---
name: photokit-patterns
description: Use this skill for Photos, PhotosUI, and photo/camera workflow implementation and review across PhotosPicker, PHPickerViewController, Transferable media loading, PhotoKit library authorization, limited library handling, saving to albums, PHAsset workflows, AVCaptureSession photo/video capture, camera permission, media thumbnails, downsampling, HEIC/HEIF handling, and media-grid memory behavior. Do not use for playback-only AVKit work, generic image loading, market screenshots, or visual design polish.
---

# PhotoKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for photo picking, photo
library access, media loading, camera capture, and photo asset workflows in
Apple apps.

## When To Use

- Implementing or reviewing `PhotosPicker`, `PHPickerViewController`,
  `Transferable` media loading, or selected-media state.
- Requesting photo-library read/write/add-only access, handling limited
  library, or saving media to the library.
- Working with `PHAsset`, albums, thumbnails, image managers, Live Photos, HEIC
  or HEIF media, or large media grids.
- Building camera photo/video capture with `AVCaptureSession` when the output is
  a photo-library or selected-media workflow.
- Debugging photo/camera permissions, memory, downsampling, orientation, or
  media loading failures.

## When Not To Use

- Do not use for playback-only media UI; use `avkit-patterns`.
- Do not use for generic image loading unrelated to Photos or camera capture.
- Do not use for App Store screenshots or marketing assets.
- Do not use for visual polish of media grids unless Photos/camera behavior is
  the issue.
- Do not invent picker access modes, limited-library behavior, or capture API
  availability. Verify current Apple documentation and local SDK behavior.

## Inputs To Inspect

- Picker configuration, selected item state, `Transferable` loading, and
  cancellation handling.
- Photo-library authorization, usage descriptions, add-only/read-write choices,
  and limited-library management.
- `PHAsset`, image manager, album, save, thumbnail, cache, and memory handling.
- Camera capture session ownership, permission flow, outputs, orientation,
  focus/exposure, flash/torch, and capture callbacks.
- Tests, simulator/device behavior, sample assets, and media-size edge cases.

## Workflow

1. Identify whether the user needs selection, library mutation, capture, asset
   browsing, or media-grid performance.
2. Prefer `PhotosPicker` or `PHPickerViewController` for user-selected media
   when full library access is unnecessary.
3. Request PhotoKit authorization only for app-owned library access or mutation,
   and choose add-only versus read-write deliberately.
4. Load selected media asynchronously with cancellation, progress, memory, and
   unsupported-type handling.
5. For capture, keep `AVCaptureSession` lifecycle and permission handling
   isolated from view state.
6. Downsample large images, cache thumbnails intentionally, and avoid retaining
   full-resolution assets in grid cells.
7. Validate with denied, limited, empty, large, iCloud-backed, and unsupported
   media cases.

## Review Rules

- Do not request full photo-library permission for simple user selection.
- Do not assume selected media is local, small, fast to load, or image-only.
- Do not block the main actor with image decoding, thumbnail generation, or
  PhotoKit fetches.
- Do not ignore orientation, color space, Live Photo, RAW, HEIC/HEIF, or video
  variants when the workflow supports them.
- Do not store persistent access to user assets without a clear data model and
  authorization story.
- Keep playback-only concerns in `avkit-patterns`.

## Validation

- Build the affected app target.
- Test picker cancel, single/multiple selection, unsupported media, and large
  media loading.
- Test denied, limited, add-only, and read-write photo authorization when
  permission handling changes.
- Test camera permission, capture, save, and orientation on device when camera
  behavior matters.
- Profile or manually inspect memory for media grids and batch loading.

## Output

For implementation or review work, return:

1. Media workflow and permission model
2. Picker/library/capture findings
3. Loading, memory, and format findings
4. Boundary to AVKit or design work
5. Validation run or still needed
