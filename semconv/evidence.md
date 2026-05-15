# Evidence Semantic Conventions

Evidence attributes describe proof referenced by receipts or events.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `evidence.evidence_id` | Required | string | Stable evidence identifier within the receipt or run. Maps to `evidence_id`. |
| `evidence.kind` | Required | string | Category such as `test_result`, `diff`, `log_summary`, `artifact`, or `review`. |
| `evidence.uri` | Recommended | string | URI or relative path for the evidence reference. |
| `evidence.digest` | Required | digest object | Hash of referenced evidence using declared canonicalization. |
| `evidence.summary` | Recommended | string | Short summary safe for the receipt. |
| `evidence.redaction.status` | Required | enum | One of `none`, `redacted`, or `withheld`. |
| `evidence.retention` | Optional | string | Retention class or retention period if known. |
