# Change Protocol for Motus Development

> Status: ACTIVE
> Scope: Change review protocol and gating

**Effective**: 2025-12-26
**Lesson Learned**: We shipped a partial race condition fix without proper review

---

## The Rule

**NO CHANGES WITHOUT REVIEW**

All code changes must be reviewed by a separate agent before commit.

---

## Process

### 1. PLAN (Architect Agent)
- Define what needs to change
- Identify affected files and code paths
- Identify the missing invariant (root cause)
- Bind the active roadmap item to `docs/standards/ROADMAP-ITEM-DEFINITION-STANDARD.md`
- Define a single defensive capability (not a patch list)
- Identify whether the user-facing operator interface or agent-facing execution interface changes
- Write acceptance criteria + usage-path coverage
- Decide whether the work is:
  - continuation of the same unfinished bounded slice, or
  - a new bounded work item that must be minted
- Confirm any explicit next-work routes point to real roadmap items and are executable from canon
- Confirm the item is bound to a reusable workflow class and is handoff-ready
  before release-start or governed execution begins
- If confidence affects routing, approval, or release, bind the confidence dimensions and thresholds that apply
- If the work pattern is expected to recur, bind a reusable intelligence reference or record why none is needed yet
- If the work changes workflow, release behavior, core interfaces, or recurring
  control-plane standards, create an architecture packet before implementation:
  - architecture doc
  - interface catalog
  - defect inventory
  - documentation impact plan
- If the work is seeded by prior release or workflow learnings, classify those
  learnings as `adopt_now`, `remediate_now`, or `defer_with_rationale` in the
  packet instead of relying on chat continuity
- The architecture packet is a supporting design artifact. It must not become a
  second planning system. The roadmap item, work contract, workflow contract,
  and handoff remain the authoritative execution surfaces.

Planning rule:
- Reuse the workflow class when the process is the same.
- Mint a new work item when thesis, acceptance, or deliverable changed
  materially.
- Do not silently widen a closed or completed work item just because the same
  workflow shape applies again.

### 2. IMPLEMENT (Builder Agent)
- Make the changes
- Write tests that match real usage paths (happy + exception)
- If an interface changes, include explicit interface regression coverage for that interface
- DO NOT COMMIT

### Scope And Mutation Discipline (Mandatory)
- Governed work must use explicit file targets. Do not run broad wildcard rewrites over shared handoff/audit surfaces.
- `scope_allowlist` in the active handoff is authoritative for tracked-file mutations.
- In cross-repo lanes, the destination repo that owns the resulting governed data contract must own the authoritative handoff and `scope_allowlist`.
- Source repos may appear as explicit allowlist entries and review inputs, but they must not define a competing handoff for the same lane.
- Cross-repo allowlist and review-input paths should use explicit sibling-relative form (`../<repo>/...`) rather than host-specific absolute paths.
- Successful lease release is blocked when tracked changes are outside the active `scope_allowlist` (`STOP_RELEASE_SCOPE_FILE_OUTSIDE_ALLOWLIST`).
- If broader mutation is truly required, expand handoff scope explicitly and re-run gates/review.
- Test fixtures for artifacts must use test-only IDs (for example, `RI-TEST-*`) and must not reuse canonical production IDs.

### 3. REVIEW (Reviewer Agent - DIFFERENT from Builder)
- Verify changes match plan
- Check for gaps (like the LeaseStore gap we missed)
- Run reality checks on actual code paths
- Block if user or agent interface changes lack explicit regression evidence
- For workflow/interface/release-system work, block if the architecture packet
  is missing or if standards/doc updates do not match the packet
- Block if the architecture packet duplicates or contradicts roadmap item, work
  contract, workflow contract, or handoff truth instead of tightening them
- Approve or request changes

### 4. COMMIT (Only after Review approval)
- Include review findings in commit message
- Reference the reviewer
- Merge and push only from a clean merge worktree (no unrelated changes); create a clean merge worktree if needed.

---

## Signals and CR Promotion

If a gap is observed but not yet root-caused, log it first as a signal:

- Log in `.ai/signals/SIGNAL-LOG.md`
- Track repetition or impact before CR creation
- Promote to a CR when the signal repeats or a deterministic fix is known

This prevents ad-hoc CRs and keeps root-cause work deliberate.

---

## How to Invoke Review

```
# Option 1: Spawn a review agent
Task(subagent_type="general-purpose", prompt="""
REVIEW AGENT - You are reviewing changes made by another agent.

FILES CHANGED:
- [list files]

CLAIMED FIX:
- [what was supposedly fixed]

YOUR JOB:
1. Read the actual code changes
2. Verify they do what's claimed
3. Check for gaps (other code paths, edge cases)
4. Run reality check tests
5. Report: APPROVED or BLOCKED with reasons
""")

# Option 2: Use /dev-review skill
Skill(skill="dev-review")
```

---

## Reality Check Template

For every security fix, run this:

```python
# Does the fix ACTUALLY work?
# Test the specific attack vector
# Verify in the actual code path (not just unit tests)
# Check if there are parallel code paths that need the same fix
```

---

## Contextual Correctness (Tests Must Match Usage)

Tests are only valid if they reflect how the product is used:
- Cover the happy path users actually take
- Cover the exception path users actually hit
- Cover parallel code paths that share the invariant
- Avoid "1+1=2" tests that prove nothing about real behavior

Document the usage-path coverage in the CR.

## Tool Resolution Standard

Governed scripts must resolve the Motus CLI in a deterministic order:

1. Standard path: use `motus` from `PATH` when it is schema-compatible with the live coordination DB
2. Workflow-owned correction: if the PATH CLI is provably schema-behind, governed scripts may auto-route once to the canonical repo-backed Motus wrapper
3. Exception path: export `MOTUS_BIN=/absolute/path/to/motus-wrapper`
4. Do not hardcode a builder-local binary path inside shared scripts

Auto-routing to the canonical repo-backed wrapper is part of the standard governed
workflow, not an agent improvisation.

Use the explicit `MOTUS_BIN` exception path only when a compatible wrapper must be
selected deliberately and record that reason in the CR evidence.

The exception path is for controlled recovery and parity work, not a permanent fork of
the standard execution model.

If an explicit `MOTUS_BIN` override is schema-behind, the run must fail closed with
deterministic remediation. Raw DB-level `schema_fallback` is controlled recovery only
and must not count as normal-path success.

## Governed Execution Source Routing

Execution-source correction is workflow-owned. Agents should not decide ad hoc
whether to keep running from a dirty root, remint manually, or reuse stale
state.

Standard path:

1. Builder runs invoked from a canonical root or other non-compliant source
   should auto-remint once into a clean worktree before governed execution.
2. Canonical root starts always remint from current `origin/main`.
3. The reminted worktree becomes the only valid governed execution source for
   the run.

Exception path:

1. Reviewer runs do not auto-remint the source.
2. If auto-remint is explicitly disabled, the runner must fail closed with a
   deterministic remediation command.
3. Manual root execution remains invalid even when a remediation path is
   available.

This keeps the decision bounded and deterministic:

- standard route = workflow-managed remint once
- exception route = fail closed with remediation
- no agent-local improvisation

For new governed CR or RI work, the standard bootstrap is:

1. `.ai/scripts/start-governed-work.sh <CR-or-RI> --agent ... --intent "..."`
   - this is the workflow-owned standard path
   - it registers the CR when needed
   - it bootstraps existing RIs from their roadmap row instead of forcing a CR-only path
   - it bootstraps the canonical handoff path when needed
   - it binds deterministic session/run metadata
   - after a successful claim, it reconciles the canonical handoff to the live claim state (`Claim status`, `Lease id`, `Lease expires`)
   - re-runs preserve existing handoff session/run ids unless explicitly overridden
   - any `--handoff` override must stay repo-relative under the current repo root
   - it claims through `.ai/scripts/motus-work-claim.sh`
   - it resolves workflow-owned route surfaces from the canonical workflow contract registry under `.ai/contracts/workflows/`

Lower-level primitives remain available as exception/recovery paths:

1. `.ai/scripts/register-change-request.sh CR-... --title "..."`
   - lower-level registration bootstrap only
   - it must use `.ai/scripts/motus-db-read.sh` + `.ai/scripts/motus-db-write.sh`
   - it must not hand-edit `coordination.db` or bypass the broker
2. `.ai/scripts/motus-work-claim.sh CR-... --agent ...`
   - lower-level claim primitive for existing governed packets
   - if a canonical `.ai/handoffs/HANDOFF-CODEX-<WORK_ITEM>.md` already exists, the wrapper may resolve it automatically

Do not hand-edit `coordination.db` unless you are explicitly repairing a broken bootstrap path
and the exception is recorded in the CR evidence.

---

## What We Learned

| Issue | What Happened | Prevention |
|-------|---------------|------------|
| Partial fix | Fixed ClaimRegistry but not LeaseStore | Review agent checks ALL code paths |
| Skipped tests | Marked concurrency tests as skip | Review agent questions skipped tests |
| Smooth = suspicious | Fast progress felt good but masked gaps | Reality checks mandatory |

---

## Enforcement

Before any commit with security implications:
- [ ] Review agent spawned and completed review
- [ ] Reality check run on actual code paths
- [ ] All affected code paths identified and addressed (or documented as deferred)
- [ ] Usage-path coverage documented (happy + exception)
- [ ] Interface regression coverage documented when user or agent interface changes
- [ ] Confidence dimensions/thresholds documented when confidence gates route, block, merge, or release work
- [ ] CR-REVIEW-CHECKLIST.md completed (includes minification gate)
- [ ] Decision Policy checked (auto-approval scope or stop condition)

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `.ai/cr/CR-REVIEW-CHECKLIST.md` | Mandatory review gates |
| `.ai/DECISION-POLICY.md` | Auto-approval scope + stop conditions |
| `.ai/MINIFICATION-STANDARD.md` | No emojis, no attribution blocks |
| `.ai/AGENT-ETHOS.md` | Work Loop + Six Perspectives |

---

*"Trust but verify" - but actually verify.*
