# Packaging Notes

Use this file when turning a SwiftPM executable into a local `.app` bundle.

## Bundle Layout

```text
MyApp.app/
└── Contents/
    ├── Info.plist
    ├── MacOS/
    │   └── MyApp
    ├── Frameworks/
    └── Resources/
```

## Build Output

- Build with `swift build -c <config>`.
- For arch-specific builds, SwiftPM places binaries under
  `.build/<arch>-apple-macosx/<config>/<AppName>`.
- Some products still appear under `.build/<config>/<AppName>`.
- Use `ARCHES="arm64 x86_64"` to build and merge a universal binary.
- The app bundle executable should live at `<App>.app/Contents/MacOS/<AppName>`.
- Preserve executable permissions after copying the binary.
- Verify the final architecture set with `lipo -archs`.

## Info.plist Checks

Required keys for the template:

- `CFBundleExecutable`
- `CFBundleIdentifier`
- `CFBundleName`
- `CFBundlePackageType` = `APPL`
- `CFBundleShortVersionString`
- `CFBundleVersion`
- `LSMinimumSystemVersion`
- `LSUIElement` when `MENU_BAR_APP=1`
- `CFBundleIconFile`

Validate with:

```bash
plutil -lint MyApp.app/Contents/Info.plist
```

## Local Launch

- Prefer `open MyApp.app` for Finder-equivalent launch behavior.
- If the app does not launch, inspect:
  - executable permissions
  - missing resources
  - bundle identifier mismatch
  - runtime crash logs through Console or `log show`

## Resources And Frameworks

- Copy checked-in executable target resources from
  `Sources/<AppName>/Resources` into `Contents/Resources`.
- Copy SwiftPM-emitted `*.bundle` resource bundles from the selected build
  output directory into `Contents/Resources`.
- Copy built `*.framework` outputs into `Contents/Frameworks` when present.
- Add `@executable_path/../Frameworks` as an rpath when frameworks are embedded.
- Strip extended attributes with `xattr -cr` and remove `._*` AppleDouble files
  before signing.

## Template Variables

The bundled scripts read common environment variables:

- `APP_NAME`
- `BUNDLE_ID`
- `MARKETING_VERSION`
- `BUILD_NUMBER`
- `ARCHES`
- `SIGNING_MODE`
- `APP_IDENTITY`
- `MACOS_MIN_VERSION`
- `MENU_BAR_APP`
- `APP_ENTITLEMENTS`

Set them in the shell, `version.env`, or a project-local wrapper script.

## Entitlements Input

- The packaging scripts default to
  `.build/entitlements/<AppName>.entitlements`, matching the upstream skill
  contract.
- Set `APP_ENTITLEMENTS=App.entitlements` when the app needs a checked-in or
  project-local entitlements plist.
- `ENTITLEMENTS` is accepted only as a compatibility alias.
- Keep the entitlements plist minimal. Do not add sandbox, network, file,
  automation, or hardened-runtime exceptions unless the target app requires
  them.

## Icon Input

- `Icon.icon` is converted to `Icon.icns` when present.
- Use `assets/templates/build_icon.sh` when a project needs to generate the
  iconset from Icon Composer output.

## Menu Bar Apps

- Set `MENU_BAR_APP=1` to emit `LSUIElement` in `Info.plist`.
- Do not set it for ordinary windowed apps that should appear in the Dock and
  app switcher.
