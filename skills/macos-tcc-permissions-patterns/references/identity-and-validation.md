# Identity And Validation

TCC grants are tied to the identity of the process requesting protected
capability. Most bugs in polished permission onboarding come from guiding the
user to approve the wrong bundle.

## Identity Checklist

Inspect:

- main app bundle identifier and path
- helper app bundle identifiers and paths
- login item configuration
- XPC service bundle identifiers
- command-line tool path when launched outside the app bundle
- code signing identity and whether the bundle is ad-hoc, development, or
  Developer ID signed
- sandbox state and entitlements

Do not assume a parent app grant applies to:

- a login item helper
- a bundled helper app
- an XPC service
- an Electron helper
- a command-line tool launched from inside the app
- a separately signed updater or installer

## Reset And Test Commands

Use reset commands only in development or QA instructions, not as normal user
onboarding.

```bash
tccutil reset ScreenCapture com.example.App
tccutil reset Accessibility com.example.App
tccutil reset ListenEvent com.example.App
```

When service names are uncertain on the target macOS version, verify locally
before documenting them. Avoid broad `tccutil reset All` during focused QA
unless the test explicitly needs a clean privacy database.

## QA Matrix

Test:

- fresh install, first launch
- app already granted
- app explicitly denied
- permission revoked while app is running
- helper requests permission before main app opens onboarding
- app moved between Downloads and Applications
- app upgraded with the same bundle ID and signing identity
- ad-hoc/debug build versus signed/release build
- multiple displays and Spaces
- System Settings already open to another pane

Expected evidence:

- the protected operation succeeds only after the correct identity is granted
- the UI names the same app/helper visible in System Settings
- a denied state has a recovery path
- a granted state does not keep nagging
- relaunch messaging appears only when relaunch is actually needed

## Review Red Flags

- UI says "enable the app" but code runs from a helper.
- Code tries to edit TCC databases directly.
- Product code shells out to `tccutil reset`.
- A System Settings deep link is the only instruction.
- The permission request fires repeatedly without checking current state.
- The onboarding uses Accessibility window inspection before Accessibility is
  available.
- Debug builds and release builds use different bundle IDs but the same QA
  instructions.
