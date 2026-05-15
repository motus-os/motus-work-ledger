# Event-Backed Python Implementation

This is a Level 1 conformance implementation. It emits a Store export with a
bounded run and append-only work events, then derives a Work Receipt projection
from those events.

It is intentionally small and uses only the Python standard library. It does
not import `motusos` or `/motus`.

## Run

```bash
python conformance/implementations/event-backed-python/emit_from_events.py \
  --input conformance/implementations/event-backed-python/input.example.json \
  --output-dir /tmp/motus-work-ledger-event-backed
python conformance/validator/validate_receipt.py \
  /tmp/motus-work-ledger-event-backed/receipt.json
```

The command writes:

- `store-export.json`
- `receipt.json`
- `projection-manifest.json`

## Scope

This implementation proves Level 1 portability only:

- ordered events,
- Store export shape,
- deterministic receipt projection,
- source export hash linkage,
- no `/motus` dependency.

It does not implement workflow routing, policy decisions, hosted orchestration,
or signature/attestation verification.
