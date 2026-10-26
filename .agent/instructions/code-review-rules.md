---
description: Flag swift-skills changes that misroute requests, harden one-off values into requirements, or claim untested capabilities.
---
## Code Review Rules

### Trigger and ownership

- Flag a skill description that promises work outside the skill's documented
  boundary; it can route a request to the wrong owner. Safe path: align the
  description, supported workflow and resource routes.

### Reusable guidance

- Flag guidance that turns a single organization's choices or one execution's
  inputs into a reusable requirement. Safe path: accept the value as an input
  or keep it in the example or owner that supplies it.

### Evidence and coverage

- Flag a capability claim without source support or an executable check where
  one is available, and a changed workflow without an eval that distinguishes
  the intended behavior. Safe path: verify the claim and add focused coverage
  in the owning skill.
