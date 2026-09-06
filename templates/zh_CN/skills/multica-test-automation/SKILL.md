---
name: multica-test-automation
description: Tester T3 runtime automation：仅在 G2.5 CI/CD PASS 且部署环境就绪后执行自动化测试，并产出 G3 输入。具体测试工具由团队 adapter 配置，本 Skill 不绑定具体厂商。
category: methodology
owner: Tester
version: 1.0
inputs:
  - Issue
  - Deployed Artifact Version
  - Deploy Base URL
  - Test Suite
  - G2.5 PASS evidence
outputs:
  - Machine-readable T3 test result
  - Runtime test evidence
side_effects:
  - Executes runtime tests against the deployed environment
requires:
  - G2.5 PASS
  - Deployment environment ready
  - Team test adapter / runner
forbidden:
  - Running T3 before G2.5 PASS
  - Declaring G3 PASS
  - Hard-coding vendor-specific credentials in this Skill
idempotent: true
platform_dependent: false
metadata:
  runtime:
    python: ">=3.10"
---

# Test Automation（T3）

## Purpose

执行部署后的 runtime automation，验证实现是否在目标环境满足测试场景，并产出供 G3 使用的机器可读测试结果。

**硬前置：`G2.5 = PASS`。** 未取得 G2.5 PASS 时禁止触发 T3。

## Input Contract

```yaml
t3:
  issue: <ISSUE_KEY>
  artifact_version: <DEPLOYED_VERSION>
  base_url: <DEPLOY_BASE_URL>
  test_suite: <TEST_SUITE>
  g2_5: PASS
```

若 `g2_5` 不是 `PASS`，结果必须为 `BLOCKED`，不得执行测试。

## Execution

统一以团队 adapter 提供的测试 runner 执行，例如：

```bash
python scripts/run_tests.py \
  --issue <ISSUE_KEY> \
  --base-url "<deploy_base_url>" \
  --suite <TEST_SUITE> \
  --json
```

具体 CLI、场景 ID、环境 ID、token 等属于 adapter / platform 配置，不写入 Tester Agent Instructions，也不写死在通用 Skill 中。

## Output Contract

```yaml
test_run:
  issue: <ISSUE_KEY>
  artifact_version: <DEPLOYED_VERSION>
  gate_prerequisite: G2.5:PASS
  result: PASS | FAIL | BLOCKED
  total: <N>
  passed: <N>
  failed: <N>
  blocked: <N>
  evidence: <MACHINE_READABLE_REPORT>
```

## Failure Rules

- 环境未就绪 / G2.5 非 PASS → `BLOCKED`。
- 测试失败 → `FAIL`，保留复现步骤与机器证据。
- 测试通过只代表 T3 execution PASS，不等于 G3 PASS。
- G3 由 Leader 使用 `multica-verification` 独立判门。

## Boundaries

- `multica-test-design`：T1/T2 测试设计与覆盖缺口。
- `multica-test-automation`：G2.5 后的 T3 runtime execution。
- `multica-artifact-test-sync`：测试 Artifact 发布/同步。
- `multica-verification`：Leader 的独立 Gate 判定。

任何被测 Artifact 或测试 Artifact 修改后，其下游 Gate 立即失效，必须重新验证。
