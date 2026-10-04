# Core ML Model Optimization

Use this reference when the task is compressing, profiling, or performance
tuning a Core ML model. Treat every compression choice as empirical: a smaller
artifact is not accepted until accuracy, latency, memory, and compute placement
are checked on representative hardware.

## Authority

- Official Core ML Tools optimization documentation for Python compression APIs.
- Local Core ML SDK or Swift interface for `MLModelConfiguration`, `MLTensor`,
  `MLState`, and `MLComputePlan`.
- The model artifact, calibration/evaluation data, and device measurements.

## Compression Choices

- Quantization reduces numeric precision. It can be data-free for weights or
  calibration-aware for activations and some large-model paths.
- Palettization clusters weights into lookup tables. It is often useful when
  storage and memory are the primary constraints.
- Pruning removes or sparsifies weights. It needs accuracy checks because
  sparsity can change both quality and compute placement.
- Joint compression can stack techniques, but each added technique needs a
  separate before/after comparison.

Do not promote source tables of expected size reduction into local truth without
measuring the actual model. Compression payoffs depend on architecture, target
OS, hardware, and compiler placement.

## Optimization Workflow

1. Establish the uncompressed baseline: model size, fixture accuracy, latency,
   peak memory, energy if relevant, and compute placement.
2. Pick one compression technique from the real constraint. Storage pressure,
   memory pressure, and latency are different goals.
3. Keep the compression config in source control or generated artifact metadata
   so the model can be reproduced.
4. Re-run source/Core ML parity fixtures and task-level accuracy fixtures.
5. Profile on the target hardware and OS. Simulator results are not enough for
   Neural Engine or GPU placement decisions.
6. Keep both rollback and fallback behavior explicit for downloaded or cached
   models.

## Neural Engine And Shape Review

- Prefer concrete or enumerated input shapes when the product has known sizes.
- Avoid broad dynamic ranges unless the feature truly needs them.
- Check image preprocessing and tensor layout before blaming compute placement.
- Use `MLComputePlan` or model preview/profiling tools to inspect operation
  placement when model performance is surprising.

## Swift Integration Checks

- `MLModelConfiguration.computeUnits` should be explicit when performance or
  energy is part of the requirement.
- `allowLowPrecisionAccumulationOnGPU`, model parameters, function names, and
  stateful model usage are current-SDK-gated.
- `MLTensor`, `MLState`, async prediction, and batch prediction need task
  ownership and cancellation review in Swift concurrency code.
- For Vision integration, validate both `VNCoreMLModel` setup and Vision input
  preprocessing after compression.

## Review Checklist

- [ ] Baseline artifact and compressed artifact are both identifiable.
- [ ] Compression config, calibration data, and fixture data are reproducible.
- [ ] Accuracy or task-quality delta is measured and accepted.
- [ ] Latency, memory, and compute placement are measured on representative
      hardware.
- [ ] App-side preprocessing/postprocessing was not silently changed.
- [ ] Downloaded or cached compressed models have versioning, integrity checks,
      and fallback behavior.
