# 命名规范：角色 + 姓名

> 目的：同一角色定义可以实例化多个 Agent，靠名字区分、不靠改指令——流程因此可复用。

## 规则

1. Agent 名 = `<角色>-<实例>`，角色取固定词表。
2. 角色词表：`Leader / Architect / FrontendDev / BackendDev / Tester / Reviewer`
3. `<实例>` = 领域 / 服务 / 项目名（小写连字符），例如 `user-service`、`web`、`order`。
4. 名字只区分实例，不承载职责；职责永远来自 Agent Instructions / Squad Instructions。

## 示例

| 角色 | 示例名 | 说明 |
| --- | --- | --- |
| BackendDev | `BackendDev-user-service` | 用户服务后端 |
| FrontendDev | `FrontendDev-web` | Web 前端 |
| Tester | `Tester-order` | 订单域测试 |
| Architect | `Architect-core` | 核心架构设计 |
| Leader | `Leader-core` | 核心小队 Leader |

## 为什么

- Multica 里 Agent 名必须唯一；同一角色开多个实例是常态（多服务 / 多领域），所以名字要能区分。
- 名字含角色，路由时 `@mention` 可读、不歧义——`@BackendDev-user-service` 一眼知道是谁。
- **名字变化不改变行为，行为变化改 Instructions 不改名字**：换实例只改 `<实例>`，模板原样复用。
- 命名是约束「流程可复用」的最后一块拼图：同一份 `squad.md`，换一组实例名就是一支新小队。
