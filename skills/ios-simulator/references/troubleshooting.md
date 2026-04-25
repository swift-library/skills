# Troubleshooting

Use this when a simulator command fails and the first error message is not
enough.

## Quick Diagnostics

```bash
xcrun simctl list devices
python3 "${SKILL_DIR}/scripts/sim.py" health
python3 "${SKILL_DIR}/scripts/sim.py" list --json
python3 "${SKILL_DIR}/scripts/idb_ui.py" check
```

## Common Failures

| Symptom | Likely cause | Next action |
| --- | --- | --- |
| `xcrun` missing | Xcode Command Line Tools unavailable | Run `xcode-select --install` outside the skill workflow. |
| no booted device | No simulator is running | `sim.py suggest`, then `sim.py boot --device NAME --wait`. |
| multiple device matches | Ambiguous simulator name | Re-run with exact `--udid`. |
| app launch fails | Not installed, wrong bundle id, or stale process | `sim.py app-list`, reinstall, then `sim.py restart`. |
| screenshot fails | Device not booted or Simulator service stale | Boot with `--wait`; retry screenshot. |
| logs are empty | Wrong process/bundle filter | Try `sim.py logs --last 5m --tail 200` without filter. |
| IDB target missing | IDB companion is not attached | `idb list-targets`; restart IDB companion if needed. |
| accessibility tree empty | App not foregrounded or IDB unavailable | Launch app, then `idb_ui.py map`; fall back to screenshot. |
| visual diff fails | Pillow missing or image sizes differ | Install Pillow or compare same-size screenshots. |
| `xcresulttool` output differs | Xcode version changed result schema | Use saved log/error drill-down first; then inspect result bundle manually. |

## Recovery Commands

```bash
python3 "${SKILL_DIR}/scripts/sim.py" shutdown --device booted
python3 "${SKILL_DIR}/scripts/sim.py" boot --device "iPhone 17 Pro" --wait
python3 "${SKILL_DIR}/scripts/sim.py" erase --udid <UDID> --yes
python3 "${SKILL_DIR}/scripts/sim.py" logs --device booted --last 10m --tail 200
python3 "${SKILL_DIR}/scripts/state_capture.py" --device booted --output /tmp/sim-state
```

Destructive recovery such as erase/delete should use an exact `--udid` unless
the user explicitly chooses a named target.
