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

from validate_receipt import validate_file


REPO_ROOT = Path(__file__).resolve().parents[2]
VALID_DIR = REPO_ROOT / "conformance" / "fixtures" / "valid"
INVALID_DIR = REPO_ROOT / "conformance" / "fixtures" / "invalid"
RECEIPT_ONLY_EMITTER = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-python" / "emit_receipt.py"
)
RECEIPT_ONLY_INPUT = (
    REPO_ROOT / "conformance" / "implementations" / "receipt-only-python" / "input.example.json"
)


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


def main() -> int:
    try:
        check_valid_fixtures()
        check_invalid_fixture_files()
        check_invalid_patch_cases()
        check_receipt_only_implementation()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"valid": True, "checked": "motus-work-ledger-conformance"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
