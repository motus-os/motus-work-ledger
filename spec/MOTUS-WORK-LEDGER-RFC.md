# Motus Work Ledger RFC v0.1

> Status: Draft RFC
> Scope: workflow-neutral work ledger model, portable receipts, and conformance
> Relationship to `/motus`: `/motus` is the reference implementation, not the canonical portable boundary

## Problem

AI agents, CI jobs, humans, and tools can all perform consequential work, but
their proof is scattered across logs, chats, tickets, and local state. A later
reviewer needs a small, portable answer to these questions:

1. What work was attempted?
2. Who or what performed it?
3. What evidence exists?
4. What changed or was claimed?
5. What outcome was accepted?
6. What should happen next?

Motus Work Ledger defines the journal, ledger, receipt, and conformance layer
for that answer.

## Non-Goals

Motus is not:

1. an agent runtime,
2. a workflow engine,
3. a model router,
4. a hosted control tower,
5. a compliance product,
6. a memory system.

Motus-compatible systems may run inside those environments, but Motus does not
own those environments.

## Core Model

```text
Work Journal -> Work Ledger -> Work Receipt
```

The Work Journal is the append-only event stream.

The Work Ledger is the organized durable work truth derived from those facts.

The Work Receipt is the portable proof object projected from ledger facts.

The durable facts are:

1. a bounded run,
2. append-only events,
3. event kind schema versions,
4. payload and schema hashes,
5. terminal outcome,
6. deterministic projections,
7. optional fenced lock state for protected mutable resources.

Everything else is a projection, adapter concern, or userland process.

## Durable Facts

A Motus-compatible event stream must preserve:

- stable run identity,
- ordered event sequence within a run,
- event kind,
- idempotency key,
- payload digest,
- schema digest,
- producer identity when known,
- terminal close state when the run is closed.

Adapters may add richer metadata, but they must not create a second source of
truth for the run outcome.

## Projection Model

Receipts, packets, evidence lists, decisions, handoffs, and route summaries are
read-side projections over durable facts. A projection must declare:

- source run or export reference,
- canonicalization method,
- generated digest,
- volatile fields excluded from cross-run comparison, if any.

## Work Receipt Envelope

The Work Receipt Envelope is the portable primitive. It answers what happened
without requiring the verifier to run `/motus`.

The envelope is defined in:

- `spec/work-receipt-envelope-v0.1.md`
- `schemas/work-receipt-envelope.schema.json`

## Evidence References

Evidence should be referenced by digest and URI when possible. Receipts should
not embed raw transcripts, prompts, secrets, or bulky logs by default. If
sensitive material was redacted, the receipt must carry a redaction marker so a
reviewer knows the evidence is intentionally incomplete.

## Semantic Conventions

Semantic conventions define shared attribute names for work, actors, agents,
tools, evidence, acceptance, route, handoff, and related metadata. They are
descriptive names for receipts and events, not a workflow engine or policy
system.

The alpha conventions are defined in `semconv/README.md`. Receipt envelope
attributes that use dotted convention names are mapped to canonical schema paths
in `semconv/schema-map.md`; adapters must not rely on undocumented translation
rules.

## Acceptance Boundary

Acceptance is explicit. A receipt can claim that work completed, failed, was
aborted, or was superseded, but it must distinguish the work outcome from the
actor or system that accepted that outcome.

## Handoff And Route Projections

Handoff and route data are projections or references. They describe what should
happen next; they do not replace the closed run's durable outcome.

## Adapter Contract

An adapter may claim Motus compatibility when it can:

1. emit a valid Work Receipt Envelope,
2. preserve canonical hashes,
3. reference evidence without leaking raw sensitive content by default,
4. pass the conformance fixtures for its claimed level,
5. document which runtime produced the receipt.

The adapter does not need to import `motusos` or use `/motus`.

## Conformance Levels

Level 0: Receipt-only

- emits and validates a Work Receipt Envelope.

Level 1: Event-backed

- emits durable events and derives a receipt projection.

Level 2: Governed handoff

- represents evidence, acceptance, handoff, route, and policy outcome
  projections.

Level 3: Verified provenance

- supports canonical hashes, optional signatures or attestations, and verifier
  evidence.

## Security And Privacy

Receipts are evidence indexes, not transcript dumps. Implementations must:

- avoid raw secret persistence by default,
- mark redaction explicitly,
- hash referenced evidence with declared canonicalization,
- avoid exposing local absolute paths unless the operator opts in,
- treat actor, model, tool, and instruction metadata as potentially sensitive.

## Control Crosswalks

Future crosswalks may show how Motus receipts can support audit or control
objectives. They must not claim Motus makes an organization compliant.

## Examples

See:

- `conformance/fixtures/valid/work-receipt-minimal.json`
- `conformance/fixtures/valid/work-receipt-github-action.json`
- `conformance/implementations/receipt-only-python/`
- `semconv/README.md`
