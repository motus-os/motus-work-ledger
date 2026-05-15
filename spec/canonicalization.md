# Canonicalization v0.1

Work Receipts use deterministic JSON canonicalization so independent validators
can reproduce the same receipt digest.

## Default Method

`json.sorted.compact.v0`

Rules:

1. encode JSON as UTF-8,
2. sort object keys lexicographically,
3. use compact separators,
4. preserve Unicode characters without ASCII escaping,
5. remove self-referential receipt fields before receipt self-hash.

The receipt digest removes:

```text
receipt_id
hashes.receipt
```

The computed SHA-256 digest must equal:

```text
receipt_id without the sha256: prefix
hashes.receipt.value
```

## Timestamp Format

Timestamps should use RFC 3339 date-time strings with explicit timezone. `Z`
is accepted for UTC.

## Evidence Digests

Evidence references should include:

```text
algorithm
value
canonicalization
```

If evidence is redacted or withheld, the redaction marker must remain visible in
the receipt.

## Path Handling

Receipts should not expose local absolute paths unless the operator explicitly
chooses to include them. Prefer project-relative paths, content-addressed URIs,
or external artifact URIs.

