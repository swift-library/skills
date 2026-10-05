# DocC Landing Identity

Use this rule when a Swift package's DocC landing page should carry the
package's icon and color, so hosted documentation identifies the package the
way framework documentation pages do.

## Principle

Each public module's landing page declares its identity in `@Metadata`:

```markdown
# ModuleName

@Metadata {
  @PageImage(purpose: icon, source: "modulename-icon", alt: "The ModuleName icon")
  @PageColor(blue)
}
```

- `@PageImage(purpose: icon)` replaces the generic page icon with the
  package's own icon.
- `@PageColor` tints the page introduction. It accepts only the named colors
  `blue`, `gray`, `green`, `orange`, `purple`, `red` and `yellow`.

## Resources

- Put the icon in the catalog: `Sources/<Target>/<Target>.docc/Resources/<target>-icon.png`,
  referenced by file name without extension.
- The icon is a PNG copy of the repository logo, at least 256 px. Add a
  `<target>-icon~dark.png` variant only when the logo needs one on dark
  backgrounds.
- The repository logo is the source. Never draw a separate documentation icon;
  when the logo changes, replace the catalog copy in the same change.

## Choosing The Color

- If the owning organization's design record maps icons to page colors, use
  that mapping and do not choose per package.
- Otherwise use the named color nearest the icon's dominant hue, or omit
  `@PageColor`. Never use `theme-settings.json` to approximate brand colors on
  individual packages unless the owner's design record defines one.

## Multi-Module Packages

- Every public module's landing page uses the package icon and color.
- When archives are combined with `docc merge`, the combined landing page uses
  the same metadata.

## Audit Checks

- `xcrun docc convert --warnings-as-errors` passes with the metadata in place.
- The converted landing page JSON
  (`data/documentation/<module>.json`) has `metadata.images` with an
  `icon` entry and, when a color is declared, `metadata.color`.
- The catalog icon matches the current repository logo.
