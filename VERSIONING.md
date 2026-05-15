# Versioning

Motus Work Ledger uses explicit alpha tags until the schema and conformance
surface are stable enough for broader implementation claims.

## Release Tags

Alpha releases use:

```text
v0.1.0-alpha.N
```

Each release must identify:

1. schema versions,
2. conformance levels covered,
3. fixture and golden-hash changes,
4. compatibility impact for existing Work Receipts.

## Schema Versions

Schema document versions are independent of repository tags. A schema change is:

1. **clarifying** when it changes prose or examples only,
2. **additive** when valid existing receipts remain valid,
3. **breaking** when valid existing receipts may become invalid or produce a
   different canonical digest.

Breaking schema changes require:

1. a new schema version string,
2. migration notes,
3. validator support for the prior version when practical,
4. explicit changelog entry.

## Semantic Conventions

Semantic conventions must either map directly to a strict schema field or appear
in `semconv/schema-map.md`.

Adding unmapped dotted attributes is not allowed unless the change also explains
why they are telemetry-only and must not appear in strict Work Receipt JSON.

## Conformance Levels

Implementations must name the exact release and level they claim, for example:

```text
Motus Work Ledger v0.1.0-alpha.0, Level 0 receipt-only
```

No implementation should claim Motus compatibility without passing the
conformance suite for its declared level.
