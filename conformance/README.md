# Motus Work Ledger Conformance v0.1

This directory contains the first portable conformance surface for systems that
want to emit Motus-compatible receipts without importing `motusos`.

## Scope

The v0.1 conformance target includes:

- Level 0: Receipt-only.
- Level 1: Event-backed.
- Level 2: Governed handoff.

A Level 0 implementation can:

1. emit a Work Receipt Envelope,
2. validate it against `schemas/work-receipt-envelope.schema.json`,
3. preserve canonical JSON hashing,
4. pass the golden fixture checks.

A Level 1 implementation can:

1. emit a Store export with a bounded run and ordered append-only events,
2. derive a Work Receipt from those events,
3. validate the Store export, Work Receipt, and projection manifest,
4. preserve source-export digest linkage,
5. produce deterministic output.

A Level 2 implementation can:

1. represent a governed handoff as Store events and a strict Work Receipt,
2. preserve evidence references through the receipt and handoff projection,
3. represent pending acceptance without taking over approvals,
4. align `route_summary.next_actor` with `handoff.receiver`,
5. prove the handoff projection can be reconstructed from the source export.

## Commands

Run all bundled conformance checks:

```bash
python conformance/validator/check_conformance.py
```

Validate the bundled fixtures:

```bash
python conformance/validator/validate_receipt.py \
  conformance/fixtures/valid/work-receipt-minimal.json \
  conformance/fixtures/valid/work-receipt-github-action.json
```

Validate an external receipt:

```bash
python conformance/validator/validate_receipt.py path/to/receipt.json
```

Generate and validate the bundled receipt-only second implementation:

```bash
python conformance/implementations/receipt-only-python/emit_receipt.py \
  --input conformance/implementations/receipt-only-python/input.example.json \
  --output /tmp/motus-receipt.json
python conformance/validator/validate_receipt.py /tmp/motus-receipt.json
```

Generate and validate the bundled event-backed second implementation:

```bash
python conformance/implementations/event-backed-python/emit_from_events.py \
  --input conformance/implementations/event-backed-python/input.example.json \
  --output-dir /tmp/motus-work-ledger-event-backed
python conformance/validator/validate_receipt.py \
  /tmp/motus-work-ledger-event-backed/receipt.json
```

Generate and validate the bundled governed handoff implementation path:

```bash
python conformance/implementations/event-backed-python/emit_from_events.py \
  --input conformance/implementations/event-backed-python/input.governed-handoff.json \
  --output-dir /tmp/motus-work-ledger-governed-handoff
python conformance/validator/validate_receipt.py \
  /tmp/motus-work-ledger-governed-handoff/receipt.json
```

## Canonical Hash

The validator computes SHA-256 over UTF-8 JSON with sorted keys and compact
separators after removing the self-referential `receipt_id` and
`hashes.receipt` fields. The computed hash must equal both `receipt_id` and
`hashes.receipt.value`. If `conformance/golden/<fixture-name>.sha256` exists,
the computed hash must match that golden value.

## Non-Goals

This conformance suite does not validate agent behavior, workflow routing,
policy compliance, or hosted orchestration. It validates the portable receipt
shape, event-backed projection mechanics, and governed handoff record shape.
