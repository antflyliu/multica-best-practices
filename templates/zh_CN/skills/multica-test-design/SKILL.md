---
name: multica-test-design
description: 基于需求、设计与 API 契约产出测试用例与覆盖矩阵。负责 T1/T2 的测试设计与测试缺口分析，不负责 G3 判门，也不负责部署后 T3 自动化执行。
---

# Test Design（测试设计）

## 定位

测试设计是**产出功能**，不是门禁角色。它负责让 Acceptance Criteria 在实现前就有可执行的测试设计，并在实现后识别覆盖缺口。

## 谁来执行

- **Tester**：执行本 Skill，产出 T1/T2 测试设计与覆盖分析。
- **Leader + `multica-verification`**：负责 G3 独立判门，Tester 不得给自己的测试结果盖 Gate PASS。
- **`multica-test-automation`**：只负责 G2.5 PASS 后的 T3 runtime automation。

## Workflow

### T1 — 测试设计（G1 前）

输入：PRD / Issue + 技术设计。

产出：

- 每条 `AC-*` 至少一个测试场景。
- 正常、边界、异常、回归场景。
- API 场景覆盖方法、路径、参数、预期响应。
- 标记可自动化与必须手工验证的场景。

### T2 — 测试缺口与覆盖分析（G2 前）

输入：实现后的代码、T1 测试设计、Acceptance Criteria。

产出：

- `AC-*` → test case → implementation 的覆盖矩阵。
- 未覆盖项与原因。
- 自动化缺口。
- 建议补充的测试用例。

T2 不执行 T3 runtime automation，也不宣称 G3 PASS。

## Test Case Contract

每个关键用例至少包含：

```yaml
id: TC-001
acceptance_criteria: [AC-001]
scenario: <scenario>
type: positive | negative | boundary | regression
preconditions: []
steps: []
expected: <expected_behavior>
automatable: true | false
```

## Result

- `READY`：测试设计完整，可进入下一阶段。
- `GAP`：存在覆盖缺口，必须补齐或明确风险接受。
- `BLOCKED`：缺少必要需求、设计、数据或环境信息。

## 与其他 Skill 的边界

- `multica-test-design`：T1/T2 设计、覆盖与缺口分析。
- `multica-test-automation`：**仅在 G2.5 PASS 后**执行 T3 runtime automation。
- `multica-verification`：Leader 在 G3 独立判门。
- `multica-artifact-test-sync`：负责测试 Artifact 的发布/同步。

任何测试设计 Artifact 被修改后，其下游 Gate 立即失效，必须重新验证。
