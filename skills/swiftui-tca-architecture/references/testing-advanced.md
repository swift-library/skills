# TCA Testing Advanced Patterns

Use this for larger test suites, state machines, edge cases, time control,
key-path receives, and exhaustivity decisions.

## Given When Then

Use scenario sections in long tests:

- given: initial state and dependency overrides,
- when: user/lifecycle action,
- then: state mutation, effect response, navigation, presentation, shared
  state, and dependency effects.

Keep the test executable as a user script. Do not over-document every line.

## State Machine Testing

For features with many modes:

- test legal transitions from each mode,
- test ignored actions in modes where they should do nothing,
- assert cancellation when leaving a mode,
- assert that impossible UI affordances cannot produce invalid state.

## Edge Cases

Cover empty data, duplicated IDs, permission denied, dependency failure, rapid
repeated actions, stale responses, cancellation, dismiss while loading, and
background/foreground lifecycle if those cases affect state.

## Time-Based Testing

- Inject a clock dependency.
- Use `TestClock` when you need to advance virtual time.
- Use an immediate clock only when timing itself is not behavior.
- Assert debounced actions only after advancing past the debounce interval.
- Assert cancellation by changing the input or sending the stop action before
  advancing time.
- Prefer `TestClock` for debouncing, timers, delayed effects, and animation
  timing where elapsed time is the behavior under test.
- Prefer an immediate clock when you only need async work to complete and no
  assertion depends on elapsed time.

## Key-Path Receives

Use key-path receive helpers when the action has large associated values or
when matching a specific case is clearer than constructing the full action.
Keep enough state assertion to prove the payload matters.

## Exhaustivity

Default to exhaustive tests for reducer behavior. Consider relaxed
exhaustivity only when:

- the test intentionally covers one branch of a noisy parent,
- the unasserted effects are already covered elsewhere,
- the local project has a convention for non-exhaustive integration tests.

Document why exhaustivity is relaxed. Do not use it to hide unknown effects.
- If relaxed exhaustivity is used, still assert the state fields that define
  the behavior under test. Non-exhaustive should reduce noise, not erase the
  feature contract.

## Complex Dependencies

For dependencies that call back or stream values, prefer explicit async streams
controlled by the test. Ensure the stream is finished or cancelled by the end
of the test.

For database/fetching dependencies that update over time, test the reducer
contract rather than the database library. Seed the dependency stream with
controlled values and assert the feature state after each emitted value.

## Review Checks

- Time tests sleep in real time.
- Non-exhaustive testing hides active effects.
- Edge cases are only covered in UI tests while reducer state machine is
  untested.
- Test setup is so broad that dependency calls are no longer visible.
