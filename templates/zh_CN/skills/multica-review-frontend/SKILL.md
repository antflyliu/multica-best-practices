---
name: multica-review-frontend
description: 前端实现专属评审框架，覆盖代码质量、可维护性、性能、可访问性与测试完整性。
category: methodology
owner: FrontendReviewer
version: 1.0
inputs:
  - implementation
  - acceptance_criteria
  - test_evidence
outputs:
  - frontend_review
side_effects: []
requires:
  - implementation_ready
forbidden:
  - modify_implementation
  - approve_leader_gate
idempotent: true
platform_dependent: false
---

# Frontend Review

## 职责
从前端专业角度评审实现，不直接修改实现产物，也不执行 Leader Gate。

## 检查项
- UI/UX 与需求、AC 的一致性
- API 契约吻合度
- 组件质量与可维护性
- 性能与资源加载风险
- 可访问性
- 错误处理与边界条件
- 测试覆盖与回归风险

## 输出
给出明确的 findings、风险等级与建议。评审结论汇报给 Leader；Reviewer 不授予 G1/G2/G2.5/G3 PASS。

第 3 轮仍 FAIL 时升级 Human，由 Leader 决定后续路由。
