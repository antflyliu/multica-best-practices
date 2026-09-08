---
name: multica-artifact-test-sync
description: Land test case / report artifacts to the case-management platform (default local XMind → Jira). Used by @Tester to upload cases and return a link for downstream acceptance consumption. Swappable platform.
---

# Artifact · Test Case Sync

## Purpose

Land test case / report artifacts to the team's unified case-management platform and let downstream (acceptance / Reviewer) retrieve them via a stable reference.

> This skill decouples "platform integration" from "role prompt": the role prompt only says "produce test cases", not which platform. Changing companies (TestRail / Zephyr / ZenTao / internal case lib) means editing only this skill, not the @Tester prompt.

## Default platform: local XMind → Jira

- Output: feature cases / API cases / test report (per `multica-test-design` skill).
- Upload: author cases locally in XMind, import to Jira via conversion script / tool (cases / defects linked to the Issue). Return the Jira **case-set link** and Issue association id.
- Retrieve: downstream @ProductManager / @Reviewer read via the Jira link — the link is the stable reference.

## Content spec (platform-independent part)

Cases must cover: happy path, boundaries, error state, empty state, no-permission state; mapped one-to-one to PRD's AC- acceptance criteria.

## Usage (role side writes only this line)

> @Tester: "Produce cases / report, land it via `multica-artifact-test-sync` skill to the team case platform, and return the link."

## Swap platform (no role-prompt change)

Replace this skill's "default platform" section with your tool (TestRail / Zephyr / ZenTao / internal case lib), keeping the "upload + return stable link" interface unchanged.

## Degradation when the platform is unavailable

1. Attempt the normal publish/sync operation once; when the case platform is confirmed unavailable, stop repeated writes.
2. Mark the sync step `BLOCKED` and record the platform, attempted operation, time/error, and the missing stable case-set link or reference ID.
3. If downstream only needs the case draft and the current gate does not require a stable platform reference, the Leader may explicitly accept the local cases as a **temporary reference**; never fabricate a Jira or other platform link.
4. If G2/G3 or test-report consumption requires a stable case reference, keep it `BLOCKED`. Platform unavailability cannot become a test pass, and a local result cannot masquerade as deployed-environment T3 evidence.
5. When the platform recovers, publish/sync and return the stable reference. If case/report content or its reference changes, all downstream gates are immediately invalid and must be rerun.

## Why it works

Case platforms differ by team; hard-coding the platform name into the role prompt freezes it. Sinking it into the skill keeps the role's "what to produce" description stable while the platform swaps with the skill.
