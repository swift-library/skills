# Non-Adoption Patterns

Read this file when a candidate looks plausible but dependency cost or boundary
fit may make adoption wrong.

Prefer Reference or Keep custom when:

- current code is simpler than the dependency
- package is toolchain-internal
- package is reference-only
- API is experimental or unstable
- platform or toolchain versions do not match
- package solves an adjacent but not identical problem
- migration would break public API
- dependency would leak into a core target boundary
- dependency weight is disproportionate
- official package should be used only as design reference

Do not frame non-adoption as failure. A Keep custom recommendation is valid
when it preserves a clearer dependency boundary.
