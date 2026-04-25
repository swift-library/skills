---
name: mapkit-patterns
description: Use this skill for MapKit and map-backed location implementation and review across SwiftUI Map, markers, annotations, overlays, camera state, map controls, search, directions, Look Around, snapshots, MKMapItem, Core Location authorization, live updates, geofencing, background location, simulator GPX testing, and map accessibility. Do not use for generic privacy copy, non-map location storage, broad SwiftUI architecture, or server-side geospatial systems.
---

# MapKit Patterns

## Purpose

Guide implementation, review, and troubleshooting for map-centric Apple app
features that combine MapKit, SwiftUI map views, location authorization, search,
directions, and user-visible location behavior.

## When To Use

- Building or reviewing SwiftUI `Map`, markers, annotations, overlays, camera
  state, controls, selection, or map style.
- Adding map search, autocomplete, places, directions, route display, Look
  Around, snapshots, or `MKMapItem` workflows.
- Wiring Core Location authorization, live updates, accuracy, geofencing, or
  background location because a map feature needs it.
- Testing location behavior with simulator routes, GPX, real devices, or
  accessibility checks.

## When Not To Use

- Do not use for generic privacy copy or consent wording alone.
- Do not use for app architecture unless the map/location feature boundary is
  the main issue.
- Do not use for server-side geocoding, tile infrastructure, or non-Apple map
  SDKs unless an Apple app integration is in scope.
- Do not invent Core Location authorization or new MapKit API behavior. Verify
  current Apple documentation and local SDK symbols for version-specific
  location or map APIs.

## Inputs To Inspect

- SwiftUI `Map` or UIKit/AppKit `MKMapView` code, content builders, camera
  state, and map controls.
- Marker, annotation, overlay, route, search, snapshot, and Look Around logic.
- Core Location authorization, usage descriptions, live updates, geofencing,
  background modes, and accuracy requirements.
- Deep links, selected-place models, data loading, caching, and offline/failure
  handling.
- Simulator GPX routes, UI tests, screenshots, and accessibility checks.

## Workflow

1. Identify the user task: browse places, show current location, navigate,
   search, select an item, display a route, or monitor an area.
2. Choose the map surface and state model: SwiftUI `Map`, `MKMapView`, camera
   position, selection, and overlays.
3. Keep displayed map content separate from domain data and network loading.
4. Request location authorization only when the feature needs device location,
   and handle denied, approximate, restricted, and background cases.
5. Use MapKit search, directions, and Look Around APIs with cancellation,
   throttling, empty states, and regional failure handling.
6. Review accessibility, Dynamic Type adjacent UI, annotation tap targets, and
   nonvisual alternatives for critical map content.
7. Validate with deterministic coordinates, simulator location, and device
   checks for authorization or background behavior.

## Review Rules

- Do not require location permission just to view static places.
- Do not assume location updates arrive continuously, accurately, or in the
  foreground.
- Do not mix map selection state with navigation state without a clear restore
  path.
- Do not let annotation views resize or shift the map layout unpredictably.
- Do not hide essential information exclusively in map visuals.
- Treat background location and geofencing behavior as current SDK and device
  validation gated.

## Validation

- Build the affected app target.
- Test denied, approximate, authorized, and changed authorization states when
  location access changes.
- Test search, route, and selected-place error states.
- Test overlays, annotations, and camera restoration with deterministic data.
- Use simulator GPX or real-device checks for movement, geofence, or background
  location behavior.

## Output

For implementation or review work, return:

1. Map surface and user task
2. Location authorization and data-flow status
3. Map content, search, route, and overlay findings
4. Accessibility and failure-state findings
5. Validation run or still needed
