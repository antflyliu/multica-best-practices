# 门禁与证据

多 Agent 协作最常见的翻车点：**Agent 说「做完了」，但没人知道是不是真的。**

解决方式只有一套：**每个阶段设门禁，每个门禁要求证据，关键证据由非产出者复跑。**

## 门禁是什么

门禁 = 一个可以明确回答「过 / 不过」的检查点。在 software-development Starter 中是 G0–G4：

| 门禁 | 内容 | 谁来判 |
| --- | --- | --- |
| G0 | 需求就绪：有目标 + 可测试的验收标准 | Leader / Human |
| G1 | 设计通过：设计与验收标准对齐 + 业务上可接受 | Leader（multica-verification skill）+ Reviewer |
| G2 | 实现验收：优先引用 CI 结论；CI 缺失才复跑验证 | Leader（multica-verification / multica-gate-setup） |
| G3 | 测试通过：测试报告逐条对照验收标准 | Leader（复核报告） |
| G4 | 人类验收：交付决策 | Human |

门禁的关键是**可判定**：每个门禁对应一个可以 PASS / FAIL 的问题。判不了，就不是门禁，是愿望。

## 判门动作：multica-verification skill

验证是一个**功能**，不是一个角色。它被标准化为 `templates/zh_CN/skills/multica-verification/SKILL.md`，由 **Leader** 在门禁点（G1 / G2 / G3）触发执行：

- Leader 不产出任何产物 → 判门者与被判门者不同源
- 判门 = 复跑验证命令 + 逐条对照验收标准，不引用产出者的描述；仓库已配置 CI 时**优先引用 CI 结论**（如 `[G2 PASS · CI #123]`），不重复跑（感知做法见 `multica-gate-setup` skill）
- 产出者自证（自己跑一遍）不算数，关键命令必须复跑

## 验证与评审是两类检查

| | Verification（验证） | Review（评审） |
| --- | --- | --- |
| 问的问题 | 产物合格吗？有证据吗？ | 方案 / 改动业务上可接受吗？ |
| 判定方式 | 客观可判定：命令输出、逐条对照 | 主观判断：业务意图、风险、可维护性 |
| 执行者 | Leader（multica-verification skill）/ CI | Reviewer（独立角色）/ Human |

验证能标准化成 Skill、能机器化；评审必须由独立的人带着业务视角做。

## 证据是什么

「完成」这个词没有证据价值。有价值的证据：

- 变更文件列表（git diff 摘要）
- 实际执行的命令 + 完整输出
- 与验收标准的逐条对照（每一条 → 对应的测试或检查）
- 测试 / 检查结果
- 已知限制与风险

## 如何防止「作者自证」

规则很简单：**不要让完成工作的人判断自己的工作是否合格。**

- 实现者不给自己发 PASS
- 判门由 Leader 用 multica-verification skill 复跑（或引用 CI 结论），而不是引用实现者的描述
- 自动化验证命令的输出，判门者亲自复跑

## 软门禁（Agent 世界）与硬门禁（CI）

LLM 指令是引导，不是安全边界。**必须被遵守的规则，放在 LLM 之外：**

```text
Tests / Lint / Build / CI / 分支保护 / PR 审批
```

- **软门禁**：Leader 在 Squad 内用 multica-verification skill 判门（G1–G3），靠指令和证据约束，适合起步、无 CI 或探索期。
- **硬门禁**：由 CI 出具、不可伪造的检查（部署模板与做法见 `multica-gate-setup` skill：`templates/zh_CN/skills/multica-gate-setup/`）。当需要比人工检查更可信的结果时，把关键门禁交给 CI——门禁出具方必须和被门禁方不同源。

软门禁和硬门禁是**同一个验证功能的两种执行环境**：Agent 世界的 Skill 与工程世界的 CI。能上 CI 就上 CI。

不要依赖「Agent 被要求不要这样做」。

## 一条真实需求的完整走查

以「新增导出 CSV 功能」为例：

1. **G0**：Issue 写明验收标准，例如「调用导出接口后，返回的 CSV 包含全部筛选结果」。
2. **G1**：Architect 给出最小改动方案（复用现有导出中间件）。Leader 用 multica-verification skill 确认方案覆盖验收标准，Reviewer 评审业务上可接受。
3. **实现**：Frontend / BackendDev（按 Issue 范围）提交代码 + 单元测试 + 变更文件列表 + 验证命令输出（自证）。
4. **G2**：Leader 优先引用 CI 结论（未配 CI 则自己复跑验证命令），并检查 diff 是否只涉及本次需求。PASS。
5. **G3**：Tester 按 multica-test-design skill 出功能 / 接口用例并执行，按验收标准验证「筛选 → 导出 → 检查 CSV 内容」出测试报告，Leader 复核报告是否逐条覆盖验收标准。
6. **G4**：人类查看证据后决定是否合并 / 上线。

任何一个 G2/G3 FAIL，任务回到对应实现者，且**之前的门禁结论作废，需要重新走**——不能因为「上次通过了」就跳过复跑。
