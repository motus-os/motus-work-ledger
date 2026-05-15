# Acceptance Semantic Conventions

Acceptance attributes identify who or what accepted an outcome. Acceptance is
separate from the work outcome.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `acceptance.status` | Required | enum | One of `accepted`, `rejected`, `not_required`, or `pending`. |
| `acceptance.actor.id` | Recommended | string | Actor that accepted or rejected the outcome. |
| `acceptance.actor.type` | Recommended | enum | Actor type using `actor.type` values. |
| `acceptance.accepted_at` | Recommended | RFC 3339 string | Time of acceptance decision. |
| `acceptance.method` | Required | string | Method such as `validator_pass`, `review_approval`, `merge`, or `manual`. |
| `acceptance.rationale_ref` | Optional | string | Reference to rationale when separate from the receipt. |

If `acceptance.actor` is emitted in a strict receipt envelope, both
`acceptance.actor.type` and `acceptance.actor.id` are required by the schema.
