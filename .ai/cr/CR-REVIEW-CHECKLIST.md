# CR Review Checklist

> Status: ACTIVE
> Scope: CR review gating checklist

This checklist must be completed for any CR that changes code, gates, or standards.

## Required (All)

- [ ] CR has a clear observation (file paths and behavior).
- [ ] Expected vs Actual is filled and specific.
- [ ] Root Cause is stated (not just symptoms).
- [ ] Proposed Fix is bounded and testable.
- [ ] Outcome Validation fields are complete.
- [ ] Evidence paths exist and are readable.
- [ ] Usage-path matrix included if behavior changes.
- [ ] User and agent interface regression coverage included when either interface changes.
- [ ] Confidence dimensions and thresholds are explicit when confidence gates route, block, merge, or release work.
- [ ] Owner set in coordination.db; status is in_progress or review.
- [ ] Related CRs referenced or marked as subsumed.
- [ ] Minification standard satisfied (ASCII only, no emoji, no attribution blocks).

## Reviewer Read Limits (Required)

- Token ceiling per single read: 1200 tokens max (tool output limit).
- Chunked reads required for large files (>= 400 lines).
- Chunk size: 200 lines per read (deterministic line ranges only).
- Deterministic chunk example:
  - sed -n '1,200p' path/to/file
  - sed -n '201,400p' path/to/file

## Review Notes (Required)

- Reviewer:
- Date:
- Verdict: APPROVE | CHANGES REQUESTED
- Findings (if any):

## References

- `.ai/CHANGE-PROTOCOL.md`
- `.ai/MINIFICATION-STANDARD.md`
- `docs/standards/OUTCOME-VALIDATION.md`
- `docs/standards/CONTEXTUAL-TEST-STANDARD.md`
