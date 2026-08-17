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

## 小队实例后缀与前缀通配

Squad Instructions 里用 `@Architect` / `@FrontendDev` 等**角色前缀**指代成员，而非写死完整 Agent 名——这样 `squad.md` 才能原样复制。但一个 workspace 里常驻多个同角色实例（如 `FrontendDev-web`、`FrontendDev-mobile`），指挥必须能锁定「本小队」那一个。规则如下：

1. 每个小队在启动时声明自己的**实例后缀** `suffix`（如 `payment`、`order`），与本小队所有角色绑定。
2. Squad Instructions 中凡是写 `@角色` 的地方，指挥一律按 `@角色-<本小队 suffix>` 解析后精确 @mention。
   - 例：`suffix = payment` 时，`@FrontendDev` → 实际派给 `FrontendDev-payment`，`@Architect` → `Architect-payment`。
3. 若某角色不在本小队范围（Issue【范围】不含该层），按既有规则跳过对应产物，不解析、不派活。
4. `suffix` 只在小队配置时设定一次，不写进 `squad.md`；`squad.md` 永远只出现角色前缀，保持可复制。

> 这样「角色前缀」是 Squad 内的逻辑名，「`@角色-suffix`」是 workspace 内的物理名，二者通过小队配置桥接。

## 为什么

- Multica 里 Agent 名必须唯一；同一角色开多个实例是常态（多服务 / 多领域），所以名字要能区分。
- 名字含角色，路由时 `@mention` 可读、不歧义——`@BackendDev-user-service` 一眼知道是谁。
- **名字变化不改变行为，行为变化改 Instructions 不改名字**：换实例只改 `<实例>`，模板原样复用。
- 命名是约束「流程可复用」的最后一块拼图：同一份 `squad.md`，换一组实例名就是一支新小队。
- **前缀通配解决「多实例共存」**：Squad 指令只写角色前缀（可复制），小队配置提供 suffix（可定位），二者分离既不破坏复用，又能在 workspace 里精确派活到本小队成员。
