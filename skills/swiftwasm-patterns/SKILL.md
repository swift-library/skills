---
name: swiftwasm-patterns
description: Use this skill for Swift SDKs for WebAssembly, Swift-on-Wasm, WASI build and porting work, `swift sdk install/list`, `swift build --swift-sdk ..._wasm`, `#if os(WASI)`, Wasm compatibility audits, Embedded Swift Wasm builds, WasmKit or other Wasm runtime validation, and SourceKit-LSP Swift SDK configuration. Do not use for ordinary Apple-platform Swift, raw JavaScriptKit `JSObject`/`JSValue` interop, BridgeJS typed Swift-JavaScript code generation, WebKit/Safari extension JavaScript, or community SwiftUI-on-web renderers unless the task is explicitly about their Wasm build boundary.
---

# SwiftWasm Patterns

## Purpose

Guide implementation, review, and troubleshooting for Swift code targeting
WebAssembly through Swift SDKs for WebAssembly and WASI. This is a platform and
toolchain compatibility skill, not an Apple framework skill and not an
`import SwiftWasm` package skill.

## When To Use

- Building or reviewing Swift packages with `swift build --swift-sdk <wasm-sdk-id>`
  or `swift run --swift-sdk <wasm-sdk-id>`.
- Installing, listing, or matching Swift SDKs for WebAssembly to the active
  Swift.org toolchain.
- Auditing source for WASI compatibility, unavailable Apple frameworks, POSIX
  assumptions, Foundation gaps, process/file/network behavior, or C dependency
  portability.
- Refactoring platform-specific code behind `#if os(WASI)`, `#if canImport(...)`,
  protocols, dependency injection, or package target splits.
- Configuring SourceKit-LSP or editor settings for a Wasm Swift SDK.
- Evaluating Embedded Swift Wasm as an experimental build-size or runtime path.
- Validating Wasm artifacts with WasmKit, wasmtime, Node, a browser harness, or
  another project-owned runtime.

## When Not To Use

- Ordinary Swift language, API, or style review.
- Swift package target graph decisions that are not Wasm-specific.
- JavaScriptKit raw JavaScript interop through `JSObject`, `JSValue`,
  `JSClosure`, promises, or DOM calls.
- BridgeJS `@JS`, `@JSFunction`, `bridge-js.d.ts`, TypeScript definition
  import/export, or generated glue.
- Embedded WebKit, `WKWebView`, Safari app extensions, or WebExtension JavaScript
  unless the only question is whether a Swift Wasm artifact can run there; the
  app-extension and WebKit surface is out of scope.
- SwiftUI-on-web renderer questions unless the task is explicitly about Wasm
  build compatibility. Do not present SwiftUI Web as an official Swift SDK
  feature.

## Authority

- Treat Swift.org Swift SDKs for WebAssembly documentation, current `swift`
  output, `swift sdk list`, and local compiler behavior as primary authority for
  installation, SDK IDs, build commands, Embedded Swift, and editor setup.
- Treat `swiftwasm/*` repositories as high-trust ecosystem sources for
  JavaScriptKit, BridgeJS, and community tooling, but verify mutable package
  behavior against current source, Package.swift, DocC, examples, or tests.
- Do not hardcode old SDK IDs, checksums, package versions, or install URLs.
  Read the current Swift.org page or local tool output first.

## Inputs To Inspect

- `Package.swift`, package resolution, products, targets, platform
  declarations, plugin use, conditional dependencies, and C/C++ dependencies.
- Imports and API usage for UIKit, SwiftUI, AppKit, CoreGraphics, CoreML,
  Accelerate, URLSession, Dispatch, file system, process, sockets, dynamic
  loading, Foundation, or POSIX calls.
- Existing `#if os(WASI)`, `canImport`, target-condition logic, protocol
  abstractions, and fallback implementations.
- Build scripts, CI workflows, `.sourcekit-lsp/config.json`, `swift sdk list`,
  toolchain selection, Wasm runtime commands, and browser or Node harnesses.

## Workflow

1. Identify the target runtime: WASI CLI/module, browser, Node, WasmKit,
   wasmtime, serverless Wasm, or a custom host. Runtime decides what host APIs
   exist.
2. Verify the active toolchain and SDK state before making mutable claims:
   `swift --version`, `swiftc -print-target-info`, and `swift sdk list`.
3. Inspect package and source boundaries. Separate portable core logic from
   host integrations, UI frameworks, networking, storage, and native platform
   services.
4. Keep native Apple implementations intact. Add narrow `#if os(WASI)` or
   `canImport` branches, package target splits, or protocol-backed adapters only
   where the Wasm runtime truly needs a different implementation.
5. For APIs that cannot work under WASI, define the smallest project-owned
   abstraction that preserves the public behavior, then inject a Wasm-safe
   implementation or mark the feature unavailable with a clear diagnostic.
6. Build with the exact SDK ID from `swift sdk list`; do not infer the ID from
   memory or upstream examples.
7. Run the artifact in the intended Wasm runtime. A native `swift test` is not
   enough when the risk is runtime imports, host calls, or browser packaging.

## Review Rules

- Do not call SwiftWasm an Apple framework or assume an `import SwiftWasm`
  module exists.
- Do not assume Xcode's bundled toolchain is enough for WebAssembly. Verify the
  Swift.org toolchain and matching Wasm SDK.
- Do not replace native code with Wasm-only fallback code. Preserve native paths
  behind explicit conditions.
- Do not promote JavaScriptKit or BridgeJS rules into this skill. Detailed
  JavaScript interop is out of scope.
- Do not claim browser, Safari extension, or SwiftUI-web support without a
  project-specific runtime proof.

## Validation

Use the narrowest commands that match the repository and runtime:

```bash
swift --version
swiftc -print-target-info
swift sdk list
swift build --swift-sdk <wasm-sdk-id>
swift run --swift-sdk <wasm-sdk-id>
```

For editor setup, inspect `.sourcekit-lsp/config.json` for the selected
`swiftPM.swiftSDK`. JavaScript/browser packaging validation belongs to the
JavaScriptKit or BridgeJS workflow the project uses.

This skill includes `scripts/wasm-doctor.py` for a read-only local environment
check. Use `--strict` only when the workflow should fail on missing toolchain,
SDK, Node, or npm prerequisites.

## Output

For implementation or review work, return:

1. Target runtime and active Swift SDK status
2. Source compatibility findings and native/WASI boundary changes
3. Unsupported API replacements or intentionally unavailable features
4. Wasm build and runtime validation run or still needed
5. Primary-source assumptions and any SDK/toolchain facts that must be refreshed
