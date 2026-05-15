# External Review Package: v0.1.0-alpha.1

This package is for independent review of Motus Work Ledger as a portable
framework alpha.

## Review Target

Primary target:

- Repository: `motus-os/motus-work-ledger`
- Release: `v0.1.0-alpha.1`
- Release URL: https://github.com/motus-os/motus-work-ledger/releases/tag/v0.1.0-alpha.1
- Commit: `ba21c7c6d211dcb681881f6df098681241cf7401`

Reference implementation context:

- `/motus` remains the reference implementation.
- `/motus` canonical consumption is tracked separately in issue #7.
- Do not assume `/motus` has already consumed this repo as canonical truth.

## What To Review

1. Taxonomy:
   - Motus Work Ledger is the model/category.
   - Work Receipt is the portable proof artifact.
   - `/motus` is the reference implementation.
   - Store/runs/events/projections are reference implementation substrate.
2. Schema correctness:
   - every schema is strict where practical,
   - `schemas/index.json` maps ids to files,
   - schema ids match file `$id` values,
   - receipt examples validate.
3. Semantic convention alignment:
   - dotted attributes map through `semconv/schema-map.md`,
   - semconv enum values match schema enum values,
   - telemetry-only fields are not emitted into strict receipt JSON.
4. Conformance:
   - Level 0 receipt-only fixtures validate,
   - invalid fixtures are rejected,
   - generated receipt-only implementation does not import `/motus`,
   - generated receipt validates.
5. Governance:
   - branch protection and Quality Gates are sufficient for alpha,
   - CODEOWNERS and required review do not create unresolved merge traps,
   - release evidence is sufficient to reconstruct what was published.
6. Public positioning:
   - no control-plane, governance-OS, compliance-platform, surveillance, or
     standard-status overclaim,
   - Work Ledger language feels natural and workflow-neutral.

## Required Evidence To Inspect

Release assets:

- `SHA256SUMS.txt`
- `file-manifest.txt`
- `release-commit.txt`
- `release-tree.txt`
- `schema-registry.json`
- `schema-registry-check.json`
- `conformance-check.json`
- `examples-validation.json`
- `generated-receipt.json`
- `generated-receipt-id.txt`
- `generated-receipt-validation.json`
- `motus-work-ledger-v0.1.0-alpha.1-source.tar.gz`

Repository files:

- `README.md`
- `spec/MOTUS-WORK-LEDGER-RFC.md`
- `spec/work-receipt-envelope-v0.1.md`
- `spec/canonicalization.md`
- `spec/conformance-levels.md`
- `schemas/README.md`
- `schemas/index.json`
- `schemas/work-receipt-envelope.schema.json`
- `semconv/README.md`
- `semconv/schema-map.md`
- `conformance/README.md`
- `conformance/validator/check_schema_registry.py`
- `conformance/validator/validate_receipt.py`
- `conformance/implementations/receipt-only-python/emit_receipt.py`
- `docs/privacy-and-security.md`
- `docs/terminology.md`
- `VERSIONING.md`
- `CHANGELOG.md`

## Suggested Commands

```bash
git clone https://github.com/motus-os/motus-work-ledger.git
cd motus-work-ledger
git checkout v0.1.0-alpha.1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r conformance/validator/requirements.txt
python conformance/validator/check_schema_registry.py
python conformance/validator/check_conformance.py
python conformance/validator/validate_receipt.py examples/*/receipt.json
python conformance/implementations/receipt-only-python/emit_receipt.py \
  --input conformance/implementations/receipt-only-python/input.example.json \
  --output /tmp/motus-work-ledger-review-receipt.json
python conformance/validator/validate_receipt.py /tmp/motus-work-ledger-review-receipt.json
```

## Pass / Hold Criteria

Pass only if:

1. a third party can validate bundled receipts from the released repo,
2. a third party can emit and validate a Level 0 receipt without `/motus`,
3. schemas and semantic conventions align without undocumented translation,
4. release assets are sufficient to reconstruct the released artifact,
5. public language stays workflow-neutral and does not overclaim standard,
   compliance, control-plane, or surveillance status.

Hold if:

1. following the semantic conventions produces schema-invalid receipts,
2. schema registry resolution requires private knowledge,
3. conformance does not catch obvious invalid receipt shapes,
4. the release cannot be reconstructed from tag, manifest, and assets,
5. `/motus` is presented as the canonical portable model instead of the
   reference implementation,
6. Work Ledger language implies employee monitoring, all-work tracking,
   blockchain, compliance guarantee, or workflow control.

## Required Verdict Format

Use one of:

- `APPROVED`
- `APPROVED WITH CONDITIONS`
- `HOLD`

Include:

1. top findings ordered by severity,
2. exact file or release-asset references,
3. commands run,
4. confidence limits,
5. whether Motus Work Ledger is ready for a controlled design-partner pilot.
