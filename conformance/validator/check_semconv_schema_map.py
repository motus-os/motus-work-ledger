#!/usr/bin/env python3
"""Verify strict receipt semantic attributes are mapped to schema fields."""

from __future__ import annotations

import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SEMCONV_DIR = REPO_ROOT / "semconv"
SCHEMA_MAP = SEMCONV_DIR / "schema-map.md"
STRICT_SEMCONV_FILES = [
    "work.md",
    "actor.md",
    "evidence.md",
    "acceptance.md",
    "route.md",
    "handoff.md",
    "tool.md",
]

ATTRIBUTE_CELL = re.compile(r"^\|\s*`([^`]+)`\s*\|")


def table_attributes(path: Path) -> list[tuple[str, str]]:
    attributes: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ATTRIBUTE_CELL.match(line)
        if not match:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        attributes.append((match.group(1), cells[1].lower()))
    return attributes


def mapped_attributes() -> set[str]:
    return {attribute for attribute, _ in table_attributes(SCHEMA_MAP)}


def main() -> int:
    mapped = mapped_attributes()
    missing: list[str] = []

    for filename in STRICT_SEMCONV_FILES:
        path = SEMCONV_DIR / filename
        for attribute, requirement in table_attributes(path):
            if "telemetry" in requirement:
                continue
            if attribute not in mapped:
                missing.append(f"{filename}: {attribute}")

    if missing:
        print("ERROR: strict semconv attributes missing schema-map entries")
        for item in missing:
            print(f"- {item}")
        return 1

    print(
        json.dumps(
            {
                "valid": True,
                "checked": "semconv-schema-map",
                "strict_files": len(STRICT_SEMCONV_FILES),
                "mapped_attributes": len(mapped),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
