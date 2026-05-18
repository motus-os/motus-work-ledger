# Workflow Gate Verification Standard

> Status: TEMPORARY - Until Phase F kernel enforcement ships
> Scope: All agent task execution during Phase 0 and Phase A
> Retirement: Auto-generate from kernel after RI-F-001 completes

---

## Purpose

Enforce workflow gates via process until the kernel can enforce via code. This standard makes gate verification non-skippable by embedding it in handoff documents.

---

## Execution Context (Required in All Handoffs)

Every handoff MUST specify WHERE work happens. Omitting this causes agents to work in wrong repos or miss already-fixed issues.

| Field | Required | Description |
|-------|----------|-------------|
| Target Repo | YES | Full path to repo where work will be done |
| Branch | NO | Default: `main` |
| Source of Truth | YES | What to verify against (e.g., `PyPI motusos 0.1.0`) |
| Issue Origin | If applicable | Where issue was discovered (may differ from target) |

**Multi-Repo Projects**: If issue exists in multiple repos, include a Cross-Repo Status table showing status in each.

---

## Gate Verification Section (Required in All Handoffs)

Every agent handoff MUST include this section. The drafting agent fills it. The reviewing agent verifies it.

### Exception: Provenance / Session Logs

The following archival log files are NOT required to include the Gate Verification section:
- `PROVENANCE-*.md`
- `SESSION-LOG-*.md`

These files are treated as historical records, not active work handoffs. If they reference an active CR/RI, that CR/RI must still have a proper handoff with Gate Verification.

```markdown
## Workflow Gate Verification

| Gate | Question | Pass? | Evidence |
|------|----------|-------|----------|
| G1 | Is execution context specified? | [ ] | Target repo, branch, source of truth |
| G2 | Are relevant standards loaded? | [ ] | List standards consulted |
| G3 | Is the task clearly understood? | [ ] | Restate task in own words |
| G4 | Does this conflict with existing artifacts? | [ ] | Cross-reference check results |
| G5 | Is approach aligned with standards? | [ ] | Which standards verify approach |
| G6 | Does this work follow FILE-POLICY? | [ ] | Files created/modified with justification |
| G8 | Was review triggered before completion? | [ ] | reviewer_session_id + approval_evidence_ref + reviewer_read_only (L2/L3 independent reviewer required; L0/L1 same-session requires compensating controls) |
| G9 | Do all verifications pass? | [ ] | Test/check results |

### Gate Failure Protocol

If ANY gate fails:
- [ ] Document why in "Evidence" column
- [ ] Do NOT proceed to next phase
- [ ] Escalate to human if blocked

## Preflight Risk Scan (Required)

Preflight MUST run `.ai/scripts/preflight-risk-scan.sh` to detect common friction
before work begins. This scan fails early with remediation guidance for:

- Missing handoff sections (Summary, Tests and Evidence)
- policy_commit mismatch vs origin/main
- review_inputs outside scope_allowlist or missing files

Reviewer: Verify each gate answer before approving handoff.
```

### Interface Regression Addendum

When a slice changes either of these surfaces:
- the user-facing operator interface
- the agent-facing execution interface

the handoff and review evidence must include explicit interface regression
coverage. G9 evidence is incomplete without that artifact.

Accepted evidence:
- usage-path matrix rows that name the affected interface
- deterministic regression matrix evidence
- closeout/operator summary evidence for governed path changes

### Architecture Packet Addendum

For L2/L3 work that changes workflow, release behavior, core interfaces, or
recurring control-plane standards, the handoff and review evidence must include
an architecture packet before implementation broadens beyond packet authoring.

Minimum packet contents:

- architecture doc
- interface catalog
- defect inventory
- documentation impact plan

G9 evidence is incomplete without these artifacts for qualifying work.

---

## Decision Record Schema (Append-Only)

When a gate passes, record it. This creates the audit trail the kernel will eventually enforce.

### Schema

```sql
-- Temporary: userland decision records
-- Future: kernel will generate these automatically

CREATE TABLE IF NOT EXISTS gate_decisions (
    id TEXT PRIMARY KEY,  -- {workflow_id}:{gate_id}:{timestamp_ms}
    workflow_id TEXT NOT NULL,
    gate_id TEXT NOT NULL,  -- G1, G2, G3, G5, G8, G9
    task_id TEXT,  -- P0-002, PA-001a, etc.
    agent_id TEXT NOT NULL,  -- claude-opus, codex-1, etc.
    decision TEXT NOT NULL CHECK (decision IN ('pass', 'fail', 'skip_approved')),
    evidence TEXT,  -- JSON blob of gate evidence
    reviewed_by TEXT,  -- reviewer_session_id
    reviewed_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for audit queries
CREATE INDEX IF NOT EXISTS idx_gate_decisions_task ON gate_decisions(task_id);
CREATE INDEX IF NOT EXISTS idx_gate_decisions_workflow ON gate_decisions(workflow_id);
```

### Record Format (Markdown Alternative)

If not using SQLite, append to `GATE-DECISIONS.md`:

```markdown
## Gate Decision: P0-002 / G5

- **Task**: P0-002 - Design 6-call API facade
- **Gate**: G5 - Is approach aligned with standards?
- **Agent**: gpt-pro
- **Decision**: PASS
- **Evidence**: Consulted PPP-0.1-SPEC.md invariants 1-6, API follows 6-call pattern
- **Reviewed By**: reviewer_session_id
- **Reviewed At**: 2025-12-29T14:30:00Z
```

---

## Handoff Template

Use this template for all agent handoffs during Phase 0/A.

```markdown
# Handoff: [Task ID] - [Task Title]

## Context
[What was done, current state]

## Artifacts Modified
- [file1.md] - [what changed]
- [file2.sql] - [what changed]

## Workflow Gate Verification

| Gate | Question | Pass? | Evidence |
|------|----------|-------|----------|
| G1 | Is execution context specified? | [x] | Target: /path/to/repo, Branch: main |
| G2 | Are relevant standards loaded? | [x] | PPP-0.1-SPEC.md, TERMINOLOGY.md |
| G3 | Is the task clearly understood? | [x] | Design 6-call API facade per D1 |
| G4 | Does this conflict with existing artifacts? | [x] | Checked TERMINOLOGY.md 6-call section |
| G5 | Is approach aligned with standards? | [x] | Follows PPP invariants 1-6 |
| G6 | Does this work follow FILE-POLICY? | [x] | Created .ai/specs/6-CALL-API.md per FILE-POLICY |
| G8 | Was review triggered before completion? | [x] | reviewer_session_id + approval_evidence_ref + reviewer_read_only recorded |
| G9 | Do all verifications pass? | [ ] | Pending independent review (reviewer_session_id pending) |

## For Reviewer

1. Verify gate answers are accurate
2. Check artifacts for issues
3. Record gate decisions
4. Approve or request changes

## Next Agent
[Who picks this up next and what they do]
```

---

## Integration with Existing Patterns

### Codex Review Pattern (Enhanced)

```
Builder drafts
    |
    v
Builder fills Gate Verification section
    |
    v
Independent reviewer reviews (verifies gates + technical review)
    |
    v
Reviewer records gate decisions
    |
    v
Builder fixes (if needed)
    |
    v
Gate proceeds
```

### Solo Mode Addendum

Solo refinement is allowed only under `.ai/DECISION-POLICY.md` and only for L0/L1.

Required additions when the same agent fills Builder + Reviewer roles (L0/L1 only):
- **G8 evidence**: reviewer_session_id recorded + review_auto_authorized + approval_source + approval_evidence_ref + reviewer_read_only logged.
- **G9 evidence**: tests + log entry appended to `.ai/audits/SOLO-REFINEMENT-LOG.md`.
- **Handoffs**: Builder/Reviewer/Ops handoffs still created, then archived per FILE-POLICY.

Headless SoD decision table (canonical):

| Scenario | Allowed | Evidence |
|---|---|---|
| Builder invokes headless wrapper and reviewer run writes artifact with runner-derived `reviewer_session_id`/`review_run_id` | YES | Independent session provenance in review artifact + preflight PASS |
| Builder manually writes independent review artifact text | NO | Missing independent reviewer session provenance |
| L2/L3 with `review_auto_authorized=yes` | NO | Tier policy requires independent review (`review_auto_authorized=no`) |
| Finalized independent review artifact rerun without explicit overwrite flag | NO | Output custody guard blocks late overwrite |

### Where Gates Apply

| Workflow | When to Verify |
|----------|----------------|
| wf-agent-task-v1.0.0 | Every task handoff |
| wf-code-review-v1.0.0 | Every code review |
| wf-cr-review-v1.0.0 | Every CR review |
| wf-evidence-v1.0.0 | Every evidence bundle |

---

## Failure Modes This Prevents

| Past Failure | How Gates Prevent It |
|--------------|---------------------|
| Agent works in wrong repo | G1: Execution context must be specified |
| Issue already fixed elsewhere | G1: Cross-repo status forces verification |
| Cross-document inconsistency | G2: Standards must be loaded and consulted |
| Scope drift | G3: Task must be restated, drift becomes visible |
| Conflicting definitions | G4: Cross-reference check catches terminology/API mismatches |
| Self-verification blindness | G8: Review must be triggered, different agent |
| Assumed vs verified | G5: Evidence column requires proof |
| File proliferation | G6: FILE-POLICY must be followed, files justified |
| No audit trail | Decision records create append-only log |

---

## Lifecycle

1. **Now (Phase 0/A)**: Manual enforcement via handoff templates
2. **Phase F (RI-F-001)**: Kernel enforcement ships
3. **Post Phase F**: This standard retires, gates auto-generate from kernel

---

*Temporary standard. Process enforcement until code enforcement.*
