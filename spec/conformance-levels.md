# Conformance Levels v0.1

Motus compatibility is claimed by passing the conformance tests for a declared
level.

## Level 0: Receipt-Only

A Level 0 implementation can:

1. emit a valid Work Receipt Envelope,
2. validate against the JSON schemas,
3. compute canonical receipt hashes,
4. pass golden fixture checks.

## Level 1: Event-Backed

A Level 1 implementation can:

1. emit durable work events,
2. preserve event ordering within a run,
3. derive a Work Receipt deterministically from those events,
4. expose the Store export digest used by the receipt,
5. pass Level 0 checks.

## Level 2: Governed Handoff

A Level 2 implementation can represent:

1. evidence references,
2. acceptance,
3. handoff,
4. route summary,
5. policy-result projections when present.

## Level 3: Verified Provenance

A Level 3 implementation supports optional signatures, attestations, or other
verification envelopes while preserving canonical receipt validation.
