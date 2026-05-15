# Work Semantic Conventions

Work attributes describe the bounded unit of consequential work.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `work.id` | Required | string | Stable identifier for the work unit within the emitter's scope. |
| `work.type` | Recommended | string | Category such as `code_change`, `ci_run`, `release`, `review`, or `analysis`. |
| `work.intent` | Recommended | string | Short human-readable intent. |
| `work.contract.ref` | Optional | string | Reference to an instruction, issue, PR, ticket, or work contract. |
| `work.started_at` | Recommended | RFC 3339 string | Time the bounded work started. |
| `work.closed_at` | Recommended | RFC 3339 string | Time the bounded work reached a terminal outcome. |
| `work.outcome.status` | Required | enum | One of `success`, `failure`, `partial`, `aborted`, or `superseded`. |
| `work.outcome.summary` | Recommended | string | Short outcome summary without raw transcript content. |
