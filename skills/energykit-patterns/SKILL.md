---
name: energykit-patterns
description: EnergyKit implementation and review for residential electricity guidance, cleaner-energy and utility-rate context, venues, EV/HVAC load events, guidance tokens, and unsupported regions. Not for HomeKit accessory control or commercial/industrial energy systems.
---

# EnergyKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for EnergyKit residential
electricity guidance, venue-aware clean-energy suggestions, and EV/HVAC load
event reporting.

## When To Use

- Querying electricity guidance or cleaner energy periods with EnergyKit.
- Building dashboards or recommendations around residential energy guidance.
- Handling energy venues, connected utility-provider context, rate-aware
  guidance, or unsupported-region states.
- Reporting EV charger or HVAC load event sessions.
- Reviewing EnergyKit entitlement setup, guidance tokens, suggested actions,
  and insight presentation.

## When Not To Use

- Do not use for HomeKit accessory control.
- Do not use for generic IoT, Bluetooth, or HVAC device communication.
- Do not use for marketing, sustainability claims, or campaign messaging.
- Do not use for commercial or industrial energy-management systems.

## Inputs To Inspect

- Entitlements, deployment target, region assumptions, and energy venue setup.
- Electricity guidance query code, suggested-action mapping, guidance tokens,
  and dashboard presentation.
- EV charger and HVAC load event session lifecycle.
- Unsupported-region, unavailable-utility, missing-venue, and stale-guidance
  behavior.
- Privacy, retention, and logging boundaries around energy data.

## Workflow

1. Confirm the task is EnergyKit guidance or load-event reporting rather than
   accessory control.
2. Verify current entitlement access, supported regions, and platform behavior
   before promising feature availability.
3. Model venue and utility/rate context explicitly.
4. Keep guidance values, suggested actions, and guidance tokens scoped to the
   user decision they support.
5. Handle unsupported region, missing venue, unavailable utility account, stale
   data, and failed load-event session paths.
6. Validate dashboard copy and charts against actual EnergyKit data semantics.

## Review Rules

- `ElectricityGuidance` is available on iOS/macOS 26+, not watchOS/tvOS/visionOS;
  `EnergyVenue.venues()` requires iOS/macOS 26.1+.
- Iterate `ElectricityGuidance.sharedService.guidance(using:at:)` as a throwing
  async sequence; pass an `ElectricityGuidance.Query` and venue UUID.
- Query actions are `.shift` or `.reduce`; guidance values pair `DateInterval`
  with a `Double` rating, and the response carries a UUID `guidanceToken`.
- Keep `.locationHasRatePlan` and `.guidanceIncorporatesRatePlan` distinct
  when interpreting the guidance response's `options` set.
- Submit typed load events with `EnergyVenue.submitEvents(_:)`; EV/HVAC sessions
  carry `.begin`, `.active`, or `.end` plus `wasFollowingGuidance` and a token.
- On iOS/macOS 27+, use `init(timestamp:measurement:session:device:)` with
  `ElectricalLoadDevice`; EV/HVAC `deviceID:` initializers are deprecated there.
- Do not issue device-control advice from EnergyKit alone.
- Do not treat guidance as a guarantee of cost, carbon, or grid outcome.
- Do not assume support outside documented residential EV/HVAC-style use cases.
- Do not log detailed household energy behavior unnecessarily.
- Treat entitlement access, supported regions, venue behavior, guidance tokens,
  and load-event reporting as current Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test supported and unsupported region states, missing venue, guidance query,
  suggested-action rendering, guidance token retention, load-event start/update
  and end, and error paths.
- Use representative account/device conditions when real EnergyKit data is
  needed to prove the behavior.

## Output

For implementation or review work, return:

1. EnergyKit versus HomeKit/IoT boundary decision
2. Entitlement, region, venue, and utility assumptions
3. Guidance, suggested-action, token, and dashboard findings
4. EV/HVAC load-event findings when applicable
5. Validation run or still needed
