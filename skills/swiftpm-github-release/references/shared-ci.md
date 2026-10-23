# Shared CI for Swift Packages

This reference defines what an organization's shared CI does for its Swift
packages and how a member declares what to run. Each organization family
implements it in its `<org>/github-workflows` repository; the files that
implement this contract are identical across families. A family or a member may
add jobs beyond this contract, as declared extensions.

## Required Checks

A member requires exactly two checks:

| Check | Caller job | Purpose |
| --- | --- | --- |
| `policy / policy` | `policy` | Commit signatures, pull-request title and added-line rules. When `.github/release.json` exists, also the version declaration. |
| `validate / result` | `validate` | The aggregate of every validation job the member declares. |

Validation always runs formatting, tests and a release build. Platforms,
documentation and the terminal demo run only when declared. Consumer packages,
dependency-minimum builds, public-interface comparisons and post-release
verification are not part of the contract; behavior belongs in the package's own
tests.

## Caller

```yaml
jobs:
  validate:
    uses: <org>/github-workflows/.github/workflows/swift-package.yml@<full-sha> # vX.Y.Z
```

The caller passes no inputs; the workflow reads the member's configuration from
its checkout. Pin the full commit; add the version comment once that commit is
the family release.

## Configuration

A member declares validation in `.github/swift-package.json`. The family's JSON
Schema validates it, and an invalid or unknown key fails the configuration job.

| Key | Required | Meaning |
| --- | --- | --- |
| `compilers` | yes | Non-empty list of `{name, runner, xcode, swift?}` entries. Each runs `swift test` and `swift build -c release` with the package's default traits. `swift` installs an official release toolchain after selecting `xcode`. The lowest compiler equals `minimum_swift` in `release.json` when that file exists. |
| `format` | no | `{paths}`: swift-format strict lint paths; default `["Package.swift", "Sources", "Tests"]`. Formatting runs on the last compiler entry's runner and toolchain using the repository's `.swift-format`. |
| `package_directory` | no | Package root inside the repository; default `.`. |
| `test_configurations` | no | Build configurations for `swift test`; default `["debug"]`. |
| `build_system` | no | SwiftPM `--build-system` value for every SwiftPM command. |
| `traits` | no | Additional trait sets beyond the default traits, e.g. `[[], ["Experimental", "default"]]`; `"default"` enables the default traits and an empty set disables them. Each set runs `swift test` once on the first `compilers` entry, by convention the minimum compiler, without a release build. |
| `environment` | no | String map exported to every validation command. The demo recording takes its environment only from the script's `env`, so the recording stays reproducible from the script. |
| `platforms.linux` | no | List of `{name, image}`; `image` is a digest-pinned Swift Docker image. Runs `swift test` in the container with the default traits. |
| `platforms.apple` | no | List of `{name, platform, scheme, test?, runner?, xcode?}` for iOS, tvOS, watchOS or visionOS. Builds for the generic destination; with `test: true`, prepares a matching simulator runtime and runs the scheme's tests. Defaults to the last compiler entry's runner and Xcode. |
| `docs` | no | `{targets, traits?}`: one public symbol-graph dump with extension blocks, then a DocC conversion of each target's catalog with warnings as errors. `traits` is one trait set for the dump, for documented trait-gated API. Declare it only when the package ships DocC documentation. |
| `demo` | no | `{product, script?}`: builds the release executable `product` and re-records the terminal demo (default script `.github/assets/terminal/script.yml`), comparing only `recording.json` through the `github-readme-design` action's recording-only mode. On drift the job uploads the regenerated `recording.json` as an artifact for the maintainer to commit. Declare it only for a command-line tool with a README demo. |
| `commands` | no | List of `{name, run, runner?, xcode?}` for repository-specific checks, such as `scripts/check-spec`. Each runs in the member checkout. |
| `timeout_minutes` | no | Per-job limit from 1 to 360; default 45. |

Minimal configuration:

```json
{
  "compilers": [
    { "name": "macos-26-swift-6.3", "runner": "macos-26", "xcode": "26.6" }
  ]
}
```

## Release

A member that publishes GitHub releases keeps `.github/release.json` with
`repository`, `version_file`, `version_pattern`, `changelog`, `minimum_swift`
and `platforms`, and calls `swift-package-release.yml` after a successful
validation of the tagged commit. The release workflow verifies the signed
annotated tag, the version declaration and the changelog entry, then publishes
the release notes. It attaches no assets and builds no source.

## Repository Scripts

Checks that only one member needs live in that member's lowercase `scripts/`
directory and run through `commands`. When a second member needs the same
check, the family promotes it into `github-workflows` as a declared option
instead of copying the script. A template carries no scripts.

## Implementation Requirements

- Workflows run their own scripts by checking out the workflow repository at
  `job.workflow_sha`; they embed no script source and need no generators.
- macOS builds and tests pass `--disable-index-store`; CI never uses the index.
  Linux keeps it because XCTest discovers tests through the index store.
- Each job requests only the permissions it uses. Release workflows restore
  and save no caches and never cancel running or queued releases.
- The repository validates itself: its CI calls the validation and policy
  workflows with passing fixture packages and runs each job's rejection path
  against a failing fixture through its scripts. Release and organization
  workflows are covered by workflow linting and unit tests and exercised by
  their consumers.
- The README documents the job catalog, the configuration reference, caller
  examples and pinning.
