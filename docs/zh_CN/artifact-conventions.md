# 协作产物落盘约定

> 目的：多 Agent 协作时，下游必须能**用稳定路径**找到上游产物。本文规定每个阶段产物的固定目录、文件名与引用方式。Squad 指令与 Agent 指令里的「产出」都必须落到这里定义的路径，否则下游读不到。

## 1. 产物根目录

约定单一根目录，按 Issue 隔离：

```text
artifacts/<issue-id>/
```

- `<issue-id>` = Issue 的编号（如 `ISSUE-123`、`task-2026-0817-a1`）。无 Issue 编号时，用 Leader 在启动时指定的 `<issue-slug>`（占位符，不写死）。
- 所有产物都是**相对路径**，写在产物文件里、发给下游的 @mention 里、门禁判词里；**绝不写绝对路径**（避免泄露本地 workspace，也方便跨机器复制）。
- 若你的工程已有 `docs/` 或 `deliverables/` 约定，把 `artifacts/<issue-id>/` 映射到那个目录即可，文件名与引用规则不变。

## 2. 阶段产物 → 文件路径（与 squad.md 阶段表一一对应）

| 阶段 | 产物 | 责任人 | 固定路径 |
| --- | --- | --- | --- |
| S0 | 产品需求 PRD | @ProductManager | `artifacts/<issue-id>/prd.md` |
| S1a | 技术设计 | @Architect | `artifacts/<issue-id>/design-tech.md` |
| S1b | UI 设计说明（Figma 链接 + 标注） | @Designer | `artifacts/<issue-id>/design-ui.md` |
| S2a | API 契约 | @BackendDev | `artifacts/<issue-id>/api-contract.md` |
| S2b | 功能用例 | @Tester | `artifacts/<issue-id>/cases-feature.md` |
| S3a | 前端实现 | @FrontendDev | 代码仓库（路径见 `变更文件列表`，不在此目录） |
| S3b | 后端实现 | @BackendDev | 代码仓库（路径见 `变更文件列表`，不在此目录） |
| S3c | 接口用例 | @Tester | `artifacts/<issue-id>/cases-api.md` |
| S4 | 测试报告 | @Tester | `artifacts/<issue-id>/test-report.md` |
| G* | 门禁判词 | @Leader | 回写 Issue 评论 / `artifacts/<issue-id>/gate-<g>.md` |
| 验收 | 验收清单 | @ProductManager / @Reviewer | `artifacts/<issue-id>/acceptance.md` |

> 实现类产物（代码）在真实仓库里，不在 `artifacts/`；但**变更文件列表必须写进对应阶段的产物文件**，下游与门禁据此核对。

## 3. 下游引用的硬规则

1. 上游完成后，把产物路径**显式传给下游**：Leader 派活时写明「读 `artifacts/<issue-id>/prd.md` 后做 X」，不靠"你应该知道上游产了啥"。
2. 产物文件内部用**相对路径**互相链接（如 `design-ui.md` 链接 `../prd.md`），不依赖口头约定。
3. 门禁判词引用产物用相对路径 + 编号（如「`api-contract.md` 的 BR-3 缺错误码」），不写"前面那个文档"。
4. 文件名**固定**：同一阶段产物永远叫 `prd.md` / `api-contract.md`，不因任务换名——下游靠文件名定位，不靠搜索。
5. 产物被修改后，路径不变、内容更新；下游门禁据此重新判门（见 gates 的「产物变更门禁失效」）。

## 4. 与编号规范的关系

- 产物内容用 `gates-and-evidence.md` 的「AI 可读纪律」（稳定标题、稳定表字段、G-/FR-/BR-/AC- 编号）。
- 产物**位置**用本文的「固定文件名」——位置与内容同样要稳定，下游才能机器化定位。

## 5. 常见错误

Bad: "@Architect 出个设计，@FrontendDev 你照着做。"（FrontendDev 去哪找设计？）

Better: "@Architect 把技术设计写到 `artifacts/<issue-id>/design-tech.md`；完成后我判 G1，PASS 后派 @FrontendDev 读该文件实现。"
