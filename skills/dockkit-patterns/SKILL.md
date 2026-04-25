---
name: dockkit-patterns
description: Use this skill for DockKit implementation and review across DockAccessoryManager, DockAccessory, DockKitError, dock accessory observation, system tracking enable/disable, custom tracking, motorized stand control, rotation/positioning, camera app integration, AVCaptureSession coordination, subject/object tracking, device support, user permission, and physical dock validation. Do not use for generic camera capture, Vision recognition without dock control, Core Motion sensors, or broad accessory setup.
---

# DockKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for DockKit-compatible
motorized stands, system tracking, custom tracking, and camera coordination.

## When To Use

- Observing and controlling dock accessories with `DockAccessoryManager` and
  `DockAccessory`.
- Enabling/disabling system tracking or implementing custom object/subject
  tracking behavior.
- Coordinating DockKit with camera sessions, framing, rotation, positioning,
  and physical dock state.
- Debugging `DockKitError`, unsupported devices, unavailable accessories, and
  physical dock validation.

## When Not To Use

- Do not use for generic camera capture or AVFoundation pipeline work unless
  dock control is the concrete issue.
- Do not use for Vision recognition without DockKit accessory movement; use
  `vision-patterns`.
- Do not use for Core Motion sensors or generic accessory setup.
- Do not use for product video strategy without DockKit implementation.
- Do not invent accessory support, permission behavior, or tracking semantics.
  Verify current Apple documentation and physical dock behavior.

## Inputs To Inspect

- DockKit imports, accessory manager/observation code, `DockAccessory` control,
  system tracking toggles, custom tracking code, and error handling.
- Camera permission, `AVCaptureSession` coordination, Vision/custom object
  tracking integration, and user-visible control state.
- Physical dock model, device support, platform target, logs, and test notes.

## Workflow

1. Confirm a DockKit-compatible accessory and iPhone camera flow are actually
   in scope.
2. Check device support, camera permission, accessory availability, and system
   tracking state before custom behavior.
3. Keep accessory observation, movement commands, and cancellation explicit.
4. Coordinate camera frame analysis with DockKit control loops carefully; avoid
   fighting system tracking.
5. Handle accessory disconnects, command failures, unavailable state, and user
   override.
6. Validate on the physical dock; simulator behavior is not enough.

## Review Rules

- Do not assume DockKit is available without an attached compatible accessory.
- Do not run a custom control loop while system tracking should own movement.
- Do not issue unbounded motor commands without cancellation and limits.
- Do not log camera-derived sensitive data unless the feature requires it.
- Treat custom tracking and accessory-control behavior as current-source and
  hardware gated.

## Validation

- Build the affected app target.
- Test accessory absent, present, disconnected, system tracking on/off, custom
  tracking start/stop, command failure, and camera permission states.
- Test physical movement limits and user override.
- Inspect battery, thermal, camera, and motion behavior for long-running
  tracking.

## Output

For implementation or review work, return:

1. DockKit surface, accessory, and camera assumptions
2. Tracking, control, error, and lifecycle findings
3. Vision/camera, privacy, hardware, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for DockKit behavior
