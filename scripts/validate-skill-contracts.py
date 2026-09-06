#!/usr/bin/env python3
"""Validate Skill Contracts and zh/en locale parity.

Stdlib-only validator. It intentionally validates the contract surface rather
than comparing localized prose, so zh_CN and en_US may differ in content.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = (
    "name",
    "description",
    "category",
    "owner",
    "version",
    "inputs",
    "outputs",
    "side_effects",
    "requires",
    "forbidden",
    "idempotent",
    "platform_dependent",
)
LIST_FIELDS = {"inputs", "outputs", "side_effects", "requires", "forbidden"}
BOOL_FIELDS = {"idempotent", "platform_dependent"}
ALLOWED_CATEGORIES = {"methodology", "orchestration", "platform", "gate"}
SEMVER_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")


def fail(errors: list[str], path: Path, message: str) -> None:
    errors.append(f"[FAIL] {path}: {message}")


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(errors, path, "missing YAML frontmatter")
        return {}

    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        fail(errors, path, "unterminated YAML frontmatter")
        return {}

    data: dict[str, object] = {}
    duplicates: set[str] = set()
    i = 1
    while i < end:
        raw = lines[i]
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        if raw.startswith((" ", "\t")):
            fail(errors, path, f"unexpected indentation at line {i + 1}")
            i += 1
            continue
        if ":" not in raw:
            fail(errors, path, f"invalid frontmatter line {i + 1}")
            i += 1
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in data:
            duplicates.add(key)
        if value == "":
            items: list[str] = []
            j = i + 1
            while j < end:
                child = lines[j]
                if child.strip() == "" or child.lstrip().startswith("#"):
                    j += 1
                    continue
                if not child.startswith((" ", "\t")):
                    break
                stripped = child.strip()
                if not stripped.startswith("-"):
                    fail(errors, path, f"unsupported nested YAML under '{key}' at line {j + 1}")
                    j += 1
                    continue
                item = stripped[1:].strip()
                items.append(item)
                j += 1
            data[key] = items
            i = j
            continue
        data[key] = value
        i += 1

    for key in sorted(duplicates):
        fail(errors, path, f"duplicate top-level key '{key}'")
    return data


def validate_skill(path: Path, locale: str, root: Path, errors: list[str]) -> dict[str, object]:
    data = parse_frontmatter(path, errors)
    rel = path.relative_to(root)
    dirname = path.parent.name

    for key in REQUIRED:
        if key not in data:
            fail(errors, path, f"missing required field '{key}'")

    if data.get("name") != dirname:
        fail(errors, path, f"name must equal directory name '{dirname}'")

    category = data.get("category")
    if category not in ALLOWED_CATEGORIES:
        fail(errors, path, f"category must be one of {sorted(ALLOWED_CATEGORIES)}, got {category!r}")

    version = data.get("version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        fail(errors, path, "version must be numeric semver-like (e.g. 1.0 or 1.0.0)")

    for key in LIST_FIELDS:
        if key in data and not isinstance(data[key], list):
            fail(errors, path, f"{key} must be a YAML list (use [] when empty)")

    for key in BOOL_FIELDS:
        if key not in data or data[key] not in {"true", "false"}:
            fail(errors, path, f"{key} must be YAML boolean true/false")

    for key in ("name", "description", "owner"):
        if key in data and not isinstance(data[key], str):
            fail(errors, path, f"{key} must be a scalar string")

    return {"path": str(rel), **data}


def discover(locale_dir: Path) -> dict[str, Path]:
    result: dict[str, Path] = {}
    if not locale_dir.is_dir():
        return result
    for skill_file in sorted(locale_dir.glob("*/SKILL.md")):
        result[skill_file.parent.name] = skill_file
    return result


def check_parity(zh: dict[str, dict[str, object]], en: dict[str, dict[str, object]], errors: list[str]) -> None:
    zh_names = set(zh)
    en_names = set(en)
    for name in sorted(zh_names - en_names):
        fail(errors, Path(f"zh_CN/skills/{name}"), "missing en_US counterpart")
    for name in sorted(en_names - zh_names):
        fail(errors, Path(f"en_US/skills/{name}"), "missing zh_CN counterpart")

    for name in sorted(zh_names & en_names):
        z = zh[name]
        e = en[name]
        for key in REQUIRED:
            if key not in z or key not in e:
                continue
            if key in {"name", "category", "owner", "version"} and z[key] != e[key]:
                fail(errors, Path(f"skills/{name}"), f"zh/en mismatch for {key}: {z[key]!r} != {e[key]!r}")
        for key in REQUIRED:
            if (key in z) != (key in e):
                fail(errors, Path(f"skills/{name}"), f"zh/en contract key-set mismatch for '{key}'")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--contract-only", action="store_true", help="skip zh/en parity checks")
    parser.add_argument("--parity-only", action="store_true", help="skip field-level contract validation")
    args = parser.parse_args()

    if args.contract_only and args.parity_only:
        parser.error("--contract-only and --parity-only are mutually exclusive")

    skills_root = args.root / "templates"
    zh_paths = discover(skills_root / "zh_CN" / "skills")
    en_paths = discover(skills_root / "en_US" / "skills")
    errors: list[str] = []
    zh_data: dict[str, dict[str, object]] = {}
    en_data: dict[str, dict[str, object]] = {}

    if not args.parity_only:
        for name, path in zh_paths.items():
            zh_data[name] = validate_skill(path, "zh_CN", skills_root, errors)
        for name, path in en_paths.items():
            en_data[name] = validate_skill(path, "en_US", skills_root, errors)
    else:
        for name, path in zh_paths.items():
            zh_data[name] = parse_frontmatter(path, errors)
        for name, path in en_paths.items():
            en_data[name] = parse_frontmatter(path, errors)

    if not args.contract_only:
        check_parity(zh_data, en_data, errors)

    total = len(zh_paths) + len(en_paths)
    if errors:
        print(f"Skill Contract validation FAILED: {len(errors)} error(s), {total} locale skill file(s) checked.")
        for error in errors:
            print(error)
        return 1

    print(f"Skill Contract validation PASSED: {total} locale skill file(s) checked; zh/en parity OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
