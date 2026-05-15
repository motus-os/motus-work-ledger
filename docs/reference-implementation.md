# Reference Implementation

`/motus` is the reference implementation of Motus Work Ledger.

It provides:

1. a local CLI,
2. Store-backed runs and events,
3. receipt projection,
4. `motus wrap`,
5. GitHub Action adapter support,
6. compatibility work-loop commands.

This repository defines the canonical portable model. `/motus` should consume
this repo and validate generated receipts against it.

Other systems can emit Motus-compatible Work Receipts without importing or
running `/motus`.

