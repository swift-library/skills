# Topics and About

Use this rule to propose Swift ecosystem topics and a homepage candidate, and
to check an About sentence against the package. The presentation owner writes
the sentence, decides the final topic set, and applies all settings.

## About Claims

- Every capability the About sentence names exists in public source or is
  demonstrated by a verified README snippet.
- Platform, Swift version, or dependency claims equal the facts from
  `readme_facts.py`.
- Report a claim that the package does not support as a finding with its
  evidence; do not rewrite the sentence.

## Topics

- Lowercase letters, digits, and hyphens; at most 50 characters each; at most
  20 per repository.
- Lead with the ecosystem: `swift`, plus `swift-package`,
  `swift-package-manager`, or `swiftpm-plugin` as they apply to what the
  repository ships. Then add the domain words a user would search for.
- Prefer established topic names over new spellings, and the topic pattern
  the repository's family already uses.

## Homepage Candidate

Propose a homepage only when a page that documents this package exists and
resolves, such as hosted DocC. Otherwise propose none.
