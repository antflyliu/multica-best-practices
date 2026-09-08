#!/usr/bin/env python3
"""Repository-level validation for the Copy. Paste. Run. template library."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
SKILL_REQUIRED = (
    "name", "description", "category", "owner", "version",
    "inputs", "outputs", "side_effects", "requires", "forbidden",
    "idempotent", "platform_dependent",
)
SKILL_LIST_FIELDS = {"inputs", "outputs", "side_effects", "requires", "forbidden"}
SKILL_BOOL_FIELDS = {"idempotent", "platform_dependent"}
SKILL_CATEGORIES = {"methodology", "orchestration", "platform", "gate"}
SKILL_VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")
MIXED_LANGUAGE_FRAGMENTS = (
    "no无效的", "only无效", "data口径", "cross-scope口径", "cross-cutting口径", "field口径",
)
FORBIDDEN_AGENT_PLATFORM_PATTERNS = (
    r"https?://[^\s<>]+",
    r"(?:JENKINS_TOKEN|ATLASSIAN_TOKEN|API_KEY)\s*[:=]",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"non-UTF-8 file: {path}: {exc}")


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = read_text(path)
    if not text.startswith("---"):
        fail(f"missing YAML frontmatter: {path}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"invalid YAML frontmatter: {path}")
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        fail(f"invalid frontmatter YAML in {path}: {exc}")
    if not isinstance(meta, dict):
        fail(f"frontmatter must be a YAML mapping: {path}")
    return meta


def discover_skills(locale: str) -> dict[str, Path]:
    root = TEMPLATES / locale / "skills"
    if not root.is_dir():
        fail(f"missing skill directory: {root}")
    result: dict[str, Path] = {}
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        skill_file = child / "SKILL.md"
        if not skill_file.is_file():
            fail(f"skill directory missing SKILL.md: {child}")
        result[child.name] = skill_file
    return result


def validate_skill_contract(path: Path) -> dict[str, object]:
    meta = parse_frontmatter(path)
    dirname = path.parent.name
    for key in SKILL_REQUIRED:
        if key not in meta:
            fail(f"missing Skill Contract field '{key}': {path}")
    if meta.get("name") != dirname:
        fail(f"skill name mismatch: {path}: {meta.get('name')!r} != {dirname!r}")
    if meta.get("category") not in SKILL_CATEGORIES:
        fail(f"invalid skill category: {path}: {meta.get('category')!r}")
    version = meta.get("version")
    if not isinstance(version, str) or not SKILL_VERSION_RE.fullmatch(version):
        fail(f"invalid skill version: {path}: {version!r}")
    for key in SKILL_LIST_FIELDS:
        if not isinstance(meta.get(key), list):
            fail(f"Skill Contract field '{key}' must be a YAML list: {path}")
    for key in SKILL_BOOL_FIELDS:
        if not isinstance(meta.get(key), bool):
            fail(f"Skill Contract field '{key}' must be boolean true/false: {path}")
    for key in ("name", "description", "owner"):
        if not isinstance(meta.get(key), str):
            fail(f"Skill Contract field '{key}' must be a string: {path}")
    return meta


def validate_skill_contracts_and_parity() -> None:
    zh = discover_skills("zh_CN")
    en = discover_skills("en_US")
    zh_meta = {name: validate_skill_contract(path) for name, path in zh.items()}
    en_meta = {name: validate_skill_contract(path) for name, path in en.items()}
    if set(zh) != set(en):
        missing_en = sorted(set(zh) - set(en))
        missing_zh = sorted(set(en) - set(zh))
        if missing_en:
            fail(f"zh_CN skill(s) missing en_US counterpart: {', '.join(missing_en)}")
        if missing_zh:
            fail(f"en_US skill(s) missing zh_CN counterpart: {', '.join(missing_zh)}")
    for name in sorted(set(zh) & set(en)):
        for key in ("name", "category", "owner", "version"):
            if zh_meta[name].get(key) != en_meta[name].get(key):
                fail(f"zh/en Skill Contract mismatch for {name}.{key}: {zh_meta[name].get(key)!r} != {en_meta[name].get(key)!r}")
        for key in SKILL_REQUIRED:
            if (key in zh_meta[name]) != (key in en_meta[name]):
                fail(f"zh/en Skill Contract key-set mismatch for {name}.{key}")


def validate_skill_frontmatter() -> None:
    # Kept as a focused repository check in addition to the full Skill Contract validation.
    validate_skill_contracts_and_parity()


def validate_yaml_files() -> None:
    for path in sorted(TEMPLATES.rglob("*.yaml")) + sorted(TEMPLATES.rglob("*.yml")):
        try:
            yaml.safe_load(read_text(path))
        except yaml.YAMLError as exc:
            fail(f"invalid YAML: {path}: {exc}")


def validate_python_syntax() -> None:
    import ast
    for path in sorted(TEMPLATES.rglob("*.py")):
        try:
            ast.parse(read_text(path), filename=str(path))
        except SyntaxError as exc:
            fail(f"invalid Python syntax: {path}: {exc}")


def validate_mixed_language_fragments() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or path.name == "CHANGELOG.md":
            continue
        text = read_text(path)
        for fragment in MIXED_LANGUAGE_FRAGMENTS:
            if fragment in text:
                fail(f"audited mixed-language fragment {fragment!r} found in {path}")


def validate_agent_platform_separation() -> None:
    for root in (TEMPLATES / "zh_CN" / "agents", TEMPLATES / "en_US" / "agents"):
        if not root.is_dir():
            fail(f"missing agent directory: {root}")
        for path in sorted(root.glob("*.md")):
            text = read_text(path)
            for pattern in FORBIDDEN_AGENT_PLATFORM_PATTERNS:
                if re.search(pattern, text, flags=re.IGNORECASE):
                    fail(f"platform-specific URL/credential pattern in Agent Instructions: {path}")


def validate_gate_contracts() -> None:
    for lang in ("zh_CN", "en_US"):
        gate = read_text(ROOT / "docs" / lang / "gates-and-evidence.md")
        for marker in ("G2.5", "G2.5 PASS", "T3", "APPROVED_NA", "BLOCKED"):
            if marker not in gate:
                fail(f"missing gate contract {marker!r}: docs/{lang}/gates-and-evidence.md")
        if "any artifact is modified" not in gate.lower() and "任何产物" not in gate:
            fail(f"missing downstream invalidation rule: docs/{lang}/gates-and-evidence.md")


def validate_t3_dependencies() -> None:
    for lang in ("zh_CN", "en_US"):
        squad = read_text(TEMPLATES / lang / "squad" / "software-development" / "squad.md")
        if "@DevOps" not in squad:
            fail(f"software-development squad missing @DevOps: templates/{lang}/squad/software-development/squad.md")
        if "multica-test-automation" not in squad:
            fail(f"software-development squad missing multica-test-automation: templates/{lang}/squad/software-development/squad.md")
        if "G2.5 PASS" not in squad:
            fail(f"software-development squad missing G2.5→T3 dependency: templates/{lang}/squad/software-development/squad.md")
        automation = TEMPLATES / lang / "skills" / "multica-test-automation"
        if not (automation / "SKILL.md").is_file():
            fail(f"missing multica-test-automation Skill: {automation}")


def main() -> int:
    validate_skill_frontmatter()
    validate_yaml_files()
    validate_python_syntax()
    validate_mixed_language_fragments()
    validate_agent_platform_separation()
    validate_gate_contracts()
    validate_t3_dependencies()
    print("repository validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
