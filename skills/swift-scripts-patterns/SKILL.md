---
name: swift-scripts-patterns
description: Use this skill when writing, reviewing, or debugging Swift scripts that run through swift-sh, including swift-sh shebangs such as `#!/usr/bin/swift sh`, `swift-sh` or `swift sh` invocation, swift-sh import-line dependency comments, local path dependency comments, script argument passthrough, stdout/stderr, exit codes, cache/package/open command usage, and script-level validation. Do not use for ordinary Swift scripts with no swift-sh runner or dependency-comment behavior, installing swift-sh or Swift toolchains, Homebrew/tap/PATH setup, Xcode/CLT setup, app implementation, SwiftPM package architecture, or package migration as the primary task.
---

# swift-sh Scripts

## Purpose

Guide authoring and review for scripts whose runner is `swift-sh` or
`swift sh`.

The command surface here is that of
[swift-library/swift-sh](https://github.com/swift-library/swift-sh) 0.1 and
later, which provides `package`, `open`, and `cache clean`. Other tools named
swift-sh, such as 2.x releases, use different commands. When
`swift sh --version` reports another tool, say that its commands differ
instead of translating this skill's commands.

Owned artifact: a one-file swift-sh script, or a review of swift-sh-specific
behavior in that script.

Owned invariant: a kept swift-sh script is explicit about its runner,
import-line dependency comments, dependency source, script-argument boundary,
stdout/stderr contract, failure behavior, and validation.

This skill may mention general script hygiene only when it directly affects a
swift-sh script being written or reviewed. It does not own ordinary Swift
script design, tool installation, package architecture, app implementation, or
migration into a maintained SwiftPM package.

## When To Use

- Writing or reviewing a Swift script that uses a swift-sh shebang, usually
  `#!/usr/bin/swift sh`, or is run with `swift-sh <script>`,
  `swift sh <script>`, stdin mode, or shell process substitution.
- Adding package source and version comments after `import` lines in swift-sh
  scripts, for example `import Markdown  // swiftlang/swift-markdown == 0.8.0`.
- Explaining or validating swift-sh import-line dependency syntax, including
  remote, local path, version, and revision forms.
- Debugging swift-sh runner behavior: script path detection, argument
  passthrough, stdout/stderr, exit codes, cache behavior, or generated package
  behavior.
- Choosing a stable swift-sh invocation when toolchain managers affect
  `swift sh` subcommand lookup.

## When Not To Use

- Installing `swift-sh`, Homebrew, Mint, Swiftly, Xcode, or Command Line Tools.
- Creating or maintaining Homebrew taps, formulas, shell `PATH`, or local tool
  installation state.
- Designing SwiftPM target graphs, products, package dependency direction, or
  package architecture.
- Writing or reviewing an ordinary Swift script that has no swift-sh runner,
  swift-sh command behavior, or swift-sh dependency comments.
- Migrating a script into a maintained package as the implementation task.
- Building app features, SwiftUI/UIKit screens, or framework-specific code.
- Reviewing broad Swift code taste unless the issue is script-specific.

## Authoring Workflow

1. Confirm swift-sh is actually in scope.
   Continue only when the script uses a swift-sh shebang, a `swift-sh` or
   `swift sh` invocation, swift-sh dependency comments, or swift-sh
   cache/package/open behavior.
2. Keep runner assumptions explicit.
   Prefer an executable shebang for scripts meant to be run directly. Use the
   script's documented invocation when one exists.
3. Add dependencies deliberately.
   A dependency should remove real parsing, protocol, or integration risk. Do
   not add a package just to avoid writing a small direct operation.
4. Keep dependency source explicit.
   Put `swift-sh` dependency specs on the relevant `import` line. Prefer local
   path dependencies for local or auditable package code. Prefer explicit
   stable tags for remote dependencies that will be kept.
5. Preserve the argument boundary.
   Arguments after the script path belong to the script. Treat them as opaque
   values from the runner's perspective.
6. Keep the script direct.
   Avoid fake architecture, hidden global state, broad abstractions, service
   layers, and package-shaped module boundaries inside a one-file script.
7. Validate behavior.
   Prefer running the executable script path with an explicit shebang. If the
   file is not executable, use `swift-sh <script>` or `/usr/bin/swift sh
   <script>`. Check arguments, stdout, stderr, exit code, success path, and at
   least one failure path.

## swift-sh Basics

For executable swift-sh scripts, the shebang is the first line that asks a
launcher to run the `sh` subcommand. When writing a new executable script,
prefer this form unless the project documents a different supported swift-sh
shebang:

```swift
#!/usr/bin/swift sh

import Foundation
```

When reviewing existing scripts, recognize other supported swift-sh shebangs,
including `#!/usr/bin/env swift sh` and `#!/usr/bin/swift-sh`. Do not rewrite a
supported shebang unless the task is specifically about runner portability or
project convention.

For normal script use, prefer making the file executable and running it
directly:

```bash
chmod +x script.swift
./script.swift
```

This keeps the script self-describing: the shebang declares the intended
runner, and callers do not need to know which command launches it.

For command-style repo scripts, an extensionless executable name is acceptable
when the filename is the command surface. Do not rename the command to add
`.swift` only to satisfy formatter or editor file detection. In formatting
workflows, invoke the formatter explicitly against the script path and the
project's reviewed formatter configuration:

```bash
swift-format format --in-place --configuration <repo-format-config> <path-to-script>
swift-format lint --strict --configuration <repo-format-config> <path-to-script>
```

If a formatter integration cannot infer Swift syntax from an extensionless
script, fix the formatter invocation or editor file association for that
workflow. Use the project's own formatter configuration; do not bake a
machine-local absolute path into skill docs or scripts. Keep command naming and
formatting mechanics separate.

If direct execution is not appropriate, run through the `swift-sh` binary:

```bash
swift-sh script.swift
```

`swift sh script.swift` can work when the active `swift` binary supports
external `swift-*` subcommands and can find `swift-sh` in `PATH`. Do not assume
that bare `swift sh` works under every toolchain manager. If a toolchain
manager such as Swiftly places its own `swift` first in `PATH`, that `swift`
may report:

```text
error: unknown or missing subcommand 'swift-sh'
```

In that case, the script can still be valid. Use one of the explicit forms:

```bash
swift-sh script.swift
/usr/bin/swift sh script.swift
```

This intentionally chooses the system Swift launcher for direct script
execution instead of whichever `swift` a toolchain manager has placed first in
`PATH`.

## Current Command Surface

Use the current `swift-sh` command tree:

```bash
swift sh <script> [arguments...]
swift sh - [arguments...]
swift sh -- [arguments...]
swift sh package <script> [--force] [--move]
swift sh open <script> [--xcode]
swift sh cache clean [<script>]
```

`swift sh <script> [arguments...]` is the default run mode. Arguments after the
script path are opaque script arguments; do not parse or reinterpret them as
runner flags. If a script needs a typed command interface, import
Swift Argument Parser inside the script and parse `CommandLine.arguments`
there.

`swift sh - [arguments...]` and `swift sh -- [arguments...]` force stdin mode.
With no arguments, `swift sh` reads the script from stdin when stdin is not a
TTY and reports invalid usage when it is. Any other first argument is a script
path, whether or not stdin is a TTY. A path that cannot be opened exits with
status 2 and names the path; it never falls back to stdin. Shell process
substitution, such as `swift sh <(curl https://example.com/script) arg1`, is
path-like input provided by the shell; treat following values as script
arguments.

`swift sh package <script>` converts a script into a SwiftPM package and keeps
the original script by default. Use `--force` only when the user explicitly
wants to package a script without a supported swift-sh shebang. Use `--move`
only when the user explicitly wants the source script moved into the package.

`swift sh open <script>` writes the cached SwiftPM package and opens the
generated source in `$EDITOR`. `swift sh open --xcode <script>` opens the
generated SwiftPM package in Xcode on macOS; it does not generate an
`.xcodeproj`.

`swift sh cache clean` clears all cached builds, and
`swift sh cache clean <script>` clears one script's cache.

Do not recommend removed legacy names such as `eject`, `editor`, `edit`,
`--clean-cache`, or `-C`.

For package dependencies, declare the dependency on the import line:

```swift
#!/usr/bin/swift sh

import Foundation
import Markdown  // swiftlang/swift-markdown == 0.8.0
```

## Dependency Comments

`swift-sh` dependency comments are a comment DSL on Swift import lines. The
Swift compiler and IDEs do not understand them; `swift-sh` reads them and maps
them to SwiftPM package dependencies.

When adding, reviewing, explaining, or testing dependency comments, use
`references/swift-sh-import-spec.md` for supported forms and mapping rules.

Default recommendation:

- Use local path dependencies for local or auditable package code.
- Use explicit stable `~>` or `==` constraints for remote dependencies that
  will be kept.
- Reserve bare remote dependencies for throwaway scripts where following newer
  versions is acceptable.
- Use neutral or official owners in public examples. Use real third-party
  owners in tests only when the test needs concrete resolution behavior.
- Do not silently introduce a remote dependency when the task expects local,
  auditable tooling.

## Script Shape Rules

- Keep top-level flow readable: parse inputs, perform work, print output, exit.
- Prefer small local functions over broad helper types.
- Print machine-readable output when another tool will consume it.
- Use stderr for diagnostics and stdout for the requested result.
- Exit non-zero for invalid arguments, missing files, parse failures, and
  unmet preconditions.
- Do not hide file writes, network access, process launches, or destructive
  changes behind vague helper names.
- Keep comments for non-obvious constraints, not narration of ordinary Swift.

## Failure Modes

- `swift sh` missing from `PATH`: report the missing runner; do not install it.
- `swift sh` fails with `unknown or missing subcommand 'swift-sh'` while
  `swift-sh` works directly: treat this as active Swift toolchain or toolchain
  manager incompatibility with external subcommand lookup. Use `swift-sh
  <script>`, `/usr/bin/swift sh <script>`, or an explicit shebang.
- Dependency comment accidentally names a remote package when a local package
  was intended: switch to an explicit path dependency or ask for the intended
  source.
- The script grows package-shaped: stop adding layers and route to SwiftPM
  package guidance.
- Output mixes diagnostics with data: move diagnostics to stderr.
- Validation only checks the happy path: add an argument, missing-input, or
  parse-failure check.

## Output

When producing or reviewing a swift-sh script, return:

1. Runner form: shebang, `swift-sh <script>`, or `swift sh <script>`.
2. Dependency comments: none, remote package, explicit local path, version, or
   revision.
3. Script argument boundary and stdout/stderr contract.
4. Failure behavior and exit-code policy.
5. Validation command and result, or why validation was not run.
