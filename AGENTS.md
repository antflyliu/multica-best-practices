# AGENTS.md

This repository is a practical **Copy. Paste. Run.** library of Agent · Squad · Skill · Issue templates for [Multica](https://github.com/multica-ai/multica). Every template can be copied and used as-is. Chinese is the source language of the content; this file is the agent entry point and is intentionally always in English (see the i18n convention below).

## Project structure

```text
README.md            Project entry: quick start / principles / structure (bilingual switcher)
AGENTS.md            Agent entry: project conventions and change rules (always English)
templates/           Everything copy-paste-ready (split by language)
├── zh_CN/           Chinese templates (default)
│   ├── agents/      Shared Agent Instructions (6 role definitions)
│   ├── skills/      Shared Skills (6, unified multica- prefix)
│   │   └── multica-gate-setup/  CI hard-gate templates ship inside this Skill
│   └── squad/       Squad starters (copy the whole subdirectory and run)
│       ├── software-development/  Regular development (recommended)
│       └── bug-fix/               Minimal fix combination
└── en_US/           English templates (same structure as zh_CN/)
docs/                Methodology (split by language: zh_CN/ + en_US/)
SECURITY.md          Security check before sharing templates
```

## Core conventions

- **Skill naming**: `multica-` prefix + lowercase hyphenated; the `name` field in `SKILL.md` matches the directory name.
- **Skills mount by name**: documents reference `multica-xxx` (in backticks), never a repo path.
- **Agent naming**: `role + name` (e.g. `BackendDev-user-service`).
- **Directory semantics**: inside each language tree, `agents/` = roles, `skills/` = practices, `squad/` = squad combinations, and `docs/` = methodology. CI hard-gate templates live in the `multica-gate-setup` skill; there is no standalone `gates/` directory.

## i18n convention (how Chinese and English coexist)

- **Source language is Chinese**: the Chinese tree is the source of truth.
- **Language directories**: `templates/` and `docs/` each contain a `zh_CN/` and an `en_US/` directory with the same file names (e.g. `docs/zh_CN/where-to-put-things.md` ↔ `docs/en_US/where-to-put-things.md`).
- **Root docs are single-file bilingual**: `README.md` / `README.en.md` each carry a switcher at the top; `CHANGELOG.md`, `ROADMAP.md`, `SECURITY.md`, `CONTRIBUTING.md` are single files written Chinese-first with English alongside.
- **One exception**: `AGENTS.md` is a single file, always English (the working language for agents). It has no Chinese mirror — agents read English directly.
- **Links are language-aware**: inside an English file, relative links point into `en_US/` trees; the Chinese tree is never moved or rewritten for translation purposes.
- **No build tooling**: this is a plain Markdown repo — do not add a docs generator or symlinks.
- **Machine files are not translated**: `LICENSE`, `*.yml`, `*.json`, `*.sh` (CI gate files are copied into both `zh_CN/` and `en_US/` skill directories).
- **Keep both in sync**: content changes to a Chinese file must be mirrored to its English counterpart in the same change (or explicitly tracked as pending in `CHANGELOG.md`).

## Change conventions

- **Repo-wide sync**: once a path, name, or structure diagram changes, sync README / Starter README / docs / ROADMAP, and grep the repo for stale names to confirm no residue (historical CHANGELOG entries excluded).
- **Record CHANGELOG**: every user-visible change appends an entry to `CHANGELOG.md` (version + date + Added / Changed / Removed).
- **Keep starters copy-paste-ready**: `templates/zh_CN/squad/software-development` is the MVP; changes must not break "copy → paste → run".
- **New templates come with explanation**: provide "why it works" and "common failure modes"; templates not yet proven on real tasks go to `ROADMAP.md` first.
- **Template style**: prefer directly copyable Markdown code blocks; agent templates state responsibilities / prohibitions / delivery format.

## Don't

- Commit secrets or sensitive information (tokens, API keys, private keys, local absolute paths, real workspace slugs / emails). Use placeholders (`YOUR_API_KEY`, `<workspace-slug>`).
- Claim there is a single "correct" number of agents — pick the smallest viable combination for the task.
- Replace the official Multica documentation — link to it instead.
- Introduce large binaries without good reason.
- Let completers approve their own work — gatekeeping is done by a non-producer (the Leader reruns `multica-verification` or relies on the CI verdict).

## How to work

1. `read_file` before editing.
2. Make minimal edits (`replace_in_file`); never rewrite whole files.
3. Confirm before destructive operations (delete, move, external publish).
4. After changes, grep for stale names/paths, run `read_lints`, and get zero errors.
