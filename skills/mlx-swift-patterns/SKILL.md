---
name: mlx-swift-patterns
description: Use this skill for MLX Swift package implementation and review across SwiftPM dependency setup, MLX arrays, MLXNN, MLXOptimizers, MLXRandom, Apple silicon execution, Metal shader build constraints, model examples, MLX Swift LM/VLM workflows, model download and size selection, memory pressure, backend selection, and package/runtime fallback decisions. Do not use for Apple SDK framework work, Core ML deployment, Foundation Models generation, llama.cpp C/C++ runtime implementation, or server model APIs.
---

# MLX Swift Patterns

## Purpose

Guide implementation, review, and troubleshooting for the `ml-explore/mlx-swift`
package and related Swift package workflows for local machine-learning
experimentation and inference.

## When To Use

- Adding or reviewing the `mlx-swift` SwiftPM dependency and product selection,
  including `MLX`, `MLXNN`, `MLXOptimizers`, and `MLXRandom`.
- Working with MLX arrays, transformations, neural-network modules, optimizers,
  random APIs, and model examples in Swift.
- Building or adapting MLX Swift LM/VLM, chat, evaluation, Stable Diffusion, or
  training examples.
- Debugging Apple silicon, Metal shader, Xcode versus command-line SwiftPM, or
  memory-pressure constraints.
- Comparing MLX Swift against Foundation Models, Core ML, local C/C++ runtimes,
  or server APIs as a backend choice.

## When Not To Use

- Do not treat MLX Swift as an Apple SDK framework. It is a Swift package.
- Do not use for Core ML model conversion, deployment, or `MLModel` prediction.
- Do not use for Foundation Models generation sessions.
- Do not use for llama.cpp C/C++ runtime implementation, GGUF internals, or CLI
  server operation unless the task is only choosing a Swift-app backend.
- Do not use for server model APIs, cloud training, or generic ML theory.
- Do not invent MLX Swift package behavior. Verify the current package source,
  examples, and build instructions.

## Inputs To Inspect

- `Package.swift`, package resolution, product dependencies, and Xcode project
  integration.
- MLX imports, array/model code, training or inference loops, tokenizer/model
  loading, and example-derived code.
- Model download, cache, size, quantization, memory, and device-selection
  assumptions.
- Xcode, SwiftPM, CMake, submodule, Metal shader, and CI build commands.
- Fallback code that chooses between MLX Swift, Foundation Models, Core ML,
  local C/C++ runtimes, or server APIs.

## Workflow

1. Confirm the task is package/runtime integration, not an Apple SDK framework
   workflow.
2. Check the current `mlx-swift` package version, products, source layout,
   examples, and build caveats before editing code or docs.
3. Keep SwiftPM dependency and product selection minimal. Avoid duplicate MLX
   linkage across app and framework targets.
4. Validate Xcode build requirements when Metal shader compilation or iOS/macOS
   app examples are involved.
5. Bound model selection by device memory, storage, download path, tokenizer
   compatibility, and user-visible latency.
6. Preserve fallback decisions explicitly. MLX Swift, Foundation Models, Core
   ML, local C/C++ runtimes, and server APIs solve different product and
   deployment problems.
7. Treat example-derived code as a starting point; adapt state ownership,
   cancellation, cache, and UI update paths to the target app.

## Review Rules

- Do not present MLX Swift as a drop-in replacement for Foundation Models or
  Core ML without checking model format, runtime, and UX constraints.
- Do not assume command-line SwiftPM builds every app target path that Xcode
  builds when Metal shaders are involved.
- Do not download large models without user-visible progress, cancellation,
  disk-space handling, and cache policy.
- Do not keep tokenizer/model compatibility or quantization assumptions only in
  comments.
- Treat package APIs, example names, release versions, and build caveats as
  primary-source gated.

## Validation

- Run the repo's relevant SwiftPM or Xcode build/test command for the target
  platform.
- Exercise a small model/example path before scaling to larger models.
- Test model download, cache hit, cache miss, cancellation, low-storage, and
  memory-pressure states when in scope.
- Measure first-token or first-result latency, steady-state throughput, memory,
  and energy on representative hardware.
- Recheck fallback behavior when MLX Swift cannot build, load a model, or meet
  latency/memory constraints.

## Output

For implementation or review work, return:

1. MLX Swift package, product, and build integration status
2. Array/model/example/runtime findings
3. Model size, memory, fallback, and backend-selection risks
4. Validation run or still needed
5. Primary-source assumptions for package behavior
