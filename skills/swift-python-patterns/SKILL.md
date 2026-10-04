---
name: swift-python-patterns
description: Use this skill when changing, reviewing, refactoring, testing, or debugging a Swift PythonKit-style bridge package such as swift-python, the `Python` module/product, `PythonObject`, `PythonConvertible`, `ConvertibleFromPython`, `PythonLibrary`, dynamic Python library loading, `PYTHON_VERSION`, `PYTHON_LIBRARY`, `PYTHON_LOADER_LOGGING`, Swift-callable Python functions/classes, numpy array conversion, or runtime Python bridge failures. Do not use for ordinary Python application code, Python package management, or unrelated app business logic.
---

# Swift Python Patterns

## Purpose

Guide implementation, review, and troubleshooting for Swift packages that
provide PythonKit-style Swift/Python bridging. These packages expose a Swift
module such as `Python`, dynamically load a Python runtime, and wrap Python
objects/functions for Swift callers.

## When To Use

- Editing or reviewing a `swift-python` / PythonKit-style SwiftPM package.
- Debugging `PythonObject` behavior, dynamic member access, call semantics,
  Swift/Python conversions, ranges, dictionaries, bytes, or numeric operations.
- Working with `PythonConvertible` / `ConvertibleFromPython`.
- Changing `PythonLibrary` runtime discovery, Python C API symbol loading, or
  runtime selection with environment variables.
- Reviewing Swift callbacks exposed to Python through `PythonFunction`,
  `PythonInstanceMethod`, or `PythonClass`.
- Debugging numpy array conversion helpers.

## When Not To Use

- Ordinary Python scripts, Python dependency management, virtualenv setup, or
  Python application architecture.
- ML model usage just because Python is involved, when the Swift/Python bridge
  is not the issue.
- App-specific document, workspace, UI, or domain behavior.

## Package Surface

Verify the manifest before assuming the import name. Some README material may
say `import PythonKit`, while local package manifests may expose product and
module name `Python`.

Common surfaces:

- `Python`: global interface for importing modules, accessing builtins, calling
  Python functions, and creating Python slices.
- `PythonObject`: dynamic Python value wrapper with collection, numeric,
  comparable, string, callable, and dynamic member behavior.
- `PythonConvertible` / `ConvertibleFromPython`: Swift/Python conversion
  protocols.
- `PythonLibrary`: dynamic Python library loader and environment-variable based
  runtime selection.
- `PythonFunction`, `PythonInstanceMethod`, `PythonClass`: Swift callbacks and
  dynamic Python class construction.
- `Array.init?(numpy:)`: one-dimensional numpy array conversion for supported
  scalar types.

## Workflow

When changing runtime loading:

1. Inspect `Package.swift` and `PythonLibrary.swift` first.
2. Preserve environment-variable controls: `PYTHON_VERSION`, `PYTHON_LIBRARY`,
   and `PYTHON_LOADER_LOGGING`.
3. Keep loader diagnostics useful for the common fatal path: "Python library
   not found".
4. Do not call runtime-selection APIs after Python has already initialized.
5. Validate in a shell where the intended Python runtime is visible.

When changing conversions:

1. Update conversion tests for scalar, optional, collection, dictionary, range,
   bytes, and callable behavior.
2. Preserve Swift error reflection for throwing Python calls.
3. Keep dictionary initialization order and duplicate-key behavior aligned with
   tests.
4. Treat numpy as optional runtime evidence. Tests should skip numpy-specific
   assertions when `Python.attemptImport("numpy")` fails.

When adding consumers:

1. Depend on the product/module exported by the local manifest.
2. Keep Swift/Python bridge use behind a narrow package or feature boundary.
3. Document required Python runtime, Python packages, and library path
   assumptions near the consuming code.

## Validation

Use the package path in the target repo:

```bash
swift test --package-path <path-to-swift-python>
```

If runtime discovery fails, rerun with loader logging:

```bash
PYTHON_LOADER_LOGGING=TRUE swift test --package-path <path-to-swift-python>
```

For host-specific Python selection, set one of:

```bash
PYTHON_VERSION=3 swift test --package-path <path-to-swift-python>
PYTHON_LIBRARY=/path/to/libpython3.dylib swift test --package-path <path-to-swift-python>
```

## Failure Modes

- Importing the README module name without checking the local manifest can fail
  when the package product/module name differs.
- Missing, incompatible, or unsigned Python runtime libraries can crash or fail
  during dynamic loading, especially under macOS hardened runtime constraints.
- numpy-dependent behavior must not fail unrelated bridge tests when numpy is
  unavailable.
- Dynamic Python exceptions should remain diagnosable as Python failures rather
  than generic Swift errors.
- App-specific domain behavior inside the bridge package turns infrastructure
  into an unrelated runtime owner.
