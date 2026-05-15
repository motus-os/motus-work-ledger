# Motus Work Ledger Conformance v0.1

This directory contains the first portable conformance surface for systems that
want to emit Motus-compatible receipts without importing `motusos`.

## Scope

The v0.1 conformance target is Level 0: Receipt-only.

A Level 0 implementation can:

1. emit a Work Receipt Envelope,
2. validate it against `schemas/work-receipt-envelope.schema.json`,
3. preserve canonical JSON hashing,
4. pass the golden fixture checks.

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

## Canonical Hash

The validator computes SHA-256 over UTF-8 JSON with sorted keys and compact
separators after removing the self-referential `receipt_id` and
`hashes.receipt` fields. The computed hash must equal both `receipt_id` and
`hashes.receipt.value`. If `conformance/golden/<fixture-name>.sha256` exists,
the computed hash must match that golden value.

## Non-Goals

This conformance suite does not validate agent behavior, workflow routing,
policy compliance, or hosted orchestration. It validates the portable receipt
shape.
