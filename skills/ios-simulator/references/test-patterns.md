# Test Patterns

Use these only when the user asks for a repeatable simulator test flow or when
an investigation needs a concise runbook.

## Smoke Test

```bash
python3 "${SKILL_DIR}/scripts/sim.py" boot --device "iPhone 17 Pro" --wait
python3 "${SKILL_DIR}/scripts/sim.py" install --device booted --app /path/App.app
python3 "${SKILL_DIR}/scripts/sim.py" launch --device booted --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/idb_ui.py" map --device booted --hints
python3 "${SKILL_DIR}/scripts/sim.py" screenshot --device booted --output /tmp/smoke.png
```

## Login Flow

```bash
python3 "${SKILL_DIR}/scripts/idb_ui.py" tap-text --device booted --text "Login"
python3 "${SKILL_DIR}/scripts/idb_ui.py" find --device booted --find-type TextField --index 0 --enter-text "person@example.com"
python3 "${SKILL_DIR}/scripts/idb_ui.py" find --device booted --find-type TextField --index 1 --enter-text "password"
python3 "${SKILL_DIR}/scripts/idb_ui.py" key --device booted --key return
python3 "${SKILL_DIR}/scripts/test_recorder.py" --device booted --test-name "Login smoke" --output test-artifacts
```

## Visual Regression

```bash
python3 "${SKILL_DIR}/scripts/sim.py" screenshot --device booted --output baseline.png
# perform change or navigate
python3 "${SKILL_DIR}/scripts/sim.py" screenshot --device booted --output current.png
python3 "${SKILL_DIR}/scripts/visual_diff.py" baseline.png current.png --threshold 1.0 --output diff.png
```

## Permission And Push Flow

```bash
python3 "${SKILL_DIR}/scripts/sim.py" privacy --device booted --grant camera,photos --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" push --device booted --bundle-id com.example.App --title "Alert" --body "Message"
python3 "${SKILL_DIR}/scripts/sim.py" logs --device booted --last 2m --process Example --tail 80
```

## Bug Report Capture

```bash
python3 "${SKILL_DIR}/scripts/state_capture.py" \
  --device booted \
  --app-bundle-id com.example.App \
  --output bug-report \
  --log-lines 150
```

## Model Inspection

```bash
python3 "${SKILL_DIR}/scripts/model_inspector.py" --project-path . --json
python3 "${SKILL_DIR}/scripts/model_inspector.py" --project-path . --raw ModelName
```
