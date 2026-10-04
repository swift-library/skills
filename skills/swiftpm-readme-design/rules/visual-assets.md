# Visual Assets

Use this rule before adding, placing, or generating any image for a README,
organization page, or repository setting.

## Logo

- Use the logo the repository or organization already has. Do not draw,
  redesign, or recolor one as part of README work.
- Keep a vector master and a raster copy next to each other, for example
  `Documentation/Assets/Logo.svg` and `Logo.png` (1024 px square). The README
  references the SVG.
- Header width 160 px; organization profile 128 px; table rows 40 px.
- `alt` text is "<name> logo" in headers and empty (`alt=""`) in tables where
  the name sits next to it.
- A logo that carries its own background works in both themes as one SVG.
  A transparent logo with dark strokes needs either a light plate or a
  `<picture>` element with a `prefers-color-scheme: dark` source.

## Theme Check

Render every image on a white and on a dark (`#0d1117`) background before
use. Fix contrast or add a theme-specific variant; do not ship an image that
disappears in either theme.

## Terminal Demos

- The transcript must be real: run the commands and capture their output, or
  copy output that was produced by the exact version being documented.
- Edit only for privacy and length: replace home directories with `~`,
  drop machine names, and cut long output with an explicit `...` line.
- Lines beginning with `$ ` are commands; a trailing backslash continues the
  command on the next line.
- Render with `scripts/terminal_svg.py transcript.txt demo.svg --title name`.
- Keep the transcript next to the image so the demo can be regenerated when
  output changes.

## Licensing Limits

- Fonts: generated images convert text to outlines from a font whose license
  permits embedding and redistribution, such as fonts under the SIL Open Font
  License. Do not use Apple system fonts (SF Pro, SF Mono, New York) or other
  fonts whose license restricts use to a platform's own apps.
- Symbols: do not copy glyphs from SF Symbols or other symbol sets whose
  license restricts redistribution. Draw shapes as plain paths instead.
- Third-party marks: do not include, modify, or imitate another company's or
  project's logo (including the Swift bird and Apple logos) unless the owner
  has explicitly accepted that trademark's terms for this use. Colors and
  general styles are not marks and may be referenced.
- Record the font and its license next to any generator configuration that
  uses one.

## File Hygiene

- Optimize SVGs to plain paths and gradients; no embedded raster unless the
  image is a photograph or screenshot.
- Keep generated files deterministic so regeneration produces no diff when
  inputs are unchanged.
- Do not commit intermediate renders, contact sheets, or comparison images.
