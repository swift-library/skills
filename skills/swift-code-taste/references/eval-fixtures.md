# Eval Fixtures

These fixtures protect Swift code-shape and comment-quality behavior. They are
durable inputs for skill evaluation, not review history.

## Accepted Feedback Produces A Canonical Implementation

Input: A Swift patch adds JSON and YAML export. Review feedback clarifies that
YAML was an unnecessary intermediate idea and the final API should export JSON.
Revise the code, tests, examples, and comments.

Expected behavior:

- Removes YAML types, cases, branches, configuration, tests, examples, and
  comments that no longer serve the current contract.
- Exposes a direct JSON export API with semantic names.
- Avoids names such as `JSONOnlyExporter` or comments such as "YAML was
  removed".
- Keeps a negative YAML invariant only when compatibility, safety, or an
  architectural boundary independently requires it.
- Uses comments only for non-obvious current semantics.

Forbidden behavior:

- Leaves dead YAML scaffolding behind a disabled flag.
- Adds a comment that retells the review conversation.
- Adds documentation to every obvious property or private helper merely to
  satisfy a comment quota.
- Removes still-required compatibility behavior without evidence that the
  contract ended.

Acceptance checks:

- A reader who has not seen the review understands the complete current API.
- Code and comments contain no rejected YAML vocabulary without a current
  semantic reason.
- Critical non-obvious fields and methods document their current contract.
