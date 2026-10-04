# Scripts

These scripts wrap `xctrace` and need only the Python 3 standard library. Run
each entry point with `--help` for the current command surface.

- `analyze_trace.py`: analyze an existing `.trace` bundle and emit JSON plus a
  Markdown summary; also lists runs, logs, and signposts, scopes analysis to a
  time window, and ranks cause-graph fan-in for a view.
- `record_trace.py`: wrap `xctrace record` for attach, launch, all-process,
  time-limited, or stop-file recordings, and list devices and templates as
  JSON.
- `instruments_parser/`: lane parsers and helpers used by `analyze_trace.py`:
  - `xctrace.py`: `xctrace export` wrapper and table-of-contents reading.
  - `xml_utils.py`: streaming XML helpers that resolve `id`/`ref` values.
  - `time_profiler.py`: Time Profiler samples aggregated by symbol.
  - `hangs.py`: `potential-hangs` lane.
  - `hitches.py`: Animation Hitches lane.
  - `swiftui.py`: SwiftUI update lane.
  - `causes.py`: SwiftUI cause-graph lane.
  - `correlate.py`: per-hang and per-hitch correlation with Time Profiler
    samples and SwiftUI updates.
  - `events.py`: `os_log` and `os_signpost` discovery for focus windows.
  - `summary.py`: Markdown summary renderer.
