---
name: swiftpm-plugin-patterns
description: Use this skill for designing, implementing, reviewing, or debugging Swift Package Manager command plugins, build tool plugins, executable tool targets, plugin tool/core target topology, Package.swift plugin dependencies, context.tool(named:) workflows, generated source or generated host flows, SwiftSyntax parser tools inside plugins, macro-target interactions, host-tool build graph diagnostics, and plugin fixture validation. Do not use for general SwiftPM dependency management, app release packaging, macro expansion authoring unrelated to plugins, or non-plugin Swift package architecture.
---

# SwiftPM Plugin Patterns

## Purpose

Design and debug SwiftPM plugins with the official thin-plugin pattern:

```text
Plugin target
  -> executableTarget Tool
    -> internal Core target
```

The plugin orchestrates SwiftPM context, permissions, and process execution.
The executable tool and core target own parsing, planning, source generation,
discovery, and business logic.

## When To Use

- Designing a command plugin or build tool plugin.
- Moving plugin logic into an executable tool and internal core target.
- Adding generated sources, generated hosts, bridge code, or discovery tools.
- Deciding where SwiftSyntax, SwiftParser, or custom scanners should live.
- Debugging `context.tool(named:)`, host-tool builds, `Modules-tool`,
  `*-tool.build`, or `no such module` failures.
- Reviewing `Package.swift` plugin dependencies and plugin/tool boundaries.

## When Not To Use

- Do not use for ordinary SwiftPM target graph design without plugins.
- Do not use for app release packaging, signing, or notarization.
- Do not use for macro implementation design unless the macro is part of a
  plugin/tool build graph.
- Do not use for general dependency update advice unless the dependency affects
  a plugin executable tool or host-tool build.

## Core Workflow

1. Identify the plugin kind: command plugin, build tool plugin, or both sharing
   one tool.
2. Inspect `Package.swift` first. Confirm the plugin depends only on executable
   or binary tools.
3. Keep `Plugin.swift` thin: collect SwiftPM metadata, compute inputs/outputs,
   call `context.tool(named:)`, launch or return commands, and propagate status.
4. Put implementation in `Tool/Main.swift` and an internal Core target.
5. If SwiftSyntax is needed, put it in the executable tool or core target, not
   the plugin target, then validate the real plugin path.
6. For source generation, write generated files only to plugin work directories
   or declared output paths.
7. Validate the ordinary product build and the real plugin path.
8. If the real plugin path fails, inspect the host-tool build graph before
   changing architecture.

## Decision Rules

- Plugin targets do not import SwiftSyntax, SwiftParser, local runtime products,
  or library products.
- Tool/core targets may depend on library products, including SwiftSyntax, but
  SwiftSyntax must pass the command-plugin host-tool hard gate.
- Do not hide package discovery or generation behind an ordinary CLI subcommand
  if it is a SwiftPM plugin concern. Use a dedicated tool executable.
- Do not claim plugin support from `swift build --product Tool` alone; always
  run the SwiftPM plugin command.
- If a SwiftSyntax host-tool hard gate fails, keep a production fallback and
  record an ADR with reproduction commands, upstream evidence, workaround
  status, and build graph evidence.

## Reference Files

- `references/official-patterns.md`: official SwiftPM sources, proposals, and
  versioned citations.
- `references/package-swift-samples.md`: copyable package/plugin/tool/core and
  generated source patterns.
- `references/swiftsyntax-plugin-gotchas.md`: SwiftSyntax, macro targets, and
  host-tool failure patterns.
- `references/debugging-checklist.md`: command and `debug.yaml` inspection
  checklist.
- `references/adr-template.md`: compact ADR template for plugin build graph
  decisions.

## Output

For design work, return:

1. Plugin topology.
2. `Package.swift` shape.
3. Tool/Core responsibilities.
4. Generated file and permission model.
5. Validation commands.
6. Known risks and ADR notes.

For debugging work, return:

1. Failing command.
2. Direct tool build result.
3. Real plugin path result.
4. `debug.yaml` / `Modules-tool` evidence.
5. Root cause class.
6. Minimal fix or fallback.
