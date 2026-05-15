# Changelog

All notable changes to Motus Work Ledger are recorded here.

Motus Work Ledger is currently alpha. Until `v0.1.0`, compatibility claims are
limited to the exact tagged release and conformance level named by an
implementation.

## Unreleased

- No unreleased changes.

## v0.1.0-alpha.3 - 2026-05-15

- Add a dependency-free Node.js Level 0 receipt-only implementation that emits
  a strict Work Receipt without importing `/motus` or `motusos`.
- Pin Node 20 in Quality Gates so the Node implementation is verified in CI.
- Add Level 2 governed handoff conformance over the existing strict receipt
  schemas, including route/handoff receiver alignment, pending acceptance actor
  alignment, evidence-reference preservation, and negative semantic checks.

## v0.1.0-alpha.2 - 2026-05-15

- Fix semantic-convention/schema-map alignment for strict Work Receipt fields.
- Add a Quality Gates check that blocks strict semantic attributes missing from
  `semconv/schema-map.md`.
- Add a controlled design-partner pilot packet with falsifiable success and
  failure criteria, privacy boundaries, and stop/remove guidance.
- Add a Level 1 event-backed Python implementation that emits a Store export,
  derives a Work Receipt, and emits a projection manifest without importing
  `/motus` or `motusos`.
- Extend conformance to validate event ordering, terminal close, event hashes,
  source-export linkage, and receipt projection consistency against Store facts.
- Harden repository security posture with secret scanning, push protection,
  Dependabot security updates, restricted Actions policy, and updated security
  documentation.

## v0.1.0-alpha.1 - 2026-05-15

- Add repository governance templates and schema registry documentation.
- Add schema registry consistency validation to Quality Gates.
- Add branch protection and release-tracking issues for governed alpha release.

## v0.1.0-alpha.0

- Initial public Motus Work Ledger bootstrap.
- Add Work Ledger RFC, Work Receipt Envelope, canonicalization rules, schemas,
  semantic conventions, conformance validator, fixtures, examples, and
  receipt-only Python implementation.
