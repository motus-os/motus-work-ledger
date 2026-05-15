# Handoff Semantic Conventions

Handoff attributes describe transfer of context to another actor or system.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `handoff.status` | Required | enum | One of `none`, `ready`, or `blocked`. |
| `handoff.receiver.type` | Optional | enum | Type of actor or system expected to receive the handoff. |
| `handoff.receiver.id` | Optional | string | Actor or system identifier expected to receive the handoff. |
| `handoff.expected_action` | Optional | string | Short next action expected of the receiver. |
| `handoff.reason` | Optional | string | Short reason for the handoff status. |
| `handoff.evidence_refs` | Optional | array | Evidence identifiers included in the handoff. |

If `handoff.receiver` is emitted in a strict receipt envelope, both
`handoff.receiver.type` and `handoff.receiver.id` are required by the schema.
