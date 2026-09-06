---
name: multica-verification
description: 独立门禁验证：由 Leader 在 G1/G2/G3 复跑验收标准并输出 PASS、FAIL 或 BLOCKED。用于客观判定交付条件，不负责产出业务/技术/测试产物。
---

# Verification（独立门禁）

## 定位

Verification 是**门禁动作**，不是角色，也不是产出 Skill。它只回答：

> 当前版本的指定产物，是否有客观证据满足当前 Gate 的验收标准？

**唯一门禁执行者：Leader。** 产出角色不得使用本 Skill 给自己的产物盖 PASS。

如果产出角色需要提前检查，应在自己的产出 Skill 中执行 pre-submit checklist；该检查不产生 Gate 状态，也不能替代 Leader 的 Verification。

## Gate 输入

Leader 执行本 Skill 时至少需要明确：

- `Gate ID`：`G1` / `G2` / `G3`
- `Issue`
- `Artifact`
- `Artifact Version`
- `Upstream Gates`
- `Acceptance Criteria`
- `Evidence`

若任一必需输入缺失，结果必须是 `BLOCKED`，不得降级为 `PASS`。

## Process

1. 读取 Issue 的 Acceptance Criteria。
2. 确认被验证 Artifact 及其当前 Version。
3. 确认所有 Upstream Gates 仍为有效状态。
4. 将每条 Acceptance Criterion 映射到可复跑 Evidence。
5. **由 Leader 独立复跑**验证命令、测试或检查；不得把产出者口述/粘贴的结果当作复跑证据。
6. 检查 diff / 变更范围是否符合 Issue Scope。
7. 逐条记录检查结果，并汇总 Gate 状态。

## Gate Result

### PASS

所有当前 Gate 的 Acceptance Criteria 均满足，且 Upstream Gates 有效。

### FAIL

至少一条 Acceptance Criterion 未满足。必须记录：

- 问题
- 为什么重要
- 证据 / 位置
- 修复方向

### BLOCKED

缺少必要信息、环境、证据或有效的上游 Gate，无法客观判定。**BLOCKED 永远不能转换成 PASS，除非阻塞项被补齐并重新验证。**

## Artifact 变更规则

**任何产物被修改后，其下游 Gate 立即失效。**

Leader 必须：

1. 识别被修改 Artifact 的下游依赖。
2. 将受影响的下游 Gate 标记为需要重新验证。
3. 不得复用修改前版本的 Gate PASS 作为当前版本的有效证据。
4. 从最近受影响的 Gate 重新执行 Verification。

因此，Gate PASS 必须绑定到具体的 `Artifact Version`，而不是只绑定 Issue。

## Gate 与其他角色的边界

- **Reviewer**：判断专业质量是否达标，输出 review finding。
- **Leader / Verification**：判断是否满足交付 Gate，输出 Gate Result。
- **CI/PR**：提供机器可验证证据，不能被文字描述替代。
- **Human Acceptance**：最终业务/产品是否接受，不由 Verification 代替。

## 与 CI 的关系

`multica-verification` 是 Agent 侧的 Gate 执行方式；CI 是机器侧的硬门禁。两者不是互相替代：

- 能自动化的检查应进入 CI。
- Leader 在 Gate 时仍需核对 CI 结果与 Artifact Version 是否对应。
- `G2.5` CI/CD PASS 后，才允许触发 T3 自动化测试。

## Result Contract

建议 Leader 统一输出以下结构：

```yaml
gate:
  id: G2
  issue: <ISSUE_KEY>
  artifact: <ARTIFACT_TYPE>
  artifact_version: <VERSION>
  upstream_gates: [G1]
  result: PASS | FAIL | BLOCKED
  checks:
    - criterion: <AC_ID>
      result: PASS | FAIL | BLOCKED
      evidence: <COMMAND_OR_EVIDENCE_REF>
  failures: []
```
