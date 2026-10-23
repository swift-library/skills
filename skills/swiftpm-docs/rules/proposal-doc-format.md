# Proposal Doc Format

Use this rule when writing or normalizing documents under `Documentation/Proposals/*`.

## Purpose

- Keep design-in-progress proposals concise, structured, and easy to review.
- Prepare change without treating the proposal as current architecture truth or
  an adopted decision record.

## Recommended Sections

- `# <title>`
- `Status`
- `Authors / Owners`
- `Summary`
- `Motivation`
- `Proposed Change`
- `Detailed Design`
- `Compatibility / Migration Impact`
- `Alternatives Considered`
- `Related Documentation`

## Format Expectations

- Keep the proposal focused on one change or one tightly related change set.
- Use the document to explain what is being proposed, why, and how.
- Keep current truth in `Documentation/Architecture/*`; update it with the
  implementation merge, not merely with acceptance.
- Record adopted rationale in `Documentation/Decisions/*` at acceptance.

## Entry, Acceptance, and Index

- Start a proposal when design choices need agreement before implementation.
  Set Status to `Proposed`; identify the author, affected owners, and the
  accepting authority assigned by repository governance under Authors / Owners.
  The author does not assume acceptance authority by writing the proposal.
- Keep `Documentation/Proposals/README.md` as an index of active proposals with
  title/link, owner, and review status. Add or update the entry with the proposal;
  keep open implementation work in its task or issue rather than in this index.
- Acceptance creates an `Accepted` Decision with the authority and date. Follow
  `proposal-vs-truth-vs-history.md` to split rationale from current-model docs
  and delete or archive the settled proposal. Remove its active index entry and
  repair inbound links in the same change.

## Does Not Replace Truth Or Decisions

- Do not treat a proposal as the current repository model.
- Do not use a proposal as the only record of an adopted decision.
- Do not leave architecture truth implied only through proposal text.

## Basis

This rule is inspired by
[Swift Evolution](https://github.com/swiftlang/swift-evolution), using its
proposal document shape as a lightweight basis only. It does not import the
Swift Evolution review process.
