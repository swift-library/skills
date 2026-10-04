# Scripts

All scripts take `--help`. Run them with Python 3.9 or later from any
directory; they read the target repository and never change it.

| Script | Purpose | Exit codes |
| --- | --- | --- |
| `readme_facts.py REPO [--badges \| --install]` | Facts as JSON, the badge block, or the SwiftPM dependency line, derived from the origin remote, tags, `Package.swift`, `LICENSE`, and the CI workflow. | 0, or 1 when URLs cannot be built |
| `check_readme.py REPO` | README findings: shadowed README, broken links and anchors, missing alt text, emoji, local paths, install owner, version, or branch that does not exist, and badges that differ from facts. | 0 clean, 1 findings |
| `quickstart_check.py REPO [--run] [--local] [--destination D]` | Builds the Quick start in a scratch consumer that depends on the published URL with the README's requirement. | 0 pass, 1 build failed, 2 input missing |
| `social_preview.py --logo ... --out card.svg [--png card.png]` | 1280x640 social preview card from an existing logo, with text converted to outlines. | 0 |
| `logo_row.py LOGO ... --out banner.svg` | Text-free banner of existing logos in one row. | 0 |
| `terminal_svg.py TRANSCRIPT OUT.svg [--title T]` | Static terminal window from a real transcript. | 0 |
| `svg_embed.py` | Helper module: places an SVG or PNG logo inside another SVG with prefixed ids. | not a command |

## Dependencies

- `git` for facts and checks; `swift` (and `xcodebuild` for `--destination`)
  for `quickstart_check.py`, which also needs network access to resolve the
  published package unless `--local` is used.
- `fontTools` for `social_preview.py` (`python3 -m pip install fonttools`) and
  font files whose license allows converting text to outlines.
- `rsvg-convert` (librsvg) for `--png` and for previewing SVGs as PNG.

## Examples

```bash
python3 scripts/readme_facts.py . --badges
python3 scripts/check_readme.py .
python3 scripts/quickstart_check.py . --run
python3 scripts/social_preview.py --logo Documentation/Assets/Logo.svg \
  --owner example-org --name swift-example \
  --summary "Parse and format example values in Swift." \
  --font-bold Inter-Bold.ttf --font-regular Inter-Regular.ttf \
  --out /tmp/card.svg --png /tmp/card.png
python3 scripts/logo_row.py a/Logo.svg b/Logo.svg c/Logo.svg --out /tmp/banner.svg
python3 scripts/terminal_svg.py demo.txt Documentation/Assets/Demo.svg --title swift-example
```
