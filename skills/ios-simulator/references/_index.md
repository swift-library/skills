# Reference Index

Use this index only when `SKILL.md` routing is not enough.

## References

- `simctl.md`: simulator lifecycle, app lifecycle, screenshots, logs,
  permissions, clipboard, status bar overrides, health checks, and simulated
  push notifications.
- `xcodebuild.md`: build and test against iOS Simulator destinations, scheme
  discovery, concise output, result bundle handling, and log drill-down.
- `idb.md`: optional IDB semantic UI tree inspection, element mapping,
  tapping by text/type/id, typing, keys, hardware buttons, swiping, scrolling,
  long press, pinch, refresh, lightweight audit, and dependency failure
  handling.
- `output.md`: output shapes, JSON handling, destructive-operation guardrails,
  and handoff of source-code fixes.
- `troubleshooting.md`: high-density failure diagnosis and recovery commands.
- `test-patterns.md`: repeatable simulator smoke, login, visual regression,
  permissions, bug-report, and model-inspection flows.

## Routing

- Device or app operation with `simctl`: `simctl.md`.
- Build, test, scheme, destination, or `.xcresult`: `xcodebuild.md`.
- Accessibility tree, semantic tap/type/swipe, or `idb`: `idb.md`.
- Visual diff, state capture, test recorder, or model inspector:
  `output.md` plus the target script `--help`.
- Command failed or environment is unclear: `troubleshooting.md`.
- User asks for a repeatable testing flow: `test-patterns.md`.
- Unsure how much to report or when to hand off: `output.md`.
