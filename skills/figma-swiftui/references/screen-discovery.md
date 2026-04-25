# Screen Discovery

Use this when a Figma node is not obviously a single implementable screen or
component.

## When To Trigger

- Link points to a page, root canvas, flow, or large frame.
- Screenshot would include multiple screens, device frames, or variants.
- Source brief describes multiple screens.
- Multiple child frames could plausibly match the user's requested screen.
- The node name is generic, such as "Screens", "Flow", "Prototype", or "Page".

## Goal

Build a small candidate screen map before fetching expensive design context or
writing code.

## Process

1. Fetch metadata for the provided node.
2. List candidate child frames/components with node ID, name, size, and role.
3. Compare candidates with the source brief and user request.
4. Assign confidence: high, medium, or low.
5. Fetch design context only for high-confidence targets.
6. Ask the user when two or more candidates materially change implementation.

## Candidate Map Shape

```text
Target candidates:
- Login / 390x844 / node 12:34 / high / matches brief primary screen
- Forgot Password / 390x844 / node 12:56 / medium / linked secondary action
- Marketing Hero / 1440x900 / node 12:78 / low / web frame, probably out of scope
```

## Confidence Rules

- High: name, size, and surrounding nodes match the request.
- Medium: likely match, but there are variants or nearby alternatives.
- Low: broad container, wrong platform size, or missing behavior match.

## Stop Conditions

Ask before proceeding when:

- source document and Figma disagree on screen count
- multiple candidate frames map to the same product screen
- the node appears to be a prototype or FigJam board
- the only available frame is the wrong platform size and no adaptive rule is
  stated
