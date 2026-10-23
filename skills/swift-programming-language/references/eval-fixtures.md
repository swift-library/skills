# Eval Fixtures

## Single-Owner Storage And Compatibility

Input: A package needs storage for a noncopyable element and asks whether
UniqueBox or UniqueArray can replace its existing container. Compiler and
deployment requirements are supplied.

Expected behavior: checks compiler support and each API's SDK availability,
keeps older supported paths, and chooses storage by ownership requirements.
Explains consuming transfer, borrowed access/iteration and the Copyable
constraint on cloning, without claiming an unmeasured performance benefit.

Acceptance checks: compile and run mutation, consumption and borrowing
iteration, then reuse the container after iteration. Verify independent
copyable clones. Reject use after consumption and cloning noncopyable contents.
Check an older deployment target's availability diagnostics without treating
that compilation as an older-system runtime test.

## Temporary Buffer Initialization And Lifetime

Input: A routine needs a temporary typed buffer and raw-byte scratch space.
It may throw after initializing only part of the reserved capacity.

Expected behavior: initializes through OutputSpan/OutputRawSpan before reading,
keeps borrowed views in the allocation closure, and preserves cleanup on normal
and throwing exits. Does not promise that temporary storage is always on stack.

Acceptance checks: verify initialized typed-element destruction on both exit
paths and rejection of an escaping temporary view. Capacity alone must not be
treated as initialized elements.

## Byte Conversion, Bounds And Endianness

Input: Parse a fixed-width integer from a potentially unaligned byte offset
under a protocol-defined byte order, while preserving older platform support.

Expected behavior: uses the declared conversion constraints, checks input
length before loading, and gates byte-order APIs independently from basic
span/temporary-allocation availability. Does not equate native memory layout
with a stable wire format or treat a bounds-checked load as format validation.

Acceptance checks: round-trip an integer at an unaligned offset with explicit
byte order; reject an unsupported load type; verify out-of-bounds failure in
an isolated probe. Inspect each selected SDK declaration and preserve supported
fallbacks.

## Output Proportionality

Input: Ask what `defer` does, or request a small local correction to one Swift
routine.

Expected behavior: answer the question directly; for the correction, summarize
the change, validation, and open risks.

Input: Request an audit of a package's Swift language compatibility.

Expected behavior: use all six Output Format sections, beginning with
Phase / stage judgment, and keep compatibility findings and risks explicit.

Acceptance checks: the question and small correction use the short path; the
audit retains every named section from `SKILL.md`.
