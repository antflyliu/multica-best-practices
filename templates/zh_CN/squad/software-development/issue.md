# Issue Template

> 复制到新 Issue，填写后交给 Squad。

```markdown
# Feature

## Issue 来源（必填，二选一）
- [ ] 外部系统链接（轻量）：仅填「链接 / 一句话摘要 / 涉及端」，其余章节省略
      - 链接：https://jira.example.com/browse/<ISSUE-KEY>
      - 摘要：<!-- 一句话说明要做什么 -->
- [ ] 全量自包含（默认）：本 Issue 即为需求，完整填写以下所有章节

## 变更类型（必填）
- [ ] Feature
- [ ] Bug Fix
- [ ] Refactor
- [ ] Performance
- [ ] Security
- [ ] Documentation
- [ ] Infrastructure
- [ ] Other: <!-- 说明 -->

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

## 参考资料
<!-- 文档、Issue、截图、代码位置 -->

## 备注
<!-- 其他小队需要知道的信息 -->
```

---

## 为什么这么写

- **变更类型先于路由**：Feature、Bug Fix、Refactor、Performance、Security 等任务的风险和验证方式不同，先声明类型，Squad 才能选择合适流程。
- **范围里的「涉及端」是路由输入**：Leader 的 G0 靠它决定派哪些角色。范围缺失或含糊 → G0 FAIL，而不是 Leader 猜。
- **目标 / 范围 / 非目标**三段分离：防止 Agent 自由发挥扩大范围。
- **验收标准必须可测试**：没有可测试的验收标准，`multica-verification` 无从对照，整个门禁体系会失效。
- **Issue 是需求契约，不是实现蓝图**：技术上下文、约束、追踪矩阵、验证方式、Git 分支等工程产物由 Squad 在运行中产出，不前置成提单人的负担。

## 常见失败

- **没有 Change Type**：所有任务都被当成 Feature，导致验证强度和路由失真。
- **只写「帮我把这个功能做了」**：小队要么瞎猜，要么卡在 G0。
- **不勾选「涉及端」**：Leader 不知道要不要派 Frontend / Backend，流程会按默认全栈跑。
- **把需求细节写进 Agent Instructions 而不是 Issue**：换一个任务这些指令就失效了。
