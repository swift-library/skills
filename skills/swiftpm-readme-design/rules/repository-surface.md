# Repository Surface

Use this rule for GitHub settings and pages that frame the README: About,
topics, homepage, social preview, organization profile, and banner.

## About Description

- One sentence that says what the repository does, matching the README value
  sentence.
- Start with the capability, not with "A Swift package that". Name the
  repository type only when it is not obvious, such as a plugin or a tap.
- At most 350 characters (GitHub's limit); aim for under 120.
- No emoji, version numbers, or status words such as "WIP" or "new".
- Forks and adaptations say what they are in plain terms when that matters
  to users, without comparing quality.

Set it with `gh repo edit OWNER/REPO --description "..."`.

## Topics

- Lowercase letters, digits, and hyphens; at most 50 characters each; at most
  20 per repository.
- Start with the language and ecosystem (`swift`, `swift-package`,
  `swift-package-manager`, `swiftpm-plugin`), then the domain words a user
  would search for.
- Prefer established topic names over new spellings.
- Keep the family consistent across an organization's repositories.

Set them with `gh repo edit OWNER/REPO --add-topic a --add-topic b`; remove
stale ones with `--remove-topic`.

## Homepage

Set the homepage only to a page that exists and documents this repository,
such as hosted DocC. Leave it empty rather than pointing to an empty site or
a placeholder.

## Social Preview

- 1280x640 PNG, under 1 MB, as GitHub recommends.
- Content: the logo, the owner, the repository name, and the About sentence.
  Nothing else.
- Generate the SVG with `scripts/social_preview.py`, then convert to PNG at
  1280x640.
- GitHub has no API for this setting. Upload it in the repository's
  Settings > General > Social preview, or report the file for the owner to
  upload.

## Organization Profile

- Lives at `profile/README.md` in the organization's public `.github`
  repository. The `.github` repository's own root README describes that
  repository and does not appear on the organization page.
- Shape: logo, one-sentence identity, a short paragraph on how repositories
  relate, then grouped tables (for example packages, tools, templates) with a
  small logo, linked name, and the About sentence for each repository.
- Use absolute `raw.githubusercontent.com/OWNER/REPO/HEAD/...` URLs for other
  repositories' logos so the profile renders outside those repositories.
- List public repositories only. Regenerate the tables when a repository is
  added, renamed, archived, or its About changes.

## Banner

- A row of existing repository logos with no text, so it does not depend on
  fonts or need translation.
- Generate with `scripts/logo_row.py` in a stable order, such as by hue or by
  group, and regenerate when the set of repositories changes.

## Consistency Check

For each repository confirm:

- the About sentence equals the README value sentence;
- topics follow the family pattern;
- the homepage, if set, resolves;
- the social preview shows the current name and sentence;
- the repository appears in the organization profile when it is public.
