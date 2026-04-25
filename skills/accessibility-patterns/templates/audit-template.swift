// AccessibilityAuditTests.swift
// XCUITest starter for automated accessibility audits.
//
// Usage:
// 1. Add this file to the UI test target.
// 2. Replace sample navigation with app-specific flows.
// 3. Keep manual accessibility testing; this catches common static issues only.

import XCTest

final class AccessibilityAuditTests: XCTestCase {
    private let app = XCUIApplication()

    override func setUpWithError() throws {
        continueAfterFailure = false
        app.launch()
    }

    func testLaunchScreenAccessibility() throws {
        try performAudit()
    }

    func testPrimaryFlowAccessibility() throws {
        try performAudit()

        // Example:
        // app.tabBars.buttons["Search"].tap()
        // try performAudit()
        //
        // app.tabBars.buttons["Settings"].tap()
        // try performAudit()
    }

    func testContrastAndLabels() throws {
        try performAudit([.contrast, .sufficientElementDescription])
    }

    func testHitRegionsAndDynamicType() throws {
        try performAudit([.hitRegion, .dynamicType, .textClipped])
    }

    func testAuditWithKnownIssueExclusions() throws {
        try performAudit(.all) { issue in
            // Example:
            // if issue.auditType == .contrast,
            //    issue.element?.identifier == "brandLogo" {
            //     return true
            // }
            return false
        }
    }

    private func performAudit(
        _ auditTypes: XCUIAccessibilityAuditType = .all
    ) throws {
        try requireAccessibilityAuditSupport()
        if #available(iOS 17, macOS 14, tvOS 17, watchOS 10, visionOS 1, *) {
            try app.performAccessibilityAudit(for: auditTypes)
        }
    }

    private func performAudit(
        _ auditTypes: XCUIAccessibilityAuditType = .all,
        issueHandler: @escaping (XCUIAccessibilityAuditIssue) throws -> Bool
    ) throws {
        try requireAccessibilityAuditSupport()
        if #available(iOS 17, macOS 14, tvOS 17, watchOS 10, visionOS 1, *) {
            try app.performAccessibilityAudit(
                for: auditTypes,
                issueHandler: issueHandler
            )
        }
    }

    private func requireAccessibilityAuditSupport() throws {
        guard #available(iOS 17, macOS 14, tvOS 17, watchOS 10, visionOS 1, *) else {
            throw XCTSkip(
                "performAccessibilityAudit() requires iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, or visionOS 1+."
            )
        }
    }
}
