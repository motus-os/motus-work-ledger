# Motus Semantic Conventions v0.1

> Status: Draft alpha
> Scope: shared attribute names for Motus-compatible receipts and events

Semantic conventions keep Motus-compatible receipts portable across adapters
and runtimes. They define common names and meanings for fields that appear in
receipt envelopes, evidence references, Store events, and projections.

They are not a workflow model. They do not require a policy engine, hosted
control plane, model router, or governance system.

## Principles

1. Durable facts remain runs, events, kind versions, hashes, outcomes, and
   optional fenced locks.
2. Semantic conventions name facts and references; they do not create a second
   source of truth.
3. Evidence may be referenced by digest without embedding sensitive content.
4. Acceptance is explicit and separate from outcome.
5. Model, tool, policy, and risk attributes are descriptive metadata, not Motus
   control authority.

## Convention Files

- [Schema Mapping](schema-map.md)
- [Work](work.md)
- [Actor](actor.md)
- [Agent](agent.md)
- [Tool](tool.md)
- [Model](model.md)
- [Evidence](evidence.md)
- [Code](code.md)
- [CI](ci.md)
- [Review](review.md)
- [Acceptance](acceptance.md)
- [Policy](policy.md)
- [Risk](risk.md)
- [Security](security.md)
- [Route](route.md)
- [Handoff](handoff.md)

## Requirement Levels

- Required: needed for the convention's primary object to be useful.
- Recommended: strongly preferred when known.
- Optional: useful context that must not be fabricated.

If a value is unknown, omit it or mark it as unknown. Do not invent placeholders
to satisfy a field.

For receipt envelope objects, semantic convention attributes must either match
the canonical schema field or be listed in the schema mapping table. An adapter
that follows these conventions should be able to emit JSON that validates
without an undocumented translation layer.
