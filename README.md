# Multica Best Practices

[English](./README.en.md) | 中文

> 面向 [Multica](https://github.com/multica-ai/multica) 的 Agent · Squad · Skill · Issue 实战模板。
> **Copy. Paste. Run.**

Multica 很强大，但第一次上手可能意外地难：

- Instructions 里该写什么？
- 这条规则放 Agent Instructions 还是 Squad Instructions？
- Leader 该干什么？成员之间怎么交接？
- Issue 里该有什么？
- 怎么防止 Agent 跳过步骤？
- 检查和测试怎么分工？

本仓库给出可直接复用、并持续通过真实任务验证的实践答案。

## 这是什么

一句话：**一套面向真实任务持续迭代的 Multica 小队配置**——每个 Agent 只负责一件事，Leader 负责编排与判门，每步产出都要证据。

```text
你创建：Agent（角色） + Squad（编排） + Skill（做法） + Issue（任务）
                  ↓
       Leader 带队：设计 → 实现 → 测试
                  ↓
   每步判门（multica-verification skill 复跑）→ Human 最终验收
```

## 5 分钟快速开始

### 前置条件

一个 **Multica 环境**（能创建 Agent / Squad / Skill / Issue）。
还没有？先看 [Multica 文档](https://www.multica.ai/docs) 或 [How Multica works](https://www.multica.ai/docs/how-multica-works)（3 分钟）。

### 复制 software-development Starter

👉 **[`templates/zh_CN/squad/software-development`](./templates/zh_CN/squad/software-development)**

你将得到：

- 1 个 Squad Leader（编排 + 判门）
- 6 个 Agent：Architect / Designer / FrontendDev / BackendDev / Tester / Reviewer
- 6 个 Skill（其中 multica-verification 是必备判门 Skill）
- 1 个 Issue 模板（含「涉及端」范围声明）
- 1 个软件开发工作流（任意角色可缺失的条件路由）

### Step 1 — 创建 Agents

在 Multica 创建 5 个 Agent（命名遵循 [`docs/zh_CN/naming-conventions.md`](./docs/zh_CN/naming-conventions.md)），把 [`templates/zh_CN/agents/`](./templates/zh_CN/agents/) 下对应文件的代码块复制到各自 Instructions：

| Agent | 复制 |
| --- | --- |
| Architect | `architect.md` |
| FrontendDev | `frontend-developer.md` |
| BackendDev | `backend-developer.md` |
| Tester | `tester.md` |
| Reviewer | `reviewer.md` |

> `leader.md` 不需要单独建 Agent：Squad Instructions 只注入 Leader，`squad.md` 就是它的行为配置。

### Step 2 — 创建 Skills

在 Multica 创建 6 个 Skill，把 `SKILL.md` 的代码块复制到对应 Skill：

| Skill | 来源 | 挂给谁 |
| --- | --- | --- |
| `multica-verification`（判门，必备） | [`templates/zh_CN/skills/multica-verification/SKILL.md`](./templates/zh_CN/skills/multica-verification/SKILL.md) | **Leader** |
| `multica-gate-setup` | [`templates/zh_CN/skills/multica-gate-setup/SKILL.md`](./templates/zh_CN/skills/multica-gate-setup/SKILL.md) | Leader（集成 CI 硬门禁时） |
| `multica-test-design` | [`templates/zh_CN/skills/multica-test-design/SKILL.md`](./templates/zh_CN/skills/multica-test-design/SKILL.md) | Tester |
| `multica-requirement-analysis` | [`templates/zh_CN/skills/multica-requirement-analysis/SKILL.md`](./templates/zh_CN/skills/multica-requirement-analysis/SKILL.md) | Leader / Architect |
| `multica-technical-design` | [`templates/zh_CN/skills/multica-technical-design/SKILL.md`](./templates/zh_CN/skills/multica-technical-design/SKILL.md) | Architect |
| `multica-implementation` | [`templates/zh_CN/skills/multica-implementation/SKILL.md`](./templates/zh_CN/skills/multica-implementation/SKILL.md) | FrontendDev / BackendDev |

> 6 个 Skill 全部共享放在 `templates/zh_CN/skills/`，统一 `multica-` 前缀命名空间（multica-verification 是判门，Bug Fix 也在用；multica-gate-setup 用于把 CI 硬门禁装进仓库并在判门时感知 CI 结论；multica-test-design 给 Tester 生成用例与测试报告）。Skill 靠**名称**挂载，谁需要就在自己的 Instructions 里写「用 xxx skill」，与仓库路径无关。

### Step 3 — 创建 Squad

创建 Squad，把 `templates/zh_CN/squad/software-development/squad.md` 复制到 Squad Instructions。

### Step 4 — 创建 Issue

把 `templates/zh_CN/squad/software-development/issue.md` 复制到新 Issue，填上你的需求。

### Step 5 — 分配

把 Issue 分配给这个 Squad。

### Step 6 — 运行

```text
Issue → [设计] → [API 契约 ∥ 功能用例] → [前端 ∥ 后端实现 ∥ API 测试用例] → [测试报告] → Human
```

每个产物的门禁由 Leader 用 multica-verification skill 判门，PASS 才进入下一阶段；范围里没有的角色直接跳过；设计与关键改动由 Reviewer 做业务评审。
就这些。先跑一个真实需求，再按你的团队调整。

## Agent Matrix

| Agent | 该做 | 不该做 |
| --- | --- | --- |
| Architect | 设计方案 | 大量写代码 |
| FrontendDev | 前端实现（对接 UI 设计） | 修改需求 / 自审自放行 / 发明 API |
| BackendDev | 后端实现 + API 契约 | 修改需求 / 自审自放行 / 处理 UI |
| Tester | 功能用例 / 接口测试用例 / 验证验收标准 | 修改需求 |
| Reviewer | 业务评审（设计 / 关键改动） | 替代客观验证 / 替代人类验收 |
| Leader | 编排与判门（用 multica-verification skill） | 亲自实现 / 给自己盖章 |

## 一条指令该放哪？

| 我想告诉 Agent…… | 放这里 |
| --- | --- |
| 「这次要做什么」 | Issue |
| 「这个项目有哪些背景」 | Project Instructions |
| 「你是什么角色」 | Agent Instructions |
| 「谁负责什么」 | Squad Instructions |
| 「怎么做某类工作」 | Skill |
| 「必须通过测试」 | CI（工程系统） |
| 「谁最终决定上线」 | Human |

```text
Issue   = 我们在做什么？
Project = 我们应该知道什么？
Agent   = 我的职责是什么？
Squad   = 谁应该做什么？
Skill   = 我该怎么做？
CI / PR = 什么必须真的通过？
```

## 原则

1. Agent 职责保持狭窄。
2. 不要把路由逻辑复制进每个 Agent。
3. 由 Squad Leader 统一协调。
4. 完成者不得审批自己的工作（判门动作标准化为 multica-verification skill，由不产出的 Leader 或 CI 执行）。
5. 用证据代替「做完了」的口头声明。
6. 不用自然语言指令做硬性约束。
7. 复杂多 Agent 之前，先用简单流程。
8. 临时故障重试。
9. 方向错误就重启新会话，别硬推。
10. 在重要的不可逆边界保留人类审批。

> **Instructions 是引导，不是安全边界。** 必须被遵守的规则请放到 LLM 之外：测试、Lint、构建、CI、分支保护、PR 审批。不要依赖「Agent 被要求不要这样做」。

## Starters

| Starter | 用途 | 状态 |
| --- | --- | --- |
| [Software Development](./templates/zh_CN/squad/software-development) | 常规功能开发（前后端按范围路由，任意角色可缺失） | 推荐 |
| [Bug Fix](./templates/zh_CN/squad/bug-fix) | 根因 / 修复 / 回归（按影响面路由，跳过 Architect） | 实验性 |

更多 Starter（Technical Research 等）将基于真实任务验证后补充。**不要假装最佳实践已经完成。**

## 仓库结构

```text
AGENTS.md     ⭐ Agent 入口：项目约定与改动规范
templates/  ⭐ 从这里开始：可直接复制的全部配置
├── zh_CN/              中文模板（默认；复制整个子目录即用）
│   ├── agents/           共享 Agent Instructions（6 个角色定义）
│   ├── skills/           共享 Skill（6 个，统一 multica- 前缀：判门 / 集成 CI / 测试设计 / 需求分析 / 技术设计 / 实现）
│   │   └── multica-gate-setup/  CI 硬门禁模板随 Skill 自包含（delivery-gate.yml 等）
│   └── squad/            小队 Starter
│       ├── software-development/ 常规开发（squad / issue / README 含工作流）
│       └── bug-fix/             最小修复组合（只换编排）
└── en_US/              英文模板（与 zh_CN/ 结构一致）
docs/          ⭐ 先读这一页：指令放哪 / 门禁证据 / 常见错误 / 裁剪扩展
├── zh_CN/              中文方法论
└── en_US/              英文方法论
```

详细说明见：

| 文档 | 内容 |
| --- | --- |
| [where-to-put-things](docs/zh_CN/where-to-put-things.md) | 指令归属速查表（最值得读） |
| [gates-and-evidence](docs/zh_CN/gates-and-evidence.md) | 门禁 G0–G4 与证据要求 |
| [common-mistakes](docs/zh_CN/common-mistakes.md) | Bad → Good 错误示范 |
| [adapt-and-scale](docs/zh_CN/adapt-and-scale.md) | 裁剪、扩展、试点推广 |
| [naming-conventions](docs/zh_CN/naming-conventions.md) | Agent 命名规范（角色+项目+成员标识） |

## 与相关项目的关系

| 项目 | 关系 |
| --- | --- |
| [Multica](https://github.com/multica-ai/multica) | 运行与协作底座（Issue、Agent、Squad、Runtime） |
| [multica-agent-workflow-template](https://github.com/wksudud/multica-agent-workflow-template) | Agent/Skill 数量与路由设计方法论，可并用 |
| [oh-my-multica](https://github.com/xiaohei-info/oh-my-multica) | 生产级确定性 DAG / Loop；本仓库偏 Squad 与门禁约定层 |

## 贡献

请不要提交「听起来不错」的 Prompt。一次有价值的贡献应包含：

1. 它解决的问题
2. 适用场景
3. 完整模板
4. 至少一个真实示例
5. 已知失败案例

实战经验比提示词复杂度更有价值。详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 资源

- [Multica GitHub](https://github.com/multica-ai/multica)
- [Multica 文档](https://www.multica.ai/docs)
- [How Multica works](https://www.multica.ai/docs/how-multica-works)
- [Agents](https://www.multica.ai/docs/agents)
- [Squads](https://www.multica.ai/docs/squads)
- [Tasks](https://www.multica.ai/docs/tasks)

## 安全

分享配置前必读 [SECURITY.md](SECURITY.md)：禁止上传 token、绝对路径、真实 workspace / 邮箱。

## License

[MIT](LICENSE)
