---
name: browserenginekit-patterns
description: Use this skill for BrowserEngineKit implementation and review across alternative browser engine eligibility, host apps, web content extensions, networking extensions, rendering extensions, XPC, sandboxing, JIT, rendering layer hosting, text input, downloads, process lifecycle, and non-WebKit browser-engine boundaries. Do not use for WKWebView/WebKit embedding, ordinary web content, or generic XPC work without BrowserEngineKit extensions.
---

# BrowserEngineKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for BrowserEngineKit
alternative browser engine apps, including host/extension architecture, XPC,
sandboxing, rendering, text input, networking, and process lifecycle.

## When To Use

- Designing or reviewing an alternative browser engine app using
  BrowserEngineKit.
- Wiring the host app with web content, networking, and rendering extensions.
- Implementing `WebContentExtension`, `NetworkingExtension`, or
  `RenderingExtension`.
- Building XPC communication between the host app and browser extensions.
- Handling JIT, sandboxing, rendering layer hosting, text input, downloads,
  media, process invalidation, or extension lifecycle.
- Checking eligibility, entitlements, device capabilities, and distribution
  constraints for non-WebKit browser engines.

## When Not To Use

- Do not use for `WKWebView`, SwiftUI `WebView`, `WebPage`, or ordinary WebKit
  embedding.
- Do not use for generic XPC services without BrowserEngineKit.
- Do not use for generic HTTP clients built on URLSession or the Network
  framework.
- Do not use for web app content design or JavaScript debugging unless
  BrowserEngineKit architecture is the task.

## Inputs To Inspect

- Entitlements, eligibility assumptions, device capabilities, host app target,
  and extension targets.
- Extension entry points, `@main` conformances, XPC connection setup, and
  anonymous endpoint passing.
- Web content parsing, networking, rendering, media, download, text input, and
  layer hosting paths.
- Sandbox, JIT, arm64e, process invalidation, memory attribution, and error
  handling.
- Boundary between non-WebKit engine code and WebKit fallback surfaces.

## Workflow

1. Confirm the task is BrowserEngineKit, not WebKit embedding.
2. Verify current eligibility, entitlements, region/platform requirements, and
   device capabilities before making implementation claims.
3. Check target split first: host app, web content extension, networking
   extension, and rendering extension.
4. Keep XPC message schemas explicit and avoid calling XPC entry points that do
   not match BrowserEngineKit extension processes.
5. Propagate visibility, lifecycle, invalidation, download, and process-failure
   state back to the host app.
6. Review sandbox, JIT, file access, text input, accessibility, and rendering
   boundaries as first-class security and UX concerns.
7. Validate with the current SDK and device conditions required by the feature.

## Review Rules

- Do not treat non-WebKit browser engine work as WebKit embedding.
- Do not treat BrowserEngineKit entitlements or eligibility as generally
  available without current verification.
- Do not let extension processes access more file, network, or rendering
  capability than the architecture needs.
- Do not hide XPC schema and process invalidation behind vague helper layers.
- Treat entitlement programs, regional requirements, JIT restrictions, process
  extension behavior, and API changes as current Apple documentation and SDK
  gated.

## Validation

- Build the host app and all extension targets.
- Test extension launch, XPC connection, anonymous endpoint passing, page load,
  rendering, media, text input, download, process invalidation, and failure
  recovery paths.
- Validate on a device and OS combination that can actually run the requested
  BrowserEngineKit capability.

## Output

For implementation or review work, return:

1. BrowserEngineKit versus WebKit/XPC boundary decision
2. Eligibility, entitlement, and target-split assumptions
3. Extension, XPC, rendering, networking, and text-input findings
4. Sandbox, JIT, download, and lifecycle findings
5. Validation run or still needed
