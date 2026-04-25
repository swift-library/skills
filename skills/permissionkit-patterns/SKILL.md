---
name: permissionkit-patterns
description: Use this skill for PermissionKit implementation and review across child communication experiences, communication limits, contact handles, AskCenter, PermissionButton, PermissionQuestion, CommunicationTopic, PermissionChoice, PermissionResponse, significant app update topics, response observation, AskError, family/child account behavior, and iMessage-only availability. Do not use for generic app permissions, privacy prompts, parental controls strategy, or contact access without PermissionKit.
---

# PermissionKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for PermissionKit
communication experiences between a child and parent or guardian, including
permission requests, system UI, communication limits, and response handling.

## When To Use

- Creating communication permission requests for child account experiences.
- Using `AskCenter`, `PermissionQuestion`, `PermissionButton`,
  `CommunicationTopic`, `CommunicationHandle`, or `CommunicationLimits`.
- Observing `PermissionResponse` sequences and mapping `PermissionChoice`
  values.
- Handling significant app update topics or custom question topics.
- Reviewing `AskError`, empty handle validation, response observer lifecycle,
  and family/child account behavior.

## When Not To Use

- Do not use for generic camera, contacts, location, notification, or privacy
  permissions.
- Do not use for Contacts access unless PermissionKit communication handles are
  the issue.
- Do not use for broad parental-control product strategy without PermissionKit
  API implementation.
- Do not use for Screen Time or FamilyControls APIs unless the task also
  involves PermissionKit.

## Inputs To Inspect

- PermissionKit imports, deployment target, account/availability assumptions,
  and communication experience entry points.
- `PermissionQuestion`, `CommunicationTopic`, `CommunicationHandle`, and
  `PermissionChoice` construction.
- `AskCenter` send paths, `PermissionButton` presentation, custom UI wrappers,
  and SwiftUI/UIKit/macOS integration.
- Response observation, cancellation, observer ownership, empty-handle
  validation, and `AskError` handling.
- Copy, logging, and privacy treatment of contact handles and family decisions.

## Workflow

1. Confirm the task is PermissionKit communication permission, not generic app
   permission handling.
2. Verify current platform availability, account requirements, and iMessage-only
   communication behavior before making claims.
3. Build permission questions from explicit topics or handles and validate empty
   or malformed inputs.
4. Use system presentation when possible, or keep custom UI clear about what
   system request will be sent.
5. Observe responses with a durable owner and remove or cancel observation when
   the flow ends.
6. Handle denied, approved, no response, unavailable, and `AskError` paths.

## Review Rules

- Do not conflate PermissionKit with ordinary app permissions.
- Do not assume every user is in a child/family account context.
- Do not use deprecated presentation APIs when current replacements are
  available.
- Do not log contact handles, guardian responses, or child account context
  unnecessarily.
- Treat account behavior, platform support, response delivery, and deprecated
  API replacement as current Apple documentation and SDK gated.

## Validation

- Build the affected app target.
- Test unavailable account/platform, empty handles, one contact, multiple
  contacts, custom topic, significant app update topic, send failure, approved
  response, denied response, and observer cleanup paths.
- Validate real account behavior when simulator or mocked flows cannot prove
  system response delivery.

## Output

For implementation or review work, return:

1. PermissionKit versus generic permission boundary decision
2. Topic, handle, and question construction findings
3. Presentation, response, and observer lifecycle findings
4. Availability, account, and privacy findings
5. Validation run or still needed
