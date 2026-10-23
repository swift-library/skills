# Command Recipes

Set the variables used by the selected recipe from the task's inputs. Paths,
module names, symbol selectors, configuration IDs and budgets are parameters.
`API_DIR` is the target's ignored output directory; keep generated snapshots,
views, run reports and caches there. Commands below use the installed executable
name.

## Install And Check

```sh
brew install swift-library/tap/swift-interface-distiller
interface-distiller --version
interface-distiller --help
```

Check the installed version against the intended contract. If package-manager
metadata is stale, refresh it before relying on its release identity. Toolchain
and platform prerequisites come from the selected release's README and the
tap's requirements.

Alternatively, build a selected release through SwiftPM. `DISTILLER_TAG` and
`TOOL_CHECKOUT` identify the release and its checkout:

```sh
git clone --branch "$DISTILLER_TAG" --depth 1 \
  https://github.com/swift-library/swift-interface-distiller.git "$TOOL_CHECKOUT"
swift build --package-path "$TOOL_CHECKOUT" --build-system native \
  -c release --product interface-distiller
"$TOOL_CHECKOUT/.build/release/interface-distiller" --version
```

Invoke that executable directly or put it on PATH for the remaining recipes.
Do not install a different tool with a similar name.

## Collect A Package

Detect the configuration for a local build, review/edit it, then pass it
explicitly. `languageMode: "package"` honors each manifest; a numeric mode is
a global override, including dependencies. Conditions, traits, build mode and
declared environment belong in the configuration. `--sdk-path` supplies a
custom SDK's actual path when its identity is recorded in the configuration.

```sh
mkdir -p "$API_DIR"
interface-distiller configuration --output "$API_DIR/configuration.json"
interface-distiller collect package "$PACKAGE_PATH" \
  --configuration "$API_DIR/configuration.json" \
  --output "$API_DIR/api.json" --report "$API_DIR/run.json"
```

To replace the default library scope and add a resolved dependency module:

```sh
interface-distiller collect package "$PACKAGE_PATH" \
  --configuration "$API_DIR/configuration.json" \
  --module "$MODULE" --dependency-module "$DEPENDENCY_MODULE" \
  --output "$API_DIR/selected.json"
```

Repeat module options as needed. `--include` and `--exclude` match compiler
IDs, names or `Module.name`; exclusion wins. `--include-spi`,
`--include-synthesized` and `--source-locations` are explicit scope choices.
Source locations require the appropriate source root. Default synthesized
exclusion retains original protocol extensions and conformances.

## Normalize Graphs, Import A Module Or Collect Headers

Graphs require the producer's configuration; do not label them with locally
detected settings merely to make a command run. Graph paths may be files or
directories. Main and extension graphs contribute to the same module.

```sh
interface-distiller normalize "$GRAPH_PATH" --configuration "$PRODUCER_CONFIG" \
  --source-root "$SOURCE_ROOT" --source-locations --output "$API_DIR/graphs.json"
```

Importable binary modules require the exact producer configuration, a matching
executing compiler and explicit content/search roots, including imports:

```sh
interface-distiller collect module "$MODULE" --search-path "$BINARY_SEARCH_PATH" \
  --built-with "$PRODUCER_CONFIG" --configuration "$PRODUCER_CONFIG" \
  --output "$API_DIR/module.json"
```

Clang ExtractAPI collects an explicitly selected C or Objective-C view. Use
the actual header source root and target/SDK configuration:

```sh
interface-distiller collect headers "$HEADER_MODULE" --header "$HEADER_PATH" \
  --source-root "$SOURCE_ROOT" --language c \
  --configuration "$API_DIR/configuration.json" --output "$API_DIR/c.json"
interface-distiller collect headers "$HEADER_MODULE" --header "$OBJC_HEADER_PATH" \
  --source-root "$SOURCE_ROOT" --language objective-c \
  --configuration "$API_DIR/configuration.json" --output "$API_DIR/objc.json"
```

These are language-labelled observations, not an inferred Swift imported API.
Keep different supplied configurations distinct when combining snapshots:

```sh
interface-distiller merge "$FIRST_SNAPSHOT" "$SECOND_SNAPSHOT" \
  --output "$API_DIR/combined.json"
interface-distiller query "$API_DIR/combined.json" lookup "$SYMBOL" \
  --configuration-id "$CONFIGURATION_ID"
```

## Read The Interface

```sh
interface-distiller render "$API_DIR/api.json" --docs summary \
  --output-dir "$API_DIR/interface" --report "$API_DIR/interface-size.json"
interface-distiller render "$API_DIR/api.json" --docs full --show-implied \
  --output-dir "$API_DIR/full"
interface-distiller render "$API_DIR/api.json" --view evidence \
  --output-dir "$API_DIR/evidence"
interface-distiller render "$API_DIR/api.json" --by-module \
  --byte-budget "$MAX_BYTES" --output-dir "$API_DIR/modules"
```

Read the generated Markdown parts, not only the JSON file list on stdout.
Default docs are the leading prose paragraph; `full` retains all comments and
`none` omits them. `--show-implied` expands collected standard conformance
requirements collapsed in readable views. Rendering with `--view evidence`
keeps detailed metadata and per-symbol anchors. See [interpretation](interpretation.md) before
using measurements or a strict byte limit.

## Query And Slice

Lookup accepts semantic/compiler IDs, displayed names or joined paths;
ambiguous names return all observations. Prefer a precise ID when selecting
one overloaded or similarly named symbol. Relationship queries report observed
members, conformers and candidates, not inferred behavior.

```sh
interface-distiller query "$API_DIR/api.json" lookup "$SYMBOL"
interface-distiller query "$API_DIR/api.json" members "$SYMBOL" --format swift --show-implied
interface-distiller query "$API_DIR/api.json" conformers "$PROTOCOL" --format json
interface-distiller query "$API_DIR/api.json" initializers "$SYMBOL" --format markdown --docs full
interface-distiller query "$API_DIR/api.json" returning "$SYMBOL" --format swift --docs none
interface-distiller query "$API_DIR/api.json" slice "$SYMBOL" \
  --format json --max-symbols "$MAX_SYMBOLS" --max-bytes "$MAX_BYTES"
interface-distiller slice "$API_DIR/api.json" "$SYMBOL" \
  --format swift --max-bytes "$MAX_BYTES" --output "$API_DIR/context.swift"
```

All query kinds and the `slice` alias accept `json|swift|markdown` and budgets.
`--output` atomically writes the selected format. A budgeted non-slice JSON
query uses the slice-shaped envelope rather than the unbudgeted result shape.
For a hard total delivery limit, measure the output, account for context and
diagnostics, and reduce the payload selection as needed; do not cut raw bytes
out of structured snapshots or declarations.

## Compare And Baseline

When the user asks for a comparison, run swift-interface-distiller explicitly.
Collect the requested revisions with the same collector and matching
configuration and scope before comparing; recollect both when collector
versions differ. Use baseline write/check only when the user requests a
persisted baseline.

```sh
interface-distiller compare "$BASELINE_SNAPSHOT" "$CANDIDATE_SNAPSHOT" \
  --output "$API_DIR/comparison.json"
interface-distiller baseline write "$BASELINE_SNAPSHOT" "$API_DIR/baseline.json"
interface-distiller baseline check "$CANDIDATE_SNAPSHOT" "$API_DIR/baseline.json"
interface-distiller coverage "$API_DIR/api.json"
```

Baseline write validates before atomic replacement; baseline check never writes.
Keep a reviewed baseline separate from candidate output. Compiler compatibility
diagnostics are separate observations and do not turn a comparison into a version
or release decision. Handle nonzero exit codes explicitly as described in
[interpretation](interpretation.md).
