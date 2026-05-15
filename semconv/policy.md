# Policy Semantic Conventions

Policy attributes describe policy checks or controls that influenced acceptance.
They do not make Motus a policy engine.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `policy.id` | Recommended | string | Policy, rule, or control identifier. |
| `policy.version` | Optional | string | Policy version or digest. |
| `policy.result` | Required | enum | One of `pass`, `fail`, `waived`, `not_applicable`, or `unknown`. |
| `policy.waiver.ref` | Optional | string | Reference to a waiver or exception record. |
| `policy.evidence.ref` | Optional | string | Evidence reference supporting the policy result. |
