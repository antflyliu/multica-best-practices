---
name: multica-review-frontend
description: 前端实现专属评审框架。由 FrontendReviewer 调用，对 FrontendDev 产出做专业分析（UI/API 契约吻合度/组件质量/单测充分性/验收对照），输出 PASS/FAIL 与修改清单，汇报 Leader。
---

# 前端实现专业评审（FrontendReviewer）

本 skill 提供对 **前端实现产物**的结构化专业评审框架。调用方为 `FrontendReviewer`，评审对象为 `FrontendDev` 经代码类 skill 回传的变更文件列表 / 仓库引用，以及 Leader 派活时给的 UI 链接 + API 契约链接。

## 什么时候用
- FrontendReviewer 收到 Leader 派发的「评审前端实现」任务时。
- 实现修改后进入复审轮次时（对照上一轮修改清单逐条核对）。

## 评审维度（逐项给结论）
1. **UI 吻合度**：布局、交互、状态、边界态是否对齐 Designer 产出。
2. **API 契约吻合度**：调用参数、返回处理、错误分支是否对齐 BackendDev 契约。
3. **组件质量**：可复用性、职责单一、无明显坏味道。
4. **单测充分性**：关键路径、边界条件、异步/错误分支是否覆盖；有无为凑覆盖率而无效的测试（标记并阻断）。
5. **验收对照**：实现是否真正满足每条 AC-。

## 输出格式
```
【前端实现评审】<变更链接>
结论：PASS / FAIL
阻断项（FAIL 时必填，每项含 理由 / 涉及点 / 修改方向）：
- ...
建议项（非阻断）：
- ...
与上一轮修改清单核对（复审时）：已解决 X 项 / 未解决 Y 项
轮次：第 N / 3 轮
```
结论与修改清单**汇报给 Leader**，不自行改代码、不自行通知 FrontendDev。

## 边界
- 只评前端实现与单测，不评架构、需求、UI 设计稿、后端、测试用例。
- 不替代 Leader 的通用门禁（multica-verification skill）。
- 第 3 轮仍 FAIL → 标注「升级人类」，交 Leader 处理，停止循环。
