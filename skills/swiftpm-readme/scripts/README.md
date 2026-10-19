# Scripts

All scripts take `--help`. Run them with Python 3.9 or later from any
directory; they read the target repository and never change it.

| Script | Purpose | Exit codes |
| --- | --- | --- |
| `readme_facts.py REPO [--install]` | Facts and badge values as JSON, or the SwiftPM dependency line, derived from the origin remote, tags, `Package.swift`, `LICENSE`, and the CI workflow. | 0, or 1 when URLs cannot be built |
| `check_readme.py REPO [--readme PATH]` | README findings: shadowed README, broken links and anchors, missing alt text, local paths, an install owner, version, or branch that does not exist, badge values that differ from facts or have none, and CI badges for missing workflows. | 0 clean, 1 findings |
| `quickstart_check.py REPO [--readme PATH] [--section TITLE] [--run] [--local] [--destination D]` | Builds the snippet under the named section (default "Quick start") in a scratch consumer that depends on the published URL with the README's requirement. | 0 pass, 1 build failed, 2 input missing |

`--readme` paths are relative to `REPO` and default to `README.md`.

`readme_facts.py` reports `badges` as values keyed by kind (`ci`, `swift`,
`platforms`, `license`), with a kind present only when a repository fact backs
it. `check_readme.py` compares the label and message of shields.io static
badges with those values and ignores colors, styles, and other query
parameters.

## Dependencies

- `git` for facts and checks.
- `swift` (and `xcodebuild` for `--destination`) for `quickstart_check.py`,
  which also needs network access to resolve the published package unless
  `--local` is used.

## Examples

```bash
python3 scripts/readme_facts.py .
python3 scripts/readme_facts.py . --install
python3 scripts/check_readme.py .
python3 scripts/quickstart_check.py . --section "Quick look" --run
```
