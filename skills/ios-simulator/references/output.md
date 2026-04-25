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

Simulator evidence can identify where to look, but source fixes belong in the
appropriate skill:

- SwiftUI source behavior: `swiftui-patterns`.
- Visual SwiftUI polish: `swiftui-design`.
- Dedicated accessibility issues: `accessibility-patterns`.
- Focus behavior: `focus-engine-patterns`.
- Performance trace work: `xcode-instruments`.
- Persistence issues: `swiftdata-patterns` or `core-data-patterns`.

## Script Mapping

- Upstream-style build/test and progressive disclosure:
  `scripts/xcode_build.py`.
- Upstream-style simulator lifecycle, app lifecycle, log monitor, clipboard,
  privacy, push, status bar, selector, and health check: `scripts/sim.py`.
- Upstream-style screen mapper, navigator, gesture, keyboard, and lightweight
  accessibility-tree audit: `scripts/idb_ui.py`.
- Upstream-style app state capture: `scripts/state_capture.py`.
- Upstream-style test recorder: `scripts/test_recorder.py`.
- Upstream-style visual diff: `scripts/visual_diff.py`.
- Upstream-style Core Data / SwiftData model inspection:
  `scripts/model_inspector.py`.
