# Changelog / 更新日志

All notable changes to this project will be documented in this file.
本文件记录本项目的所有重要变更。新条目采用中英结合写法（Chinese-first, English alongside）。

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
