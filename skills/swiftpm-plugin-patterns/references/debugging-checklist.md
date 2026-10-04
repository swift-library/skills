# Debugging Checklist

Use this checklist when a plugin tool works under `swift build --product Tool`
but fails through `swift package <plugin-verb>`.

## Commands

```bash
swift build --product Tool
swift build --explicit-target-dependency-import-check warn --product Tool
swift package <plugin-verb>
swift package --disable-experimental-prebuilts <plugin-verb>
swift package -v <plugin-verb> 2>&1 | tee /tmp/plugin.log
```

When debugging another package:

```bash
swift package \
  --package-path /path/to/client-package \
  --scratch-path /tmp/plugin-scratch \
  --allow-writing-to-directory /tmp/plugin-scratch \
  <plugin-verb>
```

## Search The Verbose Log

```bash
rg -n "Tool-tool\\.build|Modules-tool|SwiftParser\\.swiftmodule|no such module" /tmp/plugin.log
```

Useful build artifacts:

```bash
find .build -name debug.yaml -print
find .build -path "*/Modules-tool/*.swiftmodule" -print
find .build -path "*-tool.build" -type d -print
```

## Classify The Failure

- `context.tool(named:)` cannot find the tool: plugin dependency or tool name is
  wrong.
- Plugin target cannot depend on a library: move implementation to executable
  tool/core.
- `swift build --product Tool` fails: fix normal target dependencies first.
- Explicit import check reports a missing dependency: add a direct target or
  product dependency for the module being imported before debugging plugin
  host-tool behavior.
- Product build passes but plugin path fails: inspect host-tool build graph.
- `Modules-tool/<Dependency>.swiftmodule` exists but import still fails:
  inspect `-I` paths and stale build caches.
- Link inputs contain dependency objects, but module compile inputs omit the
  dependency `.swiftmodule`: host-tool dependency edge issue.
- A SwiftSyntax failure disappears with `--disable-experimental-prebuilts`:
  classify it as a SwiftSyntax prebuilt / macro-plugin mixed-environment issue,
  then decide whether a fallback, binary tool, or toolchain bump is acceptable.
- SwiftSyntax reports platform floor errors: raise the package platform to the
  dependency floor, such as macOS 10.15+ for SwiftSyntax 602.0.0.

## Evidence To Keep

- Swift version: `swift --version`.
- SwiftPM source revision or Xcode version.
- SwiftSyntax version from `Package.resolved`.
- The exact failing command.
- Whether `--disable-experimental-prebuilts` changes the failure.
- Whether `--explicit-target-dependency-import-check warn|error` reports an
  undeclared direct import.
- `swift build --product Tool` result.
- `swift package -v <verb>` excerpt showing the importing module compile
  command.
- `debug.yaml` excerpt showing module inputs and link inputs.
