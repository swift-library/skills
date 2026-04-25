# Optional IDB UI Interaction

Use `scripts/idb_ui.py` only when IDB is installed and semantic UI interaction
is useful. IDB is optional; simulator lifecycle and `xcodebuild` workflows do
not require it.

## Check Availability

```bash
python3 "${SKILL_DIR}/scripts/idb_ui.py" check
```

If IDB is missing, report that semantic UI tree and text-based interaction are
blocked. Continue with `simctl` operations when possible.

## Inspect The Current Screen

```bash
python3 "${SKILL_DIR}/scripts/idb_ui.py" map --device booted
python3 "${SKILL_DIR}/scripts/idb_ui.py" map --device booted --hints
python3 "${SKILL_DIR}/scripts/idb_ui.py" tree --device booted --json
```

Use `map` for concise interactive elements. Use `tree --json` only when the
full accessibility hierarchy is needed.

## Basic Actions

```bash
python3 "${SKILL_DIR}/scripts/idb_ui.py" tap-text --device booted --text "Login"
python3 "${SKILL_DIR}/scripts/idb_ui.py" find --device booted --find-type TextField --index 0 --tap
python3 "${SKILL_DIR}/scripts/idb_ui.py" find --device booted --find-id submitButton --tap
python3 "${SKILL_DIR}/scripts/idb_ui.py" type --device booted --text "person@example.com"
python3 "${SKILL_DIR}/scripts/idb_ui.py" key --device booted --key return
python3 "${SKILL_DIR}/scripts/idb_ui.py" button --device booted --button home
python3 "${SKILL_DIR}/scripts/idb_ui.py" tap --device booted --x 200 --y 400
python3 "${SKILL_DIR}/scripts/idb_ui.py" swipe --device booted --direction up
python3 "${SKILL_DIR}/scripts/idb_ui.py" long-press --device booted --point 200,300 --duration 2
python3 "${SKILL_DIR}/scripts/idb_ui.py" pinch --device booted --direction out
python3 "${SKILL_DIR}/scripts/idb_ui.py" audit --device booted --json
```

Prefer semantic `tap-text` over raw coordinates when the screen exposes usable
labels. Use raw coordinates only when location itself matters or semantics are
missing.

## Boundaries

- IDB output is accessibility-tree evidence, not a complete accessibility
  audit. Use `accessibility-patterns` for dedicated accessibility findings.
- Do not assert that a screen is correct from one tree dump. Pair it with the
  user task, logs, screenshots, tests, or source inspection as needed.
