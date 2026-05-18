# Schemas

This directory contains the strict JSON schemas for Motus Work Ledger objects.

The canonical schema identifiers use the `https://motus.dev/schemas/` namespace.
During alpha, those `$id` values are identifiers, not network retrieval URLs.
Validators should resolve them through the local registry in `schemas/index.json`
or through the bundled validator.

Do not configure alpha validators to fetch schemas from `motus.dev/schemas/`.
Hosted schema URLs require a drift-safe publishing path and a registry update
that changes `hosted_resolution.status` from `not_served_in_alpha`.

## Registry

`schemas/index.json` maps each schema id to the repository path that defines it.
It also records the hosted-resolution decision so reviewers can tell whether
the identifiers are expected to resolve over the network.

Verify the registry:

```bash
python conformance/validator/check_schema_registry.py
```

## Rules

1. Keep `additionalProperties: false` wherever practical.
2. Keep enum values aligned with `semconv/schema-map.md`.
3. Update fixtures and golden hashes when schema behavior changes.
4. Document compatibility impact in `CHANGELOG.md` and `VERSIONING.md`.
