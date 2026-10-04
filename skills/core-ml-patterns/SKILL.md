---
name: core-ml-patterns
description: Use this skill for Core ML implementation and review across coremltools conversion, .mlmodel, .mlpackage, .mlmodelc, generated model classes, MLModel loading, MLModelConfiguration, compute units, MLFeatureProvider, async and batch prediction, MLState, MLTensor, MLMultiArray, image preprocessing, VNCoreMLModel integration, quantization, palettization, pruning, MLComputePlan profiling, downloaded model deployment, and on-device model performance. Do not use for Foundation Models generation, MLX Swift package runtime work, Vision request semantics without Core ML model issues, or server model APIs.
---

# Core ML Patterns

## Purpose

Guide implementation, review, and troubleshooting for Core ML model loading,
configuration, prediction, deployment, profiling, and app-side model lifecycle.

## When To Use

- Converting PyTorch, TensorFlow, or other supported trained models with
  `coremltools`, including deployment-target, shape, precision, and model-type
  decisions.
- Integrating `.mlmodel`, `.mlpackage`, or compiled `.mlmodelc` assets into an
  app or package.
- Choosing generated model classes versus manual `MLModel` loading.
- Configuring compute units, model parameters, async loading, caching, or
  downloaded model storage.
- Compressing or optimizing models with quantization, palettization, pruning,
  Neural Engine-friendly shapes, or current `coremltools.optimize` APIs.
- Implementing typed predictions, `MLFeatureProvider`, batch prediction,
  `MLState`, `MLTensor`, `MLMultiArray`, image preprocessing, or pixel-buffer
  conversion.
- Profiling model placement and performance with `MLComputePlan`, Instruments,
  or device measurements.
- Connecting a Core ML model to Vision through `VNCoreMLModel` or related
  requests.

## When Not To Use

- Do not use for Foundation Models generation sessions.
- Do not use for MLX Swift package arrays, training examples, or model runtime
  integration.
- Do not use for Vision built-in request semantics unless a Core ML model is
  the integration point.
- Do not use for server-side model APIs, MLOps, model marketing, or broad AI
  strategy.
- Do not invent version-specific Core ML API behavior. Verify current Apple
  documentation, the local SDK, and the actual model artifact.

## Inputs To Inspect

- Model files, build phases, bundle resources, package resources, and download
  locations.
- Conversion scripts, source model framework, `coremltools` version, Python
  environment, deployment target, input/output types, and shape constraints.
- Generated model interfaces, manual `MLModel` loading code, configurations,
  prediction calls, and error handling.
- Compression scripts, calibration data, accuracy reports, and before/after
  model artifacts.
- Input/output feature names, shapes, image preprocessing, tensor/multiarray
  conversion, and postprocessing.
- Vision integration, pipelines, model collections, On-Demand Resources, and
  cache invalidation. `MLModelCollection` and On-Demand Resources are
  deprecated; the SDK names Background Assets (or `URLSession` for model
  collections) as the replacement.
- Profiling traces, `MLComputePlan` output, memory measurements, tests, and
  sample fixtures.

## Workflow

1. Identify the source model, conversion path, Core ML format, target OS,
   expected input/output schema, and whether the model is bundled, downloaded,
   or generated at build time.
2. For conversion work, verify current `coremltools` docs and prefer an
   explicit `ct.convert` setup with deployment target, input/output types,
   precision, shape strategy, and saved model package path.
3. Prefer generated model classes when they make feature names and types safer;
   use manual `MLModel` loading when dynamic model selection or downloaded
   models require it.
4. Configure `MLModelConfiguration` deliberately: compute units, parameters,
   specialization, and device placement should reflect measured constraints.
5. Keep preprocessing and postprocessing explicit and tested. Verify image
   orientation, color space, scaling, normalization, shape, and data type.
6. Bound model loading, compilation, and cache paths. Handle unavailable,
   corrupt, incompatible, or stale downloaded models.
7. Use async and batch prediction paths when they match the app workflow, but
   keep actor/thread ownership clear for stateful model usage.
8. Treat compression as an experiment: choose quantization, palettization, or
   pruning from the model and device constraint, then re-check accuracy,
   latency, memory, and compute placement.
9. Profile on representative hardware before making performance claims.
10. Treat pure Vision request behavior as out of scope once the Core ML model
    handoff is no longer the main issue.

## Review Rules

- Do not assume a model in the repo is included in the app bundle or package.
- Do not accept a converted model without checking the source model was in
  inference/evaluation mode where the source framework requires it.
- Do not ignore feature-name, shape, color-space, and orientation mismatches.
- Do not compress a model without an accuracy fixture and a latency or memory
  comparison on representative hardware.
- Do not leave model downloads without versioning, integrity checks, and
  fallback behavior.
- Do not put heavyweight model work on the main actor unless the API requires
  it and the work is trivial.
- Treat `MLTensor`, `MLState`, `MLComputePlan`, async prediction, and compute
  unit behavior as current-source gated.

## Validation

- Build the affected app/package and confirm model resources are present.
- For conversion changes, run the conversion script and inspect the generated
  model package, input/output names, shapes, deployment target, and precision.
- Run at least one known input fixture through the model and assert output
  shape, labels, score ranges, or downstream behavior.
- For compression changes, compare compressed and uncompressed outputs with a
  representative fixture set before accepting the artifact.
- Test missing, incompatible, corrupt, and upgraded model artifacts when model
  files are downloaded or cached.
- Profile latency, memory, compute placement, and energy on target hardware for
  user-facing model paths.
- Test Vision integration with representative images or frames when
  `VNCoreMLModel` is in scope.

## Output

For implementation or review work, return:

1. Model artifact, loading, configuration, and deployment judgment
2. Conversion or compression pipeline findings when in scope
3. Prediction, preprocessing, postprocessing, and Vision-integration findings
4. Performance, memory, cache, and fallback risks
5. Validation run or still needed
6. Current-source assumptions for version-specific behavior

## References

- `references/model-conversion.md`: `coremltools` conversion, model formats,
  inputs/outputs, shape strategy, and conversion validation.
- `references/model-optimization.md`: quantization, palettization, pruning,
  Neural Engine shape choices, Swift loading, and profiling validation.
