# Package.swift Samples

Use these samples as starting points. Keep plugin targets thin and put real
logic in the tool/core targets.

## Command Plugin With Tool And Core

```swift
// swift-tools-version: 6.0
import PackageDescription

let package = Package(
  name: "MyPackage",
  products: [
    .plugin(name: "MyGeneratorCommand", targets: ["MyGeneratorCommand"]),
  ],
  targets: [
    .plugin(
      name: "MyGeneratorCommand",
      capability: .command(
        intent: .custom(
          verb: "my-generator",
          description: "Run the package generator"
        ),
        permissions: [
          .writeToPackageDirectory(
            reason: "Allow explicit generation into package-owned output paths"
          )
        ]
      ),
      dependencies: ["MyGeneratorTool"]
    ),
    .target(
      name: "_MyGeneratorCore",
      path: "Plugins/_MyGeneratorCore"
    ),
    .executableTarget(
      name: "MyGeneratorTool",
      dependencies: ["_MyGeneratorCore"],
      path: "Plugins/MyGeneratorTool"
    ),
  ]
)
```

`Plugins/MyGeneratorCommand/Plugin.swift`:

```swift
import Foundation
import PackagePlugin

@main
struct MyGeneratorCommand: CommandPlugin {
  func performCommand(context: PluginContext, arguments: [String]) async throws {
    let tool = try context.tool(named: "MyGeneratorTool")
    let process = Process()
    process.executableURL = tool.url
    process.arguments = arguments
    try process.run()
    process.waitUntilExit()

    guard process.terminationReason == .exit,
          process.terminationStatus == 0
    else {
      throw PluginError.toolFailed(status: process.terminationStatus)
    }
  }
}

enum PluginError: Error, CustomStringConvertible {
  case toolFailed(status: Int32)

  var description: String {
    switch self {
    case let .toolFailed(status):
      return "my-generator exited with status \(status)"
    }
  }
}
```

`Plugins/MyGeneratorTool/Main.swift`:

```swift
import _MyGeneratorCore

@main
struct MyGeneratorTool {
  static func main() {
    MyGeneratorToolDriver.run(
      arguments: Array(CommandLine.arguments.dropFirst())
    )
  }
}
```

`Plugins/_MyGeneratorCore/MyGeneratorToolDriver.swift`:

```swift
public enum MyGeneratorToolDriver {
  public static func run(arguments: [String]) {
    // Parse arguments, plan work, emit files, and return process status.
  }
}
```

## Build Tool Plugin

```swift
import PackagePlugin

@main
struct MyBuildPlugin: BuildToolPlugin {
  func createBuildCommands(
    context: PluginContext,
    target: Target
  ) async throws -> [Command] {
    let tool = try context.tool(named: "MyGeneratorTool")
    let output = context.pluginWorkDirectoryURL
      .appending(path: "\(target.name)-Generated.swift")

    return [
      .buildCommand(
        displayName: "Generate \(target.name)",
        executable: tool.url,
        arguments: [
          "generate",
          "--target", target.name,
          "--output", output.path
        ],
        inputFiles: target.sourceModule?.sourceFiles.map(\.url) ?? [],
        outputFiles: [output]
      )
    ]
  }
}
```

Build tool plugins should declare all generated files as `outputFiles` and
write undeclared scratch data only under `pluginWorkDirectoryURL`.

## Shared Command And Build Tool

It is valid for command and build tool plugins to share one executable tool:

```swift
.plugin(
  name: "MyGenerator",
  capability: .buildTool(),
  dependencies: ["MyGeneratorTool"]
),
.plugin(
  name: "MyGeneratorCommand",
  capability: .command(
    intent: .custom(
      verb: "my-generator",
      description: "Run the generator"
    ),
    permissions: []
  ),
  dependencies: ["MyGeneratorTool"]
)
```

Keep the tool interface explicit: command plugin arguments should not silently
reuse build tool generated paths unless that is the documented contract.

## SwiftSyntax Tool Dependency

Put SwiftSyntax dependencies on the tool or core target, never on the plugin
target:

```swift
.target(
  name: "_MyGeneratorCore",
  dependencies: [
    .product(name: "SwiftParser", package: "swift-syntax"),
    .product(name: "SwiftSyntax", package: "swift-syntax"),
  ],
  path: "Plugins/_MyGeneratorCore"
)
```

Validate both paths:

```bash
swift build --product MyGeneratorTool
swift package my-generator --help
```

## Generated Host Or Bridge

For discovery, test bridges, or generated hosts, use the tool to emit source
into `pluginWorkDirectoryURL`, then have the plugin compile or pass that source
through the intended SwiftPM workflow.

Do not make an ordinary CLI own package discovery just because it can parse
files. Package discovery is a plugin/tool concern when it depends on SwiftPM
target metadata.
