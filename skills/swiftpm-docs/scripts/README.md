# Scripts

| Script | Purpose |
| --- | --- |
| `export_profile.py --profile {minimal,standard} --output DIR` | Exports the profile, accepts identity placeholders with `--set NAME=VALUE`, fills package facts with `--package-root DIR`, selects optional contracts with `--module canonical-artifacts`, skips inherited community files with `--inherited PATH`, and overwrites existing files only with `--force`. `--check` instead compares the exported files with those in `DIR`, prints a unified diff for each difference, writes nothing and exits 1 on any difference. |
| `profile_export.py` | Shared output-map parsing, package facts, module selection, placeholder replacement, file export and export comparison used by the command and validator. |
| `action.yml` | Composite action that runs `export_profile.py --check` in a repository's CI. Inputs: `path` (repository and package root, default `.`), `profile`, and one-per-line `modules`, `values` (`NAME=VALUE`) and `inherited`. |
| `validate_template_exports.py` | Materializes the `minimal` and `standard` profiles from `templates/` into a temporary directory and checks the exported files with and without the optional canonical-artifacts contract, including its Code Review Rules section. Run after changing templates or profiles. |
| `validate_canonical_target.py REPOSITORY` | For a target carrying the canonical-artifacts module, checks its `AGENTS.md` and documentation surface against the canonical-artifact rules before handoff, including the Code Review Rules section and the 32 KiB agent guide budget. |

The command and validators use only the Python standard library and exit non-zero
on findings.

`--package-root` names the repository root. The exporter reads `Package.swift`
at `.github/swift-package.json`'s `package_directory` (default `.`) for
requirements. Local commands are `swift build` and `swift test`, with
`--package-path` for a nested package. Explicit `--set` values take precedence.

A repository's CI pins the action by full commit SHA, so its documentation stays
checked against that commit until the repository moves the pin:

```yaml
- uses: <owner>/<repository>/skills/swiftpm-docs/scripts@<full-sha>
  with:
    profile: minimal
    modules: canonical-artifacts
    values: |
      repo-name=<repository name>
      package-name=<package name>
```

When a moved pin reports differences, run `export_profile.py` from a checkout of
the new commit with the same arguments and `--force`, review the result, and
commit it with the pin.

The export smoke test materializes local community files. Collection checks also
exercise inherited and mixed community-file selections through `export_profile`,
whose `inherited_paths` input comes from the repository's GitHub settings owner.

Modules are off by default in `export_profile.py`. The template validator checks
both profiles in both modes; `--module canonical-artifacts` selects only that
module variant. The target validator detects `## Canonical Artifacts` in
`AGENTS.md` and reports not applicable when absent. Pass
`--module canonical-artifacts` to require the contract, including its heading.
