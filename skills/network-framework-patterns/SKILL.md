---
name: network-framework-patterns
description: Use this skill for Network.framework implementation and review across NWConnection, NWListener, NWBrowser, NWPathMonitor, NWParameters, NWEndpoint, NWProtocolTCP/UDP/TLS/WebSocket/QUIC options, local network privacy, Bonjour browsing, peer-to-peer protocols, connection state machines, backpressure, receive loops, TLS parameters, and path-aware networking. Do not use for ordinary HTTP API clients, URLSession transfers, App Transport Security-only review, or generic package architecture.
---

# Network Framework Patterns

## Purpose

Guide implementation, review, and troubleshooting for Network.framework
connections, listeners, browsers, path monitoring, custom protocols, local
network discovery, and transport-level behavior.

## When To Use

- Implementing `NWConnection`, `NWListener`, `NWBrowser`, `NWPathMonitor`,
  `NWParameters`, or `NWEndpoint` workflows.
- Building custom TCP, UDP, TLS, WebSocket, QUIC, multicast, Bonjour, or
  peer-to-peer transport behavior.
- Debugging connection state, receive loops, send completion, backpressure,
  path changes, local network privacy, or TLS parameter setup.
- Reviewing protocol framing, message boundaries, reconnection, cancellation,
  and queue ownership.

## When Not To Use

- Do not use for ordinary HTTP API clients or REST/GraphQL calls.
- Do not use for background task scheduling.
- Do not use for certificate trust and pinning rules without Network.framework
  transport integration.
- Do not use for generic package architecture, UI state, or app feature design.
- Do not invent transport, QUIC, local network privacy, or platform behavior.
  Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- `NWConnection`, `NWListener`, `NWBrowser`, `NWPathMonitor`, queue, state, send,
  receive, cancellation, and restart code.
- Protocol framing, message parsing, backpressure, reconnect, heartbeat, and
  timeout logic.
- `NWParameters`, protocol options, TLS settings, local endpoint, Bonjour
  service, peer-to-peer, and local network usage strings.
- Logs, packet traces, Network Instruments, fixture servers, and device tests.

## Workflow

1. Classify the transport: client connection, server listener, browser,
   multicast/group, path monitor, or custom protocol stack.
2. Confirm queue ownership and lifecycle. Each connection/listener/browser
   needs explicit start, state handling, cancellation, and cleanup.
3. Make framing and parsing explicit. TCP is a byte stream; message boundaries
   are the app protocol's responsibility.
4. Configure `NWParameters` deliberately: required interface, TLS, privacy,
   multipath, Bonjour, peer-to-peer, and protocol options.
5. Handle `NWPath` changes as signals for user state and reconnection, not as a
   promise that a request will succeed.
6. Keep receive loops bounded and backpressure-aware.
7. Validate on physical devices when local network, Bonjour, Bluetooth/Wi-Fi,
   or peer-to-peer behavior is involved.

## Review Rules

- Do not treat `NWConnection` as a drop-in HTTP client.
- Do not restart connections recursively without cancellation and backoff.
- Do not ignore state transitions such as waiting, failed, cancelled, and
  viability/path changes.
- Do not assume Bonjour or local network discovery works without user consent
  and Info.plist purpose strings.
- Treat QUIC, WebSocket protocol options, local network privacy, and peer-to-peer
  behavior as current-source gated.

## Validation

- Build the affected target.
- Run transport tests against a local or fixture endpoint when feasible.
- Test connection refused, DNS failure, TLS failure, path change, cancellation,
  reconnect, partial frames, and malformed frames.
- Test local network permission, Bonjour browsing, and physical-device behavior
  when discovery is in scope.
- Capture Network Instruments or packet/log evidence for performance or
  interoperability failures.

## Output

For implementation or review work, return:

1. Network.framework surface and transport shape
2. State, queue, framing, parameter, and privacy findings
3. Reconnect, TLS, local network, and validation boundaries
4. Validation run or still needed
5. Current-source assumptions for protocol or platform behavior
