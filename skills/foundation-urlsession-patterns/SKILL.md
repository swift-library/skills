---
name: foundation-urlsession-patterns
description: Use this skill for Foundation URL Loading System and URLSession implementation and review across URLSessionConfiguration, URLRequest, HTTPURLResponse validation, async data/download/upload tasks, byte streams, background URLSession transfers, delegates, authentication challenges, cookies, caches, redirects, retries, pagination, SSE, WebSocket tasks, URLProtocol mocks, ATS, and API client shape. Do not use for Network.framework sockets/listeners/path monitoring, BackgroundTasks scheduling except background transfer handoff, certificate trust internals, or generic package architecture.
---

# Foundation URLSession Patterns

## Purpose

Guide implementation, review, and troubleshooting for Foundation URL loading,
`URLSession`, HTTP API clients, transfers, request/response validation, and
background transfer handoff.

## When To Use

- Implementing or reviewing HTTP API clients with `URLSession`,
  `URLRequest`, `HTTPURLResponse`, decoding, pagination, retries, and auth
  refresh.
- Using async `data`, `download`, `upload`, bytes, streaming, SSE, WebSocket
  tasks, or delegate-driven transfer flows.
- Configuring sessions, caches, cookies, connectivity waits, cellular policy,
  timeouts, redirects, background transfers, or App Transport Security.
- Testing with `URLProtocol`, local servers, fixtures, network errors, and
  response validation.
- Reviewing trust challenge handoff where `URLSession` integration is the
  issue.

## When Not To Use

- Do not use for `NWConnection`, `NWListener`, `NWBrowser`, local network
  discovery, or path monitoring; use `network-framework-patterns`.
- Do not use for OS task scheduling; use `background-tasks-patterns` unless
  the task is only a background `URLSession` transfer.
- Do not use for certificate pinning or trust-chain rules without URLSession
  integration; use `certificate-trust-patterns`.
- Do not use for generic package architecture or API-surface review.
- Do not invent protocol, ATS, background transfer, or WebSocket behavior.
  Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- API client, request builder, middleware/interceptor, authentication, retry,
  pagination, cache, and logging code.
- `URLSessionConfiguration`, delegates, delegate queues, background identifiers,
  cookies, cache policy, timeout, connectivity, and cellular settings.
- Request/response validation, decoding, error taxonomy, cancellation,
  progress, and upload/download file handling.
- `URLProtocol` mocks, fixtures, integration tests, local servers, Instruments
  traces, and privacy/logging redaction.

## Workflow

1. Classify the operation: data request, download, upload, byte stream, SSE,
   WebSocket, background transfer, or API client architecture.
2. Check session configuration before debugging task behavior.
3. Validate request construction and response handling explicitly: method,
   headers, body, status code, content type, cache policy, redirects, and
   decoding.
4. Keep retries bounded, idempotency-aware, cancellable, and observable.
5. Keep authentication refresh serialized enough to avoid token storms.
6. For background transfers, confirm identifiers, delegate delivery, app
   relaunch handling, file moves, and background event completion.
7. Keep logs, analytics, and error reports free of tokens, cookies, and
   sensitive payloads.

## Review Rules

- Do not rely on `URLSession.shared` when the feature needs custom cache,
  cookie, timeout, waits-for-connectivity, proxy, or delegate behavior.
- Do not decode before validating HTTP status and response type.
- Do not retry unsafe methods without idempotency keys or product approval.
- Do not keep downloaded files at temporary URLs after the delegate returns.
- Do not mix certificate trust policy into random request code; isolate trust
  challenge decisions.
- Treat HTTP/3, WebSocket, background transfer, and ATS behavior as
  current-source gated.

## Validation

- Build the affected target.
- Run unit tests around request construction, validation, decoding, error
  mapping, retry, cancellation, and auth refresh.
- Run integration tests against a fixture server when behavior depends on real
  HTTP, redirects, cookies, streams, or WebSockets.
- Test offline, timeout, bad status, bad JSON, cancelled, background relaunch,
  and credential-expired paths when in scope.
- Use Instruments or logs for high-volume or performance-sensitive clients.

## Output

For implementation or review work, return:

1. URLSession surface and configuration inspected
2. Request, response, transfer, retry, auth, and cache findings
3. Background, trust, privacy, and test boundaries
4. Validation run or still needed
5. Current-source assumptions for protocol or platform behavior
