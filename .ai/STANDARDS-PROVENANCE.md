# Standards Provenance

This repository carries repo-local Motus gate standards so agents do not rely on
ambiguous fallback paths.

## Source

- Source repo: operator-approved Motus standards source
- Clean source worktree: recorded in batch evidence, not committed as public repo truth
- Baseline source commit: `623d149060d8a2b2f6d4c0462ddbf253d25e43f9`
- Baseline work item: `motus-work-ledger#23`
- Store-first modernization work item: `motus-work-ledger#35`
- Claim evidence: `https://github.com/motus-os/motus-work-ledger/issues/35#issuecomment-4478970032`

## Files

| File | SHA-256 |
| --- | --- |
| `.ai/WORKFLOW-GATE-STANDARD.md` | `f6cc6fb61966da0738d095f62e663969354bf2327a4f3649dbc0d77298f2b4f2` |
| `.ai/CHANGE-PROTOCOL.md` | `f7dba68508875bc85d9d44e3ea392ca49cd0da5a8388e18235cf3527ecf080a8` |
| `.ai/cr/CR-REVIEW-CHECKLIST.md` | `da8a3c66dcbde7abaa74f617e40236d70dce311bdf924d9a4d58d5b0ac6cfd5d` |
| `.ai/RELEASE-STANDARD.md` | `b3c0f1b64c1875a00924a69158ab80a0f71a212b119ab2b399d06260673e8741` |

## Resolution Rule

Agents working in this repository must load these repo-local standards before
making code or documentation changes. These files are the repo-local gate
baseline, not a complete copy of every supplemental Motus standard ever
referenced by the copied text.

If a loaded repo-local standard references a supplemental standard that is not
present in this repository, resolve that supplemental reference through the
operator-approved Motus standards source recorded in batch evidence, or stop and
ask if the required source is unclear. Do not treat the absence of a
supplemental reference as permission to ignore the loaded repo-local standards.

The copied `CHANGE-PROTOCOL.md` was whitespace-normalized to satisfy repository
diff hygiene; the hash above reflects that normalization.
