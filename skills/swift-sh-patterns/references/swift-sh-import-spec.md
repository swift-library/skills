# swift-sh Import Spec Reference

Use this reference only when a task adds, reviews, explains, or tests
`swift-sh` dependency comments.

`swift-sh` dependency comments live on Swift import lines. They are consumed by
`swift-sh` and mapped to SwiftPM dependencies; the Swift compiler and IDEs
ignore them as comments.

Only direct dependencies need comments. Transitive dependencies are resolved by
SwiftPM through the direct packages.

## Remote Packages

Supported owner shorthand:

```swift
import Foo  // @owner
import Foo  // @owner ~> 1.2
import Foo  // @owner == 1.2.3
import Foo  // @owner == revision
```

Use `@owner` when the imported module name and repository name match. GitHub
user or organization names with dots are normalized to hyphens to match GitHub
behavior.

Supported owner/repository shorthand:

```swift
import Foo  // owner/repo
import Foo  // owner/repo ~> 1.2
import Foo  // owner/repo == 1.2.3
import Foo  // owner/repo == revision
```

Supported URL forms:

```swift
import Foo  // https://github.com/owner/repo.git ~> 1.2
import Foo  // git@github.com:owner/repo.git ~> 1.2
import Foo  // ssh://git@github.com/owner/repo.git ~> 1.2
```

## Local Packages

Path dependencies must be explicit paths:

```swift
import Foo  // ./local-package
import Foo  // ../local-package
import Foo  // ~/local-package
import Foo  // /absolute/local-package
```

Bare owner/repository dependency comments are remote source-control
dependencies, not local paths.

Local packages must expose library products in their `Package.swift`. Relative
paths are resolved relative to the script path for file-backed scripts. Prefix
local relative paths with `./` or `../`; a value like `foo/bar` is a remote
GitHub dependency form.

## Import Variants

Dependency comments can be attached to normal imports and import variants:

```swift
@testable import Foo  // owner/repo ~> 1.2
import struct Foo.Bar  // owner/repo ~> 1.2
```

## Constraint Mapping

- `~>` maps to SwiftPM's up-to-next-major requirement.
- `==` with a semantic version maps to an exact version.
- `==` with a non-version value maps to a revision.
- No version maps to a broad range and is convenience behavior, not
  reproducible dependency locking.
- Local path dependencies do not need version constraints.
- Pre-release versions are fetched only when specified explicitly, such as
  `~> 1.0.0-alpha.1` or `== 1.0.0-alpha.1`.

## Example Policy

For user-facing examples, prefer placeholders or neutral/official owners, such
as `@example`, `apple/swift-argument-parser`, or
`swiftlang/swift-markdown`. Avoid using an unrelated owner namespace unless the
example intentionally demonstrates that third-party dependency.

Test fixtures may use real third-party owners when they need to validate
concrete dependency resolution.
