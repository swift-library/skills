# Scripts

| Script | Purpose |
| --- | --- |
| `export_profile.py --profile {minimal,standard} --output DIR` | Exports the profile, accepts identity placeholders with `--set NAME=VALUE`, fills package facts with `--package-root DIR`, skips inherited community files with `--inherited PATH`, and overwrites existing files only with `--force`. |
| `profile_export.py` | Shared output-map parsing, package facts, placeholder replacement, and file export used by the command and validator. |
| `validate_template_exports.py` | Materializes the `minimal` and `standard` profiles from `templates/` into a temporary directory and checks the exported files and the generated agent guide contract, including its Code Review Rules section. Run after changing templates or profiles. |
| `validate_canonical_target.py REPOSITORY` | Checks an edited target repository's `AGENTS.md` and documentation surface against the canonical-artifact rules before handoff, including the Code Review Rules section and the 32 KiB agent guide budget. |

The command and validators use only the Python standard library and exit non-zero
on findings.

The export smoke test materializes local community files. Collection checks also
exercise inherited and mixed community-file selections through `export_profile`,
whose `inherited_paths` input comes from the repository's GitHub settings owner.
