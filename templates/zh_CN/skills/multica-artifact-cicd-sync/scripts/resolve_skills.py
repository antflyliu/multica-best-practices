"""Resolve platform skill directories for orchestrator scripts."""
from __future__ import annotations

import os
from pathlib import Path


def resolve_skill_dir(skill_name: str, caller_skill_dir: Path | None = None) -> Path:
    root = os.environ.get("MULTICA_SKILLS_ROOT")
    if root:
        candidate = Path(root) / skill_name
        if candidate.is_dir():
            return candidate

    if caller_skill_dir is not None:
        sibling = caller_skill_dir.parent / skill_name
        if sibling.is_dir():
            return sibling

    raise FileNotFoundError(
        f"Cannot locate skill '{skill_name}'. Set MULTICA_SKILLS_ROOT or co-locate under templates/skills/."
    )
