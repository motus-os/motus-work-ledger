# Actor Semantic Conventions

Actor attributes identify the entity responsible for an action, outcome, or
acceptance decision.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `actor.id` | Required | string | Stable actor identifier within the emitter's scope. |
| `actor.type` | Required | enum | One of `human`, `agent`, `service`, `ci`, or `tool`. |
| `actor.display` | Optional | string | Human-readable actor name for strict receipt-envelope actor objects. |
| `actor.authn.method` | Optional | string | Authentication method when relevant, such as `oauth`, `ssh`, `oidc`, or `local`. |
| `actor.org` | Optional | string | Organization, team, or project namespace. |
