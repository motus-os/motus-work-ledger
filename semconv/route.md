# Route Semantic Conventions

Route attributes describe the next step projected from completed work. They do
not reopen the closed run or replace its outcome.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `route.status` | Required | enum | One of `complete`, `handoff`, `blocked`, or `none`. |
| `route.next_actor.type` | Optional | enum | Type of actor expected to take the next step. |
| `route.next_actor.id` | Optional | string | Actor identifier expected to take the next step. |
| `route.reason` | Optional | string | Short reason for the route. |
| `route.route_ref` | Optional | string | Reference to next issue, PR, job, or receipt. |

If `route.next_actor` is emitted in a strict receipt envelope, both
`route.next_actor.type` and `route.next_actor.id` are required by the schema.
