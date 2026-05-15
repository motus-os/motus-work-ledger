# Review Semantic Conventions

Review attributes describe review evidence. They do not require a Motus-specific
review process.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `review.id` | Recommended | string | Review identifier within the host system. |
| `review.actor.id` | Recommended | string | Actor that performed the review. |
| `review.method` | Recommended | string | Method such as `human_pr_review`, `automated_gate`, or `independent_agent`. |
| `review.status` | Required | enum | One of `approved`, `changes_requested`, `commented`, `not_required`, or `unknown`. |
| `review.ref` | Optional | string | URL or reference for the review evidence. |
| `review.summary` | Optional | string | Short safe summary. |
