# Actor Semantic Conventions

Actor attributes identify the entity responsible for an action, outcome, or
acceptance decision.

In a strict Work Receipt Envelope, actor objects accept only `actor.type`,
`actor.id`, and optional `actor.display`. Other actor attributes are telemetry
metadata and must not be emitted as extra fields inside the strict receipt
actor object.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `actor.id` | Required | string | Stable actor identifier within the emitter's scope. |
| `actor.type` | Required | enum | One of `human`, `agent`, `service`, `ci`, or `tool`. |
| `actor.display` | Optional | string | Human-readable actor name for strict receipt-envelope actor objects. |
| `actor.authn.method` | Optional telemetry | string | Authentication method when relevant, such as `oauth`, `ssh`, `oidc`, or `local`. |
| `actor.org` | Optional telemetry | string | Organization, team, or project namespace. |
