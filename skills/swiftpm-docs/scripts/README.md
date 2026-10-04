# Scripts

| Script | Purpose |
| --- | --- |
| `validate_template_exports.py` | Materializes the `minimal` and `standard` profiles from `templates/` into a temporary directory and checks the exported files and the generated agent guide contract. Run after changing templates or profiles. |
| `validate_canonical_target.py REPOSITORY` | Checks an edited target repository's `AGENTS.md` and documentation surface against the canonical-artifact rules before handoff. |

Both use only the Python standard library and exit non-zero on findings.
