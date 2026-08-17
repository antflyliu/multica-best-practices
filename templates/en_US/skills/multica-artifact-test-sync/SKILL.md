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

## Why it works

Case platforms differ by team; hard-coding the platform name into the role prompt freezes it. Sinking it into the skill keeps the role's "what to produce" description stable while the platform swaps with the skill.
