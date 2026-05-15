# Security Semantic Conventions

Security attributes describe security-relevant evidence and boundaries.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `security.scan.name` | Recommended | string | Security scanner, gate, or review name. |
| `security.scan.status` | Required | enum | One of `pass`, `fail`, `warning`, `skipped`, or `unknown`. |
| `security.finding.count` | Optional | integer | Number of findings, if disclosed. |
| `security.secret_scan.status` | Recommended | enum | One of `pass`, `fail`, `not_run`, or `unknown`. |
| `security.attestation.ref` | Optional | string | Reference to an attestation or provenance artifact. |
| `security.redaction.status` | Recommended | enum | One of `none`, `redacted`, or `withheld`. |
