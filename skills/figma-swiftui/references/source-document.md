# Source Document Before Figma

Use this when the user provides a brief, ticket, `.txt`, `.md`, PRD, or inline
spec together with Figma work.

## Why It Comes First

The source document owns behavior and scope. Figma owns visuals inside that
scope. Reading the document first prevents fetching or implementing the wrong
screen, missing required states, or treating mockup-only elements as product
requirements.

## Extract A Compact Contract

Before any Figma MCP call, extract:

- feature goal
- expected screens or components
- entry point
- primary and secondary actions
- loading, empty, error, disabled, selected, pressed, and success states
- async work and data dependencies
- navigation or completion behavior
- device/platform scope
- out-of-scope items
- unclear points

Keep the contract short. It is working context, not a design document.

## Use The Contract To Narrow Figma

- If the document names one screen and the Figma link points to one frame, fetch
  that node.
- If the document names multiple screens and the Figma link points to a root or
  page node, run screen discovery before fetching design context.
- If the document says some Figma elements are out of scope, do not fetch or
  implement them.
- If the document describes behavior not visible in Figma, implement or account
  for that behavior while using Figma for visuals.

## Conflict Rules

- Document names a screen not visible in Figma: ask; do not invent it.
- Figma contains extra screens not mentioned by the document: ask; do not
  silently add them.
- Document action does not clearly map to a Figma control: ask before wiring it.
- Document state is missing in Figma: implement the state using project
  conventions and note the visual assumption.
- Figma and document disagree on primary CTA or screen count: stop and clarify.

## Stop Conditions

Do not fetch large Figma context while these are unresolved:

- which screen or component is in scope
- whether the request is new implementation or existing-screen adaptation
- whether multiple Figma frames map to one adaptive SwiftUI view
- whether Figma prototype/system chrome should be treated as product UI
