// swift-tools-version: 6.2
import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .macOS(.v14),
    ],
    products: [
        .executable(name: "MyApp", targets: ["MyApp"]),
    ],
    targets: [
        .executableTarget(
            name: "MyApp",
            path: "Sources/MyApp",
            resources: [
                .process("Resources"),
            ]),
    ]
)
