# Swift Programming Language Baseline

This baseline contains repository-local Swift language and coding-pattern
review rules. It is not a complete Swift best-practices catalog.

## Assumptions

- This baseline strongly targets new Apple APIs.
- The baseline assumes iOS 26+ and Swift 6.2+.
- These assumptions must be checked against the local repository before
  applying rules.
- Do not force these assumptions onto a repository that does not declare them.

Repository-local truth wins over this skill.

## Core Baseline

- Prefer async/await APIs over closure-based variants when compatible.
- Avoid old GCD patterns such as `DispatchQueue.main.async()` when Swift
  concurrency is appropriate.
- Assume strict Swift concurrency only if the project does.
- Nontrivial concurrency diagnostics, Swift 6 migration, actor-isolation
  design, data-race work, `Sendable` fixes, and concurrency performance work are
  out of scope for this baseline.
- Do not introduce third-party frameworks without explicit approval.
- Avoid UIKit unless requested or justified.
- Avoid force unwraps and force `try` unless the failure is genuinely
  unrecoverable.
- Prefer static member lookup where it is clearer and compatible, such as
  `.circle` or `.borderedProminent`.
- Prefer user-visible error handling for user-triggered failures. Do not
  silently swallow errors or replace UI feedback with only `print(...)`.

## Observation Baseline

- Prefer `@Observable` for shared SwiftUI data when compatible.
- `@Observable` classes should be `@MainActor` unless the project uses Main
  Actor default isolation.
- Prefer `@State` for ownership and `@Bindable` / `@Environment` for passing
  observable data.
- Avoid `ObservableObject`, `@Published`, `@StateObject`, `@ObservedObject`,
  and `@EnvironmentObject` unless needed for legacy or integration contexts.

## Foundation Modernization Baseline

- Prefer Swift-native alternatives where they exist and are compatible.
- Prefer modern URL APIs such as `URL.documentsDirectory` and
  `appending(path:)` when available.
- Prefer `FormatStyle` APIs over legacy `Formatter` subclasses when
  compatible.
- For detailed user-visible formatting review, use
  `references/format-style.md`.
- Prefer localized text matching such as `localizedStandardContains()` for
  user-input filtering.
- Avoid C-style formatting for SwiftUI text.
- Prefer `Date.now` over `Date()` for current timestamps when compatible.
- Prefer `count(where:)` over `filter { ... }.count` when compatible.
- Prefer modern date parsing strategies such as `Date(_:strategy:)` for
  compatible input formats.
- Prefer `PersonNameComponents` and formatted person-name components over
  simple first-name / last-name string interpolation for user-visible names
  when the project needs locale-aware name display.

## SwiftUI Baseline

- Prefer `foregroundStyle()` over `foregroundColor()` when compatible.
- Prefer `clipShape(.rect(cornerRadius:))` over `cornerRadius()` when
  compatible.
- Prefer modern `Tab` APIs when compatible.
- Avoid outdated `onChange()` forms.
- Prefer `Button` over `onTapGesture()` unless tap location or tap count is
  required.
- Prefer `Task.sleep(for:)` over `Task.sleep(nanoseconds:)` when compatible.
- Avoid `UIScreen.main.bounds`.
- Split complex views into `View` structs rather than computed properties.
- Prefer Dynamic Type over forced font sizes.
- Prefer `NavigationStack` and `navigationDestination(for:)` over
  `NavigationView` when compatible.
- Include accessible labels for image-only buttons.
- Prefer `ImageRenderer` over `UIGraphicsImageRenderer` for SwiftUI rendering
  when compatible.
- Avoid unnecessary `AnyView`.
- Avoid UIKit colors in SwiftUI code.
- Avoid hard-coded spacing unless intentional.
- Prefer `bold()` over `fontWeight(.bold)` unless a specific weight is needed.
- Avoid `GeometryReader` when newer layout alternatives fit.
- Avoid converting `enumerated()` sequences to arrays solely for `ForEach`
  when a direct enumerated sequence is compatible.
- Prefer `.scrollIndicators(.hidden)` over legacy scroll indicator
  initializers when compatible.
- Prefer newer `ScrollView` positioning APIs when compatible.
- Keep view logic testable outside the view when practical.

## SwiftData CloudKit Baseline

If SwiftData is configured to use CloudKit:

- Do not use `@Attribute(.unique)`.
- Model properties must have default values or be optional.
- Relationships must be optional.

Do not expand this into general SwiftData schema design.

## Project Structure Baseline

- Use a consistent feature-oriented project structure.
- Follow the repository's existing naming conventions for types, properties,
  methods, and models when they are clear from docs or nearby code.
- If no clear local convention exists, prefer Apple / Swift API Design
  Guidelines for Swift naming style.
- For public or reusable API naming, argument labels, documentation comments,
  overloads, and fluent call-site design, use
  `references/api-design-guidelines.md`.
- Do not impose third-party style guides unless the repository already adopts
  them.
- If the repository explicitly adopts Google Swift style, use
  `references/google-swift-style.md` as an overlay for source structure,
  formatting, import layout, comments, access control, and stricter style
  conventions.
- Place different types in different Swift files.
- Write unit tests for core application logic.
- Write UI tests only when unit tests are not possible.
- Add comments and documentation comments where useful.
- Never commit secrets such as API keys.
- Never store sensitive values such as usernames, passwords, tokens, or API
  credentials in `@AppStorage`; use Keychain or the project's approved secure
  storage.

## Localization Baseline

- If the project uses `Localizable.xcstrings`, prefer string catalog entries
  for user-facing strings.
- Prefer symbol keys when generated symbols are available.
- Preserve the project's existing localization strategy.
- String Catalog setup or migration, XLIFF/xcloc exchange,
  pseudolocalization, localized package/framework resources, bundle lookup,
  RTL validation, and locale UI tests are out of scope for this baseline.

## Formatting And Linting Baseline

- Preserve the project's existing formatting style.
- If SwiftLint is installed or configured, keep it free of warnings and errors
  before committing.
- Do not use Google Swift style as a formatting requirement unless the project
  or user explicitly asks for it.

## Xcode MCP Baseline

- If Xcode MCP is configured, prefer it for Apple documentation lookup, builds,
  build logs, previews, navigator issues, snippets, and Xcode project file
  operations.
- Do not claim Xcode MCP is available unless the local environment or project
  configuration says so.
