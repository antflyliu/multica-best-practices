---
name: multica-review-product
description: 需求/PRD 专属评审框架。由 ProductReviewer 调用，对 ProductManager 产出的 PRD 做专业分析（范围清晰/目标明确/验收可测/约束完备/待确认项），输出 PASS/FAIL 与修改清单，汇报 Leader。
---

# 需求（PRD）专业评审（ProductReviewer）

本 skill 提供对 **PRD / 需求产物**的结构化专业评审框架。调用方为 `ProductReviewer`，评审对象为 `ProductManager` 经 `multica-artifact-req-sync` 回传的 PRD 链接。

## 什么时候用
- ProductReviewer 收到 Leader 派发的「评审 PRD」任务时。
- PRD 修改后进入复审轮次时（对照上一轮修改清单逐条核对）。

## 评审维度（逐项给结论）
1. **范围清晰**：边界清楚、无歧义、可拆分任务；无隐含范围。
2. **目标明确**：解决的问题可度量，不含模糊表述。
3. **验收可测**：每条 AC- 都能被客观验证，无「体验好」类模糊标准。
4. **约束完备**：权限、异常、合规、依赖方、数据口径是否列出。
5. **待确认项**：OP- 是否完整列出，是否阻塞后续开发（阻塞项须为阻断项）。

## 输出格式
```
【PRD 评审】<PRD 链接>
结论：PASS / FAIL
阻断项（FAIL 时必填，每项含 理由 / 涉及点 / 修改方向）：
- ...
建议项（非阻断）：
- ...
与上一轮修改清单核对（复审时）：已解决 X 项 / 未解决 Y 项
轮次：第 N / 3 轮
```
结论与修改清单**汇报给 Leader**，不自行改 PRD、不自行通知 ProductManager。

## 边界
- 只评 PRD/需求，不评设计、代码、测试用例、UI。
- 不替代 Leader 的通用门禁（multica-verification skill）。
- 技术可行性交 ArchReviewer，你只管需求层质量。
- 第 3 轮仍 FAIL → 标注「升级人类」，交 Leader 处理，停止循环。
