# Fetch Strategy

Use this to call Figma MCP tools without wasting context or fetching the wrong
node.

## URL Parsing

Accept:

- `figma.com/design/:fileKey/:fileName?node-id=...`
- `figma.com/file/:fileKey/:fileName?node-id=...`
- same URLs with `www.`, `m=dev`, `t`, `page-id`, or other query parameters

Rules:

- `fileKey` is the path segment after `/design/` or `/file/`.
- URL `node-id` uses hyphen form such as `3166-70147`; MCP tools usually expect
  colon form such as `3166:70147`.
- Ignore unrelated query parameters.
- Reject `/proto/` and `/board/` links and ask for a design node link.

## Call Order

Use this default order:

1. `get_metadata` if the node may be broad, ambiguous, or multi-screen.
2. `get_design_context` for exact target nodes.
3. `get_screenshot` for the same target nodes.
4. `get_variable_defs` once per file when tokens matter.
5. Asset node screenshots or provided asset URLs for visible assets.

If the server supports a prompt parameter, steer design context toward SwiftUI
or iOS, but treat returned code as design data rather than source code.

## Metadata-First Triggers

Run metadata before design context when:

- the link points to a root, page, flow, or large container
- the screenshot would contain multiple plausible screens
- the source document names more screens than the node clearly contains
- a prior design context fetch was truncated or timed out
- the same icon/component appears many times and can be deduplicated

## Circuit Breaker

If `get_design_context` times out or returns truncated output:

1. Do not retry the same broad node.
2. Fetch metadata for the parent.
3. Select smaller child frames or components.
4. Fetch each child independently.
5. Keep a short map of fetched node IDs so repeated work is avoided.

## Deduplication

- Fetch variables once per Figma file unless mode-specific tokens require more.
- Deduplicate repeated assets by node ID or localhost source.
- Export shared component assets once and reuse the same asset catalog entry.
- Keep source node IDs in scratch notes for traceability.

## Code Connect

If the MCP server exposes Code Connect mapping, check it before rebuilding a
component. When a mapped project component exists, inspect and reuse it rather
than creating a visually similar duplicate.
