# Anti-AI UI Guardrails

Use this reference when a SwiftUI screen feels generic, template-like,
over-decorated, visually vague, or "AI-generated". The goal is not novelty for
its own sake. The goal is a native Apple interface with a clear design
direction, source-backed brand choices, and enough craft that the screen feels
intentional.

## Design First Moves

Start from context before drawing or coding:

- Look for an existing design system, Figma file, app screenshots, shipped
  screens, asset catalog, color tokens, typography, or product docs.
- If the app has a brand, ask for brand files or inspect official sources
  before inventing a palette.
- If no design context exists, define a small working design spec before
  implementing screens: accent color, neutral palette, font roles, spacing
  scale, control style, and example usage.

When requirements are vague, do not present one "final" design. Offer two or
three directions that differ in philosophy, density, and visual language:

| Direction | Best For | Typical Choices |
|---|---|---|
| Information-first | Dashboards, finance, logs, admin tools | Dense hierarchy, restrained color, compact rows, charts or tables first. |
| Editorial | Reading, learning, lifestyle, reflective tools | Serif display, generous whitespace, strong text rhythm, fewer controls. |
| Expressive | Consumer products, launch moments, playful flows | Bolder accent, asymmetric composition, motion or one standout component. |
| Functional | Pro utilities, capture tools, repeat workflows | Compact controls, predictable lists, keyboard/pointer affordances. |
| Warm minimal | Personal apps, notes, wellness, creator tools | Warm neutrals, soft grouping, low visual noise, careful empty states. |

For each direction, name the palette, typography, density, and one signature
detail. After the user chooses, keep later screens inside that visual system.

## Banned Generic Patterns

Treat these as warning signs during review:

- Purple-to-blue gradient backgrounds without a brand reason.
- Emoji used as functional icons, tab icons, empty-state icons, or production
  symbols.
- Rounded white cards with a vertical colored stripe on the left.
- Centered "Welcome to App" hero sections over gradients that hide the real
  task or content.
- Inter, Roboto, or web-default display typography on Apple-platform app
  surfaces unless the product brand explicitly requires it.
- Neon green or cyan on near-black "cyber dashboard" styling for ordinary app
  UI.
- Symmetric three-column feature grids copied from SaaS landing pages.
- AI-drawn inline SVG illustrations, abstract people-at-work clip art, or CSS
  silhouettes.
- Default-blue buttons, links, toggles, and selection states everywhere.
- Padding, corner radii, or frame heights that look accidental rather than
  token-driven.

Prefer these replacements:

- Semantic Apple colors or a small project palette with one deliberate accent.
- SF Symbols or real icon assets with consistent weight and rendering mode.
- Real product content early in the screen; keep marketing copy compact.
- Clean placeholders when real photos, logos, or illustrations are unavailable.
- Native grouped backgrounds, system dividers, modest radii, and consistent
  internal padding.
- Asymmetric or content-driven layouts when the screen is promotional or
  discovery-oriented.

## Brand Asset Protocol

For branded work, gather evidence before inventing visual identity:

1. Ask for brand guidelines, logo files, palette, typography, and example
   screens.
2. If missing and the task allows web lookup, inspect official brand sources.
3. Prefer actual assets from the brand over generated approximations.
4. Verify important colors and font names before turning them into tokens.
5. Write or update a local design spec with colors, typography, spacing,
   logo-use notes, and dark-mode behavior.

If no brand exists, create a minimal working spec:

- One primary accent color and two accent support roles.
- A neutral light/dark palette.
- One display role and one body role, usually system-backed.
- A 4/8 point spacing scale.
- Modest corner-radius roles for buttons, cards, and sheets.

Do not let the brand protocol become decoration. Brand choices should clarify
hierarchy, reinforce recognition, or improve task confidence.

## Five-Part Review

Score each screen from 1 to 10 in five dimensions. Anything below 7 needs a
specific fix before calling the design polished.

| Dimension | Review Question | Failure Signals |
|---|---|---|
| Philosophy | Does the screen follow one coherent visual direction? | Trend mashup, contradictory fonts/icons/colors, no recognizable identity. |
| Hierarchy | Can the user immediately tell what matters? | Same-sized text everywhere, competing primary actions, weak grouping. |
| Craft | Are spacing, alignment, typography, color, and icon details intentional? | Random padding, inconsistent radii, orphaned text, mismatched icon weights. |
| Function | Does the layout serve the user's real task? | Hidden primary action, blank loading state, vague empty state, unclear form errors. |
| Originality | Does it avoid generic AI/template defaults? | Banned patterns, no product-specific detail, easy brand-name swap. |

Output the review as:

```text
SwiftUI Design Review

Direction:
- ...

Scores:
- Philosophy: ...
- Hierarchy: ...
- Craft: ...
- Function: ...
- Originality: ...

Fix First:
- ...

Keep:
- ...
```

## Craft Refinement Pass

Use this pass when a screen already has a direction but still feels thin,
generic, or assembled too quickly. Do not import static poster or canvas-art
workflows into app UI. Apply the useful constraint: refine what already exists
before adding more decoration.

- Improve composition before adding new elements: alignment, margins,
  typography, contrast, rhythm, and removal of stray details usually matter
  more than another background, badge, gradient, or illustration.
- Keep text as a contextual element. In visual-first or promotional app
  surfaces, use short labels, captions, and product copy that anchor the
  design; avoid explanatory paragraphs that compensate for weak layout.
- Add product-specific detail through real content, task state, data shape,
  imagery, icon choice, or interaction affordance. Do not paste in a literal
  motif just to prove originality.
- Make the final pass subtractive: check overlap, edge breathing room,
  inconsistent radii, mismatched icon weights, accidental colors, and weak
  empty/loading/error states.
- If the instinct is to add another decorative layer, first ask whether the
  existing hierarchy, spacing, or typography can carry the idea more cleanly.

## Code Shape Guidance

Keep code examples project-compatible rather than forcing a new helper layer:

- Use existing design tokens if the project has them.
- If the project does not have tokens, propose a tiny token enum or asset
  catalog mapping before scattering hex colors and magic numbers.
- Use `.font(.system(..., design: .serif))` for system serif roles instead of
  pretending New York is a custom bundled font.
- Prefer `Color(.systemBackground)` and project semantic colors over raw hex
  unless the brand spec requires exact values.
- Use `Label` and `Image(systemName:)` for ordinary icon rows and controls.
- Keep placeholder views clean, labeled when needed, and easy to replace with
  real assets.
- Do not add `Color(hex:)`, image caching, or animation helpers unless the
  target project needs them and owns the helper placement.

## Closeout Checklist

- The source design context or absence of context is named.
- The chosen direction is explicit.
- Banned generic patterns were checked.
- Brand choices are evidence-backed or labeled as a temporary working spec.
- Typography, color, spacing, and icon style are internally consistent.
- The primary task appears before decorative explanation.
- Empty, loading, and error states do not look unfinished.
- A refinement pass improved the existing composition before adding new
  decorative elements.
- Any code guidance fits the existing project architecture and token system.
