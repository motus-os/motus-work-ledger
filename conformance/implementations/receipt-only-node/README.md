# Receipt-Only Node Emitter

This is a minimal independent implementation for Motus Level 0 conformance.

It does not import `/motus` or `motusos`. It reads a small input document, emits
a Work Receipt Envelope, computes the receipt self-hash, and writes JSON that
validates against the public conformance validator.

## Usage

Requires Node.js 20 or newer. The conformance workflow pins Node 20.

```bash
node conformance/implementations/receipt-only-node/emit-receipt.mjs \
  --input conformance/implementations/receipt-only-node/input.example.json \
  --output /tmp/motus-node-receipt.json

python conformance/validator/validate_receipt.py /tmp/motus-node-receipt.json
```

This implementation is deliberately receipt-only. It does not create Store
events, run commands, route work, or manage policy.
