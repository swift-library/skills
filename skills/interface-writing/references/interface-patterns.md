# Interface Writing Patterns

Use this file for pattern-specific interface text guidance. Apply each pattern
through the product voice and the clarity-first rule in `voice-and-tone.md`.

When design-side UX writing shapes the product-facing copy, use this file to
check implementation-facing risks:
source string context, CLI context, localization expansion, placeholders,
accessibility-label wording, and terminology consistency.

## Alerts And Dialogs

Use alerts sparingly. They interrupt the user and should justify that
interruption.

Good alert copy answers:

- What happened?
- Why does it matter?
- What can the user do now?

Rules:

- Put the main point in the title.
- Keep body copy optional and short.
- Do not use the body to explain unclear buttons; fix the buttons.
- Use specific action labels.
- Avoid alerts for information that can live inline.

Example shape:

| Element | Better |
| --- | --- |
| Title | Can't Open "Report.pdf" |
| Body | Update the app to open this file format. |
| Actions | Update / Cancel |

## Error Messages

Errors should get the user unstuck.

Rules:

- Name the problem in plain language.
- Explain the cause only when it helps.
- Give the next step when one exists.
- Place field errors near the field.
- Avoid blame, vague error codes, and generic fallback text.

Prefer:

```text
Can't upload the file. Check your connection and try again.
```

Avoid:

```text
Something went wrong. Please try again.
```

Use technical details only when the audience can act on them.

## Destructive Actions

Destructive copy must make the object and consequence explicit.

Rules:

- Name the specific item or scope.
- State the irreversible or risky consequence.
- Label the destructive button with the destructive action.
- Provide a safe cancel path.
- Avoid double negatives.

Example shape:

```text
Delete "Vacation Photos"?
You'll lose all 847 photos in this album.

Delete Album / Keep Album
```

## Empty States

An empty state should explain what belongs there and how to make progress.

Rules:

- Say what is missing.
- Explain how content appears there.
- Add a primary action when useful.
- Use personality only when it matches the context.
- Avoid jokes or idioms in core flows.

Prefer:

```text
No Saved Episodes
Save episodes you want to listen to later, and they'll appear here.
```

## Onboarding And Setup

Onboarding should explain value and help the user start.

Rules:

- Give the whole flow and each screen one purpose.
- Lead with why the user benefits or why a permission is needed.
- Keep each screen focused on one idea.
- Use consistent progress actions such as Continue, Next, Done, or Get Started.
- Be honest about data, privacy, cost, and availability.

## Notifications

Notifications compete with the user's current context.

Rules:

- Lead with the useful information.
- Make the notification actionable or time-sensitive.
- Keep one idea per notification.
- Match urgency with tone.
- Avoid prompting app opens when the notification already contains the answer.

Prefer:

```text
Package arriving in 10 minutes
```

Avoid:

```text
Open the app for a delivery update
```

## Accessibility Labels

Accessibility labels are interface text. They should provide equivalent meaning
for users who do not see the visual UI.

Rules:

- Label meaningful images and unlabeled controls.
- Do not include the control type when the platform announces it.
- Describe intent or meaning, not just appearance.
- Update labels when state changes.
- Keep common controls short, but allow richer descriptions for expressive
  visual content when it improves equivalence.

Accessibility behavior, audits, inspector workflows, WCAG, and Nutrition Labels
are out of scope.

## Buttons And Actions

Buttons are high-value copy. Users often scan headings and actions first.

Rules:

- Use specific verbs.
- Make paired choices understandable independently.
- Avoid Yes, No, Submit, Confirm, and OK when a concrete action exists.
- Match the label to the surrounding instruction.
- Keep repeated action labels consistent across the product.

Prefer:

```text
Save Changes
Cancel Subscription
Add Payment Method
Keep Editing
```

## Instructional And Inline Copy

Inline copy should reduce uncertainty at the moment of action.

Rules:

- Put instructions where the user is acting.
- Lead with the benefit or reason when the request needs justification.
- Keep one instruction per location.
- Use examples for format-sensitive fields.
- Show validation feedback near the source of the problem.

## Settings And Preferences

Settings are utility surfaces.

Rules:

- Name settings plainly.
- Explain what the setting does when on.
- Avoid explaining the opposite state unless it is surprising.
- Link directly to related settings when possible.
- Keep descriptions short enough to scan.

## CLI Output

CLI text is interface writing.

Rules:

- Say what happened before showing what to do next.
- Use stable command names and flags.
- Make destructive prompts explicit.
- Keep success output short.
- Make errors actionable and include diagnostic details only when useful.

Prefer:

```text
No package index found. Run `pkgindex update` to create one.
```

Avoid:

```text
Error: missing data
```
