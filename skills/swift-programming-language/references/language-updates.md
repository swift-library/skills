# Swift Language Updates

Keep the project's supported toolchain, language mode, SDK and deployment
target separate. New syntax requires a compiler that parses it; a newer
compiler does not by itself authorize raising the minimum OS or enabling every
upcoming feature. The existing baseline in `rules/baseline.md` remains
conditional on project facts.

## Swift 6.3 / 6.4

- Swift 6.3 module selectors such as `Swift::Int` disambiguate a module from a
  same-named type. Use them for real ambiguity; existing unambiguous qualified
  names need no blanket rewrite.
- Swift 6.4 permits optional opaque and existential spellings such as
  `some Value?` and `any Value?`, equivalent to `(some Value)?` and
  `(any Value)?`. Keep the parenthesized forms for older compiler compatibility.
  Protocol compositions still need parentheses: `any (Value & Named)?` is
  valid, while `any Value & Named?` is rejected. See SE-0521 in the source map.
- Swift 6.4 supports `anyAppleOS` in availability declarations, for example
  `@available(anyAppleOS 27.0, *)`. Continue to check each API's platform
  exclusions; a shared availability spelling does not make every Apple API
  available on every platform.

## Source-level warning control

Swift 6.4 adds `@diagnose` (SE-0522) for a specific compiler warning group in a
declaration's signature and lexical scope. Read the actual diagnostic group
before choosing a control; the behavior identifiers are `error`, `warning`,
and `ignored`, without a leading dot:

```swift
@diagnose(DeprecatedDeclaration, as: warning,
          reason: "Retained compatibility bridge")
func bridgeToLegacySystem() {
  oldAPI()
}
```

Here `oldAPI()` represents an existing deprecated API. The attribute can make
its warning remain a warning even under `-warnings-as-errors`; unrelated
declarations keep their configured policy. Nested declarations can refine the
enclosing control. It cannot downgrade a genuine compilation error.

Keep the project's warning policy. Use local control for a justified exception,
not as a replacement for diagnosing the underlying problem. `reason:` is an
optional string literal, not interpolated text. Older compilers need their
existing supported diagnostic path; do not insert the new attribute
unconditionally.

Async cleanup, isolation and task cancellation changes, and Swift Testing
assertions, interoperability and test-runner behavior, are out of scope for this
reference. Session examples are leads until the current declaration
and a small compiler probe confirm the exact shape. In particular, do not
promote a `mapKeyedValues` spelling solely from a session mention when it cannot
be found in the selected standard library.

Use `official-sources.md` for source verification. Record compiler and runtime
results in the calling repository's validation logs, not as a universal readiness
claim in this reference.

## Uniquely owned storage

Swift 6.4 adds `UniqueBox` (SE-0517) for one heap-owned value and
`UniqueArray` (SE-0527) for a growing buffer, including `~Copyable` values.
Choose them when the API needs one owner or noncopyable elements. Keep ordinary
`Array` for copyable values when its value semantics fit; removing copy-on-write
does not eliminate buffer growth or prove a performance improvement.

Both containers are noncopyable. Assignment transfers ownership; a later use
of the consumed container is invalid. `UniqueBox.value` supports borrowed reads
and in-place mutation; `consume()` transfers the value out and releases the
box allocation. `clone()` explicitly allocates a new container and requires
copyable contents.

```swift
struct Item: ~Copyable {
  var identifier: Int
}

@available(anyAppleOS 27.0, *)
func inspectItems() {
  var box = UniqueBox(Item(identifier: 1))
  box.value.identifier = 2
  let item = box.consume()

  var items = UniqueArray<Item>()
  items.append(item)
  for element in items {
    print(element.identifier)
  }
}
```

The loop borrows the noncopyable elements through `Iterable` (SE-0516);
iteration leaves the container usable. Inspect iterator lifetime and throwing
requirements before generalizing an algorithm from `Sequence`.

Check compiler support and the selected standard library's availability. The
Apple SDK marks these containers `@available(anyAppleOS 27.0, *)`; place code
that uses them behind the project's appropriate availability boundary. Retain
existing storage paths for older compilers and deployment targets. Ownership
does not imply thread safety; concurrency still depends on the element and
isolation contracts.

## Temporary storage and raw bytes

Swift 6.4 adds `withTemporaryAllocation` (SE-0524). Its typed overload passes
an `inout OutputSpan<T>`; the raw-byte overload passes an `inout OutputRawSpan`.
Capacity reserves uninitialized storage: initialize elements with `append`
before reading them. The typed overload destroys initialized elements on both
normal and throwing exits, and both overloads release the temporary storage.
Keep borrowed views within the closure; do not return a span into that storage.
Stack allocation is an optimization, not a guarantee.

SE-0525 adds bounds-checked, unaligned `RawSpan` and `MutableRawSpan` loads for
`ConvertibleFromBytes` types. Safe byte stores and appends additionally require
`ConvertibleToBytes`; `BitwiseCopyable` alone does not establish either
conversion contract. For example, arbitrary bytes cannot be loaded as `Bool`.
Validate input length before a load because an out-of-bounds access traps.
These operations do not validate a binary format or provide atomic access.

```swift
@available(anyAppleOS 27.0, *)
func readHeader() -> UInt32 {
  withTemporaryAllocation(byteCount: 4, alignment: 4) { output in
    output.append(UInt32(0x01020304), as: UInt32.self, .bigEndian)
    return output.bytes.load(fromByteOffset: 0, as: UInt32.self, .bigEndian)
  }
}
```

Use explicit byte order for a format that defines it. Reading native memory
does not make a type's layout a stable wire or file format. The Swift 6.4 Apple
SDK gives the basic span and temporary-allocation APIs back-deployed
availability, while `ByteOrder` and the byte-order overloads require OS 27.
Check each declaration instead of applying one OS requirement to the whole
family. Preserve the established initialization and cleanup path for older
compilers, and test older supported systems separately.

Exercise the storage and byte-contract cases in `eval-fixtures.md` when changing
this guidance or its examples.
