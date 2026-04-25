# Testing And Auditing Accessibility

Use this file for Accessibility Inspector, manual testing, XCUITest
accessibility audits, P0/P1/P2 finding triage, and QA handoff.

## Audit Modes

Use blocker-only mode only when the user asks for quick, critical, or blocker
scope.

Use comprehensive mode by default when the user asks for an accessibility
audit. Comprehensive mode includes blockers, high-friction issues, incomplete
support, and testing gaps.

## Severity Triage

- P0: Blocks assistive technology users from completing a core task.
- P1: Significantly degrades discoverability, comprehension, or operation.
- P2: Improves consistency, polish, completeness, or Nutrition Label readiness
  without blocking the flow.

Each finding should include:

- what is wrong
- why it matters
- exact patch-ready fix
- manual verification step
- compatibility or regression risk when relevant

## Manual Testing

Manual testing is required for meaningful accessibility claims.

VoiceOver:

- Navigate the full flow in logical order.
- Confirm labels, values, traits, state, and grouping.
- Confirm focus after navigation, modals, validation errors, and dynamic
  updates.

Voice Control:

- Test "Show Names" and "Show Numbers".
- Activate controls using spoken labels.
- Check duplicate names and hidden actions.

Switch Control:

- Verify scanning order and action reachability.
- Confirm custom actions and modal dismissal.
- Watch for time-limited interactions.

Full Keyboard Access:

- Navigate with Tab / Shift-Tab and arrows.
- Confirm focus visibility and no traps.
- Dismiss modals and popovers with keyboard paths.

Dynamic Type and display:

- Test large accessibility text sizes.
- Check light/dark appearance and increased contrast.
- Check Reduce Motion, Differentiate Without Color, and Reduce Transparency
  when those settings affect the UI.

## Device vs Simulator

The simulator is useful for layout, Dynamic Type, and many inspector checks.
Use physical devices for final VoiceOver, Voice Control, Switch Control,
camera/media, haptics, audio, and hardware-input validation.

## Accessibility Inspector

Use Accessibility Inspector to inspect labels, traits, hierarchy, hit targets,
contrast, and notifications. Treat findings as evidence, not the whole audit.
Some real assistive technology behaviors only appear during manual use.

## XCUITest Accessibility Audits

When available for the platform target, `performAccessibilityAudit()` can catch
common issues such as missing labels, hit-region problems, contrast, and trait
problems.

Gate availability-sensitive audit APIs:

```swift
func testAccessibilityAudit() throws {
    let app = XCUIApplication()
    app.launch()

    if #available(iOS 17, macOS 14, tvOS 17, watchOS 10, *) {
        try app.performAccessibilityAudit()
    } else {
        XCTAssertTrue(app.buttons["Continue"].exists)
    }
}
```

Automated audits do not replace manual VoiceOver, Voice Control, Switch
Control, keyboard, media, or flow testing.

## Patch-Ready Audit Output

Use this shape:

```text
Phase / stage judgment
Accessibility surface inspected

Findings
- P0: ...
- P1: ...
- P2: ...

Patch-ready changes
...

Compatibility / availability impact
...

Validation performed or required
...

Risks
...

Next steps
...
```

## Review Anti-Patterns

- Reporting generic accessibility advice without tying it to a user impact.
- Adding labels everywhere instead of fixing semantics.
- Treating automated audits as proof of accessibility.
- Skipping manual verification for VoiceOver or Voice Control issues.
- Changing product copy or layout broadly when a localized semantic fix would
  solve the issue.
