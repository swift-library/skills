# Visual Design Principles

## Core Philosophy

Use restraint over decoration. A polished SwiftUI app normally uses fewer
colors, fewer font sizes, fewer spacing values, and fewer words, but applies
them consistently. Native components, semantic colors, and system rhythm carry
more quality than custom gradients, decorative borders, and bespoke dividers.

Keep copy compact. Prefer one clear title and one useful supporting block over
repeating the same rationale in title, subtitle, body, and footer.

## Spacing

Use a small base-4/base-8 spacing scale:

```text
4, 8, 12, 16, 20, 24, 32, 40, 48
```

Common assignments:

- Outer content padding: 16-20 pt horizontal.
- Between major sections: 24-32 pt vertical.
- Within grouped components: 4-12 pt.
- Row/card internal padding: 12-16 pt vertical and 16 pt horizontal.

Avoid arbitrary near-values such as 14, 18, 26, 34, or 36 unless project-local
tokens already define them and they serve a real component need.

## Typography

Use hierarchy through role and weight, not size churn. A screen usually needs a
small set of text roles:

- Hero number or primary metric: large, visually light.
- Secondary stat: smaller but in the same family.
- Body/control label: standard body scale.
- Section label: small, often medium weight.
- Caption/subtitle: secondary, compact, and legible.

Pick one font design per product surface unless the project has a clear
typographic system. Do not mix `.monospaced`, `.rounded`, and default system
design casually across related app and extension surfaces.

Use tracking sparingly and mostly for uppercase labels. Two values is usually
enough. Years and other identifiers should avoid locale grouping when the text
is an identifier rather than a number:

```swift
Text(String(year))
Text(year, format: .number.grouping(.never))
```

## Color

Prefer semantic system colors and hierarchical foreground styles:

```swift
Color(.systemBackground)
Color(.secondarySystemBackground)
Color(.separator)
Color.primary
.foregroundStyle(.secondary)
.foregroundStyle(.tertiary)
```

Use manual opacity only for a few deliberate roles, such as subtle strokes or
separator emphasis. Many slightly different opacity values create inconsistency
and often fail in light mode, dark mode, or accessibility settings.

## Component Sizing

Components should be proportional to their role. Progress rings and circular
indicators should not dominate unless they are the primary screen purpose.
When a shape has background and foreground strokes, use matching line widths
unless the mismatch is a deliberate visual system rule.

Rows should rely on natural sizing plus padding. Avoid fixed oversized row
heights that make controls feel inflated or detached from the system.

## Grouped Content And Cards

Prefer native grouped styling:

```swift
VStack(spacing: 0) {
    row1
    Divider().padding(.leading, 16)
    row2
}
.background(Color(.secondarySystemBackground))
.clipShape(.rect(cornerRadius: 10))
```

Rules:

- Use modest corner radii for standard grouped content.
- Use system `Divider()` with inset padding instead of custom divider views.
- Keep internal padding around 12-16 pt vertical and 16 pt horizontal.
- Avoid custom gradients, decorative border overlays, and overly large rounded
  rectangles for ordinary cards.

## Navigation Chrome

Use platform navigation structure rather than manually placing title-like text
inside a bare background stack. Keep toolbar titles compact and subordinate to
content.

If a screen requires a custom header, make the safe-area contract explicit and
keep the header compact enough to feel like chrome rather than content.

## Controls

Use system controls with their labels and semantics intact:

- Use `Toggle(isOn:) { Text(...) }` instead of hiding the toggle label and
  building a manual row.
- Use `Label` for icon + text rows.
- Use one selected enum/value for mutually exclusive options instead of
  several independent booleans.
- Use `contentTransition(.numericText())` for changing numbers when the
  transition improves readability without adding visual noise.

Do not rely on low-contrast custom tints for control state. Keep interactive
controls at least 44x44 pt effective hit size on iOS.

## Pre-Ship Checklist

- [ ] Spacing values come from a small grid.
- [ ] Font sizes are limited and each role is clear.
- [ ] Font design is consistent across related surfaces.
- [ ] Colors are semantic or project-token based.
- [ ] Manual opacity values are limited and purposeful.
- [ ] Cards/groups use native backgrounds, modest radii, and system dividers.
- [ ] Controls preserve labels, semantics, and tap targets.
- [ ] Exclusive choices have one source of truth.
- [ ] Identifier text avoids unintended locale grouping.
- [ ] Text fits without relying on `minimumScaleFactor` as the primary fix.
