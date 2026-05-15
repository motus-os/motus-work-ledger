#!/usr/bin/env python3
"""Validate Motus Work Receipt Envelope fixtures."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - exercised by users without dev deps
    jsonschema = None


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
GOLDEN_DIR = REPO_ROOT / "conformance" / "golden"
ENVELOPE_SCHEMA_ID = "https://motus.dev/schemas/work-receipt-envelope.schema.json"
DATE_TIME_FIELDS = {
    "accepted_at",
    "closed_at",
    "created_at",
    "exported_at",
    "generated_at",
    "occurred_at",
    "started_at",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def receipt_digest(document: dict[str, Any]) -> str:
    return sha256_document(receipt_digest_document(document))


def load_schema_store() -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for path in SCHEMA_DIR.glob("*.schema.json"):
        schema = load_json(path)
        schemas[schema["$id"]] = schema
    return schemas


def validate_schema(document: dict[str, Any], schema_id: str = ENVELOPE_SCHEMA_ID) -> None:
    if jsonschema is None:
        raise SystemExit("jsonschema is required: pip install jsonschema")
    store = load_schema_store()
    schema = store[schema_id]
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        resolver = jsonschema.RefResolver.from_schema(schema, store=store)
    validator = jsonschema.Draft202012Validator(
        schema,
        resolver=resolver,
        format_checker=jsonschema.FormatChecker(),
    )
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        rendered = []
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "<root>"
            rendered.append(f"{path}: {error.message}")
        raise ValueError("\n".join(rendered))


def validate_golden(path: Path, digest: str) -> None:
    golden = GOLDEN_DIR / f"{path.stem}.sha256"
    if not golden.exists():
        return
    expected = golden.read_text(encoding="utf-8").strip()
    if digest != expected:
        raise ValueError(f"golden mismatch for {path}: expected {expected}, got {digest}")


def validate_date_times(document: Any, path: str = "<root>") -> None:
    if isinstance(document, dict):
        for key, value in document.items():
            child_path = f"{path}.{key}" if path != "<root>" else key
            if key in DATE_TIME_FIELDS and isinstance(value, str):
                try:
                    datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError as exc:
                    raise ValueError(f"{child_path}: {value!r} is not a date-time") from exc
            validate_date_times(value, child_path)
    elif isinstance(document, list):
        for index, value in enumerate(document):
            validate_date_times(value, f"{path}[{index}]")


def validate_declared_receipt_hashes(document: dict[str, Any], digest: str) -> None:
    receipt_id = document["receipt_id"]
    expected_receipt_id = f"sha256:{digest}"
    if receipt_id != expected_receipt_id:
        raise ValueError(f"receipt_id mismatch: expected {expected_receipt_id}, got {receipt_id}")

    receipt_hash = document["hashes"]["receipt"]
    if receipt_hash["value"] != digest:
        raise ValueError(
            "hashes.receipt.value mismatch: "
            f"expected {digest}, got {receipt_hash['value']}"
        )


def validate_file(path: Path) -> dict[str, str]:
    document = load_json(path)
    validate_schema(document)
    validate_date_times(document)
    digest = receipt_digest(document)
    validate_declared_receipt_hashes(document, digest)
    validate_golden(path, digest)
    return {"path": str(path), "receipt_id": document["receipt_id"], "sha256": digest}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipts", nargs="+", type=Path)
    args = parser.parse_args(argv)

    results = []
    try:
        for receipt in args.receipts:
            results.append(validate_file(receipt))
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"valid": True, "receipts": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
