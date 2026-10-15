# Eval Fixtures

## Runner-Specific XCTest Interoperability

Input: A package is migrating helpers between XCTest and Swift Testing. Its
strict-mode run passed, and the maintainer asks whether that proves all legacy
XCTest usage is gone. The compiler, runner, manifest and mode are supplied.

Expected behavior:

- Distinguishes the Corelibs scope of ST-0021 from Xcode's XCTest implementation.
- Checks the selected runner's support instead of inferring it solely from the
  compiler version or proposal status.
- Probes a failing XCTest assertion from Swift Testing and a failing Swift
  Testing expectation from XCTest under the intended interoperable mode.
- Verifies that both failures fail the test process, and checks misuse
  diagnostics and strict-mode failure separately.
- Reviews source for remaining XCTest calls; a successful strict run is not
  complete API-usage detection evidence.

Acceptance checks: use filtered failing-helper tests and inspect the actual
issues, process exit codes and mode. Keep intentionally failing probes separate
from the production suite. Report unsupported behavior or missing checks and
preserve safe native assertions until the chosen runner's failure propagation
is established.
