# Recommendation Taxonomy

Use this rule when assigning final candidate recommendations.

## Adopt

Use when the candidate library directly replaces custom implementation, the
dependency boundary is acceptable, and API/platform/toolchain fit is good.

## Wrap

Use when the candidate library should sit behind a local facade or adapter. This
is useful when public API or module boundaries must remain stable.

## Reference

Use when the package should not be added as a dependency, but should inform API
or architecture design. This is common for toolchain, internal, adjacent, or
reference-only packages.

## Keep Custom

Use when the current implementation remains justified because the candidate is
too heavy, stale, poorly licensed, unstable, mismatched, boundary-breaking, or simpler
than the dependency.

## Rule

The taxonomy answers one question: should the target package use a candidate
library instead of maintaining its own implementation? Do not assign Adopt or
Wrap from index presence alone; require target code evidence and verified
candidate source evidence.

## Dependency-Cost Checks

- platform support
- Swift tools version
- API stability
- package maturity/status
- license and maintenance health
- transitive dependency weight
- target/module boundary fit
- public API leakage
- normal dependency versus toolchain/internal/reference-only status
