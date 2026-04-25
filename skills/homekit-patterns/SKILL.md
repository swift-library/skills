---
name: homekit-patterns
description: Use this skill for HomeKit and MatterSupport implementation and review across HMHomeManager, homes, rooms, accessories, services, characteristics, action sets, triggers, Matter commissioning, MatterAddDeviceExtensionRequestHandler, HomeKit entitlements, delegate lifecycle, and HomeKit Accessory Simulator validation. Do not use for generic Bluetooth, generic networking, SwiftUI architecture, or broad IoT product strategy.
---

# HomeKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for HomeKit smart-home
features, including HomeKit data modeling and Matter commissioning flows.

## When To Use

- Building or reviewing HomeKit access with `HMHomeManager`, homes, rooms,
  accessories, services, and characteristics.
- Reading, writing, observing, or presenting `HMCharacteristic` values and
  metadata.
- Implementing action sets, timer triggers, event triggers, accessory setup, or
  home automation workflows.
- Adding Matter commissioning with MatterSupport and
  `MatterAddDeviceExtensionRequestHandler`.
- Validating entitlements, single-manager lifecycle, delegate wiring, and HomeKit
  Accessory Simulator behavior.

## When Not To Use

- Do not use for generic Bluetooth communication; use
  `core-bluetooth-patterns`.
- Do not use for generic transport or Bonjour networking; use
  `network-framework-patterns`.
- Do not use for AccessorySetupKit picker flows outside HomeKit/Matter handoff;
  use `accessorysetupkit-patterns`.
- Do not use for SwiftUI app architecture unless the HomeKit integration is the
  reason for the task.

## Inputs To Inspect

- Entitlements, capabilities, Info.plist keys, and deployment targets.
- `HMHomeManager` ownership, delegate lifetime, and home/accessory observation.
- Characteristic read/write paths, notification handling, metadata parsing, and
  error recovery.
- MatterSupport extension target, principal class, commissioning methods, and
  home/room/network selection behavior.
- Simulator, accessory, and device test notes.

## Workflow

1. Confirm the task is HomeKit or MatterSupport, not generic accessory or
   network work.
2. Verify current platform, entitlement, and device availability before treating
   the API path as usable.
3. Keep one durable `HMHomeManager` owner and avoid view-local manager
   lifetimes.
4. Model the HomeKit hierarchy explicitly: home, room, accessory, service, and
   characteristic.
5. Read characteristic metadata before rendering or writing values, and handle
   unsupported, unauthorized, unreachable, and stale states.
6. For Matter commissioning, inspect the extension request handler methods,
   home/room selection, device credential validation, Thread/Wi-Fi selection,
   and commissioning error paths.
7. Validate with simulator support where useful and with physical accessories
   when the behavior depends on hardware.

## Review Rules

- Do not flatten HomeKit into generic IoT or Bluetooth advice.
- Do not recreate `HMHomeManager` from transient SwiftUI view updates.
- Do not assume all accessories expose the same services, characteristic types,
  metadata, or writability.
- Treat entitlement, accessory category, and Matter commissioning behavior as
  current Apple documentation and SDK gated.
- Keep user home structure and accessory identifiers out of unnecessary logs.

## Validation

- Build the affected app and extension targets.
- Test authorized, denied, unavailable, no-home, unreachable accessory, read,
  write, notification, and stale-data paths.
- Exercise action sets, triggers, and Matter commissioning paths that the app
  claims to support.
- Use HomeKit Accessory Simulator or physical accessories for behavior that
  cannot be proven from code.

## Output

For implementation or review work, return:

1. HomeKit or MatterSupport boundary decision
2. Entitlement, availability, and lifecycle assumptions
3. Home/accessory/service/characteristic findings
4. Matter commissioning or trigger/action-set findings when applicable
5. Validation run or still needed
