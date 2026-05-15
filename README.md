# Motus Work Ledger

> Motus Work Ledger is a workflow-neutral model for consequential human, AI,
> CI, and tool-driven work. It records work as append-only events and produces
> verifiable Work Receipts.

This repository is the canonical portable surface for Motus-compatible Work
Receipts. It defines schemas, semantic conventions, conformance fixtures,
validation rules, and examples that other systems can implement without using
the `/motus` reference CLI.

## Why Work Needs A Ledger

Important work often disappears into pull requests, tickets, CI logs, chat,
agent transcripts, scripts, and memory. Later, a reviewer needs direct answers:

1. What work was attempted?
2. Who or what performed it?
3. What evidence existed?
4. What outcome was claimed?
5. What was accepted?
6. What should happen next?

Motus Work Ledger gives those answers a common structure.

## Core Model

```text
Work Journal -> Work Ledger -> Work Receipt
```

- The **Work Journal** is the append-only event stream.
- The **Work Ledger** is the organized durable work truth.
- The **Work Receipt** is the portable proof object projected from that truth.

## What This Repo Contains

- `spec/` - Work Ledger RFC, receipt envelope, canonicalization, and conformance docs.
- `schemas/` - strict JSON schemas for receipts and related objects.
- `semconv/` - common semantic attributes and schema mapping.
- `conformance/` - validator, fixtures, golden hashes, and second implementations.
- `examples/` - receipts for common human, AI, CI, and tool-driven work.
- `docs/` - implementation, privacy, terminology, and adoption guidance.

Versioning and release notes:

- [Versioning](VERSIONING.md)
- [Changelog](CHANGELOG.md)
- [Schema Registry](schemas/index.json)
- [Batch Recap Template](docs/batch-recap-template.md)
- [External Review Package](docs/external-review-package.md)
- [Controlled Design-Partner Pilot](docs/design-partner-pilot.md)

## Validate A Receipt

Install the validator dependency:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r conformance/validator/requirements.txt
```

Validate bundled receipts:

```bash
python conformance/validator/validate_receipt.py \
  conformance/fixtures/valid/work-receipt-minimal.json \
  conformance/fixtures/valid/work-receipt-github-action.json
```

Generate and validate the receipt-only second implementation:

```bash
python conformance/implementations/receipt-only-python/emit_receipt.py \
  --input conformance/implementations/receipt-only-python/input.example.json \
  --output /tmp/motus-work-receipt.json
python conformance/validator/validate_receipt.py /tmp/motus-work-receipt.json
```

## Relationship To `/motus`

`/motus` is the reference implementation. It provides the CLI, Store-backed
runtime, adapters, and compatibility paths that exercise this model.

This repository is the canonical portable model. Other systems can emit
Motus-compatible Work Receipts without importing or running `/motus`.

## Non-Goals

Motus Work Ledger is not:

1. a workflow engine,
2. an agent runtime,
3. a model router,
4. a hosted control tower,
5. a compliance product,
6. employee surveillance,
7. a blockchain,
8. a raw transcript archive.

Workflow tools do the work. Control planes steer the work. Motus records the
work. Receipts prove the work.
