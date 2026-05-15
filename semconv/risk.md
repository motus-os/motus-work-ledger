# Risk Semantic Conventions

Risk attributes describe material risk context without turning Motus into a risk
management system.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `risk.level` | Recommended | enum | One of `low`, `medium`, `high`, `critical`, or `unknown`. |
| `risk.category` | Optional | string | Risk category such as `security`, `release`, `data`, `availability`, or `compliance`. |
| `risk.reason` | Optional | string | Short reason for the risk classification. |
| `risk.mitigation.ref` | Optional | string | Evidence or control reference for mitigation. |
| `risk.accepted_by` | Optional | string | Actor that accepted the residual risk. |
