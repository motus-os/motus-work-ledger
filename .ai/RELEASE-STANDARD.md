# Release Standard

> Status: AUTHORITATIVE
> Version: 1.0.0
> Effective: 2026-01-05

This document defines the complete release process for Motus. All releases MUST follow this standard.

---

## Versioning Contract

Motus follows SemVer with pre-1.0 semantics:

```
0.FEATURE.PATCH
```

| Version Type | Pattern | May Break? | Requirements |
|--------------|---------|------------|--------------|
| Feature Release | `0.X.0` | YES | Full release cycle |
| Hardening Release | `0.X.Y` | NO | Abbreviated cycle |
| Stable Release | `1.0.0+` | Major only | Full cycle + LTS |

### Feature Release (0.X.0)

New capabilities that MAY include breaking changes.

**Examples:**
- `0.2.0` = Boundary hardening (new enforcement)
- `0.3.0` = Payment integration (new module)

**Breaking changes MUST be:**
- Documented in CHANGELOG with `**BREAKING:**` prefix
- Announced in release notes
- Include migration guide if applicable

### Hardening Release (0.X.Y)

Improvements that SHOULD NOT break existing usage.

**Examples:**
- `0.1.2` = Failure mode test coverage
- `0.2.1` = Timeout handling improvements

**Allowed changes:**
- Test additions
- Error message improvements
- Performance optimizations
- Bug fixes
- Documentation updates

**NOT allowed:**
- API signature changes
- New required parameters
- Stricter validation that rejects previously-valid input
- Behavior changes that break existing code

---

## Release Types

### Type A: Feature Release (0.X.0)

Full 8-phase cycle required.

| Phase | Gate | Required |
|-------|------|----------|
| 1. Planning | Scope locked | YES |
| 2. Build | CI green | YES |
| 3. Test | Full suite passes | YES |
| 4. Harden | Security clean | YES |
| 5. Website Sync | Docs updated | YES |
| 6. Canary | 24h internal | YES |
| 7. Release | PyPI published | YES |
| 8. Announce | Notes published | YES |

### Type B: Hardening Release (0.X.Y)

Abbreviated 5-phase cycle.

| Phase | Gate | Required |
|-------|------|----------|
| 1. Planning | Scope defined | YES |
| 2. Build | CI green | YES |
| 3. Test | Full suite passes | YES |
| 4. Harden | Security clean | YES |
| 5. Release | PyPI published | YES |

**Skipped for hardening:**
- Website sync (unless docs changed)
- Canary (tests are sufficient)
- Formal announcement (changelog entry is sufficient)

---

## Stabilization Mode (Mandatory Until 0.4.0)

Motus is currently stabilizing the `0.3.x` line.

Standard path:

1. One bounded slice ships per hardening release.
2. The release records a single thesis and explains why the live product is
   materially better.
3. Residual friction discovered mid-slice is routed into the next slice instead
   of widening the current release.

Exception path:

1. Multiple completed slices may share one hardening release only when they
   support the same release thesis.
2. The publish decision must list the included slice IDs explicitly.

Required stabilization artifacts:

- `.ai/releases/RELEASE-X.Y.Z-BASELINE.md`
- `.ai/releases/RELEASE-X.Y.Z-PUBLISH-DECISION.md`
- `.ai/releases/RELEASE-X.Y.Z-SCORECARD.md`
- `.ai/releases/RELEASE-X.Y.Z-LEARNINGS.md`

These four artifacts are the continual-improvement loop:

1. baseline = what is being improved now
2. publish decision = ship now / hold
3. scorecard = what actually shipped
4. learnings = what becomes the next slice

### Learning Adoption Loop (Mandatory)

When a release surfaces workflow, interface, or release-system friction, the
next hardening work item must bind directly to the prior release learnings and
classify them as:

1. `adopt_now`
2. `remediate_now`
3. `defer_with_rationale`

If that next hardening work changes workflow, release behavior, or recurring
control-plane standards, it must open with an architecture packet before
implementation. The packet must include:

- architecture doc
- interface catalog
- defect inventory
- documentation impact plan

Do not add a second planning system for this. Use the existing release cycle
and release artifacts.

End-of-release requirement:

1. the release must emit exact next candidate work from the learnings artifact
2. that next candidate must be framed as a bounded work item or explicit
   terminal `complete`
3. the next candidate must be materialized in the canonical roadmap/work-item
   surface before the next lane starts
4. the next release or hardening lane starts only after that next candidate is
   approved

This keeps recursive improvement at the end of the release loop instead of
restarting informally from operator memory or chat.

### Release-Start Readiness Sweep (Mandatory)

Before a hardening or feature release starts its governed execution lane, every
included bounded slice must pass a readiness sweep.

The readiness sweep must prove that each included slice:

1. exists as a canonical roadmap/work-item entry,
2. is correctly classified as either:
   - continuation of the same unfinished bounded slice, or
   - a new bounded work item minted from prior release or workflow truth,
3. is bound to a reusable workflow class or workflow contract,
4. is handoff-ready (`canonical_handoff_present` or `compilable_from_canon`),
5. has explicit route on success and route on failure targets that resolve from
   canon or terminate explicitly,
6. does not rely on ad hoc packet authoring during the release itself.

If the sweep fails:

1. stop the release-start lane,
2. open or route to the corrective readiness work item,
3. tighten the standards, roadmap item, workflow binding, or handoff path
   before continuing.

Do not build missing work-item topology on the fly inside the release packet.
The release should start from executable item truth, not reconstruct it.

---

## Release Candidate Materiality (Mandatory)

Release-entry work must fail closed before packet assembly when the canonical
`/motus` candidate has no post-tag delta.

Applies to:

- publish-packet startup
- release-execution startup

Does not apply to:

- normal `/motus` product slices that create the candidate delta
- internal workflow-hardening or release-hygiene slices that are not starting
  the public release packet/execution lane

Decision rule:

1. resolve the canonical `/motus` candidate ref (`origin/main` when available,
   otherwise `HEAD`)
2. find the latest reachable public semver tag
3. fail closed when there are `0` commits beyond that tag

Workflow owner:

- `.ai/scripts/start-governed-work.sh`
- `.ai/scripts/check-release-candidate-materiality.sh`

This gate exists to remove agent memory from release admission. A zero-touch
operator should not need to reason manually about whether a publish packet or
release execution lane is materially justified.

---


## Outcome Validation (Mandatory)

Every feature must include an outcome validation bundle before it can be marked complete.
See `docs/standards/OUTCOME-VALIDATION.md` for required fields, evidence layout, and review checkpoints.

## Release Effectiveness Review Window (Mandatory)

Each release must schedule and complete effectiveness reviews for the next N releases.
Default window: N=3.

Required checkpoints:
- Pre-release baseline
- 7-day effectiveness review
- 30-day effectiveness review

Record review outcomes in `.ai/releases/RELEASE-X.Y.Z-LEARNINGS.md`.

## Release-Scope Decision (Mandatory)

Every hardening release must record an explicit release-scope decision before
publish:

- `SHIP_NOW`
- `HOLD_FOR_NEXT_TRAIN`
- `MERGE_ONLY_NO_PUBLISH`

Record the decision in `.ai/releases/RELEASE-X.Y.Z-PUBLISH-DECISION.md`.

The decision must name:

1. the release thesis
2. the included slice IDs
3. the material improvement for users/operators
4. residual risks
5. exact next slice candidates when publish is blocked or deferred

## Remote Branch Governance (Mandatory)

Every release must record a remote branch governance audit before publish or
defer decision.

Canonical artifact:

- `.ai/audits/REMOTE-BRANCH-GOVERNANCE-X.Y.Z.json`

Standard invocation:

```bash
.ai/scripts/check-remote-branch-governance.sh \
  --report .ai/audits/REMOTE-BRANCH-GOVERNANCE-X.Y.Z.json \
  --repo-root "${MOTUS_REPO_ROOT:?set MOTUS_REPO_ROOT}" \
  --repo-root "${MOTUS_WEBSITE_REPO_ROOT:?set MOTUS_WEBSITE_REPO_ROOT}" \
  --repo-root "${MOTUS_INTERNAL_REPO_ROOT:?set MOTUS_INTERNAL_REPO_ROOT}"
```

Set the three `*_REPO_ROOT` variables to the canonical checkout roots that the
release is responsible for auditing.

Fail-closed rules:

1. report `status = FAIL_CLOSED` blocks publish
2. any `UNKNOWN` remote branch classification blocks publish
3. apply mode requires explicit approval evidence and an active claimed work item

Decision rule:

1. if stale merged remote branches are present, the publish decision must state
   either:
   - cleanup applied, or
   - defer with explicit rationale
2. unmerged remote branch debt must be visible in the audit even when publish is
   not blocked
3. if cleanup was applied before publish, preserve both:
   - the apply-mode mutation report + command log
   - the final post-apply dry-run verification report

## Evidence Bundle (Mandatory)

Every release MUST produce an evidence bundle. Release is BLOCKED if any artifact fails.

**Fail-closed behavior:** If any artifact is missing or fails validation, the release is blocked. No bypass.

### Expanded Preconditions (Release Lane)

If the release process relies on Motus Expanded automation, these preconditions are mandatory:

- Context snapshot verifies (fail closed) per `docs/standards/CONTEXT-SNAPSHOT-STANDARD.md`.
- Coordination DB schema satisfies the minimal contract per `docs/standards/SCHEMA-TRANSACTION-CONTRACT.md`.
- Schema drift check passes per `.ai/scripts/check-schema-drift.sh`.

### Claims Posture (Mandatory)

Release management (RM) must maintain an explicit claims posture based on evidence of
enforcement at the acceptance boundary.

Stable-path artifacts:

- `.ai/audits/CLAIMS-POSTURE.md` (append-only log; dated sections)
- `.ai/audits/CLAIMS-POSTURE.json` (overwrite-in-place current state)

Claims must be either:

- allowed (with concrete evidence pointer), or
- blocked (with required CR(s) to unblock)

### Dry-Run Must Be Publish-Proof (Mandatory)

All dry-run release execution batches (no publish, no deploy) must be mechanically
publish-proof.

The publish credential denylist is owned by RM and must be checked by:

- `.ai/scripts/release-publish-credential-precheck.sh`

If any denylisted publish credential surface is present, the dry-run is BLOCKED.

RM dry-run execution must be invoked via a publish-proof wrapper that runs the
precheck before any release verification work begins.

For sync-verify dry-run batches, use:

- `.ai/scripts/release-sync-verify-no-publish.sh`

Running the underlying sync-verify script directly is forbidden in RM dry-run:

- `.ai/scripts/release-sync-verify.sh`

### RM Loop Trigger Entrypoint (Mandatory)

RM execution must be triggerable through a single deterministic entrypoint:

- `.ai/scripts/rm-release-loop.sh`

This entrypoint executes the RM loop in order:

1. Publish-proof sync verify (RM-ACT-2)
2. Proof-watch artifact + GO/NO-GO memo (RM-ACT-3)
3. Optional go-live + post receipts for public releases (RM-ACT-4/5)

The script returns deterministic exit codes so orchestrators (for example N8N)
can branch fail-closed without parsing prose.

Example (public proof-watch):

```bash
.ai/scripts/rm-release-loop.sh --release-id X.Y.Z --contract .ai/releases/RELEASE-X.Y.Z-SYNC-CONTRACT.json --release-class public --json-out .ai/audits/RM-LOOP-X.Y.Z.json
```

### RM Preconditions Contract (Mandatory)

Every RM run is fail-closed unless all preconditions below pass together:

1. `release_target` is explicit and equals `release_id` for the run.
2. Canonical release anchors exist in the control-plane repository for that target:
   - `.ai/releases/RELEASE-X.Y.Z-SCOPE-LOCK.json`
   - `.ai/releases/REQUIRED-SET-X.Y.Z.json`
   - `.ai/releases/RELEASE-X.Y.Z-SYNC-CONTRACT.json`
3. Promise-to-Truth Step 0 reconcile passes at run-start and batch-close.
4. Release registry parity precheck passes for `release_target`:
   - `releases.id = X.Y.Z` exists (not deleted)
   - `release_required_sets.release_id = X.Y.Z` exists with `status_key='locked'` (not deleted)
5. Any mismatch between environment release target and handoff release target is a hard STOP.
6. Tracked-file scope guard passes for the active release handoff:
   - successful release requires tracked changes to remain within handoff `scope_allowlist`
   - out-of-scope tracked changes are a hard STOP (`STOP_RELEASE_SCOPE_FILE_OUTSIDE_ALLOWLIST`)

### RM Precondition Remediation Gate (Mandatory)

Before RM Step 1 begins, the remediation gate must pass:

1. Canonical sync contract exists on control-plane `origin/main` for the target release:
   - `.ai/releases/RELEASE-X.Y.Z-SYNC-CONTRACT.json`
2. Release DB parity is present for `X.Y.Z`:
   - one active `releases` row
   - one active locked `release_required_sets` row
   - canonical lease-bound remediation command is available:
     `MOTUS_WORK_ITEM_ID=<work_item> MOTUS_AGENT_ID=<agent> .ai/scripts/reconcile-release-registry-truth.sh --release-id X.Y.Z --apply --report .ai/audits/RELEASE-REGISTRY-TRUTH-RECONCILE-X.Y.Z.json`
   - canonical release-checklist close command is available:
     `MOTUS_WORK_ITEM_ID=<work_item> MOTUS_AGENT_ID=<agent> .ai/scripts/release-roadmap-item-state-sync.sh --release-id X.Y.Z --apply --report .ai/audits/RELEASE-ROADMAP-ITEM-STATE-SYNC-X.Y.Z.json`
3. Remediation evidence artifact includes:
   - sync contract artifact path
   - sync contract merge SHA
   - DB parity query outputs
   - format follows `.ai/templates/RELEASE-PRECONDITION-REMEDIATION.md`
4. Promise-to-Truth reconcile is rerun and evidence is attached.
5. Gate status must be `READY`; otherwise release remains `BLOCKED`.

### Merge Governance Fallback (Mandatory, Solo-Maintainer Safe)

If the normal merge path is blocked only by self-approval policy, the run may proceed only through a controlled admin merge path with explicit evidence:

1. Approval evidence artifact.
2. Merge receipt artifact.
3. Policy reset confirmation artifact.

Silent bypasses are forbidden.

### Mandatory Phase Sign-off (Every Major Phase)

For each major phase, all four artifacts are required before proceeding:

1. Builder sign-off artifact.
2. Independent reviewer sign-off artifact (SoD).
3. Promise-to-Truth delta artifact.
4. Machine GO/STOP decision artifact.

If any required sign-off artifact is missing or contradictory, the phase is STOPPED.

### RM Artifact + Action Contract (Mandatory)

RM must define both an Artifact Contract and an Action Contract for each release
cycle (`X.Y.Z`) before GO/NO-GO is allowed.

Artifact Contract requirements:
- Every required artifact has a stable `artifact_id`.
- Every artifact row includes:
  - canonical path
  - producer `action_id`
  - verification command or check
  - pass criteria
- Missing or unverifiable artifact rows are fail-closed.

Action Contract requirements:
- Every release action has a stable `action_id`.
- Every action row includes:
  - preconditions
  - actor (`human`, `automation`, or `agent`)
  - command/procedure reference
  - output artifact IDs
  - completion criteria
- Skipped or partial action rows are fail-closed unless explicitly marked
  `not_applicable` with rationale.

Minimum RM action IDs (required):
- `RM-ACT-1`: refresh claims posture from current evidence.
- `RM-ACT-2`: run publish-proof dry-run and record output.
- `RM-ACT-3`: produce GO/NO-GO memo with explicit gate results.
- `RM-ACT-4`: execute go-live only after explicit human approval.
- `RM-ACT-5`: run post-publish verification and issue receipt.

Minimum RM artifact IDs (required):
- `RM-ART-1`: claims posture (`.ai/audits/CLAIMS-POSTURE.md` + `.json`).
- `RM-ART-2`: publish-proof dry-run evidence.
- `RM-ART-3`: GO/NO-GO memo.
- `RM-ART-4`: go-live receipt.
- `RM-ART-5`: post-publish receipt.

GO/NO-GO gate requirement:
- GO is allowed only when required artifact and action rows are `pass`.
- Any unresolved row keeps status at NO-GO with remediation.

### Required Artifacts

| Artifact | Source | Pass Criteria |
|----------|--------|---------------|
| `pytest-results.json` | `pytest --json-report` | 0 failures |
| `bandit-results.json` | `bandit -r src/ -f json` | 0 HIGH/CRITICAL |
| `pip-audit-results.json` | `pip-audit --format json` | 0 vulnerabilities |
| `doctor-results.json` | `motus doctor --json` | All checks pass |
| `import-path.txt` | `python -c "import motus; print(motus.__file__)"` | Canonical path |
| `commit-sha.txt` | `git rev-parse HEAD` | Match release tag |
| `health-ledger.md` | `packages/cli/docs/quality/` | Updated within 24h |
| `health-baseline.json` | `packages/cli/docs/quality/` | Exists |
| `health-policy.json` | `packages/cli/docs/quality/` | Exists |

### Clean Environment Requirement

All test and evidence generation MUST run in a clean virtual environment:

```bash
# Create clean venv
python3 -m venv /tmp/release-venv
source /tmp/release-venv/bin/activate

# Install from source
pip install -e ".[dev,web]"

# Verify import path (CRITICAL)
python3 -c "import motus; print(motus.__file__)" > .release-evidence/import-path.txt

# Record commit SHA
git rev-parse HEAD > .release-evidence/commit-sha.txt

# Generate doctor evidence
motus doctor --json > .release-evidence/doctor-results.json
```

### Evidence Generation

```bash
# Generate all evidence artifacts
mkdir -p .release-evidence/

# 1. Test results
pytest tests/ --json-report --json-report-file=.release-evidence/pytest-results.json -q

# 2. Security scan
bandit -r src/ -f json -o .release-evidence/bandit-results.json

# 3. Dependency audit
pip-audit --format json -o .release-evidence/pip-audit-results.json

# 4. Health ledger (must be manually updated)
cp packages/cli/docs/quality/health-ledger.md .release-evidence/
cp packages/cli/docs/quality/health-baseline.json .release-evidence/
cp packages/cli/docs/quality/health-policy.json .release-evidence/
```

### Evidence Verification

```bash
# Verify evidence bundle (fail-closed)
motus release check

# Expected output:
# [PASS] pytest-results.json: 0 failures
# [PASS] bandit-results.json: 0 HIGH/CRITICAL
# [PASS] pip-audit-results.json: 0 vulnerabilities
# [PASS] health-ledger.md: updated 2026-01-05
# [PASS] health-baseline.json: exists
# [PASS] health-policy.json: exists
#
# Evidence bundle: PASS
# Release: ALLOWED
```

---

## Release Boundary (Mandatory)

Every release MUST define a release boundary and produce a boundary audit artifact.

- Standard: `docs/standards/RELEASE-BOUNDARY-STANDARD.md`
- Artifact: `.ai/releases/RELEASE-X.Y.Z-BOUNDARY-AUDIT.md`

Fail-closed: A release cannot be marked complete if the boundary audit artifact
is missing or indicates any BLOCKLIST entry in the public output.

---

## Release Scorecard (Mandatory)

Complete a release scorecard before tagging or publishing:

- `.ai/releases/RELEASE-X.Y.Z-SCORECARD.md`

Use the template in `.ai/templates/RELEASE-SCORECARD.md`.

---

## Coverage Gates

### Minimum Coverage Requirements

| Metric | Threshold | Check |
|--------|-----------|-------|
| Test coverage | >= 80% | `pytest --cov` |
| Happy path coverage | 100% | All boundaries |
| Exception path coverage | >= 90% | All boundaries |
| Failure mode coverage | >= 80% | P0/P1 boundaries |

### Coverage by Release Type

| Release Type | Happy Path | Exception Path | Failure Mode |
|--------------|------------|----------------|--------------|
| Feature (0.X.0) | 100% | 100% | 80% |
| Hardening (0.X.Y) | 100% | 90% | N/A |

### Coverage Verification

```bash
# Check coverage metrics
pytest tests/ --cov=src/motus --cov-report=json

# Verify thresholds
python3 -c "
import json
with open('coverage.json') as f:
    data = json.load(f)
    pct = data['totals']['percent_covered']
    print(f'Coverage: {pct:.1f}%')
    exit(0 if pct >= 80 else 1)
"
```

---

## Phase Details

### Phase 1: Planning

**Gate:** Scope locked in coordination.db

**Checklist:**
- [ ] Version number confirmed (follows versioning contract)
- [ ] Release type determined (Feature or Hardening)
- [ ] Scope items tagged with `release:X.Y.Z`
- [ ] Breaking changes identified and documented
- [ ] CHANGELOG draft started
- [ ] Dependencies frozen
- [ ] Bundled modules review completed and recorded in `.ai/releases/RELEASE-X.Y.Z-BUNDLED-MODULES.md`

**Command:**
```bash
# Lock scope in coordination.db
sqlite3 ~/.motus/coordination.db "
  UPDATE release_cycles
  SET scope_locked_at = datetime('now')
  WHERE version = 'X.Y.Z'
"
```

### Phase 2: Build

**Gate:** CI passes

**Checklist:**
- [ ] All scoped items completed (status = done)
- [ ] Version bumped in pyproject.toml
- [ ] Version bumped in `__init__.py`
- [ ] Build artifacts created

**Commands:**
```bash
# Bump version
scripts/release/bump-version.py X.Y.Z

# Build
python3 -m build

# Verify
twine check dist/*
```

### Phase 3: Test

**Gate:** Full test suite passes

**Checklist:**
- [ ] Full pytest suite passes
- [ ] Snapshot tests pass (deterministic)
- [ ] Fresh install test passes
- [ ] Upgrade test passes with user data preserved (if not first release)

**Commands:**
```bash
# Full suite
python3 -m pytest tests/ -q

# Snapshots (deterministic)
PYTHONHASHSEED=0 TZ=UTC python3 -m pytest tests/test_snapshots.py -q

# Fresh install
.ai/scripts/test-fresh-install.sh

# Upgrade (if applicable)
.ai/scripts/test-upgrade.sh X.Y.Z
```

### Phase 4: Harden

**Gate:** Security clean, evidence bundle passes

**Checklist:**
- [ ] Bandit clean (no HIGH/CRITICAL)
- [ ] pip-audit clean (no vulnerabilities)
- [ ] No blocklist matches (CUDA, DNA, local home paths, etc.)
- [ ] No emoji in source
- [ ] No hardcoded secrets
- [ ] Migration safety scan passes (no destructive/unscoped SQL)
- [ ] Evidence bundle generated
- [ ] Evidence verification passes

**Commands:**
```bash
# Security
bandit -r src/ -f json -o .release-evidence/bandit-results.json
pip-audit --format json -o .release-evidence/pip-audit-results.json

# Content sanitization
! grep -rqiE "CUDA|4IR|\\bDNA\\b|ben@|/U[s]ers/|/h[o]me/" src/ && echo "PASS" || echo "FAIL"
! grep -rqP "[\x{1F300}-\x{1F9FF}]" src/ && echo "PASS:emoji" || echo "FAIL:emoji"

# Evidence verification
motus release check
```

### Phase 5: Website Sync (Feature Releases Only)

**Gate:** Website builds, docs synced

**Checklist:**
- [ ] messaging.yaml version bumped
- [ ] messaging.json regenerated
- [ ] README.md updated
- [ ] CHANGELOG.md finalized
- [ ] Website builds without errors
- [ ] No broken links
- [ ] Release sync contract exists and verifies (cross-repo)

**Commands:**
```bash
# Generate public surfaces
scripts/generate-public-surfaces.py

# Build website
cd packages/website && npm run build

# Check links
packages/website/scripts/ci/check_links.py

# Cross-repo verification (motus + website)
# Produces concrete evidence and fails closed on drift.
.ai/scripts/release-sync-verify.sh --release-id X.Y.Z \
  --contract .ai/releases/RELEASE-X.Y.Z-SYNC-CONTRACT.json
```

### Phase 6: Canary (Feature Releases Only)

**Gate:** 24h internal use without issues

**Checklist:**
- [ ] Published to TestPyPI
- [ ] Internal dogfood for 24h minimum
- [ ] Error rate < 1%
- [ ] No P0/P1 issues discovered

**Commands:**
```bash
# Publish to TestPyPI
twine upload --repository testpypi dist/*

# Test install
pip install --index-url https://test.pypi.org/simple/ motusos==X.Y.Z

# Monitor for 24h
```

### Phase 7: Release

**Gate:** PyPI published, tag created

**Checklist:**
- [ ] Git tag created
- [ ] GitHub release created
- [ ] PyPI published
- [ ] Fresh install from PyPI verified
- [ ] Release scorecard completed (`.ai/releases/RELEASE-X.Y.Z-SCORECARD.md`)
- [ ] Archive prior release artifacts (`.ai/releases/archive/X.Y.Z/`)
- [ ] Go-live receipt generated (`.ai/releases/RELEASE-X.Y.Z-GO-LIVE-RECEIPT.md`)

**Commands:**
```bash
# Tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z

# Publish
twine upload dist/*

# Verify
pip install motusos==X.Y.Z
motus --version

# Record publish evidence (fail closed if required fields are missing)
# Required env for receipts:
# - MOTUS_REPO_MOTUS: absolute path to the public /motus repo
# - MOTUS_GH_REPO_MOTUS: GitHub repo slug (example: org/repo)
.ai/scripts/release-go-live-receipt.sh X.Y.Z
```

### Phase 8: Announce (Feature Releases Only)

**Gate:** Announcement published

**Checklist:**
- [ ] Release notes published
- [ ] Documentation links verified
- [ ] Retrospective scheduled

---

## Phase 9: Post Go-Live Receipt (Mandatory)

Release completion is fail-closed: a release is not "complete" until the
post go-live receipt is generated and passes review (or an explicit override
is recorded with rationale).

**Gate:** Public surfaces verified (PyPI install + GitHub release + website live)

**Checklist:**
- [ ] Post receipt generated (`.ai/releases/RELEASE-X.Y.Z-POST-RECEIPT.md`)
- [ ] Any failures promoted to CRs (or explicitly waived with rationale)

**Commands:**
```bash
# Required env for receipts:
# - MOTUS_GH_REPO_MOTUS: GitHub repo slug (example: org/repo)
.ai/scripts/release-post-receipt.sh X.Y.Z
```

## Release Close Parity (Mandatory)

Once the go-live and post receipts exist on the canonical internal line, close the
release truth in this order:

```bash
MOTUS_WORK_ITEM_ID=<work_item> MOTUS_AGENT_ID=<agent> \
  .ai/scripts/reconcile-release-registry-truth.sh --release-id X.Y.Z --apply \
  --report .ai/audits/RELEASE-REGISTRY-TRUTH-RECONCILE-X.Y.Z.json

MOTUS_WORK_ITEM_ID=<work_item> MOTUS_AGENT_ID=<agent> \
  .ai/scripts/release-roadmap-item-state-sync.sh --release-id X.Y.Z --apply \
  --report .ai/audits/RELEASE-ROADMAP-ITEM-STATE-SYNC-X.Y.Z.json

MOTUS_WORK_ITEM_ID=<work_item> MOTUS_AGENT_ID=<agent> \
  .ai/scripts/release-required-set-item-state-sync.sh --release-id X.Y.Z --apply \
  --report .ai/audits/REQUIRED-SET-ITEM-STATE-SYNC-X.Y.Z.json
```

Rules:

1. Do not hand-edit `releases`, `roadmap_items`, or `release_required_set_items`
   with raw `sqlite3` during release close.
2. If a required artifact is missing, generate or backfill the artifact first and
   rerun the ordered sync path.
3. The workflow owns release checklist closure; operators should not infer item
   completion ad hoc.

## DORA Metrics

Track for every release:

| Metric | Target | Definition |
|--------|--------|------------|
| Lead time | < 48h | Scope lock to PyPI publish |
| Change failure rate | < 10% | Releases requiring hotfix |
| Recovery time | < 4h | Time to ship hotfix |
| Rework rate | < 10% | Items reopened after done |

---

## Rollback Procedure

### Triggers

| Condition | Action |
|-----------|--------|
| Error rate > 5% in first hour | Yank from PyPI |
| P0 bug reported | Assess, likely yank |
| Security CVE discovered | Immediate patch |
| Data corruption risk | Immediate yank + advisory |

### Emergency Rollback Runbook

If a release breaks production:

**Step 1: Immediate - Restore User Functionality (< 5 minutes)**

```bash
# Tell users to rollback immediately
pip install motusos==PREVIOUS_VERSION

# Verify rollback worked
motus --version  # Should show previous version
motus doctor     # Should pass
```

**Step 2: Assessment (< 15 minutes)**

```bash
# Gather evidence
motus doctor --json > /tmp/incident-doctor.json
sqlite3 ~/.motus/coordination.db ".dump" > /tmp/incident-db.sql

# Document the failure mode
# - What command/action triggered the failure?
# - What error message appeared?
# - Is data affected?
```

**Step 3: Containment (< 1 hour)**

```bash
# 1. Yank from PyPI (prevents new installs of broken version)
# Contact PyPI support OR use trusted publisher workflow

# 2. Keep git tag for audit trail
# Do NOT delete the git tag - it's forensic evidence

# 3. Create incident issue
gh issue create --title "INCIDENT: v${VERSION} rollback" \
  --body "$(cat /tmp/incident-doctor.json)"
```

**Step 4: Fix and Re-release**

```bash
# 1. Create hotfix branch from the broken release
git checkout -b hotfix/X.Y.Z+1 vX.Y.Z

# 2. Fix the issue
# - Reproduce on copy of affected DB
# - Capture exact failing SQL/error
# - Patch the code
# - Add regression test
# - Run migration twice (prove idempotency)

# 3. Follow abbreviated release cycle (Type B)
# DO NOT skip evidence bundle or gates
```

### Post-Incident Checklist

- [ ] Users notified of rollback instructions
- [ ] Broken version yanked from PyPI
- [ ] Incident documented with timeline
- [ ] Root cause identified
- [ ] Regression test added
- [ ] Hotfix released
- [ ] Retrospective scheduled

---

## Communication Strategy

### Channels

| Channel | Use For | Timing | Template |
|---------|---------|--------|----------|
| CHANGELOG.md | All releases | At release | Keep a Changelog |
| GitHub Releases | All releases | At release | ANNOUNCEMENT-TEMPLATES.md |
| README badge | Current version | At release | Auto-updated |
| Migration guide | Breaking changes | Before release | MIGRATION-GUIDE-TEMPLATE.md |
| Deprecation notice | Feature removal | 2+ releases ahead | DEPRECATION-NOTICE-TEMPLATE.md |

### Communication by Release Type

| Release Type | CHANGELOG | GitHub Release | Migration Guide | Announcement |
|--------------|-----------|----------------|-----------------|--------------|
| Feature (0.X.0) | YES | YES | If breaking | YES |
| Hardening (0.X.Y) | YES | YES | NO | Optional |
| Security | YES | YES | If needed | YES (immediate) |

### Timing Requirements

| Communication | Timing |
|---------------|--------|
| Deprecation notice | 2+ releases before removal |
| Breaking change warning | 1+ release before change |
| Security fix | ASAP after fix available |
| Feature announcement | At release |

### Templates

All templates in `.ai/templates/`:

| Template | Purpose |
|----------|---------|
| `ANNOUNCEMENT-TEMPLATES.md` | 6 announcement formats |
| `MIGRATION-GUIDE-TEMPLATE.md` | Breaking change migration |
| `DEPRECATION-NOTICE-TEMPLATE.md` | Feature deprecation |
| `RELEASE-CYCLE-TEMPLATE.md` | Per-release tracking |

---

## Website Release Process

The website has its own release cycle, independent of CLI versions.

### Website Environments

| Environment | URL | Branch | Deploy Trigger |
|-------------|-----|--------|----------------|
| Development | localhost:4321 | any | `npm run dev` |
| Staging | staging.motusos.ai | `main` | Push to main |
| Production | motusos.ai | `release/website-*` | Manual/CI |

### Website Release Checklist

```
[ ] Phase 1: Changes complete on main
[ ] Phase 2: Build passes (npm run build)
[ ] Phase 3: Links verified (check_links.py)
[ ] Phase 4: Proofs verified (check_proofs.py)
[ ] Phase 5: Staging deployed and QA'd
[ ] Phase 6: Release branch created (release/website-YYYY-MM-DD)
[ ] Phase 7: Production deployed
[ ] Phase 8: Post-deploy verification
```

### Website Gates

| Gate | Command | Pass Criteria |
|------|---------|---------------|
| Build | `cd website && npm run build` | 0 errors |
| TypeScript | `cd website && npm run type-check` | 0 errors |
| Links | `website/scripts/ci/check_links.py` | 0 broken |
| Proofs | `website/scripts/ci/check_proofs.py` | All verified |
| Lighthouse | `npm run lighthouse` | Score > 90 |
| Visual QA | Manual review | Checklist complete |

### Website QA Checklist

Before production deploy:

- [ ] Homepage loads correctly
- [ ] All navigation links work
- [ ] CLI examples render properly
- [ ] Code blocks have syntax highlighting
- [ ] Mobile responsive layout works
- [ ] No console errors
- [ ] Analytics tracking works
- [ ] Forms submit correctly (if any)

### Website vs CLI Releases

| Aspect | CLI Release | Website Release |
|--------|-------------|-----------------|
| Trigger | Version milestone | Content updates |
| Frequency | Weekly-monthly | As needed |
| Branch | `release/X.Y.Z` | `release/website-YYYY-MM-DD` |
| Deploy target | PyPI | GitHub Pages/Cloudflare |
| Rollback | PyPI yank | Git revert + redeploy |

---

## Quick Reference

### Feature Release (0.X.0) Checklist

```
[ ] Phase 1: Scope locked, version confirmed
[ ] Phase 2: Version bumped, build passes
[ ] Phase 3: Tests pass, fresh install works
[ ] Phase 4: Security clean, evidence bundle passes
[ ] Phase 5: Website synced, docs updated
[ ] Phase 6: Canary 24h clean
[ ] Phase 7: PyPI published, tag created, scorecard completed
[ ] Phase 8: Announcement published
[ ] Phase 8.5: Effectiveness reviews scheduled, prior artifacts archived
```

### Hardening Release (0.X.Y) Checklist

```
[ ] Phase 1: Scope defined
[ ] Phase 2: Version bumped, build passes
[ ] Phase 3: Tests pass
[ ] Phase 4: Security clean, evidence bundle passes
[ ] Phase 5: PyPI published, tag created, scorecard completed, go-live receipt generated
[ ] Phase 5.5: Post receipt generated and release close parity synced
[ ] Phase 5.6: Effectiveness reviews scheduled, prior artifacts archived
```

---

## Automation

### Release Scripts

| Script | Purpose |
|--------|---------|
| `scripts/release/bump-version.py` | Bump version across all files |
| `scripts/release/generate-changelog.py` | Generate changelog from commits |
| `scripts/release/pre-release-check.py` | Run all gates in sequence (requires explicit product root for Motus CLI) |
| `scripts/release/create-release-cycle.sh` | Seed release cycle tasks in coordination.db |
| `scripts/release/archive-release-artifacts.sh` | Archive prior release artifacts |
| `scripts/generate-public-surfaces.py` | Generate README + messaging.json |
| `motus release check` | Verify evidence bundle |
| `motus release bundle` | Generate evidence bundle |
| `.ai/scripts/release-roadmap-item-state-sync.sh` | Close canonical release roadmap proof items from release artifacts |
| `.ai/scripts/rm-release-loop.sh` | Deterministic RM loop trigger (sync verify -> proof-watch -> GO/NO-GO -> optional receipts) |

For Motus CLI releases, run the pre-release gates against the product repo/worktree:

```bash
python3 scripts/release/pre-release-check.py --product-root /path/to/motus --product-python-root packages/cli
```

### Release Process Drift Guard

Run the drift guard to ensure the release seed script matches this standard:

```bash
python3 scripts/ci/check_release_cycle_drift.py
```

### Release Scorecard Guard

Verify scorecard artifacts are present when release artifacts exist:

```bash
python3 scripts/ci/check_release_scorecard.py
```

### Operational Gate Scripts

Located in `scripts/gates/`. Run with `./scripts/gates/run-all-gates.sh`.

**Environment Gates (Phase 1):**

| Gate ID | Script | Purpose |
|---------|--------|---------|
| GATE-REPO-001 | `gate-repo-001.sh` | Verify correct repository and branch |
| GATE-PKG-001 | `gate-pkg-001.sh` | Detect conflicting package installs |
| GATE-DB-001 | `gate-db-001.sh` | Verify schema version matches code |

**Functionality Gates (Phase 2):**

| Gate ID | Script | Purpose |
|---------|--------|---------|
| GATE-CLI-001 | `gate-cli-001.sh` | Smoke test all documented commands |
| GATE-WEB-001 | `gate-web-001.sh` | Verify web UI loads and responds |
| GATE-COV-001 | `gate-cov-001.sh` | Check test coverage thresholds |
| GATE-PERF-001 | `gate-perf-001.sh` | Startup time < 500ms (catches import bloat) |

**Security Gates (Phase 3):**

| Gate ID | Script | Purpose |
|---------|--------|---------|
| GATE-SEC-002 | `gate-sec-002.sh` | Secrets scan (detect-secrets/gitleaks) |
| GATE-DEP-002 | `gate-dep-002.sh` | Dependency license check (block GPL/AGPL) |
| GATE-MIG-001 | `gate-migrations-001.sh` | Migration safety scan (no seed/destructive SQL) |

**Release Gates (Phase 4 - For Release Branches/Tags):**

| Gate ID | Script | Purpose |
|---------|--------|---------|
| GATE-INSTALL-001 | `gate-install-001.sh` | Fresh install in clean venv + data leak detection |
| GATE-UPGRADE-001 | `gate-upgrade-001.sh` | Upgrade from previous version |
| GATE-RELEASE-001 | `gate-release-001.sh` | Version coordination (tag, CHANGELOG, PyPI, GitHub) |

**Validation Gates (Standalone - Run Manually):**

| Gate ID | Script | Purpose |
|---------|--------|---------|
| GATE-FRESH-001 | `gate-fresh-001.sh` | Verify fresh DB has no leaked data |
| GATE-FRESH-002 | `gate-fresh-002.sh` | Verify directory structure has no dev artifacts |

**Run configuration:**

```bash
# Default: Phases 1-3 (CI)
./scripts/gates/run-all-gates.sh

# Full release validation: Phases 1-4
RUN_RELEASE_GATES=true PREV_VERSION=0.1.0 ./scripts/gates/run-all-gates.sh
```

**CI Integration:** `.github/workflows/release-gates.yml` runs gates on release/* branches.

---

## Sign-off

Every release requires explicit sign-off:

| Check | Required |
|-------|----------|
| Tests pass | YES |
| Evidence bundle passes | YES |
| Fresh install works | YES |
| Security clean | YES |
| Coverage thresholds met | YES |
| Breaking changes documented (if any) | YES |
| CHANGELOG updated | YES |

**Release approved by:** _______________

**Version:** _______________

**Date:** _______________

**Release type:** [ ] Feature (0.X.0)  [ ] Hardening (0.X.Y)
