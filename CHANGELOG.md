# Changelog / 更新日志

All notable changes to this project will be documented in this file.
本文件记录本项目的所有重要变更。新条目采用中英结合写法（Chinese-first, English alongside）。

## v0.0.1 - 2026-08-15 · Initial release / 初始版本

历史演进（0.1.0–0.14.0）已压缩合并为本版本：一套可直接复制运行的 Multica 模板库。
Historical iterations (0.1.0–0.14.0) are condensed into this release: a copy-paste-ready Multica template library.

### Added / 新增

- **Agent 模板 / Agent templates**：6 个共享角色（Leader / Architect / FrontendDev / BackendDev / Tester / Reviewer），位于 `templates/chinese/agents/` 与 `templates/english/agents/`
- **Skill 模板 / Skill templates**：6 个共享 Skill（`multica-verification` 判门 / `multica-gate-setup` CI 硬门禁 / `multica-test-design` / `multica-requirement-analysis` / `multica-technical-design` / `multica-implementation`），统一 `multica-` 前缀，按名称挂载
- **Squad Starter / Squad starters**：`software-development`（推荐）与 `bug-fix`（实验性），各含 README / squad / issue 三件套
- **方法论 / Methodology**：`docs/` 5 篇（指令归属 / 门禁与证据 / 常见错误 / 裁剪扩展 / 命名规范）
- **CI 硬门禁 / CI hard gates**：`delivery-gate.yml` / `branch-protection.json` / `apply-branch-protection.sh` 随 `multica-gate-setup` skill 自包含
- **国际化 / i18n**：`README.md` ↔ `README.en.md` 顶部互挂切换链接；`templates/` 与 `docs/` 按 `chinese/` / `english/` 双目录存放；根文档（AGENTS / CHANGELOG / ROADMAP / SECURITY / CONTRIBUTING）单文件化并采用中英结合写法

### Changed / 变更

- 无（本版本为压缩合并后的初始版本）。No changes — this is the initial condensed release.
