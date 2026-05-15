# Semantic Convention To Schema Mapping

This table maps dotted semantic convention attributes to canonical Work Receipt
Envelope schema fields. The dotted names are documentation and telemetry-style
attribute names; the schema paths are the JSON fields an implementation emits.
Do not emit dotted semantic attribute names as extra fields inside strict receipt
objects unless the schema explicitly allows them.

If an attribute is not listed here, it either already matches the schema field
name directly or is metadata outside the current receipt envelope schemas.

## Work

Schema: `schemas/work-receipt-envelope.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `work.id` | `work_id` | string |
| `work.outcome.status` | `outcome.status` | `success`, `failure`, `partial`, `aborted`, `superseded`, `unknown` |
| `work.outcome.summary` | `outcome.summary` | string |
| `work.closed_at` | `outcome.closed_at` | RFC 3339 string |
| `work.intent` | `instruction_ref.summary` | string |
| `work.contract.ref` | `instruction_ref.uri` | string |

`work.type` and `work.started_at` are event or telemetry metadata in v0.1.
They must not be emitted as extra fields inside a strict Work Receipt Envelope.

## Evidence Reference

Schema: `schemas/evidence-ref.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `evidence.evidence_id` | `evidence_refs[].evidence_id` | string |
| `evidence.kind` | `evidence_refs[].kind` | string |
| `evidence.uri` | `evidence_refs[].uri` | string |
| `evidence.digest` | `evidence_refs[].digest` | digest object |
| `evidence.summary` | `evidence_refs[].summary` | string |
| `evidence.redaction.status` | `evidence_refs[].redaction.status` | `none`, `redacted`, `withheld` |

## Actor

Schema: `schemas/work-receipt-envelope.schema.json#/$defs/actor`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `actor.type` | `actor.type` | `human`, `agent`, `service`, `ci`, `tool` |
| `actor.id` | `actor.id` | string |
| `actor.display` | `actor.display` | string |

`actor.authn.method` and `actor.org` are telemetry metadata in v0.1. They must
not be emitted as extra fields inside a strict receipt-envelope actor object.

## Acceptance

Schema: `schemas/acceptance.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `acceptance.status` | `acceptance.status` | `accepted`, `rejected`, `not_required`, `pending` |
| `acceptance.actor.type` | `acceptance.actor.type` | `human`, `agent`, `service`, `ci`, `tool` |
| `acceptance.actor.id` | `acceptance.actor.id` | string |
| `acceptance.accepted_at` | `acceptance.accepted_at` | RFC 3339 string |
| `acceptance.method` | `acceptance.method` | string |
| `acceptance.rationale_ref` | `acceptance.rationale_ref` | string |

## Route Summary

Schema: `schemas/route-summary.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `route.status` | `route_summary.status` | `complete`, `handoff`, `blocked`, `none` |
| `route.next_actor.type` | `route_summary.next_actor.type` | `human`, `agent`, `service`, `ci`, `tool` |
| `route.next_actor.id` | `route_summary.next_actor.id` | string |
| `route.reason` | `route_summary.reason` | string |
| `route.route_ref` | `route_summary.route_ref` | string |

## Handoff

Schema: `schemas/handoff.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `handoff.status` | `handoff.status` | `none`, `ready`, `blocked` |
| `handoff.receiver.type` | `handoff.receiver.type` | `human`, `agent`, `service`, `ci`, `tool` |
| `handoff.receiver.id` | `handoff.receiver.id` | string |
| `handoff.expected_action` | `handoff.expected_action` | string |
| `handoff.reason` | `handoff.reason` | string |
| `handoff.evidence_refs` | `handoff.evidence_refs[]` | array of evidence identifiers |

## Tool Reference

Schema: `schemas/work-receipt-envelope.schema.json`

| Semantic attribute | Schema path | Allowed values |
| --- | --- | --- |
| `tool.name` | `tool_refs[].name` | string |
| `tool.kind` | `tool_refs[].kind` | string |
| `tool.output.hash` | `tool_refs[].digest` | digest object |

Other tool attributes are event payload or evidence metadata until a future
schema version admits them directly.
