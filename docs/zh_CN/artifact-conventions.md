# 协作产物约定

> 目的：多 Agent 协作时，下游必须能**稳定地找到上游产物**。本文规定每类产物的「内容规范」与「对接 skill」——**产物落在哪个平台、怎么传 / 取，全部交给 skill，不写进角色提示词**。这样换公司（平台不同）只换 skill，不动任何 agent。

## 1. 核心原则：内容归角色，平台归 skill

- **角色提示词只描述"产出什么内容"**（如 PRD 含哪些段落、API 契约含哪些字段），**不出现任何具体平台名**（Figma / Confluence / Apifox / Jira 等）。
- **落盘 / 上传 / 取回由 `multica-artifact-*-sync` 系列 skill 负责**。每个角色在提示词里只写一句"用 `multica-artifact-xxx-sync` skill 落地"，具体平台在该 skill 内实现，可替换。
- **稳定引用 = 链接或路径**：下游通过 skill 回传的链接 / 路径定位上游产物，而不是靠"你应该知道上游产了啥"。

## 2. 产物 → 内容规范 → 对接 skill（一一对应）

| 产物 | 责任人 | 内容规范（角色侧） | 对接 skill（平台侧，可替换） |
| --- | --- | --- | --- |
| UI 设计 | @Designer | 页面结构、状态、交互、标注（对齐 PRD 信息架构） | `multica-artifact-ui-sync`（默认 Figma） |
| 产品需求 PRD | @ProductManager | G-/FR-/BR-/AC-/KPI-/RISK-/OP- 编号化需求 | `multica-artifact-req-sync`（默认 Confluence） |
| 开发设计文档 | @Architect | 当前架构、最小改动、受影响组件、实现步骤、风险 | `multica-artifact-design-sync`（默认 Git 仓库 / Confluence） |
| API 接口文档 | @BackendDev | 端点、入参 / 出参、错误码、鉴权、BR- 对应 | `multica-artifact-api-sync`（默认 Apifox） |
| 测试用例 / 报告 | @Tester | 功能 / 接口用例、覆盖 AC-、测试报告 | `multica-artifact-test-sync`（默认 本地 XMind 转 Jira） |

> 实现类产物（代码）在真实代码仓库，其变更文件列表写进对应阶段产物文件，由下游与门禁核对。

## 3. 角色侧写法（统一模板）

每个角色的「我产出什么」段落只写：

```text
产出 <产物名>，用 `multica-artifact-<xxx>-sync` skill 落地到团队约定平台，并回传稳定链接给 Leader。
内容规范见本文第 2 表 / 对应角色指令。
```

不写平台名、不写本地路径、不写"上传到 XXX"。

## 4. 下游引用的硬规则

1. 上游完成后，由 skill 回传**稳定链接 / 路径**；Leader 派活时显式带上该引用（如"读 `<PRD 链接>` 后做 X"），不靠口头约定。
2. 门禁判词引用产物用「链接 + 编号」（如「`<API 契约链接>` 的 BR-3 缺错误码」），不写"前面那个文档"。
3. 同一类产物永远用同一个 skill 落地——下游靠 skill 名称 + issue 标识定位，不靠搜索。
4. 产物被修改后，引用不变、内容更新；下游门禁据此重新判门（见 gates 的「产物变更门禁失效」）。

## 5. 与编号规范的关系

- 产物**内容**用 `gates-and-evidence.md` 的「AI 可读纪律」（稳定标题、稳定表字段、G-/FR-/BR-/AC- 编号）。
- 产物**位置**由 skill 决定（链接或路径）；位置与内容同样要稳定，下游才能机器化定位。

## 6. 平台替换（不改角色提示词）

团队换平台时，只改对应的 `multica-artifact-*-sync` skill 的「默认平台」段，把 Figma / Confluence / Apifox / Jira 换成你们的工具（蓝湖 / 语雀 / Swagger / TestRail 等），保持「上传 + 回传稳定引用」接口不变。全部角色提示词与 squad 指令**无需改动**。

## 7. 常见错误

Bad: "@Designer 把设计传到 Figma，链接发我。"（平台名固化进提示词，换公司就失效）

Better: "@Designer 产出 UI 设计，用 `multica-artifact-ui-sync` skill 落地并回传链接。"（平台在 skill 内，提示词可复制）
