---
name: bridge-js-patterns
description: Use this skill for BridgeJS typed Swift-JavaScript interoperability in JavaScriptKit projects, including `@JS`, `@JSFunction`, `@JSClass`, `@JSGetter`, `@JSSetter`, `JSTypedClosure`, `throws(JSException)`, `bridge-js.d.ts`, `bridge-js.config.json`, generated `BridgeJS.swift`, `BridgeJS.Macros.swift`, `JavaScript/BridgeJS.json`, `bridge-js.js`, `.d.ts` output, PackageToJS integration, and `swift package plugin bridge-js`. Do not use for raw JavaScriptKit `JSObject`/`JSValue` calls, generic Swift Wasm porting, or native WebKit/Safari extension JavaScript.
---

# BridgeJS Patterns

## Purpose

Guide implementation, review, and troubleshooting for BridgeJS, the
experimental JavaScriptKit code-generation layer for typed Swift-JavaScript and
Swift-TypeScript boundaries.

## When To Use

- Exporting Swift functions, classes, structs, enums, protocols, or closures to
  JavaScript and TypeScript with `@JS`.
- Importing JavaScript or TypeScript APIs into Swift with `@JSFunction`,
  `@JSClass`, `@JSGetter`, `@JSSetter`, globals, or generated declarations.
- Writing or reviewing `bridge-js.d.ts`, `bridge-js.config.json`,
  `BridgeJS.Macros.swift`, generated `BridgeJS.swift`, `JavaScript/BridgeJS.json`,
  `bridge-js.js`, or generated `.d.ts` files.
- Choosing build-tool plugin generation versus ahead-of-time checked-in
  generated files.
- Debugging BridgeJS type mapping, closure bridging, `throws(JSException)`,
  unsupported declarations, plugin output, or PackageToJS integration.

## When Not To Use

- Direct dynamic JavaScript calls through `JSObject`, `JSValue`, `JSClosure`, or
  `JSObject.global` without BridgeJS code generation.
- Generic Swift SDK for WebAssembly installation, WASI compatibility, or source
  porting.
- Native Apple WebKit, Safari app extensions, WebExtension JavaScript, or
  JavaScriptCore-style bridges.
- General TypeScript API design when no Swift Wasm BridgeJS boundary exists.

## Authority

- Treat the current JavaScriptKit repository, BridgeJS README, Package.swift,
  user DocC, tests, generated artifacts, and local plugin output as primary
  authority.
- BridgeJS is experimental. Do not assume generated ABI, macro behavior,
  supported types, or plugin output paths are stable without current source or
  local generation evidence.
- Treat Swift.org Swift SDKs for WebAssembly documentation and local tool output
  as authority for Swift SDK IDs and Wasm build commands.

## Inputs To Inspect

- `Package.swift`, JavaScriptKit dependency, products, plugins, Swift settings,
  generated-file policy, and PackageToJS integration.
- Swift source annotated with `@JS`, `@JSFunction`, `@JSClass`, `@JSGetter`,
  `@JSSetter`, `JSTypedClosure`, or `throws(JSException)`.
- `bridge-js.d.ts`, `bridge-js.config.json`, generated Swift and JavaScript
  artifacts, TypeScript declaration output, browser/Node host code, and bundler
  config.
- Plugin commands, CI scripts, snapshot tests, and diagnostics from failed
  generation.

## Workflow

1. Identify the boundary direction: export Swift to JavaScript, import
   JavaScript/TypeScript into Swift, or both.
2. Decide whether the project should use BridgeJS at all. Prefer raw
   JavaScriptKit for tiny dynamic calls; use BridgeJS when the boundary benefits
   from typed declarations, generated glue, or TypeScript-facing APIs.
3. Verify the current JavaScriptKit source and BridgeJS docs before relying on
   macro names, plugin commands, output paths, or supported type mappings.
4. Check package wiring. BridgeJS depends on JavaScriptKit's products and
   plugins, and generated code may require current experimental Swift settings
   from the package source.
5. For exported Swift APIs, keep the public JS/TypeScript surface small and
   stable. Annotate only the types and members that the JavaScript host should
   call.
6. For imported JavaScript APIs, prefer `bridge-js.d.ts` when a TypeScript
   declaration is the source of truth; otherwise use Swift macro declarations
   and keep globals explicit.
7. Model errors as `throws(JSException)` at the bridge. Do not assume plain
   Swift `throws` has bridge support.
8. Review generated artifacts as interface contracts. Decide whether they are
   checked in as ahead-of-time outputs or generated during build, then validate
   the same path CI will run.

## Review Rules

- Always call out BridgeJS experimental status when introducing it to a project
  or public API boundary.
- Do not hand-edit generated files unless the project deliberately treats them
  as ahead-of-time checked-in artifacts and records regeneration steps.
- Do not assume dictionaries, sets, generics, Foundation.URL, imported
  null/undefined unions, or TypeScript enums are supported without current
  source/tests proving the specific case.
- Do not bridge long-lived Swift closures to JavaScript without explicit
  lifetime and release handling. Use the closure type required by BridgeJS.
- Do not hide plugin diagnostics. They usually identify the unsupported
  declaration or source path that needs to change.

## Validation

Use the commands that match the project:

```bash
swift package plugin bridge-js --target <target>
swift package --swift-sdk <wasm-sdk-id> js
swift build --swift-sdk <wasm-sdk-id>
```

When working inside the JavaScriptKit repository or validating BridgeJS itself:

```bash
swift test --package-path ./Plugins/BridgeJS
npm -C Sources/TS2Swift/JavaScript test
UPDATE_SNAPSHOTS=1 swift test --package-path ./Plugins/BridgeJS
```

For application work, also run the JavaScript or browser smoke test that imports
the generated package, calls exported Swift APIs, and exercises imported
JavaScript APIs.

## Output

For implementation or review work, return:

1. Bridge direction and chosen generation mode
2. Package/plugin wiring and generated artifact status
3. Type mapping, error, closure, and unsupported-declaration risks
4. Wasm/package/browser validation run or still needed
5. Current-source assumptions for experimental BridgeJS behavior
