# Standards Provenance

This repository carries repo-local Motus gate standards so agents do not rely on
ambiguous fallback paths.

## Source

- Source repo: operator-approved Motus standards source
- Clean source worktree: recorded in batch evidence, not committed as public repo truth
- Source commit: `623d149060d8a2b2f6d4c0462ddbf253d25e43f9`
- Work item: `motus-work-ledger#23`
- Claim evidence: `https://github.com/motus-os/motus-work-ledger/issues/23#issuecomment-4478396186`

## Files

| File | SHA-256 |
| --- | --- |
| `.ai/WORKFLOW-GATE-STANDARD.md` | `f6cc6fb61966da0738d095f62e663969354bf2327a4f3649dbc0d77298f2b4f2` |
| `.ai/CHANGE-PROTOCOL.md` | `f7dba68508875bc85d9d44e3ea392ca49cd0da5a8388e18235cf3527ecf080a8` |
| `.ai/cr/CR-REVIEW-CHECKLIST.md` | `da8a3c66dcbde7abaa74f617e40236d70dce311bdf924d9a4d58d5b0ac6cfd5d` |
| `.ai/RELEASE-STANDARD.md` | `60758d09bda021c1b0b5568d2751e9babd1333fa8f84d25ad5f934e51264e65d` |

## Resolution Rule

Agents working in this repository must load these repo-local standards before
making code or documentation changes. Fallback to another standards checkout is
not needed while these files are present.

The copied `CHANGE-PROTOCOL.md` was whitespace-normalized to satisfy repository
diff hygiene; the hash above reflects that normalization.
