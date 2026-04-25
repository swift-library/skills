# UIKit MVC Migration

Use this for incremental cleanup of large UIViewControllers when a full
architecture migration is not yet justified.

## Extraction Order

1. Move networking, persistence, and parsing to services/repositories.
2. Move formatting and display mapping to view data builders or ViewModels.
3. Move validation and user-intent handling to a Presenter or ViewModel.
4. Move navigation to a Coordinator or Router when push/present calls are
   scattered.
5. Add tests around extracted collaborators before deeper migration.

## Controller Responsibility

ViewControllers should:

- Own view lifecycle and UIKit bindings.
- Render view data.
- Forward user events.
- Coordinate simple UIKit delegate/data-source glue.

They should not:

- Build live network or persistence clients.
- Own business rules.
- Parse transport DTOs into UI strings.
- Contain retry policies, caching, or complex branching state machines.

## Incremental Moves

- Extract table/collection data source objects when list configuration dominates
  the controller.
- Extract small services before introducing a full module pattern.
- Add a presenter or ViewModel only after there is real presentation logic to
  own.
- Add a coordinator only after navigation has more than one destination or flow
  state.

## Review Checklist

- [ ] Controller has a clear remaining UIKit responsibility.
- [ ] Side effects are behind injectable collaborators.
- [ ] Presentation mapping is testable outside UIKit.
- [ ] Navigation calls are either simple and local or moved to a router.
- [ ] Migration can proceed in small commits.
