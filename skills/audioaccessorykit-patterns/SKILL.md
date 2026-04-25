---
name: audioaccessorykit-patterns
description: Use this skill for AudioAccessoryKit implementation and review across AccessoryControlDevice, accessory capabilities, AccessoryControlDevice.Configuration, Placement, automatic audio switching, third-party audio accessory companion apps, AccessorySetupKit pairing handoff, connected audio sources, placement state updates, EU availability constraints, development/ad hoc distribution limits, and physical accessory validation. Do not use for AVKit playback, Core Bluetooth setup, AccessorySetupKit picker flows, generic audio sessions, or market eligibility claims.
---

# AudioAccessoryKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for AudioAccessoryKit
companion apps that update third-party audio accessory capabilities and state
for automatic audio switching.

## When To Use

- Configuring `AccessoryControlDevice`, capabilities, configuration, placement,
  and connected audio source state.
- Implementing companion-app handoff after AccessorySetupKit pairing.
- Updating in-ear, off-head, or related placement state for automatic audio
  switching.
- Reviewing development/ad hoc distribution limits, EU availability
  constraints, physical accessory validation, and graceful unavailable states.

## When Not To Use

- Do not use for AVKit playback or media-player UI; use `avkit-patterns`.
- Do not use for AccessorySetupKit picker/pairing setup; use
  `accessorysetupkit-patterns`.
- Do not use for generic Core Bluetooth runtime communication; use
  `core-bluetooth-patterns`.
- Do not use for generic `AVAudioSession` routing without AudioAccessoryKit.
- Do not invent distribution, region, device, or App Store behavior. Verify
  current Apple documentation and portal state.

## Inputs To Inspect

- AudioAccessoryKit imports, `AccessoryControlDevice` setup, capabilities,
  configuration, placement, and connected-source update code.
- AccessorySetupKit pairing handoff and accessory identity mapping.
- Distribution channel, device/region assumptions, entitlement/capability
  setup, and unavailable-state UI.
- Physical accessory state, logs, and test matrix.

## Workflow

1. Confirm the task is AudioAccessoryKit state/capability reporting, not
   pairing, playback, or generic Bluetooth.
2. Verify device, distribution, and regional constraints before promising user
   availability.
3. Keep accessory identity and pairing handoff explicit.
4. Update placement and connected-source state promptly and idempotently.
5. Handle unsupported device, unsupported region, unpaired accessory, stale
   accessory state, and update failure.
6. Validate with a physical accessory and device conditions that match the
   expected deployment.

## Review Rules

- Do not treat AudioAccessoryKit as a general audio-routing API.
- Do not duplicate AccessorySetupKit ownership inside this skill.
- Do not present automatic switching as available to all customer installs
  without current eligibility checks.
- Do not log sensitive accessory identifiers or user behavior unnecessarily.
- Treat distribution and regional constraints as current-source gated.

## Validation

- Build the affected app target.
- Test unsupported, unpaired, paired, placement update, connected-source update,
  failure, and stale-state paths.
- Test development/ad hoc deployment assumptions and eligible-region behavior
  when feasible.
- Validate with physical accessories and real audio route changes when
  possible.

## Output

For implementation or review work, return:

1. AudioAccessoryKit device, distribution, and region assumptions
2. Accessory control, capability, placement, and source-state findings
3. AccessorySetupKit, Bluetooth, playback, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for AudioAccessoryKit eligibility
