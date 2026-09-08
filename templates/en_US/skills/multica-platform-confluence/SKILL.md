---
name: multica-platform-confluence
description: Confluence platform adapter for reading and publishing knowledge-base artifacts and returning stable page references.
category: platform
owner: Platform Adapter
version: 1.0
inputs:
  - Artifact content or page reference
  - Team platform configuration
outputs:
  - Stable page reference
  - Retrieved page content
side_effects:
  - Reads, creates, or updates Confluence pages
requires:
  - Runtime platform credentials/configuration
forbidden:
  - Printing credentials
  - Putting platform credentials into Agent Instructions
  - Making Gate decisions
idempotent: true
platform_dependent: true
---

# Platform · Confluence (placeholder shell)

> This is a **platform-layer placeholder shell**. The public multica-best-practices binds to no specific company's internal URLs or credentials.
> To onboard your own Wiki, only edit this skill's `config.yaml` and `scripts/`; all upstream roles and orchestration skills stay untouched.

## Purpose

Provide **read + write** capability for "knowledge-base / Wiki" class platforms:

- **Read**: fetch an existing page by pageId / title as Markdown for downstream Agents.
- **Write**: land PRD / technical design artifacts to the team Wiki and return a **stable page link**.

Decoupled from `multica-platform-jira` (Issue system); this skill only handles Wiki, not Issue field writes. Role prompts never contain Wiki URLs / pageIds; swap platforms by swapping only this skill.

## Default landing (team-configured)

| Artifact type | Wiki parent page (config.yaml) | Local draft (Agent writes first) |
| --- | --- | --- |
| PRD | `config.yaml` → `wiki.default_parent_page_id` | structured by `multica-requirement-analysis`, landed by req-sync |
| Technical design | `config.yaml` → `wiki.design_parent_page_id` | `docs/design/<ISSUE-KEY>/design.md` |

## Files (suggested structure)

```text
multica-platform-confluence/
├── SKILL.md
├── config.yaml
├── .env.example
└── scripts/
    ├── credentials.sh
    ├── wiki.sh            # Read/Write CLI
    ├── fetch_page.py      # Wiki → local Markdown
    ├── publish_design.py  # Markdown design upsert
    └── lib/
```

## Read (downstream / Leader pulls upstream artifact)

```bash
bash scripts/wiki.sh fetch-page <page_id> [output_dir] [issue_key]
bash scripts/wiki.sh get-page <page_id>
bash scripts/wiki.sh find-page "<title>" [space_key]
```

## Write (artifact landing)

### PRD page

```bash
bash scripts/wiki.sh create-page "<title>" "<parent_page_id>" "<html_or_md>" "<space_key>"
```

Called by `multica-artifact-req-sync`.

### Technical design (Markdown → Wiki)

1. @Architect writes local via `multica-technical-design`: `docs/design/<ISSUE-KEY>/design.md`.
2. Publish under the design parent page:

```bash
python scripts/publish_design.py <ISSUE-KEY> docs/design/<ISSUE-KEY>/design.md \
  [--space SPACE] [--parent PAGE_ID] [--title "Title"] [--json]
```

3. Return `url` / `page_id` from the JSON; `multica-artifact-design-sync` then calls the Issue-platform skill to write the link back to the Issue.

**Upsert rule**: same space + same title → update version; title may get an `[AI]` suffix (team-configurable).

## Success criteria

- Read operations return the requested page content or metadata in a form downstream skills can consume.
- Create/update operations return a stable page URL and/or page identifier.
- A published page can be fetched again and verified to contain the intended artifact content.
- Upsert operations update the intended page/version without silently creating an unrelated page.
- On failure, the script exits non-zero with diagnosable error output; never fabricate a page URL or page ID.

## Agent Compatibility

- Credentials injected via runtime env vars (`.env.example` gives the variable-name template); never print passwords, never write into role prompts.
- Confirm before external writes: space, parent pageId, title.
- Prefer `scripts/`; do not call REST directly.

## Adapting To A New Team

1. Edit `config.yaml`: `wiki.url`, `default_space`, `*_parent_page_id`.
2. Change the design-doc parent page ID to the team Wiki directory page.
3. Maintain space / directory lists in `spaces.json` (if applicable).

## Why it works

Wiki auth, spaces, and parent pages differ per team; isolating them in a platform skill means Issue-system / notification / Git-change scripts don't affect Wiki scripts, and PRD + design share one read/write capability. A swappable platform layer is the core of "copy-paste-run": role prompts only ever say `multica-artifact-*-sync`, and the real internal details stay in this layer.
