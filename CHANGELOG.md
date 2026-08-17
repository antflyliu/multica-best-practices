# Changelog / 更新日志

All notable changes to this project will be documented in this file.
本文件记录本项目的所有重要变更。新条目采用中英结合写法（Chinese-first, English alongside）。

## v0.0.7 - 2026-08-17 · Artifact platform decoupled into skills / 产物平台对接下沉到 skill

### Added / 新增

- 新增 5 个产物对接 skill（中英，每个默认平台可替换）：`multica-artifact-req-sync`（PRD→Confluence）、`multica-artifact-ui-sync`（UI→Figma）、`multica-artifact-design-sync`（技术设计→Git/Confluence）、`multica-artifact-api-sync`（API 契约→Apifox）、`multica-artifact-test-sync`（用例→本地 XMind 转 Jira）/ Added 5 artifact-sync skills (zh/en, swappable default platform each)
- 新增 `artifact-conventions.md`（中英）重写为「产物内容规范 + 对接 skill」：内容归角色、平台归 skill，角色提示词不写平台名；换公司只换 skill / Rewrote `artifact-conventions.md` (zh/en) into "content spec + sync skill": content belongs to role, platform to skill; no platform name in prompts
- `README.md` / `README.en.md` Skill 表加 5 个 `multica-artifact-*-sync` 条目，计数 6→11 / README skill tables add the 5 artifact-sync skills, count 6→11

### Changed / 变更

- 全部 8 个角色指令（中英）：「我产出什么 / WHAT I PRODUCE/OWN/DELIVER」改为"用 `multica-artifact-*-sync` skill 落地并回传稳定链接"，去掉写死的 `artifacts/<issue-id>/xxx.md` 与本地产平台名（如 Designer 的 Figma）/ All 8 agent instructions (zh/en): outputs now "land via multica-artifact-*-sync and return a stable link", dropping hard-coded local paths and platform names
- `templates/zh_CN|en_US/squad/software-development/squad.md`：阶段表与产物流水线改为"角色经 skill 回传链接"，【产物落盘】段改为【产物落盘与取回】，不再写死本地路径 / Squad stage map & pipeline now say "role returns link via skill"; 【ARTIFACT LANDING】 becomes landing+retrieval, no hard-coded local paths

## v0.0.6 - 2026-08-17 · Artifact landing conventions / 协作产物落盘约定

### Added / 新增

- 新增 `artifact-conventions.md`（中英）：规定所有阶段产物统一落 `artifacts/<issue-id>/`，文件名固定（PRD=`prd.md`、技术设计=`design-tech.md`、UI 设计=`design-ui.md`、API 契约=`api-contract.md`、功能用例=`cases-feature.md`、接口用例=`cases-api.md`、测试报告=`test-report.md`、验收=`acceptance.md`）；下游用相对路径定位，绝不写绝对路径 / 不泄露 workspace / 不靠搜索 / 引用必须显式传路径 / 冲突以哪份为准 / 产物变更路径不变内容更新 / 门禁据此重判 / 文档表与常见错误同步 / Added `artifact-conventions.md` (zh/en): all stage artifacts land under `artifacts/<issue-id>/` with fixed filenames; downstream locates by relative path
- `where-to-put-things.md`（中英）加一行：协作产物放哪 → `artifacts/<issue-id>/`（见 artifact-conventions）/ where-to-put-things gains an artifact-landing row
- `README.md` / `README.en.md` 文档表加 `artifact-conventions` 条目 / README doc tables add the artifact-conventions entry

### Changed / 变更

- `templates/zh_CN|en_US/squad/software-development/squad.md`：阶段表与产物流水线每个产物标注落盘路径；新增【产物落盘】段，要求 Leader 派活时显式给出产物路径 / Squad stage map & artifact pipeline now annotate each artifact's landing path; added 【ARTIFACT LANDING】 rule requiring explicit path in dispatch
- 全部 8 个角色指令（中英）的「我产出什么 / WHAT I PRODUCE/OWN/DELIVER」补落盘路径与"读取上游 `artifacts/<issue-id>/...`"的硬指示，下游据此定位上游产物 / Every agent instruction (zh/en) now states its artifact landing path and reads upstream via `artifacts/<issue-id>/...`

## v0.0.5 - 2026-08-17 · Add ProductManager role + AI-readable requirement discipline / 新增产品经理角色与需求 AI 可读纪律

### Added / 新增

- 新增 `ProductManager` 角色指令（`templates/zh_CN|en_US/agents/product-manager.md`）：把想法 / 诉求 / 会议结论整理成可评审、可设计、可开发、可测试的 PRD（含 G-/FR-/BR-/AC-/KPI-/RISK-/OP- 编号、六类读者对准、需求类型→产物形态、AI 可读纪律、协作偏好）/ New `ProductManager` agent instructions: turns ideas / asks / meeting notes into reviewable PRDs
- 角色词表加入 `ProductManager`，`naming-conventions.md`（中英）第 2 条同步 / Role vocabulary now includes `ProductManager` in `naming-conventions.md` (zh/en)
- 软件开发展望 Starter 接入 PM：团队段加 @ProductManager，阶段表加 S0 需求产出 @ProductManager → G0 范围确定（基于 PRD），产物流水线加第 0 步；无 PM 时 Issue 直接视为就绪范围、跳过 S0 / software-development Squad wires in PM: S0 requirement @ProductManager → G0 scope; without PM, Issue is the ready scope
- `gates-and-evidence.md`（中英）新增「需求 / 设计类产物的 AI 可读纪律」：稳定标题、稳定表格字段、规则编号、待确认集中（OP- 未关闭不进开发）、文档互链、冲突指明准绳、禁用模糊词、规则文字化；违反任一条 G0/G1 判 REJECTED / Added "AI-readable discipline for requirement / design artifacts" to `gates-and-evidence.md` (zh/en)
- Starter 角色计数 7 → 8（`templates/zh_CN|en_US/squad/software-development/README.md`）/ Starter role count 7 → 8

### Changed / 变更

- @Designer / @Architect（中英）的「产品需求」来源改为以 @ProductManager 的 PRD 为主（无 PM 退化到 Issue / @Architect 说明），并明确产品范围 / 业务规则 / 字段口径归 PM、无 PM 归 Leader 收敛 / Designer & Architect now take PRD from @ProductManager as the primary source; product scope / business rules / field definitions belong to PM (or Leader without PM)

## v0.0.4 - 2026-08-17 · Three-segment naming (role + project + member-id) / 命名升级为三段式

### Changed / 变更

- 命名规范从「角色 + 实例」升级为「角色 + 项目 + 成员标识」`<角色>-<项目>-<成员标识>`，解决「真实姓名 vs 角色名」冲突：同项目同角色多人时靠成员标识（工号/花名，不用真实姓名全称）唯一区分 / Upgraded naming from `role + instance` to `role + project + member-id` `<role>-<project>-<member-id>` to resolve the "real name vs role name" collision: same project + same role + multiple people are disambiguated by the member-id (employee number / nickname, never a full real name)
- 角色前缀通配解析同步扩为三段：`@角色` → 指挥按 `@角色-<本小队 suffix>-<本小队 member>` 精确 @mention（suffix 对应 `<项目>` 段，member 对应 `<成员标识>` 段）/ Role-prefix wildcard resolution extended to three segments: `@role` → orchestrator dispatches `@role-<squad suffix>-<squad member>`
- 同步更新 `docs/zh_CN|en_US/naming-conventions.md`、`templates/zh_CN|en_US/squad/{software-development,bug-fix}/squad.md` 与 `templates/zh_CN|en_US/agents/leader.md` 的前缀解析段/精确派活描述，以及 README（中英文）、AGENTS.md、adapt-and-scale.md（中英文）、各 squad README 的命名标题引用 / Synced all references in README (zh/en), AGENTS.md, adapt-and-scale.md (zh/en), and each squad README

### Removed / 移除

- 未采纳「私有小队 Profile」机制（用户判定过于复杂，不引入）/ Did not adopt the "private squad Profile" mechanism (deemed too complex by the user)

## v0.0.3 - 2026-08-17 · Squad instructions re-leveled to Squad scope / Squad 指令重构为 Squad 级

### Changed / 变更

- Squad 指令（`templates/zh_CN/squad/software-development/squad.md` 与 `templates/en_US/...`，以及 `templates/zh_CN/squad/bug-fix/squad.md` 与 `templates/en_US/...`）改为真正的「Squad 级」：开场定义 Squad 目标 / 事实来源与待确认项 / 编号规范（G-/U-/FR-/BR-/AC-/KPI-/OP-/RISK-，software-development）/ 沟通风格 / 禁止事项（software-development），对所有角色成立；原「你是 Leader」内容下移为独立的 `【Leader 角色】` 段，明确 Leader 仅编排、推进权与判门权在 Leader。借鉴了通用写法但去掉了任何具体项目、工具链与智能体人名的绑定，保持可复制 / Re-leveled the Squad instructions to true squad scope (both `software-development` and `bug-fix`, in zh_CN and en_US): the opening now defines the Squad goal, fact-source & TBD policy, numbering convention (software-development), communication style, and prohibited list (software-development), valid for every role; the former "you are the Leader" content moved into a standalone `【Leader Role】` section stating the Leader only orchestrates and holds advancing/gating authority. Borrowed generic patterns but dropped any binding to specific projects, toolchains, or agent names to stay copy-paste-ready

### Added（追加 · 门禁纪律增强 / Gate discipline enhancements）

- 在 Squad 级规则中补充三条判门纪律（中英文 squad.md 均落地）：(1) 范围内某产物判定为「不适用（N/A）」必须显式标注 + 理由 + Leader 确认，禁止静默跳过；(2) 任一产物被修改后下游门禁立即失效必须重判，不得沿用旧 PASS（不仅实现变更，设计 / API 契约 / 用例变更同样失效）；(3) 同一产物判门连续 3 次 FAIL 强制升级人类，而非无限返工 / Added three gate disciplines to the Squad-level rules (both zh_CN and en_US squad.md): (1) an in-scope artifact judged N/A must be marked explicitly with reason + Leader confirmation — never silently skipped; (2) once any artifact is modified its downstream gates are invalidated and must be re-judged, never carry over an old PASS (not just implementation — design / API contract / case changes also invalidate downstream); (3) the same artifact failing the gate 3 times in a row escalates to Human instead of endless rework
- 同步 `docs/zh_CN` 与 `docs/en_US` 的 `gates-and-evidence.md`（扩展门禁失效原则，覆盖上游产物修改与 N/A 不静默跳过）和 `common-mistakes.md`（新增第 9 条「静默把范围内产物当 N/A 跳过」错误示范，并扩展诊断清单）/ Synced `gates-and-evidence.md` (extended gate-invalidation principle to upstream changes and non-silent N/A) and `common-mistakes.md` (new pitfall #9 on silently skipping in-scope artifacts as N/A, plus expanded diagnostic checklist) in both `docs/zh_CN` and `docs/en_US`

### Added（追加 · 借鉴邻方案的四项增强 / Borrowed enhancements）

- **角色前缀通配解析**（解决「workspace 内多个同角色实例如何锁定本小队」）：新增 `docs/zh_CN|en_US/naming-conventions.md` 的「小队实例后缀与前缀通配」规则——Squad 指令只写角色前缀（@FrontendDev 等），小队启动时声明实例后缀 suffix，指挥按 `@角色-<本小队 suffix>` 精确 @mention；并在两个 `squad.md`（中英文）+ `agents/leader.md`（中英文）补「角色前缀解析」段与精确派活规则 / **Role-prefix wildcard resolution** (solves "how to pin this squad's agent among multiple same-role instances in a workspace"): added "Squad instance suffix & prefix wildcard" to `docs/zh_CN|en_US/naming-conventions.md` — Squad instructions write only the role prefix, the squad declares a suffix at startup, and the orchestrator dispatches `@role-<squad suffix>`; also added a "role prefix resolution" section and precise-dispatch rule to both `squad.md` (zh_CN/en_US) and `agents/leader.md` (zh_CN/en_US)
- **门禁结论四值与汇合门禁 + 判门不改产物**（落到 `docs/zh_CN|en_US/gates-and-evidence.md`）：新增 APPROVED / APPROVED_NA / REJECTED / BLOCKED 四值（APPROVED_NA 区别于普通 PASS 的下游差异由 Leader 写明）；明确汇合门禁「并行分支须全 PASS 才开放下游」；判门者只给结论与修改清单、不代替作者改产物 / **Four verdict values, join gates, gatekeeper-doesn't-edit** added to `docs/zh_CN|en_US/gates-and-evidence.md`: APPROVED / APPROVED_NA / REJECTED / BLOCKED (APPROVED_NA's different downstream is stated by the Leader); join gates require every parallel branch PASS; the gatekeeper only gives a verdict + fix list and never edits the artifact
- **阶段-门禁对照表**（落到 `templates/zh_CN|en_US/squad/software-development/squad.md` 顶部）：以 `@角色` 占位、不写死人数/人名的 S0–G4 流水线一览，缺层即跳过对应行 / **Stage-gate map** added atop `templates/zh_CN|en_US/squad/software-development/squad.md`: a S0–G4 pipeline overview using `@role` placeholders (no hardcoded counts/names), skipping the line for any missing layer
- **需求追踪矩阵**（落到 `templates/zh_CN|en_US/squad/software-development/issue.md`）：建议 REQ → DESIGN → API → CODE → CASE → TEST 映射，保证验收标准无断链 / **Requirements traceability matrix** added to `templates/zh_CN|en_US/squad/software-development/issue.md`: suggested REQ → DESIGN → API → CODE → CASE → TEST mapping to prevent broken links
- **判门不改产物**同步进 squad.md 推进规则与 bug-fix 规则（中英文）及 leader.md 第 9 条 / **Gatekeeper-doesn't-edit** also synced into the advance rules of both squad.md (zh_CN/en_US, software-development + bug-fix) and leader.md rule #9 (zh_CN/en_US)

### Added（追加 · 新增 Designer 角色 / New Designer role）

- 新增 `Designer` 角色，专做 UI / 交互设计、对接 Figma 出视觉与标注，与 `Architect`（技术架构设计）明确分离；新建 `templates/zh_CN|en_US/agents/designer.md` / Added a **Designer** role for UI / interaction design working with Figma, separated from `Architect` (technical design); new `templates/zh_CN|en_US/agents/designer.md`
- `docs/zh_CN|en_US/naming-conventions.md` 角色词表加入 `Designer`，并注明 Architect ≠ Designer / `docs/zh_CN|en_US/naming-conventions.md` role vocabulary now includes `Designer`, noting Architect ≠ Designer
- 两个 `squad.md`（中英文）的【团队】段加入 `@Designer`；software-development 的阶段-门禁对照表拆分为 S1a 技术设计(@Architect) / S1b UI 设计(@Designer) 双线，并明确 @FrontendDev 同时依赖二者；bug-fix 团队段也加入 @Designer（UI bug 场景）/ Both `squad.md` (zh_CN/en_US) gained `@Designer` in the team section; software-development's stage-gate map splits into S1a technical design (@Architect) / S1b UI design (@Designer) with @FrontendDev depending on both; bug-fix team section also lists @Designer
- `frontend-developer.md`（中英文）明确 UI 来源为 @Designer 的 Figma 产出，缺位时回退设计文档或 mock / `frontend-developer.md` (zh_CN/en_US) now names @Designer's Figma output as the UI source, falling back to a design doc or mock when absent
- 同步角色计数：README / README.en / ROADMAP / AGENTS.md / software-development README 由 6 角色更新为 7 或 5→6 Agent / Synced role counts in README / README.en / ROADMAP / AGENTS.md / software-development README (6→7 roles, or 5→6 agents)

## v0.0.2 - 2026-08-16 · Template correctness fixes / 模板正确性修复

### Changed / 变更

- 修复 CI 门禁模板：结构化结论现在会输出实际 PASS / FAIL；分支保护脚本不再生成残缺请求体 / Fixed the CI gate templates so the structured verdict emits the actual PASS / FAIL value and the branch-protection script no longer produces a truncated request body
- 修复 Squad 路由：Bug Fix 会派发 Tester；软件开发中的接口测试用例与实现并行推进 / Fixed Squad routing so Bug Fix dispatches the Tester and API test cases advance in parallel with implementation
- 同步路线图中的 Skill 数量，并说明团队级审批应使用 CODEOWNERS 或 GitHub Rulesets / Synchronized the Skill count in the roadmap and clarified that team-level approval requires CODEOWNERS or GitHub Rulesets
- 调整项目定位表述，使真实任务验证状态与 ROADMAP 保持一致 / Aligned the project-positioning language with the real-task validation status in the ROADMAP

## v0.0.1 - 2026-08-15 · Initial release / 初始版本

历史演进（0.1.0–0.14.0）已压缩合并为本版本：一套可直接复制运行的 Multica 模板库。
Historical iterations (0.1.0–0.14.0) are condensed into this release: a copy-paste-ready Multica template library.

### Added / 新增

- **Agent 模板 / Agent templates**：6 个共享角色（Leader / Architect / FrontendDev / BackendDev / Tester / Reviewer），位于 `templates/zh_CN/agents/` 与 `templates/en_US/agents/`
- **Skill 模板 / Skill templates**：6 个共享 Skill（`multica-verification` 判门 / `multica-gate-setup` CI 硬门禁 / `multica-test-design` / `multica-requirement-analysis` / `multica-technical-design` / `multica-implementation`），统一 `multica-` 前缀，按名称挂载
- **Squad Starter / Squad starters**：`software-development`（推荐）与 `bug-fix`（实验性），各含 README / squad / issue 三件套
- **方法论 / Methodology**：`docs/` 5 篇（指令归属 / 门禁与证据 / 常见错误 / 裁剪扩展 / 命名规范）
- **CI 硬门禁 / CI hard gates**：`delivery-gate.yml` / `branch-protection.json` / `apply-branch-protection.sh` 随 `multica-gate-setup` skill 自包含
- **国际化 / i18n**：`README.md` ↔ `README.en.md` 顶部互挂切换链接；`templates/` 与 `docs/` 按 `zh_CN/` / `en_US/` 双目录存放；根文档（AGENTS / CHANGELOG / ROADMAP / SECURITY / CONTRIBUTING）单文件化并采用中英结合写法

### Changed / 变更

- 无（本版本为压缩合并后的初始版本）。No changes — this is the initial condensed release.
