# Repository Overview
- Repository: `MiniLedger`
- Summary: `MiniLedger` is a Swift Package with 3 targets. Architecture summary is inferred from Package.swift, source layout, and naming signals.
- Architecture style: module-oriented Swift Package; executable + library target split
- Main modules/targets: `MiniLedgerCore`, `MiniLedgerCLI`, `MiniLedgerCoreTests`
- Uncertainty: architecture intent is inferred where docs do not state design decisions explicitly.

# Directory Tree
```text
├── Package.swift
├── README.md
├── Sources
│   ├── MiniLedgerCLI
│   │   └── main.swift
│   └── MiniLedgerCore
│       ├── LedgerStore.swift
│       ├── LedgerRepository.swift
│       └── Models
│           └── LedgerEntry.swift
└── Tests
    └── MiniLedgerCoreTests
        └── LedgerStoreTests.swift
```

# Module Summary
- `MiniLedgerCore` (target): Core ledger domain logic and persistence abstraction.
- `MiniLedgerCLI` (executableTarget): Composition entrypoint for command dispatch.
- `MiniLedgerCoreTests` (testTarget): Deterministic behavior checks for state transitions.

# Key Architectural Patterns
- State flow likely centers on `LedgerStore`.
- Data flow crosses `LedgerRepository` protocol and concrete adapter.
- Dependency injection/composition entrypoints start from `main.swift`.
- Persistence boundary likely present (`FileManager`).

# Key Abstractions
- Protocols: `LedgerRepository` (`Sources/MiniLedgerCore/LedgerRepository.swift`).
- Core models: `LedgerEntry` (`Sources/MiniLedgerCore/Models/LedgerEntry.swift`).
- State containers: `LedgerStore` (`Sources/MiniLedgerCore/LedgerStore.swift`).

# Important Files to Read First
1. `Package.swift` - target graph and dependency map.
2. `Sources/MiniLedgerCLI/main.swift` - composition root and runtime wiring.
3. `Sources/MiniLedgerCore/LedgerRepository.swift` - persistence boundary protocol.
4. `Sources/MiniLedgerCore/LedgerStore.swift` - core state transitions and domain rules.
5. `Sources/MiniLedgerCore/Models/LedgerEntry.swift` - central data model.

# Selected Source Files
## `Package.swift`
- file path: `Package.swift`
- why it matters: package manifest and module graph.

```swift
// full file contents...
```

## `Sources/MiniLedgerCLI/main.swift`
- file path: `Sources/MiniLedgerCLI/main.swift`
- why it matters: entrypoint or composition root.

```swift
// full file contents...
```

# Review Notes
- Review posture: static-scan cues for review focus, not a final architecture verdict.
- Strengths:
  - Clear protocol boundary for persistence.
  - Small target graph with understandable ownership.
- Risks:
  - CLI and domain wiring are tightly coupled in one entrypoint.
- Design tradeoffs:
  - Simpler wiring, but fewer extension points for alternate runtimes.
- Possible refactoring opportunities:
  - Add a lightweight dependency container to make adapters swappable.
