---
name: javascriptkit-patterns
description: Use this skill for JavaScriptKit Swift package implementation and review in Swift-on-Wasm projects, including `import JavaScriptKit`, `JSObject`, `JSValue`, `JSClosure`, `JSOneshotClosure`, `JSException`, `JSObject.global`, DOM and browser API calls, Swift-JavaScript value conversion, JavaScript promises with Swift async/await, `JavaScriptEventLoop`, `JavaScriptBigIntSupport`, `JavaScriptFoundationCompat`, and PackageToJS packaging. Do not use for BridgeJS typed code generation/macros, generic Swift Wasm porting, WebKit/Safari extension JavaScript, or native Apple JavaScript bridges.
---

# JavaScriptKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for the `swiftwasm/JavaScriptKit`
package when Swift code compiled to WebAssembly needs to call JavaScript or be
called from JavaScript.

## When To Use

- Adding or reviewing the JavaScriptKit SwiftPM dependency and products such as
  `JavaScriptKit`, `JavaScriptEventLoop`, `JavaScriptBigIntSupport`,
  `JavaScriptFoundationCompat`, or `JavaScriptEventLoopTestSupport`.
- Accessing JavaScript globals through `JSObject.global`, dynamic members,
  subscripts, callable `JSObject` values, constructors, DOM APIs, or browser
  APIs.
- Converting between Swift values and `JSValue`, `JSObject`, `JSString`,
  `JSBigInt`, arrays, dictionaries, `Data`, and optional/null/undefined values.
- Managing `JSClosure` or `JSOneshotClosure` lifetimes for event listeners and
  callbacks.
- Handling `JSException`, throwing JavaScript calls, JavaScript promises, or
  event-loop integration.
- Packaging a Swift Wasm target for JavaScript with JavaScriptKit's package
  plugin when the workflow is raw JavaScriptKit interop rather than BridgeJS
  typed bindings.

## When Not To Use

- BridgeJS `@JS`, `@JSFunction`, `@JSClass`, `@JSGetter`, `@JSSetter`,
  `bridge-js.d.ts`, generated `BridgeJS.swift`, or TypeScript declaration
  import/export.
- Generic Swift SDK for WebAssembly install, WASI compatibility, or
  non-JavaScript Wasm porting.
- Embedded WebKit, `WKWebView`, Safari app extensions, WebExtension APIs, or
  native Apple JavaScript bridges.
- SwiftUI-on-web renderer selection unless JavaScriptKit interop is the actual
  implementation surface.

## Authority

- Treat the current JavaScriptKit repository, Package.swift, DocC, examples, and
  tests as primary authority for product names, APIs, plugin behavior, and
  validation commands.
- Treat Swift.org Swift SDKs for WebAssembly documentation and local tool output
  as primary authority for Swift SDK installation, SDK IDs, and build commands.
- Do not hardcode package versions, SDK IDs, checksums, or release-specific
  examples without current source or tool verification.

## Inputs To Inspect

- `Package.swift`, package resolution, JavaScriptKit product dependencies,
  package plugins, and Wasm SDK build settings.
- Swift imports and API usage for `JSObject`, `JSValue`, `JSClosure`,
  `JSOneshotClosure`, `JSString`, `JSException`, `JSPromise`, event loop, BigInt,
  Foundation compatibility, and PackageToJS.
- JavaScript, TypeScript, HTML, Node, browser, or bundler files that host or
  call the generated Wasm module.
- Event listener ownership, closure storage, cleanup paths, async/promise
  boundaries, and root lifetime objects.

## Workflow

1. Confirm that the project is a Swift-on-Wasm JavaScript interop workflow.
   If the task is only Wasm compatibility, it is out of scope.
2. Verify current package behavior from source or docs before changing package
   products, plugin names, or API usage.
3. Choose the interop layer:
   - Use raw JavaScriptKit for direct `JSObject`/`JSValue` access, small DOM
     calls, dynamic APIs, or simple host integration.
   - Use BridgeJS typed bindings, which are out of scope here, when the
     boundary should be typed, generated, or shared with TypeScript
     declaration files.
4. Keep UI and host integration explicit. For complex web UI, prefer a clear
   split where JavaScript owns UI state and Swift owns portable core logic, or
   document why Swift DOM manipulation is the chosen path.
5. Unwrap `JSValue` deliberately. Dynamic member lookup returns values that may
   be missing or wrong-shaped; avoid force unwraps unless the host API contract
   is validated.
6. Retain every `JSClosure` for as long as JavaScript can call it. Remove event
   listeners and release one-shot or typed closure resources when the owner
   deinitializes or the callback is no longer needed.
7. Handle JavaScript failures as `JSException` and promise rejection paths. Do
   not hide thrown JavaScript errors behind generic Swift errors without
   preserving the JS failure detail.
8. Validate both the Swift build and the JavaScript host path that loads or
   calls the Wasm artifact.

## Review Rules

- Do not use JavaScriptKit as a native Apple WebKit bridge. Its purpose is
  Swift code compiled to WebAssembly interacting with JavaScript.
- Do not leave `JSClosure` lifetimes implicit. Stored closures and cleanup are
  part of correctness.
- Do not overuse dynamic member `!` calls without checking whether the JavaScript
  property is a callable object in the target runtime.
- Do not promise SwiftUI Web support from JavaScriptKit alone.
- Do not copy stale install snippets. Refresh Swift SDK and package facts first.

## Validation

Use the commands that match the project:

```bash
swift sdk list
swift build --swift-sdk <wasm-sdk-id>
swift package --swift-sdk <wasm-sdk-id> js
npm test
```

For browser work, run the local host page or bundler smoke test that loads the
generated Wasm and exercises the JavaScript boundary. BridgeJS-generated
bindings need their own BridgeJS validation.

## Output

For implementation or review work, return:

1. JavaScriptKit product and build integration status
2. Raw interop boundary shape and key APIs used
3. Closure, async, exception, and value-conversion risks
4. JavaScript host or browser validation run or still needed
5. Current-source assumptions for package and Swift SDK behavior
