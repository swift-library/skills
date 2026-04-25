---
name: adattributionkit-patterns
description: Use this skill for AdAttributionKit implementation and review across privacy-preserving ad attribution, publisher and advertised app setup, ad network identifiers, UIEventAttributionView, JWS impressions, StoreKit-rendered ads, postbacks, conversion values, conversion tags, re-engagement, developer postback copies, testing, and server integration boundaries. Do not use for campaign strategy, ASO, App Store metadata, or market reporting without app-side AdAttributionKit APIs.
---

# AdAttributionKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for app-side
AdAttributionKit setup, ad impression registration, conversion value updates,
postback handling, and testing boundaries.

## When To Use

- Configuring publisher apps, advertised apps, or ad-network identifiers for
  AdAttributionKit.
- Rendering custom or StoreKit-rendered attributable ads.
- Using `UIEventAttributionView`, JWS impressions, app impressions, or click
  handling.
- Updating postback conversion values, coarse values, conversion types, and
  conversion tags.
- Handling install, redownload, and re-engagement attribution flows.
- Reviewing developer postback copies, server verification boundaries, and
  Developer Mode attribution testing.

## When Not To Use

- Do not use for campaign strategy, ASO, or market reporting; use
  market-operation skills.
- Do not use for StoreKit purchase implementation unless attribution is the
  issue; use `storekit-patterns`.
- Do not use for generic analytics SDK integration without AdAttributionKit.
- Do not treat attribution output as user-level tracking.

## Inputs To Inspect

- Info.plist identifiers, advertised-app and publisher-app configuration, and
  ad network setup assumptions.
- Impression signing, JWS payloads, `UIEventAttributionView`, click handling,
  and StoreKit-rendered ad code.
- Conversion value and conversion-tag update logic.
- Postback endpoint, verification code, test mode, and server integration
  boundaries.
- Re-engagement URLs, attribution parameters, and privacy/data-retention notes.

## Workflow

1. Confirm the task is app-side AdAttributionKit API behavior rather than
   campaign analysis.
2. Verify current framework behavior, App Store or marketplace requirements,
   and server endpoints before making attribution claims.
3. Check publisher and advertised app configuration separately.
4. Validate impression signing and rendering path before conversion updates.
5. Keep conversion updates idempotent, time-window aware, and separated by
   install versus re-engagement when the app needs that distinction.
6. Verify postbacks server-side and avoid treating postback contents as
   guaranteed high-granularity data.
7. Use official testing modes to reduce attribution delay during validation.

## Review Rules

- Do not use attribution APIs to identify individual users.
- Do not assume every impression produces a postback or detailed conversion
  value.
- Do not mix market-performance conclusions into the app-side API review.
- Do not log JWS payloads, postbacks, URLs, or identifiers beyond what debugging
  requires.
- Treat SKAdNetwork interoperability, conversion windows, re-engagement limits,
  regional behavior, and postback fields as current Apple documentation gated.

## Validation

- Build the affected app target.
- Test publisher configuration, impression rendering, click handling,
  conversion update, re-engagement URL handling, and postback verification where
  feasible.
- Use Developer Mode or Apple-provided test paths when attribution delay would
  otherwise block validation.

## Output

For implementation or review work, return:

1. AdAttributionKit versus market/reporting boundary decision
2. Publisher, advertised app, and ad-network configuration findings
3. Impression, conversion, postback, and re-engagement findings
4. Server verification and privacy findings
5. Validation run or still needed
