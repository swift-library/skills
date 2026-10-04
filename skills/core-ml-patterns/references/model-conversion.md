# Core ML Model Conversion

Use this reference when the task is converting a trained model into a Core ML
artifact or reviewing a conversion script. Verify current `coremltools` docs
before treating package-version, source-framework, or converter-option details
as fixed.

## Authority

- Apple Core ML SDK or local Swift interface for Swift APIs.
- Official Core ML Tools documentation for `coremltools` conversion behavior.
- The actual source model, conversion script, and generated model artifact.

## Conversion Intake

Record these before changing conversion code:

- Source framework and artifact: PyTorch module/export, TensorFlow model,
  scikit-learn/XGBoost model, or another supported source.
- `coremltools` version and Python environment.
- Target platforms and minimum deployment target.
- Desired Core ML artifact: `.mlpackage`, `.mlmodel`, or compiled `.mlmodelc`.
- Input/output names, dtypes, tensor ranks, image color layout, scale, bias,
  and channel order.
- Shape policy: fixed shape, `EnumeratedShapes`, or `RangeDim`.
- Baseline fixture that can compare source-model output against Core ML output.

## Model Format

- Prefer ML Program `.mlpackage` for modern deployments when the deployment
  target supports it. Core ML Tools 7 and newer default `ct.convert` to
  `mlprogram` for iOS 15 / macOS 12 and newer targets.
- Treat legacy neural network `.mlmodel` conversion as a compatibility choice,
  not the default for new work.
- Use `.mlmodelc` only after compile/build handoff. Do not review the compiled
  artifact alone when the source `.mlpackage` and conversion script are
  available.

## PyTorch Conversion

- Put the model in inference mode before tracing or exporting when the source
  framework requires it. For PyTorch, call `model.eval()` before
  `torch.jit.trace` or `torch.export`.
- Provide representative example inputs. A traced PyTorch program does not
  carry all shape intent by itself.
- Prefer `ImageType` when Core ML should own image scaling, bias, color layout,
  and channel order. Prefer `TensorType` when the app owns preprocessing.
- Verify output labels, logits, probabilities, or embeddings against the source
  model with known fixtures.

## Shape Strategy

- Use fixed shapes when the app has one real size.
- Use `EnumeratedShapes` for a known set of sizes; this gives the compiler
  concrete choices and is usually better for Neural Engine placement.
- Use `RangeDim` only when the product truly accepts a broad dynamic range.
  Test the default shape and edge shapes.
- Keep preprocessing, resizing, crop policy, and orientation at one explicit
  boundary.

## Deployment Target And Precision

- Set `minimum_deployment_target` deliberately. Do not rely on whatever the
  converter infers when OS compatibility matters.
- Choose `compute_precision` from the target hardware and accuracy needs.
  Re-run fixtures when changing precision.
- Keep model input dtype and app-side input dtype aligned. Watch for accidental
  `Float32` / `Float16` / integer mismatches.

## Review Checklist

- [ ] Conversion script and Python environment are reproducible.
- [ ] Source model is in inference/evaluation mode when required.
- [ ] Deployment target and model type are explicit.
- [ ] Input and output names, shapes, dtypes, and image preprocessing match the
      app contract.
- [ ] Shape policy uses fixed or enumerated shapes before broad dynamic ranges.
- [ ] Source-model and Core ML outputs are compared with representative
      fixtures.
- [ ] The generated artifact is included in the app, package resources, or
      download pipeline that production actually uses.
