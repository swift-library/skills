# Audit Workflow

Use this rule when auditing a target Swift package.

## Steps

1. Select the entry mode: automatic lightweight check or manual full index /
   discovery.
2. Inspect the target package source and existing dependencies.
3. Build a current capability inventory.
4. Identify custom implementations that may be wheels.
5. Select the candidate profile: official, SPI community, mixed, or local.
6. Map each wheel to library candidates using replacement patterns, fetched
   summaries/descriptions, and curated hint targets.
7. Check source authority, API fit, package role, license, maintenance, and
   dependency cost.
8. Classify each candidate as Adopt, Wrap, Reference, or Keep custom.
9. Identify migration seams and public API risks.
10. Produce a short library check note for automatic mode or a reviewable audit
    report for manual mode.

## Required Checks

- platform support
- Swift tools version
- API stability
- package maturity/status
- license and maintenance health for community candidates
- transitive dependency weight
- target/module boundary fit
- public API leakage
- normal dependency versus toolchain/internal/reference-only status
- whether the candidate has verified `Package.swift` and product/module facts

## Report Rule

Every candidate recommendation must include the current wheel, candidate
library, source category, authority, target evidence, source evidence, fit,
recommendation, reason, migration seam, risks, and suggested next step.
