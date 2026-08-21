---
name: multica-test-automation
description: 测试自动化 skill（占位壳）：Tester T3 自动化阶段——G2.5 部署环境就绪后，用团队的自动化测试工具执行场景用例并产出 G3 输入。具体工具（Apifox / Postman / Playwright / pytest 等）由团队接入，凭据由运行时 env 注入，不写进角色提示词。
metadata:
  layer: automation
  runtime:
    python: ">=3.10"
    external:
      - <team-test-cli>  # 团队自动化测试 CLI
---

# Test Automation（占位壳 · T3）

> 这是一个**占位壳**。公开的 multica-best-practices 不绑定任何具体公司的内网地址与测试工具。
> 团队接入自己的自动化测试工具时，只改本 skill 的 `scripts/` 与 `config.yaml`，上层 Tester 角色无需改动。

## Purpose

Tester **T3**：G2.5 拿到 `deploy_base_url` 后，用团队自动化测试工具跑用例并产出 G3 输入（测试报告）。

> 跨平台：推荐用 Python 封装配置与 subprocess 调用底层 CLI，Windows / Linux 一致。

## 安装

```bash
pip install -r scripts/requirements.txt
# 安装团队自动化测试 CLI（由团队自定，如 apifox-cli / newman / playwright）
```

## Workflow

```bash
set TEST_TOOL_TOKEN=<token>   # 运行时 env，不写进角色提示词

python scripts/run_tests.py \
  --issue <ISSUE-KEY> \
  --base-url "<deploy_base_url>" \
  --scenario-id <scenario> \
  --environment-id <env> \
  --json
```

或仅指定 Issue（从 `config.yaml` 读 scenario / environment）：

```bash
python scripts/run_tests.py --issue <ISSUE-KEY> --base-url "<deploy_base_url>" --json
```

## 为什么有效

Python 负责配置与 subprocess 调用底层测试 CLI，隔离了「Tester 角色」与「具体测试工具」——换工具只改本 skill，Tester 提示词保持「用 multica-test-automation skill 执行 T3」不变。
