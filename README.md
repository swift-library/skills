# swift-skills

`swift-skills` is a collection of Codex / Claude skills for Swift package
repository work.

This README is both the collection manual and the documentation index. It
defines the collection scope, install/use surface, layout, and links to focused
docs.

The collection focuses on repository-native Swift workflows: documentation
architecture, package dependency judgment, SwiftPM architecture, concurrency,
testing, SwiftData, Core Data, CloudKit, Keychain, CryptoKit, Certificate
Trust, AuthenticationServices, Accessibility, Focus Engine, interface writing,
Figma-to-SwiftUI translation, SwiftUI, SwiftUI performance, SwiftUI design,
SwiftUI/UIKit architecture, WidgetKit implementation, WidgetKit design,
TipKit, RelevanceKit, Swift Charts, Xcode Instruments,
MetricKit, Xcode localization workflows, App Intents, ActivityKit, App Clips,
UserNotifications/APNs, StoreKit, WebKit, MapKit, PhotoKit, AVKit, MusicKit,
PDFKit, PaperKit, PencilKit, Contacts, EventKit, HealthKit, PassKit,
WeatherKit, FinanceKit, Foundation Models, Core ML, MLX Swift, Vision,
Natural Language, Translation, Speech, Foundation URLSession,
Network.framework, BackgroundTasks, DeviceCheck/App Attest, CryptoTokenKit,
AccessorySetupKit, Core Bluetooth, Core NFC, Core Motion, DockKit, SensorKit,
AudioAccessoryKit, HomeKit/MatterSupport, CallKit/PushKit, GroupActivities and
SharePlay, CarPlay, AppMigrationKit, AdAttributionKit, AlarmKit,
BrowserEngineKit, EnergyKit, PermissionKit, GameKit, SpriteKit, SceneKit,
TabletopKit, RealityKit/ARKit, SwiftLint, iOS Simulator, Apple-platform release
engineering, macOS SwiftPM app packaging, SwiftPM library distillation into
agent skill guidance, and broad Swift language / API baseline review.

## Skills

- `swiftpm-docs`: scaffold, audit, normalize, and export Swift package
  repository documentation structure.
- `swiftpm-index`: check custom Swift reusable infrastructure against official
  Apple / swiftlang library hints, with manual full-index, SPI, and local
  candidate discovery.
- `swiftpm-architecture`: design, review, and diagnose Swift Package target
  graphs, module boundaries, dependency direction, composition roots, and
  compact evidence briefs.
- `swiftpm-distiller`: distill SwiftPM package or Swift library source into
  agent-operational skill material and usage guidance.
- `swiftui-architecture`: choose, review, refactor, and scaffold SwiftUI app or
  feature architecture with MVVM, MVI, TCA, Clean Architecture adapters,
  navigation coordinators, dependency boundaries, async effects, and tests.
- `uikit-architecture`: choose, review, refactor, and scaffold UIKit feature or
  module architecture with MVC cleanup, MVP, MVVM, VIPER, Coordinator, Clean
  Architecture adapters, reactive pipelines, SwiftUI interop, and tests.
- `swift-concurrency-patterns`: diagnose Swift Concurrency issues and guide
  Swift 6 strict concurrency migration.
- `swift-testings-patterns`: write, review, migrate, and debug Swift tests with
  Swift Testing patterns.
- `swiftdata-patterns`: review, debug, migrate, and modernize SwiftData schema,
  context, query, CloudKit sync, migration, and concurrency patterns.
- `swift-programming-language`: review broad Swift language patterns, API
  design, FormatStyle modernization, Google Swift style references, and obvious
  modernization opportunities.
- `core-data-patterns`: review, debug, and modernize Core Data stack, context,
  fetch, migration, CloudKit sync, performance, and testing patterns.
- `cloudkit-patterns`: implement and review direct CloudKit and iCloud data
  workflows, including containers, databases, records, zones, queries,
  subscriptions, `CKSyncEngine`, sharing, assets, account state, errors,
  conflict resolution, dashboard work, and iCloud key-value/document
  coordination.
- `keychain-patterns`: review, implement, debug, and modernize Apple Keychain
  Services code, credential storage, access control, sharing, biometrics,
  migration from insecure stores, and tests.
- `cryptokit-patterns`: review, implement, debug, and modernize CryptoKit
  encryption, hashing, signing, HPKE, post-quantum APIs, Secure Enclave, and
  crypto tests.
- `certificate-trust-patterns`: review, implement, debug, and modernize
  `SecTrust`, certificate pinning, SPKI pins, client certificates, mTLS, and
  URLSession trust challenge handling.
- `authenticationservices-patterns`: implement and review
  AuthenticationServices flows, including Sign in with Apple, passkeys,
  password AutoFill, `ASWebAuthenticationSession`, credential state, callback
  handling, associated domains, presentation contexts, and account-security
  upgrades.
- `accessibility-patterns`: review, implement, audit, and modernize Apple
  platform accessibility for SwiftUI, UIKit, and AppKit, including VoiceOver,
  Dynamic Type, Voice Control, testing, and Nutrition Label recommendations.
- `focus-engine-patterns`: review, implement, debug, and modernize Apple
  platform focus management and focus movement across SwiftUI, UIKit, AppKit,
  RealityKit, tvOS, iOS/iPadOS, watchOS, visionOS, and macOS.
- `interface-writing`: write, rewrite, review, and improve product interface
  text for buttons, alerts, errors, empty states, onboarding, settings,
  notifications, CLI output, accessibility labels, and terminology
  consistency.
- `figma-swiftui`: translate Figma URLs, nodes, selections, screenshots,
  assets, design tokens, variants, and briefs into production SwiftUI with
  Asset Catalog handling, responsive layout, and visual fidelity.
- `swiftui-patterns`: review, implement, and refactor SwiftUI state, view
  structure, layout, navigation, basic accessibility modifier usage,
  animation, macOS scenes, MenuBarExtra utilities, and modern API patterns.
- `swiftui-performance`: guide, review, diagnose, and optimize SwiftUI
  source-level performance for slow rendering, janky scrolling, excessive
  updates, identity churn, heavy body work, image cost, and layout thrash
  before escalating to Instruments.
- `swiftui-design`: review and polish SwiftUI visual design, native Apple UI
  feel, spacing, typography, semantic color, grouped content, controls, and
  interactive editor surfaces.
- `widgetkit-patterns`: implement and review WidgetKit extension targets,
  widgets, bundles, static and App Intents configurations, timeline providers,
  entries, reload policies, WidgetCenter, interactive widgets, Control Center
  widgets, shared App Group data, deep links, previews, snapshots, and
  extension constraints.
- `widgetkit-design`: review and polish WidgetKit visual design, native widget
  layout, widget families, `Gauge`, widget backgrounds, dense rendering, and
  timeline freshness as it affects the visible widget.
- `tipkit-patterns`: implement and review TipKit feature-discovery flows,
  `Tips.configure`, `Tip` definitions, `TipView`, popovers, `TipGroup`, rules,
  parameters, events, display frequency, datastore, CloudKit tip sync, actions,
  invalidation, and testing helpers.
- `relevancekit-patterns`: implement and review RelevanceKit widget relevance,
  watchOS Smart Stack surfacing, `RelevantContext`, relevance donation,
  time/location/fitness/sleep/hardware clues, grouping, permission boundaries,
  testing, and unsupported-platform fallback behavior.
- `swift-charts-patterns`: review, refactor, and implement Swift Charts marks,
  axes, selection, Chart3D, and chart accessibility patterns.
- `xcode-instruments`: record and analyze Xcode Instruments traces
  with `xctrace`, Time Profiler, hangs, hitches, logs, and signposts.
- `metrickit-patterns`: implement and review MetricKit runtime telemetry,
  `MXMetricManager` subscribers, metric and diagnostic payloads, call-stack
  trees, custom signpost metrics, JSON export, payload persistence, backend
  upload, Organizer correlation, privacy redaction, and delayed telemetry
  expectations.
- `xcode-localization-patterns`: implement and review Xcode String Catalogs,
  localized resources, Swift localization APIs, SwiftUI text localization,
  translator exchange, pseudolocalization, and locale tests.
- `app-intents-patterns`: implement and review App Intents actions, entities,
  shortcuts, Siri, Spotlight, widgets, controls, Focus, and related system
  integrations.
- `activitykit-patterns`: implement and review Live Activities, Dynamic Island,
  ActivityKit lifecycle, WidgetKit Live Activity UI, and ActivityKit push
  updates.
- `app-clips-patterns`: implement and review App Clip targets, invocation URLs,
  associated domains, shared code, local testing, and full-app handoff.
- `user-notifications-patterns`: implement and review UserNotifications/APNs,
  local and remote notifications, authorization, payloads, notification
  extensions, and delivery debugging.
- `storekit-patterns`: implement and review StoreKit product loading,
  purchases, subscriptions, transaction verification, entitlements, StoreKit
  views, testing, and server validation.
- `webkit-patterns`: implement and review embedded WebKit surfaces, SwiftUI
  `WebView`/`WebPage`, `WKWebView`, navigation policy, JavaScript, local
  content, and custom schemes.
- `mapkit-patterns`: implement and review MapKit views, annotations, overlays,
  camera state, search, directions, Look Around, Core Location-backed map
  behavior, and map testing.
- `photokit-patterns`: implement and review Photos/PhotosUI picking, PhotoKit
  library access, selected-media loading, camera capture tied to photo
  workflows, and photo-grid memory behavior.
- `avkit-patterns`: implement and review AVKit playback, `AVPlayer`,
  `AVPlayerViewController`, SwiftUI `VideoPlayer`, Picture in Picture, AirPlay,
  subtitles, and playback lifecycle debugging.
- `musickit-patterns`: implement and review MusicKit authorization, Apple Music
  catalog/library access, subscription state, music players, queues,
  MediaPlayer, Now Playing, and background audio.
- `pdfkit-patterns`: implement and review PDFKit display, navigation, search,
  annotations, forms, page manipulation, rendering, printing, and SwiftUI PDF
  wrappers.
- `paperkit-patterns`: implement and review PaperKit structured markup,
  `PaperMarkupViewController`, `PaperMarkup`, PencilKit coexistence,
  persistence, rendering, and compatibility checks.
- `pencilkit-patterns`: implement and review PencilKit freeform drawing,
  `PKCanvasView`, `PKDrawing`, `PKToolPicker`, Apple Pencil interactions,
  drawing persistence, export, and SwiftUI wrappers.
- `contacts-patterns`: implement and review Contacts and ContactsUI access,
  limited contact access, contact pickers, contact mutation, vCards, groups,
  and change history.
- `eventkit-patterns`: implement and review EventKit and EventKitUI calendar
  and reminder access, full versus write-only calendar access, CRUD,
  recurrence, alarms, and editor wrappers.
- `healthkit-patterns`: implement and review HealthKit authorization, health
  queries, samples, background delivery, workouts, units, and health-data
  privacy.
- `passkit-patterns`: implement and review PassKit Apple Pay, Wallet passes,
  `PKPaymentRequest`, payment authorization, merchant/pass entitlements, and
  pass-library behavior.
- `weatherkit-patterns`: implement and review WeatherKit forecasts, alerts,
  availability, attribution, weather caching, location-backed data, and weather
  dashboard validation.
- `financekit-patterns`: implement and review FinanceKit availability, managed
  entitlement gating, authorization, accounts, balances, transactions, history
  tokens, Wallet orders, background delivery, and financial-data privacy.
- `foundation-models-patterns`: implement and review Apple Foundation Models
  availability, `SystemLanguageModel`, `LanguageModelSession`, prompts,
  transcripts, structured output, `@Generable`, `@Guide`, streaming, tool
  calling, adapters, guardrails, and on-device generative fallback decisions.
- `core-ml-patterns`: implement and review Core ML model loading,
  configuration, prediction, deployment, profiling, `MLTensor`, `MLMultiArray`,
  `VNCoreMLModel` integration, and model performance.
- `mlx-swift-patterns`: implement and review MLX Swift package setup, MLX
  arrays, MLXNN, MLXOptimizers, MLXRandom, Apple silicon/Metal build
  constraints, model examples, memory pressure, and backend selection.
- `vision-patterns`: implement and review Vision and VisionKit OCR, barcode
  recognition, face detection, image classification, segmentation, tracking,
  coordinate conversion, `DataScannerViewController`, document camera, and
  SwiftUI wrappers.
- `natural-language-patterns`: implement and review Natural Language and
  Translation tokenization, language recognition, tagging, embeddings,
  `NLModel`, `TranslationSession`, language availability, batch translation,
  and deterministic text-analysis pipelines.
- `speech-patterns`: implement and review Speech framework authorization,
  microphone/audio pipeline setup, `SpeechAnalyzer`, `SpeechTranscriber`,
  `SFSpeechRecognizer`, live/file transcription, on-device/server recognition,
  cancellation, and cleanup.
- `foundation-urlsession-patterns`: implement and review Foundation URL loading,
  `URLSession`, HTTP API clients, transfers, request/response validation,
  background transfer handoff, `URLProtocol` mocks, SSE, WebSocket tasks, and
  ATS.
- `network-framework-patterns`: implement and review Network.framework
  transports, `NWConnection`, `NWListener`, `NWBrowser`, `NWPathMonitor`,
  protocol options, Bonjour, local network privacy, and receive loops.
- `background-tasks-patterns`: implement and review BackgroundTasks
  scheduling, task registration, permitted identifiers, expiration handlers,
  completion, checkpointing, background URLSession handoff, and debug launch.
- `devicecheck-patterns`: implement and review DeviceCheck and App Attest
  tokens, app/device attestation, assertions, server verification, rollout,
  retry, and graceful unsupported states.
- `cryptotokenkit-patterns`: implement and review CryptoTokenKit tokens, smart
  cards, token drivers, sessions, keychain exposure, PIN state, APDU exchange,
  and managed smart card authentication.
- `accessorysetupkit-patterns`: implement and review AccessorySetupKit picker
  discovery, Bluetooth/Wi-Fi accessory setup, session events, authorization,
  rename/remove flows, and runtime handoff.
- `core-bluetooth-patterns`: implement and review Core Bluetooth central and
  peripheral roles, BLE scanning, GATT discovery, read/write/notify flows,
  advertising, background modes, and state restoration.
- `core-nfc-patterns`: implement and review Core NFC NDEF and tag-reader
  sessions, NFC entitlements, ISO 7816/15693, FeliCa, MIFARE, background tag
  reading, session invalidation, and physical tag tests.
- `core-motion-patterns`: implement and review Core Motion device motion,
  raw sensors, pedometer, activity, altimeter, headphone motion, water
  submersion, sampling, battery, and privacy behavior.
- `dockkit-patterns`: implement and review DockKit accessory observation,
  system/custom tracking, motorized stand control, camera coordination,
  subject/object tracking, and physical dock validation.
- `sensorkit-patterns`: implement and review SensorKit entitlement-gated
  research data access, authorization, sample fetches, deletion records, and
  high-sensitivity sensor-derived metrics.
- `audioaccessorykit-patterns`: implement and review AudioAccessoryKit
  accessory capabilities, placement state, automatic audio switching,
  AccessorySetupKit pairing handoff, distribution constraints, and physical
  accessory validation.
- `homekit-patterns`: implement and review HomeKit and MatterSupport smart-home
  features, `HMHomeManager`, homes, rooms, accessories, services,
  characteristics, action sets, triggers, Matter commissioning, and HomeKit
  Accessory Simulator validation.
- `callkit-patterns`: implement and review CallKit and PushKit VoIP flows,
  `CXProvider`, `CXCallController`, `CXCallUpdate`, call actions, provider
  delegates, audio-session coordination, and Call Directory extensions.
- `group-activities-patterns`: implement and review GroupActivities and
  SharePlay sessions, `GroupActivity`, `GroupSession`,
  `GroupSessionMessenger`, synchronized playback, participant state,
  sharing UI, and `GroupSessionJournal`.
- `carplay-patterns`: implement and review CarPlay entitlements, scene setup,
  `CPTemplateApplicationScene`, `CPInterfaceController`, templates, dashboard
  and instrument-cluster surfaces, and CarPlay Simulator validation.
- `appmigrationkit-patterns`: implement and review AppMigrationKit migration
  extensions, source/destination apps, resource export/import,
  `MigrationStatus`, progress, App Group recovery, and first-launch import UX.
- `adattributionkit-patterns`: implement and review AdAttributionKit
  publisher/advertised app setup, ad identifiers, `UIEventAttributionView`,
  JWS impressions, StoreKit-rendered ads, postbacks, conversion values, tags,
  and re-engagement.
- `alarmkit-patterns`: implement and review AlarmKit authorization,
  `AlarmManager`, alarm/timer scheduling, `Alarm.Schedule`, alarm state
  observation, `AlarmAttributes`, presentation, buttons, and widget extension
  wiring.
- `browserenginekit-patterns`: implement and review BrowserEngineKit
  alternative browser engine apps, host and extension targets, XPC,
  sandboxing, JIT, rendering, text input, downloads, and process lifecycle.
- `energykit-patterns`: implement and review EnergyKit electricity guidance,
  venues, EV/HVAC load event sessions, suggested actions, guidance tokens,
  unsupported regions, dashboards, and insights.
- `permissionkit-patterns`: implement and review PermissionKit child
  communication experiences, communication limits, handles, `AskCenter`,
  `PermissionButton`, topics, choices, responses, and family account behavior.
- `gamekit-patterns`: implement and review GameKit and Game Center services,
  `GKLocalPlayer`, access point/dashboard UI, leaderboards, achievements,
  real-time multiplayer, turn-based matches, saved games, friends, challenges,
  and server identity verification.
- `spritekit-patterns`: implement and review SpriteKit 2D scenes,
  `SKScene`, `SKView`, `SpriteView`, nodes, actions, physics, contacts, camera,
  particles, tile maps, shaders, SwiftUI presentation, and performance.
- `scenekit-patterns`: implement and review SceneKit 3D scene graphs,
  `SCNView`, `SceneView`, `SCNScene`, `SCNNode`, geometry, materials, lighting,
  cameras, animation, physics, shaders, hit testing, and migration-sensitive
  maintenance.
- `tabletopkit-patterns`: implement and review TabletopKit visionOS tabletop
  games, `TabletopGame`, table setup, equipment, seats, actions, turns,
  bookmarks, score counters, interactions, RealityKit rendering, and group
  synchronization.
- `realitykit-patterns`: implement and review RealityKit and ARKit spatial
  scenes, `RealityView`, `ARView`, entities, components, systems, anchors,
  assets, materials, physics, gestures, raycasting, AR sessions, and spatial
  performance.
- `swiftlint-patterns`: implement and review SwiftLint setup,
  `.swiftlint.yml`, rule governance, suppressions, baselines, plugins, run
  scripts, CI/pre-commit wiring, analyzer rules, reporters, custom rules,
  autocorrection, and rollout strategy.
- `ios-simulator`: operate iOS Simulator devices, run simulator
  build/test helpers, capture screenshots/logs, manage app lifecycle,
  permissions, push notifications, status bar overrides, and optional IDB
  semantic UI actions.
- `apple-platform-release`: prepare Apple-platform signing assets, Xcode
  archive/export, IPA/PKG artifacts, Developer ID notarization, stapling,
  Gatekeeper verification, and upload-ready release handoffs.
- `swiftpm-macos-app-packaging`: package SwiftPM-only macOS executables into
  local or distributable `.app` bundles with Info.plist, resources, framework
  embedding, universal builds, entitlements, signing, notarization, zip, and
  optional Sparkle appcast support.

## Framework Coverage Matrix

This matrix combines the local skill routing surface with Apple documentation
areas. Each Apple framework/API row shows the local skill owner when one
exists. `Covered` means a dedicated local skill owns implementation or review;
`Adjacent` means common task slices route locally but there is no dedicated
framework skill; `Candidate` means the entry is tracked without a local skill.

Use current Apple documentation before making version-specific claims or
promoting a candidate into a new skill.

Checked against [Apple Developer Documentation technologies](https://developer.apple.com/documentation/technologies)
on 2026-05-01.

### App Frameworks

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `Accessibility` | `accessibility-patterns` | Covered |
| `Accessory Notifications` | `user-notifications-patterns`, `accessorysetupkit-patterns` | Adjacent |
| `Accessory Live Activities` | `activitykit-patterns`, `audioaccessorykit-patterns` | Adjacent |
| `Account Data Transfer` | `appmigrationkit-patterns` | Adjacent |
| `ActivityKit` | `activitykit-patterns` | Covered |
| `AlarmKit` | `alarmkit-patterns` | Covered |
| `App Clips` | `app-clips-patterns` | Covered |
| `App Data Transfer` | `appmigrationkit-patterns` | Adjacent |
| `AppKit` | `swiftui-patterns`, `accessibility-patterns` | Adjacent |
| `App License Delivery SDK` | none | Candidate |
| `Automatic Sign-In API` | `authenticationservices-patterns` | Adjacent |
| `Bundle Resources` | none | Candidate |
| `Core Foundation` | `swift-programming-language`, `foundation-urlsession-patterns` | Adjacent |
| `Declared Age Range` | none | Candidate |
| `Distributed` | `swift-programming-language`, `swift-concurrency-patterns` | Adjacent |
| `EnergyKit` | `energykit-patterns` | Covered |
| `Foundation` | `swift-programming-language`, `foundation-urlsession-patterns`, `xcode-localization-patterns` | Adjacent |
| `Foundation Models` | `foundation-models-patterns` | Covered |
| `GeoToolbox` | none | Candidate |
| `hvf` | none | Candidate |
| `Mac Catalyst` | `uikit-architecture`, `swiftui-patterns` | Adjacent |
| `ManagedApp` | none | Candidate |
| `Objective-C Runtime` | none | Candidate |
| `Observation` | `swiftui-patterns`, `swift-programming-language` | Adjacent |
| `PaperKit` | `paperkit-patterns` | Covered |
| `PermissionKit` | `permissionkit-patterns` | Covered |
| `RegexBuilder` | `swift-programming-language` | Adjacent |
| `RelevanceKit` | `relevancekit-patterns` | Covered |
| `Swift` | `swift-programming-language` | Covered |
| `SwiftData` | `swiftdata-patterns` | Covered |
| `SwiftUI` | `swiftui-patterns`, `swiftui-architecture`, `swiftui-performance`, `swiftui-design` | Covered |
| `Symbols` | `swiftui-design` | Adjacent |
| `TranslationUIProvider` | `natural-language-patterns` | Adjacent |
| `TVML` | none | Candidate |
| `TVMLKit JS` | none | Candidate |
| `TVMLKit` | none | Candidate |
| `TVUIKit` | none | Candidate |
| `UIKit` | `uikit-architecture` | Covered |
| `visionOS` | `realitykit-patterns`, `swiftui-patterns` | Adjacent |
| `Visual Intelligence` | `vision-patterns`, `foundation-models-patterns` | Adjacent |
| `WatchKit` | `widgetkit-patterns`, `relevancekit-patterns`, `swiftui-patterns` | Adjacent |
| `watchOS apps` | `widgetkit-patterns`, `relevancekit-patterns`, `swiftui-patterns` | Adjacent |
| `Wi-Fi Aware` | none | Candidate |

### App Services

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `Accounts` | none | Candidate |
| `AdAttributionKit` | `adattributionkit-patterns` | Covered |
| `Address Book` | none | Candidate |
| `Address Book UI` | none | Candidate |
| `AdServices` | `adattributionkit-patterns` | Adjacent |
| `AdSupport` | `adattributionkit-patterns` | Adjacent |
| `Advanced Commerce API` | `storekit-patterns` | Adjacent |
| `Apple Maps Server API` | `mapkit-patterns` | Adjacent |
| `Apple Pencil` | `pencilkit-patterns` | Adjacent |
| `Application Services` | none | Candidate |
| `App Intents` | `app-intents-patterns` | Covered |
| `AppMigrationKit` | `appmigrationkit-patterns` | Covered |
| `App Store Receipts` | `storekit-patterns` | Adjacent |
| `App Store Server API` | `storekit-patterns` | Adjacent |
| `App Store Server Notifications` | `storekit-patterns` | Adjacent |
| `Assignables` | none | Candidate |
| `AudioAccessoryKit` | `audioaccessorykit-patterns` | Covered |
| `Automatic Assessment Configuration` | none | Candidate |
| `Automated Device Enrollment` | none | Candidate |
| `Background Tasks` | `background-tasks-patterns` | Covered |
| `Background Assets` | none | Candidate |
| `BrowserKit` | `browserenginekit-patterns`, `webkit-patterns` | Adjacent |
| `CallKit` | `callkit-patterns` | Covered |
| `CareKit` | `healthkit-patterns` | Adjacent |
| `CarPlay` | `carplay-patterns` | Covered |
| `CarKey` | `passkit-patterns` | Adjacent |
| `Swift Charts` | `swift-charts-patterns` | Covered |
| `ClassKit` | none | Candidate |
| `ClassKit Catalog API` | none | Candidate |
| `ClassKit UI` | none | Candidate |
| `ClockKit` | `widgetkit-patterns`, `relevancekit-patterns` | Adjacent |
| `CloudKit` | `cloudkit-patterns` | Covered |
| `Combine` | `swift-concurrency-patterns`, `swift-programming-language` | Adjacent |
| `Contacts` | `contacts-patterns` | Covered |
| `ContactProvider` | `contacts-patterns` | Adjacent |
| `Contacts UI` | `contacts-patterns` | Covered |
| `Core Data` | `core-data-patterns` | Covered |
| `Core Location` | `mapkit-patterns`, `weatherkit-patterns` | Adjacent |
| `Core Location UI` | `mapkit-patterns` | Adjacent |
| `Core ML` | `core-ml-patterns` | Covered |
| `Core Motion` | `core-motion-patterns` | Covered |
| `Core Spotlight` | `app-intents-patterns` | Adjacent |
| `Core Text` | `interface-writing`, `swift-programming-language` | Adjacent |
| `Core Transferable` | `swiftui-patterns`, `app-intents-patterns` | Adjacent |
| `Create ML` | `core-ml-patterns` | Adjacent |
| `Create ML Components` | `core-ml-patterns` | Adjacent |
| `DataDetection` | `natural-language-patterns`, `vision-patterns` | Adjacent |
| `Device Activity` | `permissionkit-patterns` | Adjacent |
| `DeviceCheck` | `devicecheck-patterns` | Covered |
| `DockKit` | `dockkit-patterns` | Covered |
| `EventKit` | `eventkit-patterns` | Covered |
| `EventKit UI` | `eventkit-patterns` | Covered |
| `ExtensionFoundation` | `app-intents-patterns`, `apple-platform-release` | Adjacent |
| `ExtensionKit` | `app-intents-patterns`, `apple-platform-release` | Adjacent |
| `External Purchase Server API` | `storekit-patterns` | Adjacent |
| `Family Controls` | `permissionkit-patterns` | Adjacent |
| `File Provider` | none | Candidate |
| `File Provider UI` | none | Candidate |
| `FinanceKit` | `financekit-patterns` | Covered |
| `FinanceKitUI` | `financekit-patterns` | Adjacent |
| `HealthKit` | `healthkit-patterns` | Covered |
| `HomeKit` | `homekit-patterns` | Covered |
| `iAd` | none | Candidate |
| `IdentityDocumentServices` | none | Candidate |
| `IdentityDocumentServicesUI` | none | Candidate |
| `iWork Document Exporting API` | none | Candidate |
| `JavaScriptCore` | `webkit-patterns` | Adjacent |
| `Journaling Suggestions` | none | Candidate |
| `LiveCommunicationKit` | `callkit-patterns` | Adjacent |
| `MailKit` | none | Candidate |
| `Managed Settings` | `permissionkit-patterns` | Adjacent |
| `Managed App Distribution` | none | Candidate |
| `Managed Settings UI` | `permissionkit-patterns` | Adjacent |
| `MapKit` | `mapkit-patterns` | Covered |
| `MarketplaceKit` | none | Candidate |
| `Matter` | `homekit-patterns` | Adjacent |
| `MatterSupport` | `homekit-patterns` | Covered |
| `Messages` | none | Candidate |
| `Message UI` | none | Candidate |
| `Multipeer Connectivity` | `network-framework-patterns` | Adjacent |
| `Natural Language` | `natural-language-patterns` | Covered |
| `Notification Center` | `user-notifications-patterns` | Adjacent |
| `PassKit (Apple Pay and Wallet)` | `passkit-patterns` | Covered |
| `Preference Panes` | none | Candidate |
| `ProximityReader` | `passkit-patterns` | Adjacent |
| `PushKit` | `callkit-patterns`, `user-notifications-patterns` | Adjacent |
| `Push to Talk` | none | Candidate |
| `Quick Look` | `pdfkit-patterns`, `photokit-patterns` | Adjacent |
| `QuickLook UI` | `pdfkit-patterns`, `photokit-patterns` | Adjacent |
| `ResearchKit` | `healthkit-patterns` | Adjacent |
| `Retention Messaging API` | none | Candidate |
| `Roster API` | none | Candidate |
| `Safari Services` | `webkit-patterns`, `authenticationservices-patterns` | Adjacent |
| `SecureElementCredential` | `passkit-patterns` | Adjacent |
| `SensitiveContentAnalysis` | `vision-patterns`, `foundation-models-patterns` | Adjacent |
| `ServicesAccountLinking` | `authenticationservices-patterns` | Adjacent |
| `Shared with You` | `group-activities-patterns` | Adjacent |
| `SiriKit` | `app-intents-patterns` | Adjacent |
| `SKAdNetwork for Web Ads` | `adattributionkit-patterns` | Adjacent |
| `SMS and Call Reporting` | `callkit-patterns` | Adjacent |
| `Social` | none | Candidate |
| `Speech` | `speech-patterns` | Covered |
| `StoreKit` | `storekit-patterns` | Covered |
| `Tabular Data` | none | Candidate |
| `TelephonyMessagingKit` | `callkit-patterns` | Adjacent |
| `TipKit` | `tipkit-patterns` | Covered |
| `Translation` | `natural-language-patterns` | Covered |
| `TV Services` | none | Candidate |
| `User Notifications` | `user-notifications-patterns` | Covered |
| `User Notifications UI` | `user-notifications-patterns` | Covered |
| `Wallet Orders` | `financekit-patterns`, `passkit-patterns` | Adjacent |
| `Wallet Passes` | `passkit-patterns` | Adjacent |
| `Watch Connectivity` | `widgetkit-patterns`, `relevancekit-patterns` | Adjacent |
| `WeatherKit` | `weatherkit-patterns` | Covered |
| `WeatherKit REST API` | `weatherkit-patterns` | Adjacent |
| `WebKit` | `webkit-patterns` | Covered |
| `WidgetKit` | `widgetkit-patterns`, `widgetkit-design` | Covered |
| `WirelessInsights` | `network-framework-patterns` | Adjacent |
| `WorkoutKit` | `healthkit-patterns` | Adjacent |
| `Vision` | `vision-patterns` | Covered |
| `VisionKit` | `vision-patterns` | Covered |
| `SafetyKit` | `healthkit-patterns` | Adjacent |

### Graphics and Games

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `ARKit` | `realitykit-patterns` | Covered |
| `ColorSync` | none | Candidate |
| `Compositor Services` | `realitykit-patterns` | Adjacent |
| `Core Graphics` | `swiftui-design`, `pdfkit-patterns` | Adjacent |
| `Core Image` | `photokit-patterns`, `vision-patterns` | Adjacent |
| `Foveated Streaming` | `realitykit-patterns` | Adjacent |
| `Game Controller` | `gamekit-patterns`, `spritekit-patterns` | Adjacent |
| `GameKit` | `gamekit-patterns` | Covered |
| `GameplayKit` | `gamekit-patterns`, `spritekit-patterns`, `scenekit-patterns` | Adjacent |
| `GameSave` | none | Candidate |
| `GLKit` | none | Candidate |
| `Image I/O` | `photokit-patterns`, `pdfkit-patterns` | Adjacent |
| `Image Playground` | `foundation-models-patterns`, `vision-patterns` | Adjacent |
| `Metal` | `mlx-swift-patterns`, `core-ml-patterns`, `xcode-instruments` | Adjacent |
| `MetalFX` | `xcode-instruments`, `realitykit-patterns` | Adjacent |
| `MetalKit` | `xcode-instruments`, `realitykit-patterns` | Adjacent |
| `Metal Performance Shaders` | `core-ml-patterns`, `mlx-swift-patterns` | Adjacent |
| `Metal Performance Shaders Graph` | `core-ml-patterns`, `mlx-swift-patterns` | Adjacent |
| `Model I/O` | `scenekit-patterns`, `realitykit-patterns` | Adjacent |
| `OpenGL ES` | none | Candidate |
| `PDFKit` | `pdfkit-patterns` | Covered |
| `PencilKit` | `pencilkit-patterns` | Covered |
| `Quartz` | none | Candidate |
| `Core Animation` | `swiftui-performance`, `uikit-architecture` | Adjacent |
| `QuickTime File Format` | none | Candidate |
| `RealityKit` | `realitykit-patterns` | Covered |
| `ReplayKit` | `avkit-patterns` | Adjacent |
| `RoomPlan` | `realitykit-patterns`, `vision-patterns` | Adjacent |
| `SceneKit` | `scenekit-patterns` | Covered |
| `Spatial` | `realitykit-patterns` | Adjacent |
| `SpriteKit` | `spritekit-patterns` | Covered |
| `TabletopKit` | `tabletopkit-patterns` | Covered |
| `Touch Controller` | none | Candidate |
| `USD` | `realitykit-patterns` | Adjacent |

### Media

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `Apple Ads` | none | Candidate |
| `Apple Music Feed` | none | Candidate |
| `Apple News` | none | Candidate |
| `Assets Library` | none | Candidate |
| `Audio Toolbox` | `avkit-patterns`, `speech-patterns` | Adjacent |
| `Audio Unit` | none | Candidate |
| `AVFAudio` | `avkit-patterns`, `speech-patterns` | Adjacent |
| `AVFoundation` | `avkit-patterns`, `photokit-patterns`, `speech-patterns` | Adjacent |
| `AVKit` | `avkit-patterns` | Covered |
| `AVRouting` | none | Candidate |
| `Cinematic` | none | Candidate |
| `Core Audio` | `avkit-patterns`, `speech-patterns` | Adjacent |
| `CoreAudioKit` | none | Candidate |
| `Core Audio Types` | none | Candidate |
| `Core Haptics` | `swiftui-patterns` | Adjacent |
| `Core Media` | `avkit-patterns`, `photokit-patterns` | Adjacent |
| `Core Media I/O` | none | Candidate |
| `Core MIDI` | none | Candidate |
| `Core Video` | `avkit-patterns`, `photokit-patterns`, `vision-patterns` | Adjacent |
| `DeviceDiscoveryExtension` | none | Candidate |
| `Group Activities` | `group-activities-patterns` | Covered |
| `HTTP Live Streaming` | `avkit-patterns` | Adjacent |
| `ImageCaptureCore` | none | Candidate |
| `Immersive Media Support` | none | Candidate |
| `iTunes Library` | none | Candidate |
| `LockedCameraCapture` | `photokit-patterns` | Adjacent |
| `Media Accessibility` | `accessibility-patterns`, `avkit-patterns` | Adjacent |
| `MediaExtension` | none | Candidate |
| `Media Library` | none | Candidate |
| `Media Player` | `musickit-patterns`, `avkit-patterns` | Adjacent |
| `Media Setup` | none | Candidate |
| `Media Toolbox` | none | Candidate |
| `MusicKit` | `musickit-patterns` | Covered |
| `MusicKitJS` | `musickit-patterns` | Adjacent |
| `PHASE` | none | Candidate |
| `PhotoKit` | `photokit-patterns` | Covered |
| `Professional Video Applications` | none | Candidate |
| `Quick Look Thumbnailing` | `pdfkit-patterns`, `photokit-patterns` | Adjacent |
| `ScreenCaptureKit` | `avkit-patterns`, `xcode-instruments` | Adjacent |
| `Screen Saver` | none | Candidate |
| `ShazamKit` | `musickit-patterns` | Adjacent |
| `SiriKit Cloud Media` | `musickit-patterns`, `app-intents-patterns` | Adjacent |
| `Sound Analysis` | `speech-patterns`, `natural-language-patterns` | Adjacent |
| `Video Toolbox` | `avkit-patterns`, `xcode-instruments` | Adjacent |
| `Video Subscriber Account` | none | Candidate |

### System

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `Accelerate` | `core-ml-patterns`, `mlx-swift-patterns` | Adjacent |
| `simd` | `core-ml-patterns`, `mlx-swift-patterns` | Adjacent |
| `AccessorySetupKit` | `accessorysetupkit-patterns` | Covered |
| `Accessory Transport Extension` | none | Candidate |
| `Account & Organizational Data Sharing` | none | Candidate |
| `Apple silicon` | `mlx-swift-patterns`, `core-ml-patterns` | Adjacent |
| `Apple Archive` | `swiftpm-macos-app-packaging` | Adjacent |
| `App Tracking Transparency` | `adattributionkit-patterns` | Adjacent |
| `AudioDriverKit` | none | Candidate |
| `Authentication Services` | `authenticationservices-patterns` | Covered |
| `BlockStorageDeviceDriverKit` | none | Candidate |
| `CFNetwork` | `foundation-urlsession-patterns`, `network-framework-patterns` | Adjacent |
| `Collaboration` | none | Candidate |
| `Compression` | `swift-programming-language` | Adjacent |
| `Core Bluetooth` | `core-bluetooth-patterns` | Covered |
| `Core HID` | none | Candidate |
| `Core NFC` | `core-nfc-patterns` | Covered |
| `Core Services` | none | Candidate |
| `Core Telephony` | none | Candidate |
| `Core WLAN` | none | Candidate |
| `Apple CryptoKit` | `cryptokit-patterns` | Covered |
| `CryptoTokenKit` | `cryptotokenkit-patterns` | Covered |
| `Darwin Notify` | none | Candidate |
| `DeviceDiscoveryUI` | none | Candidate |
| `Device Management` | none | Candidate |
| `Disk Arbitration` | none | Candidate |
| `Dispatch` | `swift-concurrency-patterns` | Adjacent |
| `dnssd` | none | Candidate |
| `DriverKit` | none | Candidate |
| `Endpoint Security` | none | Candidate |
| `Exception Handling` | none | Candidate |
| `Execution Policy` | none | Candidate |
| `Exposure Notification` | none | Candidate |
| `External Accessory` | `accessorysetupkit-patterns`, `core-bluetooth-patterns` | Adjacent |
| `Finder Sync` | none | Candidate |
| `Force Feedback` | none | Candidate |
| `FSKit` | none | Candidate |
| `GSS` | none | Candidate |
| `HIDDriverKit` | none | Candidate |
| `Hypervisor` | none | Candidate |
| `InputMethodKit` | none | Candidate |
| `IOBluetooth` | none | Candidate |
| `IOBluetooth UI` | none | Candidate |
| `IOKit` | none | Candidate |
| `IOSurface` | none | Candidate |
| `IOUSBHost` | none | Candidate |
| `Kernel` | none | Candidate |
| `Latent Semantic Mapping` | none | Candidate |
| `LightweightCodeRequirements` | none | Candidate |
| `Local Authentication` | `keychain-patterns`, `authenticationservices-patterns` | Adjacent |
| `Local Authentication Embedded UI` | `keychain-patterns`, `authenticationservices-patterns` | Adjacent |
| `MetricKit` | `metrickit-patterns` | Covered |
| `MIDIDriverKit` | none | Candidate |
| `ML Compute` | `core-ml-patterns` | Adjacent |
| `Nearby Interaction` | none | Candidate |
| `Network` | `network-framework-patterns` | Covered |
| `Network Extension` | `network-framework-patterns` | Adjacent |
| `NetworkingDriverKit` | none | Candidate |
| `Open Directory` | none | Candidate |
| `os` | `xcode-instruments`, `metrickit-patterns` | Adjacent |
| `OSLog` | `xcode-instruments`, `metrickit-patterns` | Adjacent |
| `Paravirtualized Graphics` | none | Candidate |
| `PCIDriverKit` | none | Candidate |
| `SCSIPeripheralsDriverKit` | none | Candidate |
| `SCSIControllerDriverKit` | none | Candidate |
| `Security` | `keychain-patterns`, `certificate-trust-patterns` | Adjacent |
| `Security Foundation` | `certificate-trust-patterns` | Adjacent |
| `Security Interface` | none | Candidate |
| `SensorKit` | `sensorkit-patterns` | Covered |
| `SerialDriverKit` | none | Candidate |
| `Service Management` | `swiftpm-macos-app-packaging`, `apple-platform-release` | Adjacent |
| `System` | none | Candidate |
| `System Configuration` | `network-framework-patterns` | Adjacent |
| `System Extensions` | `apple-platform-release` | Adjacent |
| `Thread Network` | none | Candidate |
| `Uniform Type Identifiers` | `swift-programming-language` | Adjacent |
| `USBDriverKit` | none | Candidate |
| `USBSerialDriverKit` | none | Candidate |
| `Virtualization` | none | Candidate |
| `vmnet` | none | Candidate |
| `Wi-Fi Infrastructure` | none | Candidate |
| `XPC` | `browserenginekit-patterns`, `swiftpm-macos-app-packaging` | Adjacent |

### Web

| Framework / API | Local skill routing | Coverage |
|---|---|---|
| `Apple Music API` | `musickit-patterns` | Adjacent |
| `Apple Pay on the Web` | `passkit-patterns` | Adjacent |
| `Apple Pay Web Merchant Registration API` | `passkit-patterns` | Adjacent |
| `Apple Pay Merchant Token Usage Information API` | `passkit-patterns` | Adjacent |
| `App Store Connect API` | `apple-platform-release` | Adjacent |
| `BrowserEngineCore` | `browserenginekit-patterns` | Adjacent |
| `BrowserEngineKit` | `browserenginekit-patterns` | Covered |
| `CloudKit JS` | `cloudkit-patterns` | Adjacent |
| `CKTool JS` | `cloudkit-patterns` | Adjacent |
| `Link Presentation` | `webkit-patterns`, `swiftui-patterns` | Adjacent |
| `LivePhotosKit JS` | `photokit-patterns` | Adjacent |
| `MapKit JS` | `mapkit-patterns` | Adjacent |
| `Apple Pay Merchant Token Management API` | `passkit-patterns` | Adjacent |
| `Notary API` | `apple-platform-release` | Adjacent |
| `Safari app extensions` | `webkit-patterns` | Adjacent |
| `Screen Time` | `permissionkit-patterns` | Adjacent |
| `Sign in with Apple` | `authenticationservices-patterns` | Adjacent |
| `Siri Event Suggestions Markup` | `app-intents-patterns` | Adjacent |
| `Maps Web Snapshots` | `mapkit-patterns` | Adjacent |
| `Updates` | none | Candidate |
| `WebKit JS` | `webkit-patterns` | Adjacent |

### Other Local Capabilities

These local capabilities are not single entries in the Apple documentation
areas above, or they cut across multiple frameworks and repository workflows.

| Capability | Local skill routing | Coverage |
|---|---|---|
| Swift package documentation, README layering, and DocC placement | `swiftpm-docs`, `swiftpm-architecture` | Covered |
| Swift Package target graph and module-boundary design | `swiftpm-architecture` | Covered |
| Reusable infrastructure discovery and package alternative checks | `swiftpm-index` | Covered |
| SwiftPM library-to-skill distillation | `swiftpm-distiller` | Covered |
| Swift concurrency migration and diagnostics | `swift-concurrency-patterns` | Covered |
| Swift Testing and XCTest migration | `swift-testings-patterns` | Covered |
| Keychain storage and certificate trust workflows | `keychain-patterns`, `certificate-trust-patterns` | Covered |
| Interface writing and product UI text | `interface-writing` | Covered |
| Figma-to-SwiftUI implementation handoff | `figma-swiftui` | Covered |
| SwiftUI feature architecture | `swiftui-architecture` | Covered |
| UIKit feature architecture | `uikit-architecture` | Covered |
| SwiftUI visual design | `swiftui-design` | Covered |
| SwiftUI source performance | `swiftui-performance` | Covered |
| Widget visual design | `widgetkit-design` | Covered |
| Xcode localization workflows | `xcode-localization-patterns` | Covered |
| Xcode Instruments trace recording and analysis | `xcode-instruments` | Covered |
| iOS Simulator operation and capture | `ios-simulator` | Covered |
| MLX Swift package integration and backend selection | `mlx-swift-patterns` | Covered |
| SwiftLint package/tool governance | `swiftlint-patterns` | Covered |
| Apple-platform release engineering | `apple-platform-release` | Covered |
| SwiftPM-only macOS app packaging | `swiftpm-macos-app-packaging` | Covered |

## Install In Codex

Install a specific skill directory into `$CODEX_HOME/skills` rather than
linking the repository root.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/skills/<skill-name>" \
  "${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>"
```

If you prefer a copy instead of a symlink:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R "$(pwd)/skills/<skill-name>" \
  "${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>"
```

Restart Codex after installing so it picks up the new skill.

## Install In Claude

Install a specific skill directory rather than the repository root.

### Claude Apps

Zip one skill directory and upload that skill in Claude.

1. Open Claude.
2. Go to `Settings > Capabilities > Skills`.
3. Click upload.
4. Select the zipped skill folder.

### Claude Code

Place the skill directory in `~/.claude/skills`:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/<skill-name>" \
  ~/.claude/skills/<skill-name>
```

If you prefer a copy instead of a symlink:

```bash
mkdir -p ~/.claude/skills
cp -R "$(pwd)/skills/<skill-name>" \
  ~/.claude/skills/<skill-name>
```

### Claude Code Marketplace

For local testing from this repository:

```bash
claude plugin marketplace add ./
claude plugin install swiftpm-docs@swift-skills
claude plugin install swiftpm-index@swift-skills
claude plugin install swiftpm-architecture@swift-skills
claude plugin install swiftpm-distiller@swift-skills
claude plugin install swiftui-architecture@swift-skills
claude plugin install uikit-architecture@swift-skills
claude plugin install swift-concurrency-patterns@swift-skills
claude plugin install swift-testings-patterns@swift-skills
claude plugin install swiftdata-patterns@swift-skills
claude plugin install swift-programming-language@swift-skills
claude plugin install core-data-patterns@swift-skills
claude plugin install cloudkit-patterns@swift-skills
claude plugin install keychain-patterns@swift-skills
claude plugin install cryptokit-patterns@swift-skills
claude plugin install certificate-trust-patterns@swift-skills
claude plugin install authenticationservices-patterns@swift-skills
claude plugin install accessibility-patterns@swift-skills
claude plugin install focus-engine-patterns@swift-skills
claude plugin install interface-writing@swift-skills
claude plugin install figma-swiftui@swift-skills
claude plugin install swiftui-patterns@swift-skills
claude plugin install swiftui-performance@swift-skills
claude plugin install swiftui-design@swift-skills
claude plugin install widgetkit-patterns@swift-skills
claude plugin install widgetkit-design@swift-skills
claude plugin install tipkit-patterns@swift-skills
claude plugin install relevancekit-patterns@swift-skills
claude plugin install swift-charts-patterns@swift-skills
claude plugin install xcode-instruments@swift-skills
claude plugin install metrickit-patterns@swift-skills
claude plugin install xcode-localization-patterns@swift-skills
claude plugin install app-intents-patterns@swift-skills
claude plugin install activitykit-patterns@swift-skills
claude plugin install app-clips-patterns@swift-skills
claude plugin install user-notifications-patterns@swift-skills
claude plugin install storekit-patterns@swift-skills
claude plugin install webkit-patterns@swift-skills
claude plugin install mapkit-patterns@swift-skills
claude plugin install photokit-patterns@swift-skills
claude plugin install avkit-patterns@swift-skills
claude plugin install musickit-patterns@swift-skills
claude plugin install pdfkit-patterns@swift-skills
claude plugin install paperkit-patterns@swift-skills
claude plugin install pencilkit-patterns@swift-skills
claude plugin install contacts-patterns@swift-skills
claude plugin install eventkit-patterns@swift-skills
claude plugin install healthkit-patterns@swift-skills
claude plugin install passkit-patterns@swift-skills
claude plugin install weatherkit-patterns@swift-skills
claude plugin install financekit-patterns@swift-skills
claude plugin install foundation-models-patterns@swift-skills
claude plugin install core-ml-patterns@swift-skills
claude plugin install mlx-swift-patterns@swift-skills
claude plugin install vision-patterns@swift-skills
claude plugin install natural-language-patterns@swift-skills
claude plugin install speech-patterns@swift-skills
claude plugin install foundation-urlsession-patterns@swift-skills
claude plugin install network-framework-patterns@swift-skills
claude plugin install background-tasks-patterns@swift-skills
claude plugin install devicecheck-patterns@swift-skills
claude plugin install cryptotokenkit-patterns@swift-skills
claude plugin install accessorysetupkit-patterns@swift-skills
claude plugin install core-bluetooth-patterns@swift-skills
claude plugin install core-nfc-patterns@swift-skills
claude plugin install core-motion-patterns@swift-skills
claude plugin install dockkit-patterns@swift-skills
claude plugin install sensorkit-patterns@swift-skills
claude plugin install audioaccessorykit-patterns@swift-skills
claude plugin install homekit-patterns@swift-skills
claude plugin install callkit-patterns@swift-skills
claude plugin install group-activities-patterns@swift-skills
claude plugin install carplay-patterns@swift-skills
claude plugin install appmigrationkit-patterns@swift-skills
claude plugin install adattributionkit-patterns@swift-skills
claude plugin install alarmkit-patterns@swift-skills
claude plugin install browserenginekit-patterns@swift-skills
claude plugin install energykit-patterns@swift-skills
claude plugin install permissionkit-patterns@swift-skills
claude plugin install gamekit-patterns@swift-skills
claude plugin install spritekit-patterns@swift-skills
claude plugin install scenekit-patterns@swift-skills
claude plugin install tabletopkit-patterns@swift-skills
claude plugin install realitykit-patterns@swift-skills
claude plugin install swiftlint-patterns@swift-skills
claude plugin install ios-simulator@swift-skills
claude plugin install apple-platform-release@swift-skills
claude plugin install swiftpm-macos-app-packaging@swift-skills
```

After publishing the repository to GitHub:

```bash
claude plugin marketplace add swift-library/skills
claude plugin install swiftpm-docs@swift-skills
claude plugin install swiftpm-index@swift-skills
claude plugin install swiftpm-architecture@swift-skills
claude plugin install swiftpm-distiller@swift-skills
claude plugin install swiftui-architecture@swift-skills
claude plugin install uikit-architecture@swift-skills
claude plugin install swift-concurrency-patterns@swift-skills
claude plugin install swift-testings-patterns@swift-skills
claude plugin install swiftdata-patterns@swift-skills
claude plugin install swift-programming-language@swift-skills
claude plugin install core-data-patterns@swift-skills
claude plugin install cloudkit-patterns@swift-skills
claude plugin install keychain-patterns@swift-skills
claude plugin install cryptokit-patterns@swift-skills
claude plugin install certificate-trust-patterns@swift-skills
claude plugin install authenticationservices-patterns@swift-skills
claude plugin install accessibility-patterns@swift-skills
claude plugin install focus-engine-patterns@swift-skills
claude plugin install interface-writing@swift-skills
claude plugin install figma-swiftui@swift-skills
claude plugin install swiftui-patterns@swift-skills
claude plugin install swiftui-performance@swift-skills
claude plugin install swiftui-design@swift-skills
claude plugin install widgetkit-patterns@swift-skills
claude plugin install widgetkit-design@swift-skills
claude plugin install tipkit-patterns@swift-skills
claude plugin install relevancekit-patterns@swift-skills
claude plugin install swift-charts-patterns@swift-skills
claude plugin install xcode-instruments@swift-skills
claude plugin install metrickit-patterns@swift-skills
claude plugin install xcode-localization-patterns@swift-skills
claude plugin install app-intents-patterns@swift-skills
claude plugin install activitykit-patterns@swift-skills
claude plugin install app-clips-patterns@swift-skills
claude plugin install user-notifications-patterns@swift-skills
claude plugin install storekit-patterns@swift-skills
claude plugin install webkit-patterns@swift-skills
claude plugin install mapkit-patterns@swift-skills
claude plugin install photokit-patterns@swift-skills
claude plugin install avkit-patterns@swift-skills
claude plugin install musickit-patterns@swift-skills
claude plugin install pdfkit-patterns@swift-skills
claude plugin install paperkit-patterns@swift-skills
claude plugin install pencilkit-patterns@swift-skills
claude plugin install contacts-patterns@swift-skills
claude plugin install eventkit-patterns@swift-skills
claude plugin install healthkit-patterns@swift-skills
claude plugin install passkit-patterns@swift-skills
claude plugin install weatherkit-patterns@swift-skills
claude plugin install financekit-patterns@swift-skills
claude plugin install foundation-models-patterns@swift-skills
claude plugin install core-ml-patterns@swift-skills
claude plugin install mlx-swift-patterns@swift-skills
claude plugin install vision-patterns@swift-skills
claude plugin install natural-language-patterns@swift-skills
claude plugin install speech-patterns@swift-skills
claude plugin install foundation-urlsession-patterns@swift-skills
claude plugin install network-framework-patterns@swift-skills
claude plugin install background-tasks-patterns@swift-skills
claude plugin install devicecheck-patterns@swift-skills
claude plugin install cryptotokenkit-patterns@swift-skills
claude plugin install accessorysetupkit-patterns@swift-skills
claude plugin install core-bluetooth-patterns@swift-skills
claude plugin install core-nfc-patterns@swift-skills
claude plugin install core-motion-patterns@swift-skills
claude plugin install dockkit-patterns@swift-skills
claude plugin install sensorkit-patterns@swift-skills
claude plugin install audioaccessorykit-patterns@swift-skills
claude plugin install homekit-patterns@swift-skills
claude plugin install callkit-patterns@swift-skills
claude plugin install group-activities-patterns@swift-skills
claude plugin install carplay-patterns@swift-skills
claude plugin install appmigrationkit-patterns@swift-skills
claude plugin install adattributionkit-patterns@swift-skills
claude plugin install alarmkit-patterns@swift-skills
claude plugin install browserenginekit-patterns@swift-skills
claude plugin install energykit-patterns@swift-skills
claude plugin install permissionkit-patterns@swift-skills
claude plugin install gamekit-patterns@swift-skills
claude plugin install spritekit-patterns@swift-skills
claude plugin install scenekit-patterns@swift-skills
claude plugin install tabletopkit-patterns@swift-skills
claude plugin install realitykit-patterns@swift-skills
claude plugin install swiftlint-patterns@swift-skills
claude plugin install ios-simulator@swift-skills
claude plugin install apple-platform-release@swift-skills
claude plugin install swiftpm-macos-app-packaging@swift-skills
```

This uses `.claude-plugin/marketplace.json` as the marketplace catalog.

## Repository Layout

- `.claude-plugin/`: Claude Code marketplace metadata.
- `Docs/`: collection documentation and architecture notes.
- `skills/`: authoritative skill definitions and skill-local supporting files.

## Documentation Index

- `Docs/README.md`: collection documentation index.
- `Docs/Architecture/README.md`: architecture document index.
- `Docs/Architecture/skill-authoring.md`: skill structure, progressive
  disclosure, and trigger-precision rules.
- `AGENTS.md`: repository-local agent routing and operating contract.
- `CONTRIBUTING.md`: contribution guidance.
