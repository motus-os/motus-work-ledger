# Work Receipt Envelope v0.1

> Status: Draft
> Stability: alpha fixture contract

The Work Receipt Envelope is a portable projection that lets a verifier inspect
consequential work without needing the original runtime.

## Required Questions

Every envelope must answer:

1. What work was attempted?
2. Who or what performed it?
3. Under what instruction, contract, or trigger?
4. What tool or runtime produced the work?
5. What event stream or export supports the receipt?
6. What evidence was produced or referenced?
7. What outcome was claimed?
8. Who or what accepted it?
9. What route or handoff follows?
10. Can the receipt be independently reconstructed?

## Required Fields

- `schema_version`: envelope schema version.
- `receipt_id`: stable receipt identifier.
- `run_id`: durable run identifier.
- `work_id`: operator-facing work identifier.
- `actor`: human, agent, service, CI job, or tool that performed the work.
- `runtime`: implementation that emitted the receipt.
- `trigger`: user, CI, schedule, webhook, or tool-call trigger.
- `instruction_ref`: reference to the instruction, contract, or command.
- `events_ref`: digest and optional URI for the supporting event stream.
- `evidence_refs`: evidence references by kind, digest, URI, and redaction state.
- `tool_refs`: tools or systems used while producing the work.
- `outcome`: claimed terminal outcome.
- `acceptance`: acceptance status and actor.
- `route_summary`: next-route projection.
- `handoff`: optional handoff projection.
- `canonicalization`: canonical JSON method and volatile field policy.
- `hashes`: envelope and source digests.
- `redaction`: receipt-level redaction status.
- `created_at`: receipt creation timestamp.

## Canonicalization

The default canonical form is UTF-8 JSON with sorted object keys, compact
separators, and no insignificant whitespace. Hashes must declare the method used
to produce them.

The receipt digest is computed over the envelope with the self-referential
fields removed:

- top-level `receipt_id`
- `hashes.receipt`

The computed SHA-256 value must equal both `receipt_id` without the `sha256:`
prefix and `hashes.receipt.value`.

## Privacy Rules

Receipts should reference evidence instead of embedding sensitive content. A
missing transcript is acceptable when the receipt includes byte counts, digests,
redaction state, or an external evidence reference. Silent omission is not
acceptable.
