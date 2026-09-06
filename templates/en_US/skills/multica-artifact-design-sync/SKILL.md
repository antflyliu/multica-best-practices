---
name: multica-artifact-design-sync
description: Land technical design artifacts to the code repo or knowledge platform (default Git repo / Confluence). Used by @Architect to upload technical design for downstream implementation and test consumption. Swappable platform.
---

# Artifact · Technical Design Sync

## Purpose

Land technical design docs to the team's unified technical-doc location and let downstream retrieve them via a stable reference.

> This skill decouples "platform integration" from "role prompt": the role prompt only says "produce technical design", not which platform. Changing companies means editing only this skill, not the @Architect prompt.

## Default platform: Git repo / Confluence (choose one per team convention)

- Output: technical design (current arch, proposed change, affected components, steps, verification plan, risks).
- Upload A (Git repo): place under the repo's agreed doc dir (e.g. `docs/design/<issue-id>.md`), reviewed together with the code PR — traceable.
- Upload B (Confluence): create / update a technical design page, return the link.
- Retrieve: downstream @FrontendDev / @BackendDev / @Tester read via the **file path or page link**.

## Content spec (platform-independent part)

Per `multica-technical-design` skill: current architecture, minimal viable change, affected components, implementation steps, verification plan, risks. Keep stable headings and ids.

## Usage (role side writes only this line)

> @Architect: "Produce technical design, land it via `multica-artifact-design-sync` skill to the team's agreed location (Git / KB), and return the reference."

## Swap platform (no role-prompt change)

Replace this skill's "default platform" section with your tool (internal Wiki / Notion / Feishu), keeping the "upload + return stable reference" interface unchanged.

## Degradation when the platform is unavailable

1. Attempt the normal publish/update operation once; when the platform is confirmed unavailable, stop repeated writes.
2. Mark the affected artifact or sync step `BLOCKED` and record the platform, attempted operation, time/error, and the missing stable URL/page ID/Issue reference.
3. If downstream only needs the design draft and the current gate does not require a stable platform reference, the Leader may explicitly accept `docs/design/<issue-id>.md` as a **temporary reference**; never present it as a published page.
4. If G1 or downstream requires a stable reference, keep it `BLOCKED`; never fabricate a URL, page ID, or use an old page as evidence for the current version.
5. When the platform recovers, publish/update and return the stable reference. If design content or its stable reference changes, all downstream gates are immediately invalid and must be rerun.

## Why it works

Design-doc locations vary by team (some in repo, some in Wiki). Sinking it into the skill keeps the role's "what to produce" description stable while the location swaps with the skill.
