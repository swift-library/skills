---
name: foundation-models-patterns
description: Use this skill to implement or review Apple Foundation Models sessions, model availability, structured generation, streaming, tool calling, and LanguageModel provider integration. Covers on-device and framework-supported cloud paths with explicit privacy and fallback checks. Do not use for standalone Core ML or MLX inference, Vision recognition, deterministic Natural Language analysis, unrelated server AI APIs, or marketing copy.
---

# Foundation Models Patterns

## Purpose

Guide implementation, review, and troubleshooting for apps that use Apple's
Foundation Models framework for language understanding, generation, structured
output, and tool-backed tasks. The framework boundary includes its on-device
model and supported cloud/provider integrations, with distinct data and
availability constraints.

## When To Use

- Checking `SystemLanguageModel` availability, Apple Intelligence gating,
  device/locale/user-setting constraints, and fallback behavior.
- Creating or reviewing `LanguageModelSession` prompts, instructions,
  transcripts, prewarming, response options, and cancellation.
- Implementing structured output with `@Generable`, `@Guide`, schemas,
  validation, or streaming partial results.
- Adding model tool calls, side-effect boundaries, tool errors, transcript
  persistence, or adapter-backed customization.
- Reviewing privacy, resource use, context handling, guardrails, and app-state
  integration around local generation.
- Implementing OS-gated `LanguageModel` / `Executor` providers, framework cloud
  models, or capability-aware session selection.

## When Not To Use

- Do not use for Core ML model loading, conversion, prediction, or deployment.
- Do not use for MLX Swift package integration, arrays, or model examples.
- Do not use for Vision, Natural Language, Translation, or Speech framework
  work unless Foundation Models generation is the primary issue.
- Do not use for standalone server AI APIs without Foundation Models
  integration, unrelated web API prompt engineering, marketplace claims, or
  product copy.
- Do not invent availability, Apple Intelligence eligibility, model capability,
  or new API behavior. Verify current Apple documentation and the local SDK.

## Inputs To Inspect

- Foundation Models imports, availability checks, entitlements/capabilities if
  present, and minimum OS declarations.
- `SystemLanguageModel`, `LanguageModelSession`, `Instructions`, `Prompt`,
  `GenerationOptions`, transcript, response, and streaming code.
- `@Generable`, `@Guide`, schema, validation, and decoding types.
- Tool definitions, side-effect code, authorization checks, and error handling.
- UI state, persistence, logs, analytics, tests, and fallback/backend-selection
  code reached from generated output.

## Workflow

1. Confirm the feature is generation or language understanding through the
   Foundation Models framework, not a Core ML, MLX, Vision, Natural Language,
   Speech, or unrelated server-AI task.
2. Check availability before designing the happy path. Treat unavailable,
   disabled, unsupported, restricted, and loading states as first-class UI and
   control-flow states.
3. Keep session instructions stable and task-specific. Avoid hiding product
   state, permissions, or business rules in prompts when code can enforce them.
4. Use structured output for app-facing data. Keep schemas small, validated,
   and aligned with the downstream API or view model.
5. Bound transcript storage and context growth. Redact sensitive content before
   logging, analytics, crash reports, or support bundles.
6. Keep tools narrow, explicit, cancellable, and authorization-aware. Do not let
   tool calls perform surprising writes or broad data reads.
7. Review streaming, cancellation, retries, fallback, and error messaging as
   user-visible states, not only model-call mechanics.
8. Validate on a device and OS configuration that actually supports the needed
   model capability when feasible.

## Review Rules

For model/provider integration and version-sensitive APIs, read
`references/model-integration.md`. For source refresh, use
`references/official-sources.md`.

- Treat Foundation Models API names, availability, and capability claims as
  current-source gated.
- Prefer deterministic code for validation, permissions, formatting, and
  irreversible side effects.
- Do not persist complete transcripts unless the feature has a clear retention
  need.
- Do not treat generated output as trusted input to app services.
- Keep fallback routing explicit: Foundation Models, Core ML, MLX Swift, local
  C/C++ runtimes, and server APIs have different privacy, latency, packaging,
  and capability tradeoffs.

## Validation

- Build the affected app/package against the local SDK.
- Test unavailable, restricted, disabled, cancellation, timeout, and failure
  states.
- Test a short prompt, a longer context, structured output, and streaming when
  those paths are in scope.
- Test each tool call's success, denied, failed, and cancelled paths.
- Profile latency, memory, and energy for repeated generation when the feature
  is user-facing or runs often.

## Output

For implementation or review work, return:

1. Foundation Models availability and capability assumptions
2. Session, prompt, structured-output, and tool-call findings
3. Privacy, transcript, fallback, and resource-use boundaries
4. Validation run or still needed
5. Current-source assumptions for version-specific behavior
