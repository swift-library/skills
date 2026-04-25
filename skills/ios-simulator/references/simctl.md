# simctl Operations

Use `scripts/sim.py` for common simulator and app operations. It wraps
`xcrun simctl` and returns concise text by default or JSON with `--json`.

## Discovery

```bash
python3 "${SKILL_DIR}/scripts/sim.py" list
python3 "${SKILL_DIR}/scripts/sim.py" list --json
python3 "${SKILL_DIR}/scripts/sim.py" suggest
```

Use list output before choosing a simulator when the user did not provide a
UDID, booted device, or exact device name.

## Lifecycle

```bash
python3 "${SKILL_DIR}/scripts/sim.py" boot --device "iPhone 16 Pro" --wait
python3 "${SKILL_DIR}/scripts/sim.py" shutdown --device booted
python3 "${SKILL_DIR}/scripts/sim.py" erase --device "<UDID>" --yes
python3 "${SKILL_DIR}/scripts/sim.py" create --device-type "iPhone 17" --runtime "iOS 26"
python3 "${SKILL_DIR}/scripts/sim.py" delete --device "<UDID>" --yes
```

`erase` requires `--yes` and an explicit device. Do not erase a guessed
simulator.

## App Lifecycle

```bash
python3 "${SKILL_DIR}/scripts/sim.py" install --device booted --app /path/App.app
python3 "${SKILL_DIR}/scripts/sim.py" launch --device booted --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" restart --device booted --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" open-url --device booted --url "myapp://route"
python3 "${SKILL_DIR}/scripts/sim.py" terminate --device booted --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" uninstall --device booted --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" app-list --device booted
python3 "${SKILL_DIR}/scripts/sim.py" app-state --device booted --bundle-id com.example.App
```

Prefer `--device booted` only for non-destructive operations. Use a concrete
UDID when multiple simulators are booted.

## Screenshots And Logs

```bash
python3 "${SKILL_DIR}/scripts/sim.py" screenshot --device booted --output /tmp/app.png
python3 "${SKILL_DIR}/scripts/sim.py" logs --device booted --last 5m --process AppName
python3 "${SKILL_DIR}/scripts/sim.py" logs --device booted --duration 30s --output /tmp/logs
```

Keep logs short in chat. Save full logs to files when they are long.

## Permissions, Push, And Status Bar

```bash
python3 "${SKILL_DIR}/scripts/sim.py" privacy --device booted --grant camera --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" privacy --device booted --reset all --bundle-id com.example.App
python3 "${SKILL_DIR}/scripts/sim.py" clipboard --device booted --copy "person@example.com"
python3 "${SKILL_DIR}/scripts/sim.py" push --device booted --bundle-id com.example.App --title "Hi" --body "Message"
python3 "${SKILL_DIR}/scripts/sim.py" status-bar --device booted --preset clean
python3 "${SKILL_DIR}/scripts/sim.py" status-bar --device booted --time 9:41 --battery-level 100
python3 "${SKILL_DIR}/scripts/sim.py" status-bar --device booted --clear
python3 "${SKILL_DIR}/scripts/sim.py" health
```

Use project-local test data for notifications and permissions when available.
