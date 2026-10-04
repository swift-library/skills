# Official SwiftPM Patterns

Use these references when justifying plugin architecture or debugging host-tool
build behavior.

## Versioned Evidence

- SwiftPM source inspected: `swiftlang/swift-package-manager`
  revision `e5ac741fed39ebd16df924d3dbfa904a1c332079`.
- Local validation toolchain: `Apple Swift version 6.3.1
  (swift-6.3.1-RELEASE)`, target `arm64-apple-macosx26.0`.
- SwiftSyntax version used in plugin-tool repros: `swift-syntax 602.0.0`.

Prefer commit-pinned Markdown links when citing source behavior:

- `PluginContext.tool(named:)` requires a named executable or binary tool on
  which the plugin target depends:
  [Context.swift#L55-L59](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Runtimes/PackagePlugin/Context.swift#L55-L59).
- Plugin modules cannot depend on library modules or library products:
  [ModulesGraph+Loading.swift#L1584-L1604](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/PackageGraph/ModulesGraph%2BLoading.swift#L1584-L1604).
- Command plugins build executable host-side tools before invocation:
  [PluginCommand.swift#L333-L352](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Commands/PackageCommands/PluginCommand.swift#L333-L352).
- Host artifacts use a `-tool` suffix:
  [BuildParameters.swift#L450-L455](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/SPMBuildCore/BuildParameters/BuildParameters.swift#L450-L455).
- Host module output path is `Modules-tool`, and Swift compiles receive it via
  `-I`:
  [SwiftModuleBuildDescription.swift#L139-L142](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildDescription/SwiftModuleBuildDescription.swift#L139-L142)
  and
  [SwiftModuleBuildDescription.swift#L800-L802](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildDescription/SwiftModuleBuildDescription.swift#L800-L802).
- Swift compile inputs are derived from the target's declared dependency list:
  [ModuleBuildDescription.swift#L188-L196](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildDescription/ModuleBuildDescription.swift#L188-L196)
  and
  [LLBuildManifestBuilder+Swift.swift#L273-L292](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildManifest/LLBuildManifestBuilder%2BSwift.swift#L273-L292).
- Product link/static target collection walks dependencies recursively, so link
  inputs can contain dependency objects even when a compile-time swiftmodule edge
  is missing:
  [BuildPlan+Product.swift#L113-L126](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildPlan/BuildPlan%2BProduct.swift#L113-L126)
  and
  [BuildPlan+Product.swift#L196-L203](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildPlan/BuildPlan%2BProduct.swift#L196-L203).
- SwiftPM has a dependency import check for targets that import modules without
  explicitly declared dependencies:
  [Options.swift#L547-L550](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/CoreCommands/Options.swift#L547-L550)
  and
  [BuildOperation.swift#L332-L336](https://github.com/swiftlang/swift-package-manager/blob/e5ac741fed39ebd16df924d3dbfa904a1c332079/Sources/Build/BuildOperation.swift#L332-L336).

Swift Evolution references:

- SE-0303, Package Manager extensible build tools:
  [proposal 0303](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0303-swiftpm-extensible-build-tools.md).
- SE-0332, Package Manager command plugins:
  [proposal 0332](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0332-swiftpm-command-plugins.md).

## Known SwiftSyntax / Macro / Plugin Findings

Use these as evidence for problem-class diagnosis, not as proof that every
package has the same root cause:

- SwiftPM has had macro/plugin boundary dependency bugs where dependency
  traversal needed to be pruned when crossing macro and plugin boundaries:
  [swift-package-manager#8436](https://github.com/swiftlang/swift-package-manager/issues/8436),
  fixed by
  [swift-package-manager#8472](https://github.com/swiftlang/swift-package-manager/pull/8472)
  and listed in
  [SwiftPM release notes](https://github.com/swiftlang/swift-package-manager/releases).
- Swift Forums reports failures when macros and plugin tools both touch
  SwiftSyntax prebuilts; maintainers describe it as two build environments
  being mixed:
  [Swift-Syntax Prebuilts for Macros](https://forums.swift.org/t/preview-swift-syntax-prebuilts-for-macros/80202).
- SwiftSyntax prebuilt failures have documented workarounds such as
  `--disable-experimental-prebuilts`:
  [swift-package-manager#9193](https://github.com/swiftlang/swift-package-manager/issues/9193).
- Real-world package workaround example: avoid vending a plugin that depends on
  SwiftSyntax in the same graph:
  [SafeDI PR #161](https://github.com/dfed/SafeDI/pull/161).

## Architecture Rules From The Sources

- A plugin target declares commands or build commands; it should not contain the
  tool implementation.
- A command plugin can locate only tools declared as executable or binary
  dependencies of the plugin target.
- SwiftPM builds plugin tools for the host destination, not the client package
  target destination.
- Module search for host tools should resolve through `Modules-tool`; failures
  here are host-tool build graph failures, not runtime lookup failures.
- Product and target dependencies are scoped. A package-level dependency does
  not make a product importable from every target.
- A tool/core target must directly declare every module it directly imports.
  Do not rely on a dependency being reachable through a product's recursive link
  closure.

## Practical Reading Order

1. Check the plugin target dependencies in `Package.swift`.
2. Check whether the dependency is an executable target, executable product, or
   binary target.
3. Inspect the host build graph if `context.tool(named:)` finds the tool but
   compiling the tool fails.
4. Use `debug.yaml` to distinguish compile-module inputs from link inputs.
