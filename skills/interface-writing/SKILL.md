---
name: interface-writing
description: Use this skill to write, rewrite, review, improve, or harden text shown inside product interfaces, including UX writing, UI copy, interface text, microcopy, button labels, alerts, error messages, empty states, onboarding, settings text, tooltips, notifications, CLI output, accessibility labels, source strings, localization-risk notes, and terminology consistency. Trigger for design copy or implementation-side copy when wording may affect the experience, code strings, accessibility labels, or localization handoff. Do not use for marketing copy, blog posts, App Store listings, API docs, brand guides, resumes, or interview writing.
---

# Interface Writing

## Purpose

Guide writing and review for text that appears inside software interfaces.
Focus on clear product language, consistent terminology, voice/tone fit, and
copy that helps users understand what happened and what to do next.

When design-side UX writing already owns the wording, this skill checks
whether the same text survives implementation, source strings, accessibility
labels, localization risk, CLI output, and terminology drift.

## When To Use

- Writing new interface text for a screen, flow, component, CLI command, or
  notification.
- Reviewing or rewriting buttons, alerts, errors, empty states, onboarding,
  settings, tooltips, inline help, accessibility labels, or confirmation copy.
- Checking whether interface wording is clear, useful, consistent, and aligned
  with the product's voice.
- Checking implementation-side stability for interface text in source files,
  string catalogs, SwiftUI `Text`, CLI output, accessibility labels,
  placeholders, and localization handoff notes.
- Building or updating a terminology list for product UI strings.
- Handling broad requests such as "review the UX" when interface wording is
  part of the user experience.

## When Not To Use

- Do not use for visual design polish, layout, spacing, color, or component
  hierarchy unless the issue is specifically interface wording.
- Do not use for marketing pages, blog posts, App Store listings, press copy,
  resumes, interview answers, API documentation, or brand-guide creation.
- Do not use for accessibility implementation, such as VoiceOver behavior,
  assistive technology workflow, WCAG mapping, Accessibility Inspector, or
  Nutrition Labels.
- Do not use for Xcode String Catalogs, localization resource wiring,
  `String(localized:)`, `LocalizedStringResource`, package/framework bundles,
  translator export/import, pseudolocalization, or locale UI tests; localization
  implementation is out of scope.
- Do not rewrite product strategy, legal policy, or support commitments unless
  the user provides that source of truth.

## Inputs To Inspect

- Existing UI strings, screenshots, source files, string catalogs, CLI output,
  notification examples, or localization files.
- Local `AGENTS.md`, `README.md`, design docs, style guides, voice/tone notes,
  terminology lists, and product docs.
- The flow state: success, error, destructive action, empty state, onboarding,
  settings, notification, or command output.
- Audience, platform, language/localization constraints, and available space.

## Workflow

1. Find existing voice, tone, and terminology guidance. If none exists, infer
   from nearby product copy and state the assumption.
2. Classify the task: new copy, review, rewrite, terminology cleanup,
   implementation stability, localization-risk handoff, accessibility-label
   wording, or pattern-specific guidance.
3. Identify the interface pattern and read only the matching reference section.
4. Apply the precedence chain: clarity first, voice second, polish third.
5. Rewrite element by element. Prefer concrete nouns and specific actions.
6. Preserve product facts and user commitments. Do not invent capability,
   timing, policy, availability, or support promises.
7. Flag terminology drift, localization risks, accessibility-label wording
   risks, placeholder risks, and implementation handoff notes when repeated
   terms are inconsistent.

## Reference Files To Consult

- `references/_index.md`: routing index for writing references.
- `references/voice-and-tone.md`: product voice, tone shifts, terminology, and
  copy precedence.
- `references/interface-patterns.md`: alerts, errors, empty states,
  onboarding, notifications, buttons, settings, CLI output, and accessibility
  label copy.
- `references/apple-sources.md`: official Apple writing, accessibility-label,
  UX writing, and style-guide references for freshness checks.

## Decision Rules

- A user should understand the main point from headings and actions alone.
- Button labels should name the action, not just confirm intent.
- Error copy should say what happened and what the user can do next.
- Destructive copy should name the object and consequence.
- Empty states should explain what belongs there and how to make progress.
- Voice may add personality, but clarity wins when the user is blocked,
  confused, stressed, or making an irreversible choice.
- Keep copy localizable: avoid idioms, compact-but-dense phrasing, and strings
  that assume fixed word length.
- Treat accessibility labels as interface text. They should describe purpose
  or meaning, not visual implementation details.

## Validation Rules

- Read revised copy aloud for clarity and tone.
- Check labels and action text in context, not as isolated strings.
- Verify terminology against nearby UI and any word list.
- Check localization risk: expansion, plurality, placeholders, cultural
  idioms, and right-to-left layout assumptions.
- Check implementation risk: source string placement, CLI context,
  accessibility-label fit, and whether the actual code/resource change belongs
  to localization or accessibility implementation work.
- For critical flows, confirm the copy does not change product behavior,
  policy, privacy, billing, or legal meaning.

## Output Format

For reviews, return:

1. Phase / stage judgment
2. Interface surface inspected
3. Findings
4. Original to rewrite table
5. Rationale tied to clarity, voice, or pattern
6. Terminology notes
7. Risks / assumptions
8. Next steps

For direct writing tasks, return:

1. Proposed copy
2. Alternatives, when useful
3. Voice/tone rationale
4. Placement or implementation notes
5. Open assumptions

## Failure / Uncertainty Handling

- If voice is unclear, infer from local copy and state the assumption instead
  of blocking on a full brand exercise.
- If product facts are missing, use placeholders or ask for the missing fact;
  do not invent details.
- If copy depends on legal, privacy, medical, financial, or safety commitments,
  mark it as needing domain owner review.
