# Templates

| File | Output | Notes |
| --- | --- | --- |
| `sections.md.tpl` | The Swift sections of a package repository's root `README.md` | Use the section names and order of the README's skeleton, including `{{snippet_section}}` (for example Quick look or Quick start), and drop sections the skeleton does not contain. Fill `{{install_dependency}}` from `scripts/readme_facts.py --install` and `{{swift_tools}}` and `{{platforms}}` from its facts. Keep `## Products` only when there is more than one product. |

Placeholders use `{{name}}` syntax. A finished file contains none.
