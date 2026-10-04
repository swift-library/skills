# SwiftSyntax Plugin Gotchas

## Valid Single-Path Shapes

These shapes are valid and should not be rejected by design:

```text
plugin -> executableTarget tool -> core/tool -> SwiftParser / SwiftSyntax
```

```text
client target -> provider library product -> macro target -> swift-syntax
```

In local validation, both shapes worked with:

- Apple Swift 6.3.1.
- SwiftSyntax 602.0.0.
- SwiftPM source reference revision `e5ac741fed39ebd16df924d3dbfa904a1c332079`.

## Dual SwiftSyntax Graph Risk

The risky shape is when a client package pulls SwiftSyntax through two branches
of the same provider package:

```text
client package
  -> provider library product
       -> provider macro target -> swift-syntax
  -> provider command plugin
       -> executable tool -> core/tool -> SwiftParser / SwiftSyntax
```

Observed failure:

```text
error: no such module 'SwiftParser'
```

The important signal is not only the error text. Inspect `debug.yaml`:

- Link inputs may include `SwiftParser-tool.build/*.o`.
- The importing module compile inputs may omit
  `Modules-tool/SwiftParser.swiftmodule`.
- That means SwiftPM planned some link work for SwiftParser but did not attach
  the SwiftParser module as a compile-time input for the tool/core module that
  imports it.

This is a host-tool build graph issue. It is not proof that the
`plugin -> executableTarget tool -> core` topology is wrong.

## Resolution Status

Do not record this as impossible. The evidence recorded with Swift 6.3.1 and
SwiftSyntax 602.0.0 shows a mixed state:

- The first check is still ordinary SwiftPM correctness: if tool/core source
  directly imports `SwiftParser`, that same target must directly declare the
  `SwiftParser` product dependency, or depend on an internal wrapper target that
  declares it. Link inputs may be recursive, but compile-time module inputs are
  effectively driven by declared dependencies.
- SwiftPM has fixed related macro/plugin dependency traversal bugs in some
  versions.
- `--disable-experimental-prebuilts` can move a dual SwiftSyntax graph past the
  `SwiftParser` import failure in local reproduction.
- A source-built external tool package is not guaranteed to solve the problem
  if the client graph still resolves the same provider macro/library branch and
  a SwiftSyntax-using plugin tool branch together.
- A binary/prebuilt plugin tool or a separately distributed toolchain artifact
  can avoid compiling SwiftSyntax in the client plugin host graph, but that is
  a packaging decision with release and platform costs.

Production guidance: keep a working scanner/generator fallback unless the
default `swift package <verb>` path passes without requiring special flags.

## Mitigations

- Keep SwiftSyntax out of the plugin target.
- First try the standard tool/core topology; do not flatten implementation into
  the plugin.
- Make direct imports explicit in `Package.swift`. If `_ToolCore` imports
  `SwiftParser`, `_ToolCore` must directly depend on
  `.product(name: "SwiftParser", package: "swift-syntax")`.
- If the failure involves SwiftSyntax prebuilts, test
  `--disable-experimental-prebuilts` to confirm the class of issue. Do not make
  it the default user requirement without an explicit product decision.
- If the dual SwiftSyntax graph fails, keep a self-contained scanner or another
  production fallback behind the same tool/core interface.
- Splitting the tool into another source package may help only if it also
  avoids the mixed SwiftSyntax host graph. Validate it; do not assume the split
  fixes the issue.
- Record the failure in an ADR with the exact SwiftPM revision, Swift toolchain,
  SwiftSyntax version, command, and `debug.yaml` evidence.
- Revisit when SwiftPM or SwiftSyntax changes; do not require users to change
  package topology or pass special build flags as the normal workflow.

## Minimal Repro Matrix

Use temporary packages outside the repo when isolating the failure:

1. `plugin -> tool -> local core`, no external dependency.
2. `plugin -> tool/core -> normal external library`, such as
   Swift Argument Parser.
3. `plugin -> tool/core -> SwiftParser / SwiftSyntax`.
4. Client package depends on provider plugin only.
5. Client package depends on provider macro-driven library product and invokes
   provider plugin.

Compare:

```bash
swift build --product Tool
swift package <plugin-verb>
swift package --disable-experimental-prebuilts <plugin-verb>
swift package -v <plugin-verb> 2>&1 | tee /tmp/plugin.log
```
