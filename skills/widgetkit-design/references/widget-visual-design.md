# Widget Visual Design

## Native Components

Use native WidgetKit components when they express the design. For lock screen
progress, prefer `Gauge` over hand-drawn circles.

```swift
Gauge(value: entry.fraction) {
    Text("")
} currentValueLabel: {
    Text("\(Int(entry.percentage))%")
        .font(.system(size: 12, weight: .medium, design: .monospaced))
}
.gaugeStyle(.accessoryCircular)
.containerBackground(.fill.tertiary, for: .widget)
```

For rectangular lock screen widgets, prefer a compact hierarchy:

```swift
VStack(alignment: .leading, spacing: 4) {
    HStack {
        Text(year)
        Spacer()
        Text(percentage).foregroundStyle(.secondary)
    }
    Gauge(value: fraction) { Text("") }
        .gaugeStyle(.linearCapacity)
        .tint(.primary)
    HStack {
        Spacer()
        Text("\(dayOfYear)/\(totalDays)")
            .foregroundStyle(.secondary)
    }
}
.containerBackground(.fill.tertiary, for: .widget)
```

## Backgrounds And Color

Prefer semantic widget backgrounds:

```swift
.containerBackground(.fill.tertiary, for: .widget)
```

Avoid hardcoded backgrounds such as `.black` unless the product has a deliberate
brand rule and the widget remains legible across modes.

## Family Coverage

Support all relevant families for the product:

```swift
.supportedFamilies([
    .accessoryCircular,
    .accessoryRectangular,
    .accessoryInline,
    .systemSmall,
    .systemMedium,
    .systemLarge,
])
```

Do not skip common families without a product reason. If a family is not
supported, be ready to explain the layout or content constraint.

## Cross-Family Hierarchy

Medium and large home widgets should usually share the same structural
hierarchy:

- header: primary identifier on the left, current value on the right
- middle: progress or key visualization
- footer: secondary status, date, or count right aligned

Do not reinvent hierarchy per family unless a hard size constraint requires it.

Always include internal padding on home widgets to avoid clipping near rounded
edges:

```swift
.padding(.horizontal, 12)
.padding(.vertical, 12)
```

## Typography And Formatting

Keep typography compact and consistent with the app surface. Use the same font
design across related app and widget views unless the project has a deliberate
widget-specific type system.

Identifiers such as years should not be locale-grouped:

```swift
Text(String(year))
Text(year, format: .number.grouping(.never))
```

## Dense Visualizations

Widget extensions have tight memory budgets. Dense visualizations can be
terminated if built from too many nested SwiftUI views.

Use `Canvas` or another lightweight rendering path for dense dot grids,
calendar heat maps, or hundreds of repeated marks:

```swift
Canvas { context, size in
    // Draw dense marks in one pass.
}
```

Avoid hundreds of nested subviews for dense visuals:

```swift
LazyVGrid(columns: columns) {
    ForEach(1...366, id: \.self) { day in
        ZStack { Circle(); partialFillLayer }
    }
}
```

## Timeline Refresh Cadence

Match refresh policy to visible data granularity.

Day-level data can refresh at midnight:

```swift
let tomorrow = calendar.startOfDay(
    for: calendar.date(byAdding: .day, value: 1, to: now)!
)
Timeline(entries: [entry], policy: .after(tomorrow))
```

Time-of-day percentages or partial fills need periodic refresh:

```swift
let refresh = Calendar.current.date(byAdding: .minute, value: 15, to: now)!
Timeline(entries: [entry], policy: .after(refresh))
```

Avoid minute-level refresh for static daily data. It wastes budget without
improving the visible design.

## Shared App And Widget Model

When the app and widget show the same metric, share formatting and calculation
rules rather than duplicating date math or percentage logic. If a percentage is
presented as live progress, include the time-of-day component consistently
across app and widget.

## Review Checklist

- [ ] Lock screen progress uses `Gauge` when appropriate.
- [ ] Widget background is semantic and mode-adaptive.
- [ ] Supported families match the product's user-facing needs.
- [ ] Home widgets have explicit internal padding.
- [ ] Medium and large families share hierarchy unless constrained.
- [ ] Dense visuals avoid hundreds of nested views.
- [ ] Refresh cadence matches visible data granularity.
- [ ] App and widget share user-visible calculation and formatting rules.
