# DocC Placement

Use this rule when a Swift package needs API documentation, documentation
coverage, symbol graph validation, or generated documentation archives.

## Principle

DocC catalogs document Swift modules and should normally live with the SwiftPM
target they document:

```text
Sources/<Target>/<Target>.docc/
```

Repository-level `Documentation/` is for architecture, proposals, decisions, migrations,
archives, and reference material. It is not the default home for module API
DocC catalogs.

## Source Versus Output

DocC source inputs are:

- Swift source doc comments
- symbol graphs generated from Swift targets
- `.docc` catalogs such as `Sources/<Target>/<Target>.docc/`

DocC generated output is a `.doccarchive`. Treat `.doccarchive` directories as
build artifacts unless the repository explicitly documents a publishing policy
for checked-in generated documentation.

`swift build` and `swift test` compile and test code; they do not, by
themselves, prove that final DocC documentation archives build. Validate DocC
with `xcrun docc convert`, Xcode documentation build support, or an equivalent
repository-local documentation command.

## Target Ownership

- Public runtime/library targets with user-facing API should have a target-level
  DocC catalog when package documentation is being built.
- Macro implementation targets are implementation detail targets. They usually
  do not need user-facing DocC unless their public API is intentionally exposed
  to package consumers.
- Root README and `Documentation/README.md` may link to DocC catalogs, but should not
  absorb symbol-level API documentation.

## Placement Examples

Good target-level placement:

```text
Sources/SwiftDataWritable/SwiftDataWritable.docc/SwiftDataWritable.md
```

Good repository-level placement:

```text
Documentation/Architecture/SwiftDataWritable.md
Documentation/Decisions/SaveSemantics.md
Documentation/Reference/MigrationNotes.md
```

Avoid by default:

```text
Documentation/SwiftDataWritable.docc/
SwiftDataWritable.doccarchive/
```

## Audit Checks

- Every user-facing target that claims API documentation has a `.docc` catalog
  colocated with that target or an explicit documented exception.
- Root `Documentation/` does not contain target API DocC catalogs by accident.
- `.doccarchive` output is ignored, generated outside the source tree, or
  explicitly governed as a published artifact.
- README-class files link to DocC entry points without duplicating symbol-level
  API details.
