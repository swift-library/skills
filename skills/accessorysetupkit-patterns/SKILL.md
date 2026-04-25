---
name: accessorysetupkit-patterns
description: Use this skill for AccessorySetupKit implementation and review across ASAccessorySession, ASAccessory, ASDiscoveryDescriptor, ASPickerDisplayItem, ASPickerDisplaySettings, picker discovery, Bluetooth and Wi-Fi accessory setup, NSAccessorySetupKitSupports, event handling, authorization update/finish/fail flows, renaming/removing accessories, Bluetooth HID support options, and bridging to Core Bluetooth or Wi-Fi connection code. Do not use for generic Core Bluetooth scanning, HomeKit/Matter setup, AudioAccessoryKit state after pairing, or broad hardware strategy.
---

# AccessorySetupKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for AccessorySetupKit
discovery, picker-driven setup, accessory authorization, and handoff to
Bluetooth or Wi-Fi connection code.

## When To Use

- Setting up `ASAccessorySession`, `ASDiscoveryDescriptor`,
  `ASPickerDisplayItem`, picker display settings, and session event handling.
- Declaring `NSAccessorySetupKitSupports` and related accessory metadata.
- Reviewing picker flows, filtered discovery, add/remove/rename behavior, and
  authorization finish/fail/update flows.
- Bridging selected accessories to Core Bluetooth or Wi-Fi connection code.
- Debugging Bluetooth HID support options or accessory setup availability.

## When Not To Use

- Do not use for generic Bluetooth scanning or GATT communication after setup;
  use `core-bluetooth-patterns`.
- Do not use for AudioAccessoryKit placement/capability state after pairing;
  use `audioaccessorykit-patterns`.
- Do not use for HomeKit, Matter, or external accessory protocols that do not
  use AccessorySetupKit.
- Do not use for broad product strategy or app architecture.
- Do not invent supported accessory classes, HID behavior, picker behavior, or
  OS availability. Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- Info.plist keys, app capabilities, accessory descriptors, display items, and
  supported options.
- `ASAccessorySession` activation, event handler, picker presentation, picker
  update, finish discovery, and invalidation code.
- Accessory authorization, rename/remove, selected accessory persistence, and
  Core Bluetooth/Wi-Fi handoff code.
- Device logs, physical accessory tests, and unsupported-state UI.

## Workflow

1. Confirm the task is accessory discovery/setup, not ongoing Bluetooth or
   audio accessory state management.
2. Validate Info.plist declaration and descriptor values before debugging
   picker behavior.
3. Keep session activation, event handling, picker display, and invalidation
   lifecycle explicit.
4. Show only accessories the app can actually configure and connect to.
5. Handle added, removed, renamed, partially authorized, failed, unavailable,
   and cancelled states.
6. After setup, hand off to the narrower runtime skill such as Core Bluetooth
   or AudioAccessoryKit.
7. Validate with a physical accessory when hardware behavior is the issue.

## Review Rules

- Do not request broad Bluetooth/Wi-Fi access when AccessorySetupKit can cover
  the setup flow.
- Do not keep picker discovery open indefinitely.
- Do not persist stale accessory identifiers without rechecking state.
- Do not assume HID accessory support without checking supported options and
  descriptor requirements.
- Treat picker, authorization, and accessory class behavior as current-source
  gated.

## Validation

- Build the affected app target.
- Test picker display, cancel, timeout, add, remove, rename, authorization
  success/failure, and unsupported states.
- Test handoff to Core Bluetooth or Wi-Fi runtime code with a physical
  accessory.
- Verify Info.plist keys and user-facing purpose strings.
- Inspect logs for accidental accessory identifiers or network secrets.

## Output

For implementation or review work, return:

1. AccessorySetupKit setup surface and descriptor status
2. Picker, session, authorization, and handoff findings
3. Hardware, permission, lifecycle, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for accessory setup behavior
