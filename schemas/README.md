# Schemas

This directory contains the strict JSON schemas for Motus Work Ledger objects.

The canonical schema identifiers use the `https://motus.dev/schemas/` namespace.
Until those URLs are served directly, validators should resolve them through
the local registry in `schemas/index.json` or through the bundled validator.

## Registry

`schemas/index.json` maps each schema id to the repository path that defines it.

## Rules

1. Keep `additionalProperties: false` wherever practical.
2. Keep enum values aligned with `semconv/schema-map.md`.
3. Update fixtures and golden hashes when schema behavior changes.
4. Document compatibility impact in `CHANGELOG.md` and `VERSIONING.md`.
