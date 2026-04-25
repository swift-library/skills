# UIKit MVP

Use MVP when UIKit Views should be passive and presentation logic should be
tested without observing mutable state objects.

## Boundaries

- View: UIViewController or UIView conforming to a weak View protocol. It
  renders commands and forwards user events.
- Presenter: owns presentation logic, maps domain data to view data, handles
  async tasks, and calls View protocol methods.
- Services/repositories: injected through protocols.
- Router/Coordinator: owns navigation when needed.

## Presenter Rules

- Presenter holds `weak var view`.
- Presenter does not create live dependencies.
- Presenter does not import or manipulate UIKit controls except through the
  View protocol contract.
- Presenter cancels stale tasks and guards async responses when a newer request
  supersedes the old one.
- Presenter delegates navigation to a Router or Coordinator protocol.

## View Rules

- ViewController forwards actions to Presenter.
- ViewController renders ready-to-display view data.
- ViewController keeps table/collection configuration simple or delegates it to
  data source helpers.
- ViewController owns UIKit lifecycle details, not business rules.

## When To Prefer

- UIKit is primary and the team wants direct Presenter tests.
- Existing MVC controllers need low-risk extraction.
- The View should not own observable state.
- Feature is one screen or a small flow.

## Anti-Patterns

- Presenter holds View strongly.
- Presenter publishes state and the View observes it like MVVM.
- ViewController makes service/repository calls directly.
- Presenter owns routing implementation or creates view controllers.
- Presenter grows business logic that belongs in use cases or repositories.

## Testing

- Test Presenter with a mock View and stub repositories.
- Verify success, failure, cancellation, and stale-request behavior.
- Assert View protocol calls and navigation requests.

## PR Checklist

- [ ] View is passive and forwards events.
- [ ] Presenter owns presentation logic and maps view data.
- [ ] `view` is weak and protocol-typed.
- [ ] Dependencies are injected via protocols.
- [ ] Navigation is routed through a protocol or Coordinator.
- [ ] Presenter tests cover success, failure, and cancellation.
