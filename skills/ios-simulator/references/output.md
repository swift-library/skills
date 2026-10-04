# Output And Handoff

Keep simulator tool output short and actionable.

## Default Reporting

Include:

1. Phase / stage judgment
2. Simulator or build surface inspected
3. Actions performed
4. Findings
5. Compatibility / tooling impact
6. Validation performed
7. Risks
8. Next steps

For quick operations, a shorter answer is fine if it names the command result
and any file path produced.

## JSON

Use `--json` when another script, agent, or follow-up step needs structured
data. Summarize JSON for the user instead of pasting large payloads.

## Destructive Operations

For erase/delete/reset operations:

- Require explicit user intent.
- Use an explicit simulator UDID or exact name.
- Use the script confirmation flag.
- Report what was erased or reset.

## Handoff

Simulator evidence can identify where to look, but source fixes are out of
scope. Report the evidence and name the affected area:

- SwiftUI source behavior.
- Visual SwiftUI polish.
- Dedicated accessibility issues.
- Focus behavior.
- Performance trace work.
- Core Data or SwiftData persistence issues.

## Script Mapping

- Build/test and result drill-down: `scripts/xcode_build.py`.
- Simulator lifecycle, app lifecycle, log monitor, clipboard, privacy, push,
  status bar, selector, and health check: `scripts/sim.py`.
- Screen mapper, navigator, gesture, keyboard, and lightweight
  accessibility-tree audit: `scripts/idb_ui.py`.
- App state capture: `scripts/state_capture.py`.
- Test recorder: `scripts/test_recorder.py`.
- Visual diff: `scripts/visual_diff.py`.
- Core Data / SwiftData model inspection: `scripts/model_inspector.py`.
