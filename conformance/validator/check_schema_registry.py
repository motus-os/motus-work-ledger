#!/usr/bin/env python3
"""Verify schemas/index.json matches the schema files on disk."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMAS_DIR = REPO_ROOT / "schemas"
REGISTRY_PATH = SCHEMAS_DIR / "index.json"


def fail(message: str) -> int:
    print(f"ERROR: {message}")
    return 1


def main() -> int:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    entries = registry.get("schemas")
    if not isinstance(entries, list):
        return fail("schemas/index.json must contain a schemas array")
    hosted_resolution = registry.get("hosted_resolution")
    if not isinstance(hosted_resolution, dict):
        return fail("schemas/index.json must contain hosted_resolution")
    hosted_status = hosted_resolution.get("status")
    if hosted_status not in {"not_served_in_alpha", "served"}:
        return fail("hosted_resolution.status must be not_served_in_alpha or served")
    if hosted_status == "not_served_in_alpha":
        resolution = registry.get("resolution")
        supported = hosted_resolution.get("supported_resolution")
        if not isinstance(resolution, str) or "local" not in resolution.lower():
            return fail("not_served_in_alpha registry must document local resolution")
        if not isinstance(supported, str) or "local" not in supported.lower():
            return fail("not_served_in_alpha hosted_resolution must document local resolution")

    actual_paths = {
        path.relative_to(REPO_ROOT).as_posix() for path in SCHEMAS_DIR.glob("*.schema.json")
    }
    registry_paths: set[str] = set()
    registry_ids: set[str] = set()

    for entry in entries:
        if not isinstance(entry, dict):
            return fail("schema registry entries must be objects")
        schema_id = entry.get("id")
        schema_path = entry.get("path")
        if not isinstance(schema_id, str) or not schema_id:
            return fail(f"registry entry missing id: {entry!r}")
        if not isinstance(schema_path, str) or not schema_path:
            return fail(f"registry entry missing path: {entry!r}")
        if schema_path in registry_paths:
            return fail(f"duplicate schema path in registry: {schema_path}")
        if schema_id in registry_ids:
            return fail(f"duplicate schema id in registry: {schema_id}")

        path = REPO_ROOT / schema_path
        if not path.exists():
            return fail(f"registry path does not exist: {schema_path}")
        schema = json.loads(path.read_text(encoding="utf-8"))
        actual_id = schema.get("$id")
        if actual_id != schema_id:
            return fail(f"registry id mismatch for {schema_path}: {schema_id} != {actual_id}")

        registry_paths.add(schema_path)
        registry_ids.add(schema_id)

    missing = sorted(actual_paths - registry_paths)
    extra = sorted(registry_paths - actual_paths)
    if missing:
        return fail(f"schema files missing from registry: {', '.join(missing)}")
    if extra:
        return fail(f"registry paths without schema files: {', '.join(extra)}")

    print(
        json.dumps(
            {"valid": True, "checked": "schema-registry", "schemas": len(registry_paths)},
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
