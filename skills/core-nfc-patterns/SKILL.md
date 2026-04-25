---
name: core-nfc-patterns
description: Use this skill for Core NFC implementation and review across NFCNDEFReaderSession, NFCTagReaderSession, NFCReaderSession, NFCNDEFMessage, NFCNDEFPayload, NDEF read/write, ISO 7816, ISO 15693, FeliCa, MIFARE, VAS/payment reader sessions, background tag reading, NFCReaderUsageDescription, NFC tag reader entitlements, readingAvailable checks, session invalidation, and physical tag testing. Do not use for Core Bluetooth, PassKit checkout, general QR/barcode scanning, or generic hardware strategy.
---

# Core NFC Patterns

## Purpose

Guide implementation, review, and troubleshooting for Core NFC tag reading,
NDEF messages, protocol-specific tag sessions, write flows, entitlements, and
physical tag validation.

## When To Use

- Reading or writing NDEF messages with `NFCNDEFReaderSession`,
  `NFCNDEFMessage`, or `NFCNDEFPayload`.
- Using `NFCTagReaderSession` for ISO 7816, ISO 15693, FeliCa, or MIFARE tags.
- Configuring `NFCReaderUsageDescription`, tag reader session entitlements,
  background tag reading, and availability checks.
- Debugging session invalidation, polling options, physical tag behavior,
  payload parsing, and write failures.

## When Not To Use

- Do not use for Bluetooth or accessory setup; use the relevant Bluetooth or
  AccessorySetupKit skill.
- Do not use for PassKit checkout or Apple Pay token handling.
- Do not use for QR/barcode scanning; use `vision-patterns`.
- Do not use for generic hardware strategy without Core NFC code.
- Do not invent NFC format support, entitlement requirements, or background tag
  behavior. Verify current Apple documentation and physical device behavior.

## Inputs To Inspect

- Usage-description keys, entitlements, app IDs, target platform, and device
  support assumptions.
- NDEF session, tag session, delegate, polling option, connect, read, write,
  invalidate, and alert-message code.
- Payload parsing, URI/text/MIME records, protocol-specific commands, and error
  mapping.
- Physical tags, test matrix, device logs, and unsupported-state UI.

## Workflow

1. Classify the NFC task: NDEF read, NDEF write, protocol-specific tag,
   background tag reading, VAS/payment reader, or payload parsing.
2. Check `readingAvailable`, entitlements, usage descriptions, and app-extension
   limitations before starting sessions.
3. Keep session lifecycle explicit: create, begin, detect, connect, read/write,
   invalidate, and user-facing status.
4. Parse payloads defensively and keep tag type assumptions visible.
5. For writes, check writability, capacity, lock state, and failure paths.
6. Validate with physical tags for every supported format.

## Review Rules

- Do not start NFC sessions without availability and entitlement checks.
- Do not treat one tag format as if it covers every NFC tag.
- Do not hide session invalidation reasons behind generic errors.
- Do not log sensitive tag payloads or payment/VAS data.
- Treat background tag reading, VAS/payment reader behavior, and tag-format
  support as current-source gated.

## Validation

- Build the affected app target.
- Test unavailable device, missing entitlement, denied prompt, no tag, wrong
  tag type, read success, write success, write locked/full, and invalidation.
- Test physical tags for each promised technology.
- Test background tag reading when in scope.
- Inspect logs for tag identifiers and payload leakage.

## Output

For implementation or review work, return:

1. Core NFC session type, entitlement, and device assumptions
2. Tag, payload, lifecycle, and write/read findings
3. PassKit, Vision, privacy, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for NFC behavior
