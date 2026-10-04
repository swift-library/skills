<p align="center">
  <img src="{{docs_dir}}/Assets/Logo.svg" width="160" alt="{{name}} logo">
</p>

<h1 align="center">{{name}}</h1>

<p align="center">
  {{value_sentence}}
</p>

{{badges}}

[Overview](#overview) · [Install](#install) · [Quick start](#quick-start) ·
[Usage](#usage) · [Requirements](#requirements) ·
[Documentation](#documentation) · [License](#license)

> [!NOTE]
> {{status_note}}

## Overview

{{overview_paragraph}}

- {{capability}}
- {{capability}}
- {{capability}}

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

## Quick start

```swift
{{quick_start}}
```

## Usage

### {{task}}

{{task_explanation}}

```swift
{{task_example}}
```

## Requirements

- Swift {{swift_tools}} or later
- {{platforms}}

## Documentation

- [{{doc_title}}]({{doc_path}})

## License

{{name}} is available under the {{license_name}}. See [LICENSE](LICENSE){{notice_clause}}.
