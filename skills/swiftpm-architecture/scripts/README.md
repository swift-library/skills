# Scripts

These scripts need only the Python 3 standard library. Run the entry point with
`--help` for the current command surface.

- `build_swift_package_bundle.py`: scans a local Swift Package, extracts the
  target graph, ranks files by architectural value, and writes one Markdown
  review brief within file, byte, and line budgets.
- `test_build_swift_package_bundle.py`: `unittest` coverage for target metadata
  normalization, source selection, layout fallback, and large-file budgets; run
  it from this directory.
