# Contributing to Motus Work Ledger

Motus Work Ledger is the canonical portable model for Motus-compatible Work
Receipts. Contributions should improve schemas, semantic conventions,
conformance fixtures, validation behavior, examples, or documentation.

## Repository Layout

- `spec/` - Work Ledger model, receipt envelope, canonicalization, and conformance docs.
- `schemas/` - JSON schemas for Work Receipts and related objects.
- `semconv/` - Semantic conventions and schema mapping.
- `conformance/` - Validator, fixtures, golden hashes, and second implementations.
- `examples/` - Human-readable examples for common work receipt scenarios.
- `docs/` - Implementation, privacy, adoption, terminology, and reference docs.

## Development Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r conformance/validator/requirements.txt
```

## Validate Fixtures

```bash
python conformance/validator/validate_receipt.py \
  conformance/fixtures/valid/work-receipt-minimal.json \
  conformance/fixtures/valid/work-receipt-github-action.json
```

Validate the receipt-only second implementation:

```bash
python conformance/implementations/receipt-only-python/emit_receipt.py \
  --input conformance/implementations/receipt-only-python/input.example.json \
  --output /tmp/motus-work-receipt.json
python conformance/validator/validate_receipt.py /tmp/motus-work-receipt.json
```

## Pull Request Expectations

1. Keep the model workflow-neutral.
2. Do not add workflow routing, orchestration, policy-engine, model-router, or compliance-product claims.
3. Keep schemas and semantic conventions aligned.
4. Add negative fixtures when tightening validation.
5. Update examples when changing schema-visible behavior.
6. Run the validator before opening a pull request.

## Commit Messages

Use concise conventional-style messages when practical:

```text
docs: clarify Work Receipt envelope
schema: tighten evidence redaction enum
test: add invalid receipt fixture
```

