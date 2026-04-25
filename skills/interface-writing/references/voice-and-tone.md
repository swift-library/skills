# Voice And Tone

Use this file when interface copy needs to match a product voice, when tone is
inconsistent across a flow, or when terminology is drifting.

## Voice

Voice is the product's stable way of speaking. It should be consistent across
screens, flows, notifications, CLI output, and accessibility text.

Look for an existing voice definition in:

- local `AGENTS.md`, `CLAUDE.md`, or equivalent project instructions
- design system docs
- product or support style guides
- string catalogs and nearby shipped UI copy
- terminology or word-list files

If no definition exists, infer a working voice from nearby copy. Use short
traits such as direct, calm, expert, warm, playful, restrained, precise, or
supportive. Avoid vague traits such as "clear" or "not confusing"; those are
baseline requirements.

## Tone

Tone is how the product adjusts the same voice for a specific moment.

- Errors, safety, billing, privacy, and destructive actions: turn up clarity,
  specificity, and calm. Turn down playfulness.
- Empty states and onboarding: allow more warmth, but keep purpose clear.
- Success and milestone moments: allow personality when it does not slow the
  user down.
- Settings and CLI output: prefer direct utility over personality.

## Precedence

Apply this order:

1. Clarity: Can the user understand what happened and what to do next?
2. Voice: Does it sound like this product?
3. Craft: Can it be shorter, more specific, or more consistent?

Never keep personality that makes a blocked, stressed, or confused user work
harder.

## Terminology

Use one term for one concept. Track repeated terms in a word list:

| Use | Avoid | Meaning |
| --- | --- | --- |
| workspace | project, space | Shared area where team content lives. |
| continue | next, proceed | Advance to the next step in a flow. |

Good word-list candidates:

- core product nouns
- repeated button labels
- plan, billing, permission, or account terms
- feature names
- states such as synced, paused, archived, failed, or pending

## Craft Rules

- Cut filler only when meaning and intentional tone survive.
- Avoid vague reassurance such as "Something went wrong" when the product can
  name the problem.
- Avoid "please" and "sorry" as reflexive padding in automated messages.
- Use sentence case unless the local product style says otherwise.
- Avoid idioms, jokes, and culturally specific phrasing in core flows.
- Keep templated strings natural for zero, one, many, short values, and long
  values.
- Write for localization: leave room for text expansion and right-to-left
  layouts.
