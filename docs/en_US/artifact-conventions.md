# Artifact Conventions

> Purpose: in multi-agent collaboration, downstream agents must be able to **find upstream artifacts via a stable reference**. This doc defines the "content spec" and the "sync skill" for each artifact — **where the artifact lands and how it is uploaded/retrieved is the skill's job, never written into the agent prompt**. So when a company changes platforms, only the skill changes; no agent is touched.

## 1. Core principle: content belongs to the role, platform belongs to the skill

- **Agent prompts only describe "what content to produce"** (e.g. which sections a PRD has, which fields an API contract has). **No specific platform name appears** (Figma / Confluence / Apifox / Jira, etc.).
- **Upload / retrieval is handled by the `multica-artifact-*-sync` skill family.** Each role writes only one line in its prompt: "use `multica-artifact-xxx-sync` to land it". The concrete platform is implemented inside that skill and is swappable.
- **Stable reference = link or path**: downstream locates upstream artifacts via the link/path returned by the skill, not via "you should know what upstream produced".

## 2. Artifact → content spec → sync skill (one-to-one)

| Artifact | Owner | Content spec (role side) | Sync skill (platform side, swappable) |
| --- | --- | --- | --- |
| UI design | @Designer | page structure, states, interaction, annotations (aligned to PRD IA) | `multica-artifact-ui-sync` (default Figma) |
| Product requirement PRD | @ProductManager | G-/FR-/BR-/AC-/KPI-/RISK-/OP- numbered requirements | `multica-artifact-req-sync` (default Confluence) |
| Technical design doc | @Architect | current arch, minimal change, affected components, steps, risks | `multica-artifact-design-sync` (default Git repo / Confluence) |
| API contract | @BackendDev | endpoints, in/out params, error codes, auth, BR- mapping | `multica-artifact-api-sync` (default Apifox) |
| Test cases / report | @Tester | feature/api cases, AC- coverage, test report | `multica-artifact-test-sync` (default local XMind → Jira) |

> Code artifacts live in the real code repo; the changed-file list is written into the corresponding stage artifact file for downstream/gate review.

## 3. Role-side template (uniform)

Each role's "WHAT I PRODUCE" section writes only:

```text
Produce <artifact>, land it via `multica-artifact-<xxx>-sync` skill to the team's agreed platform, and return a stable link to the Leader.
Content spec: see section 2 / the role instruction.
```

No platform name, no local path, no "upload to XXX".

## 4. Hard rules for downstream references

1. After upstream finishes, the skill returns a **stable link/path**; the Leader includes that reference explicitly when dispatching (e.g. "read `<PRD link>` then do X"), never by word of mouth.
2. Gate verdicts reference artifacts by "link + id" (e.g. "`<API contract link>` BR-3 missing error code"), not "that doc earlier".
3. The same artifact type always lands via the same skill — downstream locates by skill name + issue id, not by search.
4. When an artifact is modified, the reference stays, content updates; downstream gates must re-judge (see gates' "artifact change invalidates gate").

## 5. Relation to the numbering spec

- Artifact **content** uses `gates-and-evidence.md`'s "AI-readable discipline" (stable headings, stable table fields, G-/FR-/BR-/AC- ids).
- Artifact **location** is decided by the skill (link or path); both location and content must be stable for machine-localizable downstream consumption.

## 6. Platform swap (no agent change)

When a team changes platforms, only edit the "default platform" section of the corresponding `multica-artifact-*-sync` skill, swapping Figma / Confluence / Apifox / Jira for your tools (MasterGo / Yuque / Swagger / TestRail, etc.), keeping the "upload + return stable reference" interface. All role prompts and squad instructions **need no change**.

## 7. Common mistakes

Bad: "@Designer upload the design to Figma and send me the link." (platform name hard-coded into the prompt; breaks on platform change)

Better: "@Designer produce UI design, land it via `multica-artifact-ui-sync` skill and return the link." (platform lives in the skill; prompt stays copy-pasteable)
