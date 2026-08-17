---
name: multica-artifact-design-sync
description: 把开发设计文档产物对接到代码仓库或知识平台（默认 Git 仓库 / Confluence）。用于 @Architect 上传技术设计，供实现与测试下游消费。平台可替换。
---

# Artifact · Technical Design Sync

## Purpose

把开发设计文档落地到团队统一的技术文档位置，并让下游用稳定方式取回。

> 本 skill 把「平台对接」与「角色提示词」解耦：角色提示词只说"产出技术设计"，不关心平台。换公司只改本 skill，不动 @Architect 提示词。

## 默认平台：Git 仓库 / Confluence（二选一，团队约定）

- 产出：技术设计（当前架构、建议改动、受影响组件、实现步骤、验证计划、风险）。
- 上传方式 A（Git 仓库）：放入仓库约定文档目录（如 `docs/design/<issue-id>.md`），随代码 PR 一起评审、留痕、可追溯。
- 上传方式 B（Confluence）：创建 / 更新技术设计页面，回传链接。
- 取回：下游 @FrontendDev / @BackendDev / @Tester 通过**文件路径或页面链接**读取。

## 产物内容规范（与角色解耦的部分）

依据 `multica-technical-design` skill 产出：当前架构、最小可行改动、受影响组件、实现步骤、验证计划、风险。保留稳定标题与编号。

## 用法（角色侧只写这一句）

> @Architect：「产出技术设计，用 `multica-artifact-design-sync` skill 落地到团队约定位置（Git / 知识平台），并回传引用。」

## 替换平台（不改角色提示词）

把本 skill 的「默认平台」段替换为你们的工具（内部 Wiki / Notion / 飞书），保持「上传 + 回传稳定引用」接口不变即可。

## 为什么有效

设计文档的存放位置各团队不同（有的进仓库、有的进 Wiki）。下沉到 skill 后，角色保持「产出什么内容」的稳定描述，位置随 skill 替换。
