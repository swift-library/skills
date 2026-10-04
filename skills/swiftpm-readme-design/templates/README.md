# Templates

| File | Output | Notes |
| --- | --- | --- |
| `README.md.tpl` | Root `README.md` of a package repository | Fill `{{badges}}` and `{{install_dependency}}` from `scripts/readme_facts.py`. Remove sections that would be empty and add `## Products` when there is more than one product. Drop the logo paragraph when the repository has no logo. |
| `profile.README.md.tpl` | `profile/README.md` in an organization's `.github` repository | Repeat the table row per repository and the group section per group. Use each repository's About sentence verbatim. |

Placeholders use `{{name}}` syntax. A finished file contains none.
