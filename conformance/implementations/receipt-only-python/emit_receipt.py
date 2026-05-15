#!/usr/bin/env python3
"""Emit a Motus Level 0 Work Receipt Envelope without importing motusos."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "motus.work-receipt-envelope.v0.1"
CANONICALIZATION = "json.sorted.compact.v0"


def canonical_bytes(document: dict[str, Any]) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def sha256_document(document: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(document)).hexdigest()


def receipt_digest_document(document: dict[str, Any]) -> dict[str, Any]:
    base = copy.deepcopy(document)
    base.pop("receipt_id", None)
    hashes = base.get("hashes")
    if isinstance(hashes, dict):
        hashes.pop("receipt", None)
    return base


def digest(value: str, canonicalization: str = "utf8") -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "value": hashlib.sha256(value.encode("utf-8")).hexdigest(),
        "canonicalization": canonicalization,
    }


def digest_document(document: dict[str, Any], canonicalization: str) -> dict[str, str]:
    return {
        "algorithm": "sha256",
        "value": hashlib.sha256(canonical_bytes(document)).hexdigest(),
        "canonicalization": canonicalization,
    }


def build_receipt(source: dict[str, Any]) -> dict[str, Any]:
    events_digest = digest_document(source["events"], CANONICALIZATION)
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "receipt_id": "sha256:" + ("0" * 64),
        "run_id": source["run_id"],
        "work_id": source["work_id"],
        "actor": source["actor"],
        "runtime": {
            "name": "motus-receipt-only-python",
            "kind": "sdk",
            "version": "0.1.0",
        },
        "trigger": source.get("trigger", {"kind": "manual"}),
        "instruction_ref": {
            "kind": source["instruction"]["kind"],
            "summary": source["instruction"].get("summary", ""),
            "digest": digest(source["instruction"]["canonical_text"], "utf8.instruction.v0"),
        },
        "events_ref": {
            "uri": source["events"]["uri"],
            "digest": events_digest,
        },
        "evidence_refs": source.get("evidence_refs", []),
        "tool_refs": source.get("tool_refs", []),
        "outcome": source["outcome"],
        "acceptance": source["acceptance"],
        "route_summary": source.get("route_summary", {"status": "complete"}),
        "handoff": source.get("handoff", {"status": "none"}),
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
            "source_export": events_digest,
        },
        "redaction": source.get("redaction", {"status": "none"}),
        "created_at": source["created_at"],
    }
    receipt_digest = sha256_document(receipt_digest_document(receipt))
    receipt["receipt_id"] = f"sha256:{receipt_digest}"
    receipt["hashes"]["receipt"]["value"] = receipt_digest
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source = json.loads(args.input.read_text(encoding="utf-8"))
    receipt = build_receipt(source)
    args.output.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(receipt["receipt_id"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
