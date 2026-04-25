---
name: weatherkit-patterns
description: Use this skill for WeatherKit implementation and review across WeatherService, current weather, hourly/daily/minute forecasts, weather alerts, historical weather, WeatherAvailability, WeatherAttribution, Apple Weather attribution display, location-backed weather, forecast caching, rate/availability handling, REST versus Swift API boundaries, and weather dashboard validation. Do not use for generic networking, non-WeatherKit providers, Core Location-only behavior, or visual chart styling with no WeatherKit data issue.
---

# WeatherKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for WeatherKit features that
fetch, cache, display, attribute, and validate Apple Weather data.

## When To Use

- Fetching current weather, minute, hourly, daily, part-of-day, historical, or
  selected weather datasets with `WeatherService`.
- Displaying weather alerts, availability, conditions, severity, measurements,
  or weather dashboards.
- Wiring Core Location into WeatherKit requests.
- Handling WeatherKit attribution, Apple Weather marks, legal attribution, and
  weather alert detail links.
- Designing weather-specific caching, request grouping, failure states, or REST
  versus Swift API boundaries.

## When Not To Use

- Do not use for generic networking or cache architecture with no WeatherKit
  data.
- Do not use for non-WeatherKit providers unless the task compares an Apple app
  WeatherKit integration.
- Do not use for Core Location-only behavior; use `mapkit-patterns` when the
  feature is map/location centric.
- Do not use for chart styling only; use `swift-charts-patterns` or design
  skills.
- Do not invent dataset availability, attribution requirements, rate behavior,
  or regional alert/minute forecast coverage. Verify current Apple
  documentation and live behavior.

## Inputs To Inspect

- WeatherKit capability, entitlements, Developer Program assumptions, and target
  platform.
- `WeatherService` requests, selected datasets, location source, units,
  availability checks, and error handling.
- Forecast caching, refresh policy, actor isolation, request coalescing, and
  dashboard state.
- Alert rendering, alert detail links, severity handling, attribution marks, and
  legal attribution display.
- Tests, sample coordinates, regional coverage, and fallback UI.

## Workflow

1. Identify datasets needed: current, hourly, daily, minute, alerts,
   historical, statistics, or selected properties.
2. Confirm WeatherKit capability and location source before changing request
   code.
3. Fetch only datasets needed by the screen or workflow, and account for
   unavailable data by location or region.
4. Cache by coordinate, dataset, unit/locale needs, and freshness. Avoid
   showing stale data without labeling or refresh behavior.
5. Display required attribution and link weather alerts to the detail URLs when
   alerts are shown.
6. Keep Core Location permission optional unless device location is required.
7. Validate with multiple coordinates, no-location, unavailable-alert, and
   poor-network cases.

## Review Rules

- Do not omit required Apple Weather attribution.
- Do not assume minute forecasts or severe alerts exist for every region.
- Do not request location permission when coordinates are user-entered or
  already known.
- Do not treat WeatherKit REST and Swift APIs as interchangeable without
  authentication and response-shape checks.
- Do not hard-code units, language, or legal attribution.
- Do not rely on weather data for safety-critical promises without clear
  product and legal review.

## Validation

- Build the affected app target.
- Test current/hourly/daily/minute/alert requests that changed.
- Test unavailable data, denied location, failed network, and stale cache
  behavior.
- Verify Apple Weather attribution in light/dark appearances where displayed.
- Test regional coordinates for alerts and minute forecasts when those features
  are in scope.

## Output

For implementation or review work, return:

1. Weather datasets and location model
2. Fetch, cache, availability, and error findings
3. Attribution and alert-link findings
4. Validation run or still needed
5. Current-source assumptions for dataset or regional behavior
