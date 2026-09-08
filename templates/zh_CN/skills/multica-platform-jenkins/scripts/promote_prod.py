#!/usr/bin/env python3
"""PROD promote — legacy profile helper (cross-platform)."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lib.config import load_config  # noqa: E402
from lib.jenkins_client import JenkinsError, parse_deploy_version  # noqa: E402
from lib import make_client  # noqa: E402


def promote_one(client, job_path: str, project: str, version: str) -> None:
    print(f"=== PROD: {project} deployVersion={version} ===")
    params = {
        "project": project,
        "deployVersion": version,
        "env": "pro",
        "branchName": "master",
        "deploy": "true",
        "sql": "false",
    }
    data = client.trigger_and_wait(job_path, params)
    print(json.dumps({"url": data.get("url"), "result": data.get("result")}, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote to PROD Jenkins job")
    parser.add_argument("--project", action="append", default=[])
    parser.add_argument("--version", action="append", default=[])
    parser.add_argument("--timeout-seconds", type=int)
    parser.add_argument("--poll-interval-seconds", type=int)
    args = parser.parse_args()

    skill_dir = SCRIPT_DIR.parent
    cfg = load_config(skill_dir)
    legacy_profiles = cfg.get("legacy_profiles") or {}
    prod = legacy_profiles.get("prod") or {}
    sit = legacy_profiles.get("sit") or {}
    job_path = prod.get("job_path", "")
    sit_job_path = sit.get("job_path", "")

    if not job_path or not sit_job_path:
        print(
            "ERROR: legacy_profiles.prod.job_path and legacy_profiles.sit.job_path must be configured",
            file=sys.stderr,
        )
        return 2

    client = make_client(skill_dir)
    if args.timeout_seconds:
        client.timeout = args.timeout_seconds
    if args.poll_interval_seconds:
        client.poll_interval = args.poll_interval_seconds

    if args.project:
        if len(args.project) != len(args.version):
            print("ERROR: each --project needs matching --version", file=sys.stderr)
            return 1
        for project, version in zip(args.project, args.version, strict=True):
            promote_one(client, job_path, project, version)
        return 0

    env_projects = os.environ.get("BUILD_PROD_PROJECTS", "").split()
    projects = env_projects if env_projects else list(prod.get("projects", []))
    if not projects:
        print("ERROR: no PROD projects configured; set BUILD_PROD_PROJECTS or legacy_profiles.prod.projects", file=sys.stderr)
        return 2

    for project in projects:
        build = client.last_success(sit_job_path, project)
        display = build.get("displayName", "")
        ver = parse_deploy_version(display)
        if not ver:
            print(f"ERROR: cannot parse version from {display!r}", file=sys.stderr)
            return 1
        promote_one(client, job_path, project, ver)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except JenkinsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1) from e
