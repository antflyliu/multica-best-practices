---
name: multica-gate-setup
description: 集成 CI 硬门禁到目标仓库，并让判门消费 CI 证据。用于部署门禁、读取 check-runs 判 G2、CI 不可用时降级软门禁。
---

# Gate Setup（CI 门禁集成）

## 这是什么

把「验证」从 Agent 自觉升级为 CI 机器产生证据的集成 Skill。
核心思想（`multica-gatekit`）：**门禁出具方必须和被门禁方不同源**——作者无法自己盖章「测试通过」；CI 的真实运行结果是证据，正式门禁结论则只能由 Leader 出具。

本 Skill 回答两个问题：

1. **怎么把 gates 装进一个仓库？**（一次性部署）
2. **判门时怎么消费 CI 证据？**（每次任务的 G2）

## 携带的模板文件

部署所需的 3 个模板文件与本 SKILL.md 同目录（Skill 自包含，随 skill 一起复制）：

| 文件 | 作用 |
| --- | --- |
| `delivery-gate.yml` | CI 工作流：在 PR 上跑 lint + test + build，并写入结构化门禁结论 |
| `branch-protection.json` | 分支保护规则：要求 `delivery-gate` 状态检查通过 + 独立审批后才能合入 |
| `apply-branch-protection.sh` | 用 `gh` CLI 把保护规则应用到仓库（修改占位符后运行） |

适用场景：已有可跑的 test / lint / build 命令；不希望「Worker 自证完成」留下作弊空间；多 Squad 并行需要统一合入门禁。

## 能力前提（按环境路由）

Leader 只有 Skill + MCP，无 shell。因此按运行时环境走分支：

| 能力 | 判门（G2） | 部署（一次性） |
| --- | --- | --- |
| 有 GitHub MCP（读） | **真集成**：查 check-runs 并收集 CI 证据 | — |
| 有 GitHub MCP（写） | — | **真集成**：创建 workflow + 设分支保护 |
| 无 MCP | **弱集成**：读取人类贴到 PR 评论里的 CI 证据 | 人类跑脚本，Leader 核对输出 |

## 部署流程（一次性）

1. 读本 Skill 同目录的 3 个模板文件：`delivery-gate.yml` / `branch-protection.json` / `apply-branch-protection.sh`。
2. 按目标仓库替换占位符：

| 文件 | 占位符 | 替换为 |
| --- | --- | --- |
| `delivery-gate.yml` | `pnpm install --frozen-lockfile` | 仓库真实安装命令 |
| | `pnpm lint` / `pnpm test` / `pnpm build` | 仓库真实验证命令 |
| `branch-protection.json` | `"delivery-gate"`（context） | 保持（除非改了 workflow job 名） |
| | `required_approving_review_count` | 独立审批人数（默认 1） |
| `apply-branch-protection.sh` | `YOUR_OWNER` | GitHub 组织 / 用户名 |
| | `YOUR_REPO` | 仓库名 |

> 该分支保护 API 只能要求审批数量，不能用团队 slug 限定“必须由某团队审批”。如需团队级审批，请配置 `CODEOWNERS` 并启用 code owner review，或使用 GitHub Rulesets；本模板不自动创建这些仓库策略。

3. 安装到目标仓库：
   - **有写权限 MCP**：创建 `.github/workflows/delivery-gate.yml`；用 GitHub API `PUT /repos/{owner}/{repo}/branches/main/protection` 设置分支保护（等效于脚本动作，body 用 `branch-protection.json`）。
   - **无 MCP**：给人类明确操作清单——复制 `delivery-gate.yml` 到 `.github/workflows/`；修改两个文件的占位符；`gh auth login` 且有 admin 权限后运行 `bash apply-branch-protection.sh`。
4. 验证生效：查分支保护规则 `GET /repos/{owner}/{repo}/branches/main/protection`，确认 `required_status_checks.contexts` 含 `delivery-gate`；或让人类贴脚本输出。

## 判门流程（G2，每次任务）

1. 通过 GitHub MCP 查 PR 的 check-runs：`GET /repos/{owner}/{repo}/commits/{sha}/check-runs`。
2. 找到名为 `delivery-gate` 的 check，并记录其已完成结果作为 **CI 证据**（`success` / `failure` / `cancelled` / `pending`）。不要把 CI 结果直接当成正式门禁结论。
3. **Leader** 使用 `multica-verification` 执行正式 G2 验证，并把当前 commit 的 CI 证据与 diff 范围作为输入：
   - **有效且已完成的 CI 证据** → 核对证据绑定当前 commit SHA，核对 diff 范围，然后由 Leader 出具正式门禁结论。
   - **CI 缺失** → 使用 `multica-verification` 的软门禁路径完成所需验证。
   - **CI 不可访问，或证据无法绑定当前 commit** → 正式结论为 `BLOCKED`。
4. 已有有效 CI 证据时，不要为了制造另一个结果而重复运行 CI 已覆盖的命令；Leader 核对证据与范围，`multica-verification` 负责正式结论的词汇与出具。

## 正式结果

Leader 通过 `multica-verification` 出具的正式门禁结果只能是：

**APPROVED** —— 所需证据有效，且门禁条件满足。

**APPROVED_NA** —— 该门禁明确不适用，并由 Leader 记录原因。

**REJECTED** —— 证据或范围不满足门禁。必须给出：问题、为什么重要、位置、修复方向、可重新验证的通过条件。

**BLOCKED** —— 所需证据或验证能力不可用。如实报告，绝不能转成批准。

`PASS` / `FAIL` 可以用于单项检查或 CI 证据摘要，但不是正式门禁结论。

## 已知失败案例

曾出现过 CI 已绿，但 Leader 只看到了 PR 上的一条旧评论就判 G2 通过，随后发现最新 commit 的 check-run 实际尚未完成。修复后规定：CI 门禁必须绑定当前 commit SHA 的最新有效 check-run；读不到对应证据就返回 `BLOCKED`，不得用旧评论或旧构建替代。

## 与 multica-verification skill 的关系

两个 Skill 的职责不同：

- `multica-verification`：由 Leader 执行正式门禁验证并出具正式结论。
- `multica-gate-setup`：部署 CI 硬门禁，并为 Leader 的验证收集机器产生的 CI 证据。

**能上 CI 就上 CI**；CI 提供证据，Leader 仍然是正式门禁验证者。两者互补，CI 不绕过 `multica-verification`。

## 为什么有效

门禁如果只有「Agent 被要求检查」，就存在两类作弊：作者假装验证过、作者替自己盖章 PASS。CI 让证据变成机器产生，同时 Leader 与产出角色保持独立，并通过 `multica-verification` 出具正式结论。本 Skill 把这条衔接编进流程——部署有明确清单，证据绑定当前 commit，CI 不可用时有明确降级，不靠临场发挥。
