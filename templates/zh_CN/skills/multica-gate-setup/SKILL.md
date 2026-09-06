---
name: multica-gate-setup
description: 将 CI 硬门禁模板接入目标仓库，并提供 CI 证据读取与门禁配置方法。
category: orchestration
owner: Leader
version: 1.0
inputs:
  - Target repository
  - CI workflow commands
  - Branch protection policy
outputs:
  - Installed CI gate configuration
  - Machine-verifiable G2.5 evidence path
side_effects:
  - Creates or updates CI workflow and branch protection configuration
requires:
  - Target repository CI capability
  - multica-verification for Leader-side gate decisions
forbidden:
  - Treating human-pasted CI claims as equivalent to machine evidence
  - Allowing T3 before G2.5 PASS
idempotent: true
platform_dependent: true
---

# Gate Setup（CI 门禁集成）

## 定位

把 CI 配置成 G2.5 的机器门禁，并让 Leader 能读取与当前 Artifact Version 对应的 CI 证据。本 Skill 负责安装与集成，不替代 `multica-verification` 的独立 Gate 判定。

## 携带模板

- `delivery-gate.yml`：CI workflow。
- `branch-protection.json`：分支保护模板。
- `apply-branch-protection.sh`：应用保护规则的脚本。

## 部署

1. 根据目标仓库真实命令修改 workflow 占位符。
2. 配置 branch protection / ruleset，使 `delivery-gate` 成为合入门禁。
3. 验证 workflow 能对目标分支产生机器可读结论。
4. 记录 CI 与 Artifact Version 的关联方式。

具体 GitHub API / Jenkins / 其他平台细节应留在对应 platform adapter；本 Skill 不要求某一种平台。

## G2.5 边界

正式状态机为：

```text
G2 PASS
  ↓
G2.5 CI/CD
  ↓
G2.5 PASS
  ↓
T3
  ↓
G3
```

- CI 缺失或 CI 结论无法读取 → `G2.5 = BLOCKED`，不得伪装成 PASS。
- 可以做人工验证，但人工验证不能冒充 G2.5 machine evidence。
- **T3 automation 只有在 G2.5 PASS 后才能触发。**

## 与 multica-verification 的关系

- `multica-gate-setup`：安装 CI 硬门禁、提供机器证据。
- `multica-verification`：由 Leader 独立执行 Gate 判定。
- Reviewer：专业质量评审，不拥有 Gate 权。

任何 Artifact 修改都会使其下游 Gate 失效，必须重新验证。
