# Collaboration Artifact Conventions

> Purpose: in multi-Agent collaboration, downstream agents must locate upstream artifacts by a **stable path**. This doc defines the fixed directory, filenames, and reference style for each stage's artifact. Every "produce" in Squad and Agent instructions must land at the path defined here, or downstream can't read it.

## 1. Artifact root

One root, isolated per Issue:

```text
artifacts/<issue-id>/
```

- `<issue-id>` = the Issue number (e.g. `ISSUE-123`, `task-2026-0817-a1`). With no Issue number, use the `<issue-slug>` the Leader sets at startup (placeholder, never hardcoded).
- All artifact references are **relative paths** — in the artifact file, in @mentions to downstream, and in gate verdicts. **Never absolute paths** (avoids leaking the local workspace and stays portable across machines).
- If your project already has a `docs/` or `deliverables/` convention, map `artifacts/<issue-id>/` onto that directory; filenames and reference rules stay the same.

## 2. Stage artifact → file path (maps 1:1 to the squad.md stage-gate map)

| Stage | Artifact | Owner | Fixed path |
| --- | --- | --- | --- |
| S0 | Product PRD | @ProductManager | `artifacts/<issue-id>/prd.md` |
| S1a | Technical design | @Architect | `artifacts/<issue-id>/design-tech.md` |
| S1b | UI design notes (Figma link + annotations) | @Designer | `artifacts/<issue-id>/design-ui.md` |
| S2a | API contract | @BackendDev | `artifacts/<issue-id>/api-contract.md` |
| S2b | Feature cases | @Tester | `artifacts/<issue-id>/cases-feature.md` |
| S3a | Frontend implementation | @FrontendDev | code repo (path in `change-file list`, not here) |
| S3b | Backend implementation | @BackendDev | code repo (path in `change-file list`, not here) |
| S3c | API cases | @Tester | `artifacts/<issue-id>/cases-api.md` |
| S4 | Test report | @Tester | `artifacts/<issue-id>/test-report.md` |
| G* | Gate verdict | @Leader | Issue comment / `artifacts/<issue-id>/gate-<g>.md` |
| Acceptance | Acceptance checklist | @ProductManager / @Reviewer | `artifacts/<issue-id>/acceptance.md` |

> Implementation artifacts (code) live in the real repo, not `artifacts/`; but the **change-file list must be written into the stage's artifact file** so downstream and the gate can verify.

## 3. Hard rules for downstream references

1. After upstream finishes, the path is **passed explicitly to downstream**: when the Leader dispatches, write "read `artifacts/<issue-id>/prd.md` then do X" — don't rely on "you should know what upstream produced".
2. Inside artifact files, cross-link with **relative paths** (e.g. `design-ui.md` links `../prd.md`); don't rely on verbal conventions.
3. Gate verdicts reference artifacts by relative path + number (e.g. "BR-3 in `api-contract.md` lacks error codes"), not "that doc earlier".
4. Filenames are **fixed**: the same stage artifact is always `prd.md` / `api-contract.md`, never renamed per task — downstream locates by filename, not by searching.
5. When an artifact is edited, the path stays, content updates; downstream gates re-judge accordingly (see "artifact change invalidates gate" in gates).

## 4. Relation to numbering conventions

- Artifact content follows the "AI-readable discipline" in `gates-and-evidence.md` (stable headings, stable table columns, G-/FR-/BR-/AC- numbering).
- Artifact **location** follows the "fixed filenames" here — location and content must both be stable for machine-like downstream locating.

## 5. Common mistakes

Bad: "@Architect produce a design, @FrontendDev you follow it." (Where does FrontendDev find the design?)

Better: "@Architect write the technical design to `artifacts/<issue-id>/design-tech.md`; after I gate G1 PASS, I'll dispatch @FrontendDev to read that file and implement."
