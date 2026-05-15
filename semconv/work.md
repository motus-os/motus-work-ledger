# Work Semantic Conventions

Work attributes describe the bounded unit of consequential work.

In a strict Work Receipt Envelope, `work.id` is emitted as `work_id`, and
`work.outcome.*` attributes are emitted under the `outcome` object. Use
[schema-map.md](schema-map.md) for the canonical mapping. Do not emit dotted
`work.*` semantic attribute names as extra receipt fields unless a future
schema explicitly admits them.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `work.id` | Required | string | Stable identifier for the work unit within the emitter's scope. |
| `work.type` | Recommended telemetry | string | Category such as `code_change`, `ci_run`, `release`, `review`, or `analysis`. |
| `work.intent` | Recommended | string | Short human-readable intent. |
| `work.contract.ref` | Optional | string | Reference to an instruction, issue, PR, ticket, or work contract. |
| `work.started_at` | Recommended telemetry | RFC 3339 string | Time the bounded work started. |
| `work.closed_at` | Recommended | RFC 3339 string | Time the bounded work reached a terminal outcome. |
| `work.outcome.status` | Required | enum | One of `success`, `failure`, `partial`, `aborted`, `superseded`, or `unknown`. |
| `work.outcome.summary` | Recommended | string | Short outcome summary without raw transcript content. |

`work.type` and `work.started_at` are event or telemetry metadata in v0.1.
They are useful for observability and event streams, but they are not strict
receipt-envelope fields.
