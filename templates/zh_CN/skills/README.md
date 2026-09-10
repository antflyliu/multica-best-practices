# Skills 索引（zh_CN）

本目录收录可直接挂载到 Multica 的共享 Skill。每个子目录即一个 Skill，`SKILL.md` 是给 Agent 读的技能说明；带脚本的 Skill 另附 `README.md` 给人类视角的快速上手。

## 一、Skill Contract

所有 Skill 的 `SKILL.md` frontmatter 应统一包含：

```yaml
---
name:
description:
category: methodology | orchestration | platform | gate
owner:
version:
inputs:
outputs:
side_effects:
requires:
forbidden:
idempotent: true | false
platform_dependent: true | false
---
```

约束：`Agent` 负责角色职责，`Skill` 负责具体做法；Gate 状态只由 Leader 使用 `multica-verification` 产生。

## 二、平台层（Platform）

平台层允许包含团队自己的 URL / 凭据占位配置，但不得把真实凭据提交到仓库。

| Skill | 用途 |
|---|---|
| `multica-platform-confluence` | Confluence 发布 / 查询适配 |
| `multica-platform-jira` | JIRA Issue 读写与流转适配 |
| `multica-platform-jenkins` | Jenkins 构建、发布与晋级适配 |

## 三、编排层（Orchestration）

编排层负责 Artifact 落地与平台 Skill 之间的路由，不把具体平台实现塞进角色提示词。

| Skill | 用途 |
|---|---|
| `multica-artifact-req-sync` | PRD / 需求 Artifact 同步 |
| `multica-artifact-cicd-sync` | 代码评审结论到 CI/CD 的编排 |
| `multica-artifact-api-sync` | API 契约 Artifact 同步 |
| `multica-artifact-design-sync` | 技术设计 Artifact 同步 |
| `multica-artifact-test-sync` | 测试 Artifact 同步 |
| `multica-artifact-ui-sync` | UI Artifact 同步 |

## 四、方法论层（Methodology）

| Skill | 用途 |
|---|---|
| `multica-implementation` | 实现阶段方法论 |
| `multica-requirement-analysis` | 需求分析 |
| `multica-technical-design` | 技术设计 |
| `multica-test-design` | T1/T2 测试设计与覆盖分析 |
| `multica-test-automation` | G2.5 后的 T3 runtime automation |
| `multica-review-architect` | 架构专业评审 |
| `multica-review-backend` | 后端专业评审 |
| `multica-review-product` | 产品专业评审 |
| `multica-review-test` | 测试专业评审 |

## 五、门禁 / 设置层

| Skill | 用途 |
|---|---|
| `multica-verification` | Leader 独立 G1/G2/G3 门禁判定 |
| `multica-gate-setup` | CI / branch protection 门禁模板 |
| `multica-manage-skills` | Multica Skill 管理适配；属于平台管理能力，非核心研发方法论 |

## 六、挂载规则

1. 把需要的 Skill 目录整体拷到 Multica workspace 的 `skills/` 下。
2. 含脚本的 Skill 按其 `README.md` / `.env.example` 配置运行环境。
3. 平台 URL、token、账号等只存在于 `multica-platform-*` 或对应 adapter 配置，不写进 Agent Instructions。
4. 任何 Artifact 修改后，其下游 Gate 立即失效，必须重新验证。
5. `G2.5` 未 PASS 时不得触发 T3；没有 CI 时 T3 automation 应保持 `BLOCKED`，不能伪装成 PASS。

## 七、命名约定

- 统一 `multica-` 前缀 + 小写连字符。
- `SKILL.md` 的 `name` 必须与目录名一致。
- `category` 只能使用 `methodology` / `orchestration` / `platform` / `gate`。
