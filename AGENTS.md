# swift-skills Agent Route

Read `README.md` first for the collection shape and authority model.

## Route

- Use each `skills/*/SKILL.md` frontmatter description as the primary trigger
  contract for that skill. Keep detailed trigger lists in the skill, not here.
- Treat `*-patterns` as framework/API or concrete Swift package/tool usage and
  implementation practice. Swift package/tool skills use the package/tool slug
  plus `-patterns`, with official project casing in display names, such as
  `swift-argument-parser-patterns` / `Swift Argument Parser Patterns`.
  Treat `*-design` as visual, interaction, information hierarchy, and
  platform-native feel. Operation words such as review/refactor/debug normally
  belong in skill descriptions and workflows, not ordinary domain skill names.
- Enter `skills/swiftpm-docs/` when the task is about repository-native
  documentation architecture for a Swift package repository: scaffold, audit,
  normalize, or export template.
- For large multi-step documentation migrations or normalize/export work inside
  that skill, emit the skill's `templates/PLANS.md.tpl` to the target
  repository root as `PLANS.md` and keep the plan updated as work proceeds.
- Enter `skills/swiftpm-index/` automatically when Swift implementation
  or review is about to introduce, rewrite, or accept custom reusable
  infrastructure that may overlap with official Apple / swiftlang libraries.
- Enter the same skill manually when the user asks for full SwiftPM Index
  audits, SPI discovery, local workspace candidates, source refresh, drift
  checks, or export bundles.
- Enter `skills/swiftpm-distiller/` when the task is to distill a SwiftPM
  package or Swift library source tree into agent-operational skill material,
  such as trigger contracts, supported tasks, API usage workflows, validation
  commands, examples, or skill skeleton/update material.
- Enter `skills/swiftpm-architecture/` when the task is about Swift Package
  architecture: target graph, module boundaries, product/library/executable
  layout, dependency direction, public API surfaces, composition roots, package
  structure, architecture review, active/proactive review, or reviewer handoff.
- For ordinary package-architecture work inside that skill, answer in place by
  default. For explicit invocation, active/proactive review, brief, bundle,
  context pack, or handoff requests, produce the compact Markdown evidence
  brief.
- Route architecture selection, migration, and feature/module architecture
  review to the matching architecture skill, such as `swiftui-architecture` or
  `uikit-architecture`.
- For implementation and review work, prefer the most specific domain skill
  over a baseline skill. Use `swift-programming-language` only when no deeper
  domain skill is the right fit.
- For broad security review requests, combine the relevant focused security
  skills rather than routing through a single umbrella skill.
- Route chart-specific accessibility to `swift-charts-patterns` after
  identifying the issue; route dedicated accessibility work to
  `accessibility-patterns`.
- Use `figma-swiftui` for SwiftUI implementation from Figma context. Use the
  general `figma` skill only for Figma MCP setup or tool troubleshooting.
- Use `swiftui-patterns` for SwiftUI view implementation, ordinary review, and
  dedicated view cleanup passes. Use `swiftui-performance` for source-level
  SwiftUI performance guidance, review, diagnosis, or optimization before
  Instruments evidence is required.
- Route WidgetKit extension targets, `Widget`, `WidgetBundle`,
  `StaticConfiguration`, `AppIntentConfiguration`, `TimelineProvider`,
  `AppIntentTimelineProvider`, `TimelineEntry`, reload policies,
  `WidgetCenter`, interactive widgets, Control Center widgets, App Group data,
  deep links, previews, snapshots, and extension constraints to
  `widgetkit-patterns`. Keep visual-only widget polish in `widgetkit-design`,
  Live Activity lifecycle in `activitykit-patterns`, and App Intent action
  design in `app-intents-patterns`.
- Route TipKit setup, `Tips.configure`, `Tip` definitions, `TipView`,
  `.popoverTip`, UIKit/AppKit tip views, `TipGroup`, rules, parameters, events,
  display frequency, datastore, CloudKit tip sync, tip actions, invalidation,
  eligibility reset, and testing helpers to `tipkit-patterns`. Keep
  generic onboarding copy and wording in `interface-writing`.
- Route RelevanceKit widget relevance, watchOS Smart Stack surfacing,
  `RelevantContext`, relevance donation, WidgetKit/App Intents integration,
  time/date/location/fitness/sleep/hardware clues, grouping, permission
  boundaries, relevant-widget testing, and unsupported-platform fallback to
  `relevancekit-patterns`. Keep generic widget timelines in
  `widgetkit-patterns` and visual-only widget review in `widgetkit-design`.
- Route trace capture and trace interpretation to `xcode-instruments`; route
  source-level fixes discovered from trace evidence to the relevant source-code
  skill when the task moves beyond trace interpretation.
- Route MetricKit subscribers, `MXMetricPayload`, `MXDiagnosticPayload`,
  runtime metrics, diagnostics, `MXCallStackTree`, custom signpost metrics,
  JSON export, payload persistence, backend upload, Organizer correlation, and
  telemetry redaction to `metrickit-patterns`. Keep `.trace` recording and
  interactive profile interpretation in `xcode-instruments`.
- Route Xcode localization resources, String Catalogs, generated symbols,
  XLIFF/xcloc exchange, pseudolocalization, localized package/framework
  resources, bundle lookup, Swift localization APIs, SwiftUI text localization,
  RTL checks, and locale UI tests to `xcode-localization-patterns`.
- Route App Intents actions, entities, App Shortcuts, Siri, Spotlight, widgets,
  controls, Focus filters, and related system integration to
  `app-intents-patterns`.
- Route Live Activities, Dynamic Island, ActivityKit lifecycle, ActivityKit push
  updates, and Live Activity WidgetKit UI wiring to `activitykit-patterns`.
- Route App Clip target setup, invocation URLs, associated domains, shared code,
  location confirmation, testing, and full-app handoff to
  `app-clips-patterns`.
- Route UserNotifications, APNs, local/remote notifications, authorization,
  payloads, notification extensions, and delivery debugging to
  `user-notifications-patterns`.
- Route StoreKit product loading, purchases, subscriptions, transaction
  verification, entitlements, StoreKit views, testing, and server validation to
  `storekit-patterns`.
- Route embedded WebKit surfaces, SwiftUI `WebView`/`WebPage`, `WKWebView`,
  navigation policy, JavaScript, local content, and custom schemes to
  `webkit-patterns`.
- Route map views, annotations, overlays, camera state, search, directions,
  Look Around, Core Location-backed map behavior, geofencing, and map testing
  to `mapkit-patterns`.
- Route Photos/PhotosUI picking, PhotoKit library access, selected-media
  loading, camera capture tied to photo workflows, and photo-grid memory
  behavior to `photokit-patterns`.
- Route AVKit playback, `AVPlayer`, `AVPlayerViewController`, SwiftUI
  `VideoPlayer`, Picture in Picture, AirPlay, subtitles, background playback,
  and playback lifecycle debugging to `avkit-patterns`.
- Route MusicKit authorization, Apple Music catalog/library access,
  subscription state, music players, queues, MediaPlayer, Now Playing, and
  background audio to `musickit-patterns`.
- Route PDFKit display, navigation, search, annotations, forms, page
  manipulation, rendering, printing, and SwiftUI PDF wrappers to
  `pdfkit-patterns`.
- Route PaperKit structured markup, `PaperMarkupViewController`,
  `PaperMarkup`, PencilKit coexistence, persistence, rendering, and
  compatibility checks to `paperkit-patterns`.
- Route PencilKit freeform drawing, `PKCanvasView`, `PKDrawing`,
  `PKToolPicker`, Apple Pencil interactions, drawing persistence, export, and
  SwiftUI wrappers to `pencilkit-patterns`.
- Route Contacts and ContactsUI access, limited contact access, contact
  pickers, contact mutation, vCards, groups, and change history to
  `contacts-patterns`.
- Route EventKit and EventKitUI calendar/reminder access, full versus
  write-only calendar access, event/reminder CRUD, recurrence, alarms, and
  editor wrappers to `eventkit-patterns`.
- Route HealthKit authorization, health queries, samples, background delivery,
  workouts, HealthKit units, and health-data privacy review to
  `healthkit-patterns`.
- Route PassKit Apple Pay, Wallet passes, `PKPaymentRequest`, payment
  authorization, merchant/pass entitlements, and pass-library behavior to
  `passkit-patterns`.
- Route AuthenticationServices flows, Sign in with Apple,
  `ASAuthorizationAppleIDProvider`, `ASAuthorizationController`,
  `ASWebAuthenticationSession`, SwiftUI `WebAuthenticationSession`, passkeys,
  password AutoFill, associated domains, credential state, callback handling,
  presentation contexts, and account-security upgrades to
  `authenticationservices-patterns`. Keep generic credential storage and
  biometric-protected local secrets in `keychain-patterns` unless the system
  authentication flow is in scope.
- Route WeatherKit forecasts, alerts, availability, attribution, weather
  caching, location-backed weather data, and weather dashboard validation to
  `weatherkit-patterns`.
- Route FinanceKit availability, managed entitlement gating, authorization,
  accounts, balances, transactions, history tokens, Wallet orders, background
  delivery, and financial-data privacy to `financekit-patterns`.
- Route direct CloudKit/iCloud data work, iCloud containers,
  public/private/shared databases, `CKRecord`, custom zones, queries,
  subscriptions, silent-change delivery, `CKSyncEngine`, server change tokens,
  `CKShare`, `UICloudSharingController`, `CKAsset`, account status, `CKError`,
  conflict resolution, dashboard workflow, `NSUbiquitousKeyValueStore`, and
  iCloud document coordination to `cloudkit-patterns`. Keep ordinary
  SwiftData/Core Data CloudKit-backed persistence in the persistence skills
  unless direct CloudKit schema, sharing, subscriptions, or dashboard behavior
  is in scope.
- Route Foundation Models generation, `SystemLanguageModel`,
  `LanguageModelSession`, Apple Intelligence availability, prompts,
  transcripts, `@Generable`, `@Guide`, streaming, tool calling, adapters,
  guardrails, and on-device generative fallback decisions to
  `foundation-models-patterns`.
- Route Core ML model loading, configuration, prediction, deployment,
  profiling, `.mlmodel`/`.mlpackage`/`.mlmodelc` handling, `MLTensor`,
  `MLMultiArray`, `VNCoreMLModel` integration, and model performance to
  `core-ml-patterns`.
- Route MLX Swift package setup, MLX arrays, MLXNN, MLXOptimizers, MLXRandom,
  Apple silicon/Metal build constraints, model examples, memory pressure, and
  backend selection to `mlx-swift-patterns`.
- Route Vision and VisionKit OCR, barcode recognition, face detection, image
  classification, segmentation, tracking, coordinate conversion, Core ML
  requests, `DataScannerViewController`, document camera, overlays, and SwiftUI
  wrappers to `vision-patterns`.
- Route Natural Language and Translation tokenization, language recognition,
  tagging, embeddings, custom `NLModel` work, `TranslationSession`, language
  availability, batch translation, and deterministic text analysis to
  `natural-language-patterns`.
- Route Speech framework authorization, microphone/audio pipeline setup,
  `SpeechAnalyzer`, `SpeechTranscriber`, `SFSpeechRecognizer`, live/file
  transcription, on-device/server recognition decisions, cancellation, and
  cleanup to `speech-patterns`.
- Route Foundation URL loading, `URLSession`, HTTP API clients, transfers,
  request/response validation, background transfer handoff, `URLProtocol`
  mocks, SSE, WebSocket tasks, and ATS to `foundation-urlsession-patterns`.
- Route Network.framework transports, `NWConnection`, `NWListener`,
  `NWBrowser`, `NWPathMonitor`, protocol options, Bonjour, local network
  privacy, peer-to-peer protocols, and receive loops to
  `network-framework-patterns`.
- Route BackgroundTasks scheduling, task registration, permitted identifiers,
  SwiftUI `.backgroundTask`, UIKit registration, expiration handlers,
  completion, checkpointing, background URLSession handoff, background push
  coordination, and debug launch to `background-tasks-patterns`.
- Route DeviceCheck and App Attest tokens, support checks, key generation,
  attestation, assertions, nonce/challenge handling, server verification,
  rollout strategy, invalidated keys, retry policy, and graceful unsupported
  states to `devicecheck-patterns`.
- Route CryptoTokenKit tokens, smart cards, token drivers, sessions, token
  keychain contents, PIN/authentication state, APDU exchange, TLV records, and
  managed smart card authentication to `cryptotokenkit-patterns`.
- Route AccessorySetupKit picker discovery, Bluetooth/Wi-Fi accessory setup,
  accessory descriptors, session events, authorization, rename/remove flows,
  Bluetooth HID support options, and runtime handoff to
  `accessorysetupkit-patterns`.
- Route Core Bluetooth central/peripheral work, BLE scanning, connection,
  service/characteristic discovery, read/write/notify flows, GATT modeling,
  advertising, L2CAP, background modes, and state restoration to
  `core-bluetooth-patterns`.
- Route Core NFC NDEF and tag-reader sessions, NFC entitlements, ISO 7816,
  ISO 15693, FeliCa, MIFARE, background tag reading, session invalidation, and
  physical tag testing to `core-nfc-patterns`.
- Route Core Motion device motion, raw sensors, pedometer, activity manager,
  altimeter, headphone motion, water submersion, sampling intervals,
  sensor-fusion data, battery, and privacy behavior to
  `core-motion-patterns`.
- Route DockKit accessory observation, system/custom tracking, motorized stand
  control, camera coordination, subject/object tracking, device support, and
  physical dock validation to `dockkit-patterns`.
- Route SensorKit entitlement-gated research data access, authorization,
  sample fetches, deletion records, high-sensitivity sensor-derived metrics,
  and research-study consent boundaries to `sensorkit-patterns`.
- Route AudioAccessoryKit accessory capabilities, placement state, automatic
  audio switching, connected audio sources, AccessorySetupKit pairing handoff,
  distribution constraints, and physical accessory validation to
  `audioaccessorykit-patterns`.
- Route HomeKit and MatterSupport smart-home work, `HMHomeManager`, homes,
  rooms, accessories, services, characteristics, action sets, triggers, Matter
  commissioning, HomeKit entitlements, and HomeKit Accessory Simulator
  validation to `homekit-patterns`.
- Route CallKit and PushKit VoIP work, `CXProvider`, `CXCallController`,
  `CXCallUpdate`, incoming/outgoing calls, call actions, provider delegates,
  VoIP pushes, audio-session coordination, and Call Directory extensions to
  `callkit-patterns`.
- Route GroupActivities and SharePlay sessions, `GroupActivity`,
  `GroupSession`, `GroupSessionMessenger`, synchronized playback, participant
  state, sharing UI, and `GroupSessionJournal` to
  `group-activities-patterns`.
- Route CarPlay category entitlements, `CPTemplateApplicationScene`, scene
  delegates, `CPInterfaceController`, CarPlay templates, dashboard and
  instrument-cluster surfaces, vehicle display constraints, and CarPlay
  Simulator validation to `carplay-patterns`.
- Route AppMigrationKit migration extensions, source/destination app transfer,
  resource export/import, `MigrationStatus`, progress, App Group recovery,
  versioned migration, and first-launch import UX to
  `appmigrationkit-patterns`.
- Route AdAttributionKit app-side attribution, publisher/advertised app setup,
  ad network identifiers, `UIEventAttributionView`, JWS impressions,
  StoreKit-rendered ads, postbacks, conversion values/tags, and re-engagement
  to `adattributionkit-patterns`.
- Route AlarmKit authorization, `AlarmManager`, alarm and timer scheduling,
  `Alarm.Schedule`, countdowns, state observation, `AlarmAttributes`,
  presentations, buttons, and widget extension wiring to `alarmkit-patterns`.
- Route BrowserEngineKit alternative browser engine work, host and extension
  processes, web content/networking/rendering extensions, XPC, sandboxing, JIT,
  rendering, text input, downloads, and process lifecycle to
  `browserenginekit-patterns`.
- Route EnergyKit electricity guidance, venues, EV/HVAC load event sessions,
  suggested actions, guidance tokens, unsupported regions, dashboards, and
  residential energy insights to `energykit-patterns`.
- Route PermissionKit child communication flows, communication limits, handles,
  `AskCenter`, `PermissionButton`, `PermissionQuestion`, `CommunicationTopic`,
  choices, responses, significant app update topics, and family account
  behavior to `permissionkit-patterns`.
- Route GameKit and Game Center services, Game Center entitlement setup,
  `GKLocalPlayer`, `authenticateHandler`, scoped player IDs, `GKAccessPoint`,
  dashboards, leaderboards, achievements, matchmaking, `GKMatch`,
  `GKTurnBasedMatch`, saved games, friends, challenges, and server identity
  verification to `gamekit-patterns`.
- Route SpriteKit 2D scene work, `SKScene`, `SKView`, `SpriteView`,
  `SKRenderer`, nodes, actions, texture atlases, physics bodies,
  `SKPhysicsWorld`, contact delegates, touch input, cameras, particles, tile
  maps, shaders, frame-cycle callbacks, and SpriteKit performance to
  `spritekit-patterns`.
- Route SceneKit 3D maintenance and migration-sensitive review, `SCNView`,
  `SceneView`, `SCNScene`, `SCNNode`, transforms, geometry, materials, lights,
  cameras, actions, animations, physics, particles, asset loading, shader
  modifiers, hit testing, and render delegates to `scenekit-patterns`.
- Route TabletopKit visionOS tabletop games, `TabletopGame`, `TableSetup`,
  `Tabletop`, equipment, seats, `TableState`, `TabletopAction`, turns, score
  counters, bookmarks, interactions, dice, RealityKit rendering, and
  GroupActivities synchronization to `tabletopkit-patterns`.
- Route RealityKit and ARKit spatial work, `RealityView`, `ARView`, entities,
  components, systems, anchors, USDZ/Reality Composer Pro assets, materials,
  physics, collision/input targets, gestures, raycasting, scene understanding,
  ARKit sessions, tracking, spatial audio, synchronization, and spatial
  performance to `realitykit-patterns`.
- Route SwiftLint setup/configuration governance, `.swiftlint.yml`,
  disabled/opt-in/only/analyzer rules, included/excluded paths, baselines,
  suppressions, reporters, custom regex/Swift rules, build tool/command
  plugins, Xcode run scripts, CI/pre-commit, analyzer runs, autocorrection, and
  rollout to `swiftlint-patterns`. Do not auto-route ordinary Swift style/code
  review here unless the task is explicitly about SwiftLint enforcement or
  configuration.
- Keep `ios-simulator` separate from `xcode-instruments`: simulator operation
  and UI-driving belongs there; `.trace` recording and interpretation belongs
  in `xcode-instruments`.
- Enter `skills/apple-platform-release/` when the task is Apple-platform
  release engineering: signing assets, certificates, provisioning profiles,
  Xcode archive/export, IPA/PKG preparation, Developer ID notarization,
  stapling, Gatekeeper verification, or upload-ready artifact troubleshooting.
- Keep `apple-platform-release` separate from `swiftpm-macos-app-packaging`:
  Xcode release engineering belongs there; SwiftPM-only no-Xcode `.app`
  packaging belongs in `swiftpm-macos-app-packaging`.
- Stop and clarify if the task drifts into feature specs, roadmap planning,
  task orchestration, release automation, or general workflow systems.

## Authority

- `AGENTS.md` files route work and define operational handling.
- `README`-class files are manuals plus indexes for scope, placement,
  ownership, install/use surface, and focused docs.
- `Docs/Architecture/skill-authoring.md` defines the collection-level skill
  authoring architecture, including progressive disclosure and trigger
  precision.
- `skills/*/SKILL.md` defines the skill boundary and supported operations.
- `skills/*/rules/` holds stable documentation-role invariants.
- `skills/*/knowledge/` holds curated skill-local domain knowledge when a skill
  needs a catalog or reusable basis.
- `skills/*/templates/` holds skill-local template source material, report
  shapes, and scaffold fragments.
- `skills/*/examples/` holds small reference examples.
- `.claude-plugin/marketplace.json` is the discovery registry for the
  collection.

## Operating Notes

- When editing target-repository templates, write for the generated target
  repository, not for the `swift-skills` collection.
- Do not leak collection-internal production terms into target-repository
  templates. Keep out references to skill-local template source material,
  source-versus-export distinctions, and collection `rules/` or `examples/`
  directories.
- Keep report templates focused on the user-facing audit or review output they
  produce.
- When creating or materially changing a skill, follow
  `Docs/Architecture/skill-authoring.md`: keep `SKILL.md` trigger-oriented,
  preserve progressive disclosure, and keep host-specific `agents/` metadata
  secondary to the skill frontmatter and workflow.
- When a skill is based on a named reference source, preserve source coverage
  for task-relevant capabilities and executable knowledge while translating it
  into this collection's structure.
- For Apple, Swift, Xcode, and swiftlang API facts that may have changed, use
  official documentation, the current local SDK/tool output, or verified
  package source before treating memory or skill references as authoritative.
- Keep changes minimal and boundary-first.
- Do not turn this file into a directory catalog.
