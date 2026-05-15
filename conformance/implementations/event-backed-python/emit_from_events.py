#!/usr/bin/env python3
"""Emit Level 1 Motus Work Ledger artifacts without importing motusos."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


CANONICALIZATION = "json.sorted.compact.v0"
RECEIPT_SCHEMA_VERSION = "motus.work-receipt-envelope.v0.1"
RUN_SCHEMA_VERSION = "motus.work-run.v0.1"
EVENT_SCHEMA_VERSION = "motus.work-event.v0.1"
STORE_EXPORT_SCHEMA_VERSION = "motus.store-export.v0.1"
PROJECTION_MANIFEST_SCHEMA_VERSION = "motus.projection-manifest.v0.1"
EVENT_KIND_SCHEMA_VERSION = "motus.event-kind-schema.v0.1"
EVENT_KIND_SCHEMAS = {
    "work.started": {
        "schema_version": EVENT_KIND_SCHEMA_VERSION,
        "event_kind": "work.started",
        "required_payload": ["work_id", "actor", "trigger", "instruction"],
    },
    "tool.used": {
        "schema_version": EVENT_KIND_SCHEMA_VERSION,
        "event_kind": "tool.used",
        "required_payload": ["tool_refs"],
    },
    "evidence.referenced": {
        "schema_version": EVENT_KIND_SCHEMA_VERSION,
        "event_kind": "evidence.referenced",
        "required_payload": ["evidence_refs"],
    },
    "work.closed": {
        "schema_version": EVENT_KIND_SCHEMA_VERSION,
        "event_kind": "work.closed",
        "required_payload": ["outcome", "acceptance", "route_summary", "handoff"],
    },
}


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def digest_object(value: Any, canonicalization: str = CANONICALIZATION) -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "value": sha256_value(value),
        "canonicalization": canonicalization,
    }


def digest_text(value: str, canonicalization: str) -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "value": sha256_text(value),
        "canonicalization": canonicalization,
    }


def prefixed_sha256(value: Any) -> str:
    return f"sha256:{sha256_value(value)}"


def receipt_digest_document(document: dict[str, Any]) -> dict[str, Any]:
    base = copy.deepcopy(document)
    base.pop("receipt_id", None)
    hashes = base.get("hashes")
    if isinstance(hashes, dict):
        hashes.pop("receipt", None)
    return base


def find_one(events: list[dict[str, Any]], event_kind: str) -> dict[str, Any]:
    matches = [event for event in events if event["event_kind"] == event_kind]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {event_kind} event, got {len(matches)}")
    return matches[0]


def event_kind_schema_hash(event_kind: str) -> str:
    try:
        schema = EVENT_KIND_SCHEMAS[event_kind]
    except KeyError as exc:
        raise ValueError(f"unknown event kind: {event_kind}") from exc
    return prefixed_sha256(schema)


def build_event(
    run_id: str,
    seq: int,
    producer_id: str,
    descriptor: dict[str, Any],
) -> dict[str, Any]:
    event_kind = descriptor["event_kind"]
    payload = descriptor["payload"]
    event_without_id = {
        "schema_version": EVENT_SCHEMA_VERSION,
        "run_id": run_id,
        "seq": seq,
        "event_kind": event_kind,
        "occurred_at": descriptor["occurred_at"],
        "idempotency_key": descriptor["idempotency_key"],
        "payload_hash": prefixed_sha256(payload),
        "schema_hash": event_kind_schema_hash(event_kind),
        "producer_id": producer_id,
        "payload": payload,
    }
    return {"event_id": prefixed_sha256(event_without_id), **event_without_id}


def build_store_export(source: dict[str, Any]) -> dict[str, Any]:
    events = [
        build_event(source["run_id"], index, source["producer_id"], descriptor)
        for index, descriptor in enumerate(source["events"], start=1)
    ]
    closed = find_one(events, "work.closed")["payload"]
    started = find_one(events, "work.started")["payload"]
    if source["work_id"] != started["work_id"]:
        raise ValueError("top-level work_id must match work.started payload work_id")
    run = {
        "schema_version": RUN_SCHEMA_VERSION,
        "run_id": source["run_id"],
        "work_id": started["work_id"],
        "status": "closed",
        "started_at": source["started_at"],
        "closed_at": closed["outcome"]["closed_at"],
        "producer_id": source["producer_id"],
        "outcome_status": closed["outcome"]["status"],
    }
    return {
        "schema_version": STORE_EXPORT_SCHEMA_VERSION,
        "exported_at": source["exported_at"],
        "canonicalization": CANONICALIZATION,
        "runs": [run],
        "events": events,
    }


def collect_payload_lists(events: list[dict[str, Any]], event_kind: str, key: str) -> list[Any]:
    values: list[Any] = []
    for event in events:
        if event["event_kind"] != event_kind:
            continue
        values.extend(event["payload"].get(key, []))
    return values


def build_receipt(source: dict[str, Any], store_export: dict[str, Any]) -> dict[str, Any]:
    events = store_export["events"]
    started = find_one(events, "work.started")["payload"]
    closed = find_one(events, "work.closed")["payload"]
    instruction = started["instruction"]
    source_export_digest = digest_object(store_export)
    receipt = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_id": "sha256:" + ("0" * 64),
        "run_id": store_export["runs"][0]["run_id"],
        "work_id": started["work_id"],
        "actor": started["actor"],
        "runtime": {
            "name": "motus-event-backed-python",
            "kind": "sdk",
            "version": "0.1.0",
        },
        "trigger": started["trigger"],
        "instruction_ref": {
            "kind": instruction["kind"],
            "summary": instruction.get("summary", ""),
            "digest": digest_text(instruction["canonical_text"], "utf8.instruction.v0"),
        },
        "events_ref": {
            "uri": source["events_ref_uri"],
            "digest": source_export_digest,
        },
        "evidence_refs": collect_payload_lists(events, "evidence.referenced", "evidence_refs"),
        "tool_refs": collect_payload_lists(events, "tool.used", "tool_refs"),
        "outcome": closed["outcome"],
        "acceptance": closed["acceptance"],
        "route_summary": closed.get("route_summary", {"status": "complete"}),
        "handoff": closed.get("handoff", {"status": "none"}),
        "canonicalization": {
            "method": CANONICALIZATION,
            "volatile_fields": ["created_at"],
        },
        "hashes": {
            "receipt": {
                "algorithm": "sha256",
                "value": "0" * 64,
                "canonicalization": CANONICALIZATION,
            },
            "source_export": source_export_digest,
        },
        "redaction": closed.get("redaction", {"status": "none"}),
        "created_at": source["receipt_created_at"],
    }
    receipt_digest = sha256_value(receipt_digest_document(receipt))
    receipt["receipt_id"] = f"sha256:{receipt_digest}"
    receipt["hashes"]["receipt"]["value"] = receipt_digest
    return receipt


def build_projection_manifest(
    source: dict[str, Any],
    store_export: dict[str, Any],
    receipt: dict[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": PROJECTION_MANIFEST_SCHEMA_VERSION,
        "projection_id": source["projection_id"],
        "source_export_hash": prefixed_sha256(store_export),
        "generated_at": source["receipt_created_at"],
        "canonicalization": CANONICALIZATION,
        "projections": {
            "work_receipt": {
                "kind": "work_receipt",
                "uri": source["receipt_uri"],
                "digest": receipt["receipt_id"],
            }
        },
    }


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    store_export = build_store_export(source)
    receipt = build_receipt(source, store_export)
    projection_manifest = build_projection_manifest(source, store_export, receipt)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "store-export.json", store_export)
    write_json(args.output_dir / "receipt.json", receipt)
    write_json(args.output_dir / "projection-manifest.json", projection_manifest)

    print(receipt["receipt_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
