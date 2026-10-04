# Foundation Models Integration

## Model And Deployment Boundaries

Keep the OS 26 `SystemLanguageModel` path for supported devices. Check model
availability, Apple Intelligence settings and the requested capability before
creating the successful user path. `tokenCount(for:)` requires 26.4 and is not
available to a 26.0 deployment target; `contextSize` is back-deployed to 26.0.

OS 27 adds framework cloud models and the public `LanguageModel` / `Executor`
provider surface. Gate these separately. watchOS 27 framework/cloud support
does not imply that `SystemLanguageModel` runs locally on Apple Watch: the
27.0 SDK marks that model unavailable on watchOS.

Before selecting another model, verify capability, destination, privacy,
credentials, entitlement, quota/cost, cancellation and fallback. Reusing
`LanguageModelSession` does not give models identical data-processing rules.
Obtain the product's required opt-in before transferring data outside the
device. Keep authorization and irreversible tool effects enforced by code.

`DynamicProfile` selects the active profile for a session declaratively. Treat
that as framework session behavior; it does not establish a general multi-agent
or skill-orchestration architecture.

## Provider Implementation

Use the installed SDK's exact `LanguageModel` and executor declarations.
Maintain executors according to their configuration; prewarming is a hint and
must not be required for correctness. Read the complete transcript. Prefix
caches can be reused for appends but must invalidate correctly for edits or
trimming. Bound retained history and redact logging independently of model use.

The 27.0 SDK uses an unlabeled capability initializer:

```swift
var capabilities: LanguageModelCapabilities { .init([]) }
```

For a text increment, `appendText` requires a token count:

```swift
await channel.send(
    .response(action: .appendText(delta, tokenCount: tokenCount))
)
```

Get `tokenCount` from the actual provider/decoder, not string length. Preserve
increment order, usage and metadata. Advertise only supported tools, schemas,
modalities and generation options; reject unsupported requests clearly rather
than weakening output validation or side-effect authorization.

Session videos may show older signatures. Compare them with the API reference
and local `.swiftinterface` before copying code. A compiled protocol adapter is
not evidence that a real provider, PCC entitlement or device model works.

## Compatibility And Validation

The 27.0 SDK marks `SystemLanguageModel.init(adapter:guardrails:)` obsoleted
on OS 27. Keep needed older-system adapter knowledge and check the current
declaration; do not invent an unverified replacement migration.

Validate unavailable/disabled/restricted states, generation failure,
cancellation, streaming order, structured-output rejection and tool denial.
Separate source confirmation, typechecking, mock-provider tests and real model
generation. A live-provider run requires the intended credentials, data boundary
and supported device/OS. Sources and unresolved version checks are listed in
`official-sources.md`.
