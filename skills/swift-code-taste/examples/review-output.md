# Swift Code Taste Review Output Sample

This composite sample combines several recurring findings in one review. Real
reviews should report only findings evidenced in the current patch. Use it as an
output-shape sample, not as a mandatory template.

## 1. Architecture Verdict

Soft fail.

The patch is moving in a useful direction, but it widens the requested scope and
adds ownership confusion around one semantic concept. The fix should be smaller:
keep the current round inside scope, preserve the real owner, and delete stale
surface instead of wrapping it.

## 2. Findings

### [Hard] Registry Becomes Runtime Truth

Evidence:

- `PageRegistry` is changed from an index of assembled pages into the place that
  registers and mutates page declarations.
- Row-authored declarations and construction-time assembly already define the
  page graph.

Why this is a smell:

- A registry can index or expose assembled truth, but it should not become the
  author of semantic truth. Moving graph mutation into the registry creates two
  owners: the DSL that declares pages and the registry that now rewrites them.

Expected shape:

- Keep declaration truth in the authored DSL and construction-time assembly.
- Let the registry consume assembled page data for identity, lookup, and host
  rendering support.

Minimal fix:

- Remove runtime registration side effects from the registry.
- If the assembly path is noisy, shrink the record shape rather than moving
  mutation to the registry.

### [Should] Weak Patch Lands Before Diagnosis

Evidence:

- A behavior patch changes scroll/render timing, but the visible delta is small
  and the root cause is still unclear.
- The review cannot explain why this change is the stable boundary.

Why this is a smell:

- Low-confidence behavior patches create stale paths and make later diagnosis
  harder. If the user cannot see a meaningful difference, the patch has not
  earned its place.

Expected shape:

- Start with evidence and root-cause ranking.
- Keep the patch only when it produces a clear behavioral improvement or
  isolates the failure mode.

Minimal fix:

- Roll the weak patch back.
- Add the narrowest probe or diagnosis note needed to decide the next change.

### [Should] Stale Public Surface Survives Final Naming

Evidence:

- The final semantic API is `enableBlockPipeline(_:)`.
- Older engine-selection names or forwarding aliases remain reachable.

Why this is a smell:

- Once the final public name is chosen, stale aliases keep old concepts alive.
  They increase the audit surface and invite callers to depend on dead naming.

Expected shape:

- Keep the final semantic command.
- Delete compatibility aliases unless compatibility is an explicit contract.

Minimal fix:

- Remove old public aliases and forwarding methods.
- Update internal call sites to the final name.

### [Should] Scope Gate Was Crossed

Evidence:

- The requested round was documentation-only and explicitly excluded Swift
  source, public API, and package graph changes.
- The patch also edits source files or `Package.swift`.

Why this is a smell:

- Crossing the user's scope gate hides design decisions inside a round that was
  supposed to establish current truth.

Expected shape:

- Keep the current patch inside the stated boundary.
- Record the implementation change separately if it still earns its place.

Minimal fix:

- Remove source, public API, and package graph edits from this round.

## 3. Public API Surface Impact

- Added public API: none expected for this round.
- Removed public API: stale aliases or forwarding surfaces should be removed
  only if the round allows source/API edits.
- Public API concerns: old names and compatibility shells should not survive
  after the final semantic surface is chosen.

## 4. Code Shape Impact

- Unnecessary wrappers: registry-as-writer introduces an avoidable ownership
  layer.
- Weak names: mechanism names need justification; the issue here is
  registry-as-writer, not the `Registry` suffix itself.
- Semantic duplication: the page graph has both an authored DSL owner and a
  runtime registry owner.
- Stale leftovers: old parser-switch names remain after the final API shape is
  chosen.
- AI-shaped smell: none evidenced in this composite sample; do not infer this
  smell without concrete scaffolding evidence.

## 5. Swift / Apple / Reference Project Alignment

- Relevant reference-project or platform semantic: in DSL-style Swift packages, authored
  structure should remain the source of truth; renderers and host projections
  should derive from that structure.
- Alignment concern: moving semantic ownership into registries, renderers, or
  host controllers makes the local API feel less Swift-like.
- Suggested correction: keep authored semantics near the model/DSL, and keep
  registries, renderers, and hosts as consumers or adapters.

## 6. Recommended Next Step

Merge after cleanup.

Block the ownership move and remove out-of-scope edits. If the behavior problem
still matters, do a diagnosis-first follow-up with evidence before landing a
replacement patch.

## 7. Code Diff (Key Hunks)

Not applicable in this scoped round.

The requested change is documentation-only, so do not include source or public
API hunks here. If the stale API surface still needs cleanup, propose it as a
separate source/API follow-up after the user widens scope.
