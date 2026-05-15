# Receipt-Only Python Emitter

This is a minimal second implementation for Motus Level 0 conformance.

It does not import `motusos`. It reads a small input document, emits a Work
Receipt Envelope, computes the receipt self-hash, and writes JSON that validates
against the public conformance validator.

## Usage

```bash
python conformance/implementations/receipt-only-python/emit_receipt.py \
  --input conformance/implementations/receipt-only-python/input.example.json \
  --output /tmp/motus-receipt.json

python conformance/validator/validate_receipt.py /tmp/motus-receipt.json
```

This implementation is deliberately receipt-only. It does not create Store
events, run commands, route work, or manage policy.
