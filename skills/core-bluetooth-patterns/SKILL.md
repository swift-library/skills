---
name: core-bluetooth-patterns
description: Use this skill for Core Bluetooth implementation and review across CBCentralManager, CBPeripheral, CBPeripheralDelegate, CBPeripheralManager, CBMutableService, CBCharacteristic, CBDescriptor, CBUUID, BLE scanning, connection, service/characteristic discovery, read/write/notify flows, GATT modeling, advertising, L2CAP channels, background modes, state restoration, NSBluetoothAlwaysUsageDescription, and Bluetooth Classic support. Do not use for AccessorySetupKit picker setup, AudioAccessoryKit automatic audio switching, Core NFC, or generic networking.
---

# Core Bluetooth Patterns

## Purpose

Guide implementation, review, and troubleshooting for Core Bluetooth central
and peripheral roles, GATT data exchange, advertising, background behavior, and
Bluetooth runtime state.

## When To Use

- Implementing BLE central scanning, connection, service discovery,
  characteristic discovery, reads, writes, notifications, or indications.
- Implementing peripheral advertising, GATT services, characteristics,
  descriptors, subscriptions, requests, or L2CAP channels.
- Debugging `CBCentralManager`, `CBPeripheral`, `CBPeripheralManager`, state
  restoration, background modes, permissions, or platform support.
- Reviewing Bluetooth Classic usage through Core Bluetooth when that API is in
  scope.

## When Not To Use

- Do not use for AccessorySetupKit picker-based setup.
- Do not use for AudioAccessoryKit placement/capability state.
- Do not use for NFC, Network.framework, or ordinary HTTP networking.
- Do not use for hardware product strategy without Core Bluetooth code.
- Do not invent background privileges, platform support, or Bluetooth Classic
  behavior. Verify current Apple documentation and physical device behavior.

## Inputs To Inspect

- Usage-description keys, background modes, entitlements, target platforms, and
  accessory/device assumptions.
- Central manager, scan filters, connection flow, peripheral delegate,
  service/characteristic discovery, read/write/notify code, and reconnect
  strategy.
- Peripheral manager, advertised data, GATT model, characteristic permissions,
  subscription, request handling, and L2CAP code.
- State restoration, physical device logs, packet captures, and test harnesses.

## Workflow

1. Classify the role: central, peripheral, or both.
2. Check authorization and manager state before scanning, advertising, or
   connecting.
3. Use targeted service UUID filters where possible and keep scan windows
   bounded.
4. Model GATT services and characteristics explicitly, including properties,
   permissions, MTU/fragmentation, endianness, and notification semantics.
5. Keep connection, discovery, subscription, transfer, timeout, and reconnect
   state machines explicit.
6. Handle background restoration and platform limitations as separate behavior,
   not as ordinary foreground scanning.
7. Validate on physical hardware; simulators are not enough for Bluetooth
   correctness.

## Review Rules

- Do not start scanning before `.poweredOn`.
- Do not scan forever or scan without filters unless the product requires it.
- Do not assume one write equals one complete application message.
- Do not ignore duplicate peripherals, stale identifiers, disconnects, or
  notification cleanup.
- Do not rely on background behavior without background modes and device tests.
- Treat iOS 26 Live Activity background privileges and Bluetooth Classic
  support as current-source gated.

## Validation

- Build the affected app target.
- Test permission denied, Bluetooth off, unsupported, scanning, connection,
  discovery, read/write/notify, disconnect, reconnect, and background paths.
- Test MTU/fragmentation and malformed payloads.
- Test with physical peripherals or centrals representative of the product.
- Inspect logs for private device identifiers and payload leakage.

## Output

For implementation or review work, return:

1. Core Bluetooth role, permission, and platform assumptions
2. Scan, connection, GATT, transfer, and background findings
3. AccessorySetupKit, AudioAccessoryKit, privacy, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for Bluetooth behavior
