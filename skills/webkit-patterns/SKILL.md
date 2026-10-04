---
name: webkit-patterns
description: Use this skill for WebKit implementation and review across SwiftUI WebView/WebPage, WKWebView fallback, page state, navigation policy, external links, JavaScript evaluation, local HTML/data loading, custom URL schemes, ephemeral pages, custom user agents, web export, and embedded-web security boundaries. Do not use for OAuth/browser authentication flows, ordinary networking/cache work, broad SwiftUI layout, or web app frontend implementation.
---

# WebKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for embedded web content in
Apple-platform apps, including SwiftUI `WebView`/`WebPage` workflows and
`WKWebView` compatibility paths.

## When To Use

- Embedding web content in SwiftUI, UIKit, or AppKit app surfaces.
- Choosing among `WebView`, `WebPage`, `WKWebView`, `SFSafariViewController`,
  and `ASWebAuthenticationSession`.
- Controlling navigation, external links, back/forward state, custom URL
  schemes, user agents, or ephemeral pages.
- Evaluating JavaScript, loading local HTML/data, exporting web content, or
  debugging page load state.
- Reviewing embedded-web security, privacy, origin, and cookie/session
  boundaries.

## When Not To Use

- Do not use for OAuth, SSO, or login browser sessions; prefer
  `ASWebAuthenticationSession`. Authentication flow design is out of scope.
- Do not use for general SwiftUI layout or architecture without an embedded web
  surface.
- Do not use for generic HTTP client work.
- Do not use for web frontend implementation outside an Apple app.
- Do not invent behavior for the SwiftUI WebKit APIs (`WebView`/`WebPage`, iOS,
  macOS, and visionOS 26+). Verify current Apple documentation and local SDK
  symbols before relying on version-specific APIs.

## Inputs To Inspect

- SwiftUI `WebView`/`WebPage` code, `WKWebView` wrappers, delegates, and
  configuration.
- URL loading, navigation policy, external-link routing, JavaScript calls, and
  custom scheme handlers.
- Local HTML/data resources, cookie/session configuration, user scripts, and
  content blocking or media settings.
- Authentication, payment, or OAuth flows that may need to leave embedded
  WebKit.
- Tests, manual repro steps, simulator/device behavior, and web console or load
  errors.

## Workflow

1. Identify whether the app needs simple display, controlled browsing, native
   web interop, authentication, or full web-app embedding.
2. Prefer SwiftUI `WebView`/`WebPage` when the target SDK supports the needed
   page control. Use `WKWebView` wrappers only for unsupported customization or
   compatibility.
3. Decide external navigation and authentication boundaries before writing
   delegate logic.
4. Keep page state observable: loading, title, URL, back/forward availability,
   errors, and navigation decisions.
5. Isolate JavaScript evaluation and message handling behind typed native
   boundaries. Validate input and output.
6. Review local content, custom schemes, cookies, ephemeral sessions, and user
   agents for privacy and origin correctness.
7. Validate on the smallest real surface: load, navigate, cancel, back/forward,
   external link, JavaScript path, and error state.

## Review Rules

- Do not use embedded WebKit for sign-in when system authentication is required.
- Do not blindly allow all navigation inside the app.
- Do not expose native APIs to arbitrary web origins.
- Do not load local files or custom schemes without explicit origin and
  resource-access reasoning.
- Do not assume SwiftUI WebKit APIs are available on all deployed platforms.
- Keep web content failures user-visible and recoverable.

## Validation

- Build the affected app target.
- Test initial load, reload, failure, redirect, and navigation-cancel paths.
- Test external links and authentication links leave the embedded surface when
  required.
- Test JavaScript/native messages and local content on device or simulator.
- Check SDK availability for `WebView`/`WebPage` APIs before adopting them.

## Output

For implementation or review work, return:

1. Container choice and platform availability
2. Navigation and external-link policy
3. JavaScript, local content, and session findings
4. Security/privacy boundaries
5. Validation run or still needed
