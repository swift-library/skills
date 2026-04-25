# Asset Handling

Use this for every visible non-text element before writing SwiftUI.

## Contents

- [Core Rule](#core-rule)
- [Inventory](#inventory)
- [Classification](#classification)
- [Export](#export)
- [Asset Catalog](#asset-catalog)
- [Rendering Mode](#rendering-mode)
- [Remote Images](#remote-images)
- [Minimal Examples](#minimal-examples)
- [Checklist](#checklist)

## Core Rule

Figma-owned visible assets come from Figma. Do not replace logos, illustrations,
photos, app icons, social icons, or designed icons with SF Symbols, text,
rectangles, circles, or hand-drawn SwiftUI shapes unless the user explicitly
approves the substitution.

SF Symbols are acceptable for system chrome or when the design clearly intends
a platform system symbol.

## Inventory

From the screenshot and design context, list every visible non-text element:

```text
| element | node/source | kind | strategy | notes |
| logo | 1:2 | logo | download | original rendering |
| chevron | 1:5 | icon | download | template if single color |
| avatar | remote data | photo | remote | existing image loader |
| divider | none | structural | code | Rectangle height 1 |
```

Do not remove a row because an SF Symbol looks similar.

## Classification

Use `download` for:

- icons drawn in Figma
- logos and brand marks
- illustrations and decorative artwork
- fixed photos or image fills owned by the design
- complex vector groups

Use `code` for:

- structural backgrounds
- dividers
- simple rounded rectangles
- borders/strokes
- gradients and shadows that are easier and more faithful in SwiftUI

Use `remote` for:

- user avatars
- feed images
- CDN content
- product images that are dynamic data

## Export

- Export during the active MCP session; localhost asset URLs may be ephemeral.
- Prefer Figma-rendered PNG for visible Figma-owned assets.
- Use node screenshots for icons, logos, artwork, and image-fill nodes when
  direct asset URLs are missing or not real PNGs.
- Treat SVG/XML/text responses as failed exports for fidelity-critical visible
  assets.
- Validate downloaded files with `file` or equivalent before adding them to the
  project.

## Asset Catalog

- Add bundled PNG assets to `Assets.xcassets`.
- Prefer a 3x source and generate 2x/1x only when the project convention
  requires variants.
- Name assets with stable, readable names such as `login_logo`,
  `settings_chevron`, or `empty_state_illustration`.
- Avoid raw Figma names like `Group 14`.
- Search existing asset catalogs before adding duplicates.

## Rendering Mode

Use template rendering for single-color UI icons that should tint with
`foregroundStyle`.

Use original rendering for:

- logos
- multicolor icons
- illustrations
- photos
- assets with intentional gradients or opacity

In SwiftUI, match the catalog setting with usage:

```swift
Image("settings_chevron")
    .renderingMode(.template)
    .foregroundStyle(.secondary)
```

## Remote Images

Use the project's existing image-loading path. Check for Kingfisher,
SDWebImage, Nuke, a custom image cache, or local conventions. If no image
loading path exists and the image is truly remote content, ask before choosing
an implementation.

## Minimal Examples

Asset catalog entry shape:

```text
Assets.xcassets/
  settings_chevron.imageset/
    settings_chevron.png
    settings_chevron@2x.png
    settings_chevron@3x.png
    Contents.json
```

```json
{
  "images": [
    { "filename": "settings_chevron.png", "idiom": "universal", "scale": "1x" },
    { "filename": "settings_chevron@2x.png", "idiom": "universal", "scale": "2x" },
    { "filename": "settings_chevron@3x.png", "idiom": "universal", "scale": "3x" }
  ],
  "info": { "author": "xcode", "version": 1 },
  "properties": { "template-rendering-intent": "template" }
}
```

SwiftUI usage:

```swift
Image("settings_chevron")
    .renderingMode(.template)
    .resizable()
    .scaledToFit()
    .frame(width: 16, height: 16)
    .foregroundStyle(.secondary)
```

Remote image decision:

```swift
// Prefer the project's existing image pipeline here.
// If the project uses Kingfisher/Nuke/SDWebImage, use that instead of AsyncImage.
AsyncImage(url: avatarURL) { image in
    image.resizable().scaledToFill()
} placeholder: {
    Color.secondary.opacity(0.12)
}
```

## Checklist

- [ ] Every visible non-text element is inventoried.
- [ ] Every Figma-owned visual has a Figma export or approved substitution.
- [ ] No placeholder `Text`, `Rectangle`, `Circle`, or hand-drawn shape stands
      in for a real asset.
- [ ] Asset files are valid image files.
- [ ] Asset names and rendering modes match project conventions.
- [ ] Remote content uses the existing image-loading path.
