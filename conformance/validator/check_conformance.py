#!/usr/bin/env python3
"""Run the Motus Work Ledger conformance checks."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from validate_receipt import sha256_document, validate_file, validate_schema


REPO_ROOT = Path(__file__).resolve().parents[2]
VALID_DIR = REPO_ROOT / "conformance" / "fixtures" / "valid"
INVALID_DIR = REPO_ROOT / "conformance" / "fixtures" / "invalid"
RECEIPT_ONLY_EMITTER = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-python" / "emit_receipt.py"
)
RECEIPT_ONLY_INPUT = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-python" / "input.example.json"
)
EVENT_BACKED_EMITTER = (
    REPO_ROOT / "conformance" / "implementations" / "event-backed-python" / "emit_from_events.py"
)
EVENT_BACKED_INPUT = (
    REPO_ROOT / "conformance" / "implementations" / "event-backed-python" / "input.example.json"
)
RECEIPT_ONLY_NODE_EMITTER = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-node" / "emit-receipt.mjs"
)
RECEIPT_ONLY_NODE_INPUT = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-node" / "input.example.json"
)
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
STORE_EXPORT_SCHEMA_ID = "https://motus.dev/schemas/store-export.schema.json"
PROJECTION_MANIFEST_SCHEMA_ID = "https://motus.dev/schemas/projection-manifest.schema.json"
CANONICALIZATION = "json.sorted.compact.v0"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def set_path(document: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = dotted_path.split(".")
    cursor: Any = document
    for part in parts[:-1]:
        cursor = cursor[int(part)] if part.isdigit() else cursor[part]
    final = parts[-1]
    if final.isdigit():
        cursor[int(final)] = value
    else:
        cursor[final] = value


def remove_path(document: dict[str, Any], dotted_path: str) -> None:
    parts = dotted_path.split(".")
    cursor: Any = document
    for part in parts[:-1]:
        cursor = cursor[int(part)] if part.isdigit() else cursor[part]
    final = parts[-1]
    if final.isdigit():
        del cursor[int(final)]
    else:
        cursor.pop(final, None)


def apply_case(base: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(base)
    for path in case.get("remove", []):
        remove_path(candidate, path)
    for path, value in case.get("set", {}).items():
        set_path(candidate, path, value)
    for key, value in case.get("literal_set", {}).items():
        candidate[key] = value
    return candidate


def expect_invalid(path: Path, expected: str) -> None:
    try:
        validate_file(path)
    except Exception as exc:
        if expected not in str(exc):
            raise AssertionError(f"{path}: expected {expected!r} in {exc!r}") from exc
        return
    raise AssertionError(f"{path}: expected validation failure")


def check_valid_fixtures() -> None:
    for fixture in sorted(VALID_DIR.glob("*.json")):
        validate_file(fixture)


def check_invalid_fixture_files() -> None:
    for fixture in sorted(INVALID_DIR.glob("*.json")):
        if fixture.name == "cases.json":
            continue
        expect_invalid(fixture, "acceptance")


def check_invalid_patch_cases() -> None:
    base = load_json(VALID_DIR / "work-receipt-minimal.json")
    cases = load_json(INVALID_DIR / "cases.json")
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for case in cases:
            candidate = apply_case(base, case)
            path = tmpdir / f"{case['name']}.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            expect_invalid(path, case["expect"])


def check_receipt_only_implementation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "receipt.json"
        result = subprocess.run(
            [
                sys.executable,
                str(RECEIPT_ONLY_EMITTER),
                "--input",
                str(RECEIPT_ONLY_INPUT),
                "--output",
                str(output),
            ],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        validate_file(output)


def check_receipt_only_node_implementation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "receipt.json"
        result = subprocess.run(
            [
                "node",
                str(RECEIPT_ONLY_NODE_EMITTER),
                "--input",
                str(RECEIPT_ONLY_NODE_INPUT),
                "--output",
                str(output),
            ],
            cwd=REPO_ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            raise AssertionError(result.stderr)
        validate_file(output)


def run_event_backed(output_dir: Path) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(EVENT_BACKED_EMITTER),
            "--input",
            str(EVENT_BACKED_INPUT),
            "--output-dir",
            str(output_dir),
        ],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr)


def check_event_ordering(store_export: dict[str, Any]) -> None:
    events = store_export["events"]
    expected_seq = list(range(1, len(events) + 1))
    actual_seq = [event["seq"] for event in events]
    if actual_seq != expected_seq:
        raise AssertionError(f"event seq mismatch: expected {expected_seq}, got {actual_seq}")
    run_ids = {event["run_id"] for event in events}
    if run_ids != {store_export["runs"][0]["run_id"]}:
        raise AssertionError(f"event run_id mismatch: {sorted(run_ids)}")
    event_kinds = {event["event_kind"] for event in events}
    if not {"work.started", "work.closed"}.issubset(event_kinds):
        raise AssertionError(f"missing required event kinds: {sorted(event_kinds)}")
    started_seq = [event["seq"] for event in events if event["event_kind"] == "work.started"]
    closed_seq = [event["seq"] for event in events if event["event_kind"] == "work.closed"]
    if len(started_seq) != 1 or len(closed_seq) != 1:
        raise AssertionError("event-backed export must contain exactly one work.started and one work.closed")
    if started_seq[0] >= closed_seq[0]:
        raise AssertionError("work.started must occur before work.closed")
    if closed_seq[0] != len(events):
        raise AssertionError("work.closed must be the terminal event")


def prefixed_sha256_document(document: dict[str, Any]) -> str:
    return f"sha256:{sha256_document(document)}"


def check_event_hashes(store_export: dict[str, Any]) -> None:
    for event in store_export["events"]:
        expected_schema_hash = prefixed_sha256_document(EVENT_KIND_SCHEMAS[event["event_kind"]])
        if event["schema_hash"] != expected_schema_hash:
            raise AssertionError(
                f"schema_hash mismatch for seq {event['seq']}: "
                f"expected {expected_schema_hash}, got {event['schema_hash']}"
            )
        expected_payload_hash = prefixed_sha256_document(event["payload"])
        if event["payload_hash"] != expected_payload_hash:
            raise AssertionError(
                f"payload_hash mismatch for seq {event['seq']}: "
                f"expected {expected_payload_hash}, got {event['payload_hash']}"
            )
        event_without_id = copy.deepcopy(event)
        event_without_id.pop("event_id", None)
        expected_event_id = prefixed_sha256_document(event_without_id)
        if event["event_id"] != expected_event_id:
            raise AssertionError(
                f"event_id mismatch for seq {event['seq']}: "
                f"expected {expected_event_id}, got {event['event_id']}"
            )


def check_source_export_hashes(
    store_export: dict[str, Any],
    receipt: dict[str, Any],
    projection_manifest: dict[str, Any],
) -> None:
    store_digest = sha256_document(store_export)
    expected_digest = {
        "algorithm": "sha256",
        "value": store_digest,
        "canonicalization": CANONICALIZATION,
    }
    if receipt["events_ref"]["digest"] != expected_digest:
        raise AssertionError("receipt events_ref digest does not match Store export")
    if receipt["hashes"]["source_export"] != expected_digest:
        raise AssertionError("receipt source_export digest does not match Store export")
    if projection_manifest["source_export_hash"] != f"sha256:{store_digest}":
        raise AssertionError("projection manifest source_export_hash does not match Store export")
    receipt_projection = projection_manifest["projections"]["work_receipt"]
    if receipt_projection["digest"] != receipt["receipt_id"]:
        raise AssertionError("projection manifest receipt digest does not match receipt_id")


def check_receipt_projection_consistency(
    store_export: dict[str, Any],
    receipt: dict[str, Any],
) -> None:
    run = store_export["runs"][0]
    events = store_export["events"]
    started = next(event for event in events if event["event_kind"] == "work.started")["payload"]
    closed = next(event for event in events if event["event_kind"] == "work.closed")["payload"]

    expected_pairs = [
        ("run_id", receipt["run_id"], run["run_id"]),
        ("work_id", receipt["work_id"], run["work_id"]),
        ("work_id", receipt["work_id"], started["work_id"]),
        ("actor", receipt["actor"], started["actor"]),
        ("trigger", receipt["trigger"], started["trigger"]),
        ("outcome", receipt["outcome"], closed["outcome"]),
        ("acceptance", receipt["acceptance"], closed["acceptance"]),
        ("route_summary", receipt["route_summary"], closed["route_summary"]),
        ("handoff", receipt["handoff"], closed["handoff"]),
        ("redaction", receipt["redaction"], closed["redaction"]),
    ]
    for label, actual, expected in expected_pairs:
        if actual != expected:
            raise AssertionError(f"receipt {label} does not match Store facts")
    if run["status"] != "closed":
        raise AssertionError("event-backed run must be closed")
    if run["outcome_status"] != closed["outcome"]["status"]:
        raise AssertionError("run outcome_status does not match work.closed outcome")
    if run["closed_at"] != closed["outcome"]["closed_at"]:
        raise AssertionError("run closed_at does not match work.closed outcome")


def check_event_backed_implementation() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "first"
        second = Path(tmp) / "second"
        first.mkdir()
        second.mkdir()

        run_event_backed(first)
        run_event_backed(second)

        for filename in ("store-export.json", "receipt.json", "projection-manifest.json"):
            first_bytes = (first / filename).read_bytes()
            second_bytes = (second / filename).read_bytes()
            if first_bytes != second_bytes:
                raise AssertionError(f"event-backed output is not deterministic: {filename}")

        store_export = load_json(first / "store-export.json")
        projection_manifest = load_json(first / "projection-manifest.json")
        receipt = load_json(first / "receipt.json")

        validate_schema(store_export, STORE_EXPORT_SCHEMA_ID)
        validate_schema(projection_manifest, PROJECTION_MANIFEST_SCHEMA_ID)
        validate_file(first / "receipt.json")
        check_event_ordering(store_export)
        check_event_hashes(store_export)
        check_source_export_hashes(store_export, receipt, projection_manifest)
        check_receipt_projection_consistency(store_export, receipt)


def main() -> int:
    try:
        check_valid_fixtures()
        check_invalid_fixture_files()
        check_invalid_patch_cases()
        check_receipt_only_implementation()
        check_receipt_only_node_implementation()
        check_event_backed_implementation()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"valid": True, "checked": "motus-work-ledger-conformance"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
