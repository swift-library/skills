# SwiftUI Text Patterns Reference

## Table of Contents

- [Text Initialization: Verbatim vs Localized](#text-initialization-verbatim-vs-localized)

## Text Initialization: Verbatim vs Localized

Use this file for SwiftUI-local text decisions. If the task involves String
Catalog setup or migration, generated symbols, translator export/import,
pseudolocalization, localized package/framework resources, bundle lookup, RTL
validation, or locale UI tests, use `xcode-localization-patterns`.

**Default: always use `Text("…")`.** Only use `Text(verbatim:)` when explicitly required for a string literal that must not be localized.

```swift
// Localized literal - "Save" is used as the localization key and looked up in Localizable.strings (only if one exists in the project)
Text("Save")

// String variable - bypasses localization automatically; no verbatim needed
let filename: String = model.exportFilename
Text(filename)

// Non-localized literal - use verbatim only when the literal must not be localized
Text(verbatim: "pencil")
```

### Decision Flow

```
Is the input a String variable or dynamic value?
└─ YES → Text(variable)          // bypasses localization automatically

Is the string literal intended for localization?
├─ YES → Text("…")               // default; key looked up in Localizable.strings
└─ NO  → Text(verbatim: "…")     // only when explicitly non-localized
```
