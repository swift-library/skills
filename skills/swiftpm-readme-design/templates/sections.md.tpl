## {{snippet_section}}

```swift
{{quick_start}}
```

## Install

Add the package and the products you use to `Package.swift`:

```swift
dependencies: [
  {{install_dependency}}
],
targets: [
  .target(
    name: "YourTarget",
    dependencies: [
      .product(name: "{{product}}", package: "{{name}}"),
    ]
  ),
]
```

## Products

| Product | Purpose |
| --- | --- |
| `{{product}}` | {{product_purpose}} |

## Usage

### {{task}}

{{task_explanation}}

```swift
{{task_example}}
```

## Requirements

- Swift {{swift_tools}} or later
- {{platforms}}
