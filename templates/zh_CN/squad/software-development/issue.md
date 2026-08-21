# Issue Template

> 复制到新 Issue，填写后交给 Squad。

```markdown
# Feature

## 背景
<!-- 为什么做这件事？ -->

## 目标
<!-- 这个功能要解决什么问题？ -->

## 范围
<!-- Leader 按此路由：缺失的端不派角色，对应产物直接跳过 -->
- 涉及端（勾选）：
  - [ ] 设计（需要 Architect 出方案）
  - [ ] 前端（需要 FrontendDev）
  - [ ] 后端（需要 BackendDev + API 契约）
- 改动内容：<!-- 应该改什么？ -->

## 非目标（Non-goals）
<!-- 明确不做哪些事？ -->

## 验收标准（必须可测试）
- [ ]
- [ ]
- [ ]

## 需求追踪矩阵（建议，保证无断链）
<!-- 用 REQ → DESIGN → API → CODE → CASE → TEST 的映射保证每条验收标准都能追到产物与测试 -->
| 验收标准 (AC) | 设计 (DESIGN-ID) | API (API-ID) | 代码 | 用例 (CASE-ID) | 测试结果 |
| --- | --- | --- | --- | --- | --- |
| AC-1 | | | | | |

## 技术上下文
<!-- 现有架构、模块、API、约束等 -->

## 约束
<!-- 兼容性、性能、安全、截止时间等 -->

## 验证方式
- [ ] 构建
- [ ] 单元测试
- [ ] CI/CD 部署到测试环境（范围含 CI/CD 时勾选；G2.5）
- [ ] 自动化测试（G2.5 后，T3）
- [ ] 手动验证（如适用）

## Git 分支
<!-- 由 Leader 在 G0 声明；所有实现 merge 到该 deploy branch，@DevOps 仅对其触发 CI/CD。feature 分支不用于 CI/CD -->
- Deploy branch：`release/<ISSUE-KEY>-<slug>`
- Feature branch（可选）：`<ISSUE-KEY>-<desc>`

## 参考资料
<!-- 文档、Issue、截图、代码位置 -->

## 备注
<!-- 其他小队需要知道的信息 -->
```

---

## 为什么这么写

- **范围里的「涉及端」是路由输入**：Leader 的 G0 靠它决定派哪些角色。范围缺失或含糊 → G0 FAIL，而不是 Leader 猜。
- **目标 / 范围 / 非目标**三段分离：防止 Agent 自由发挥扩大范围。
- **验收标准必须可测试**：没有可测试的验收标准，判门无法执行（multica-verification skill 无从对照），整个门禁体系会失效。

## 常见失败

- 只写「帮我把这个功能做了」→ 小队要么瞎猜，要么卡在 G0。
- 不勾选「涉及端」→ Leader 不知道要不要派 Frontend / Backend，流程会按默认全栈跑。
- 把需求细节写进 Agent Instructions 而不是 Issue → 换一个任务这些指令就失效了。
