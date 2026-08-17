# Security Policy / 安全策略

## When sharing this repo or your configs / 分享本仓库或你的配置时

发布模板、截图或衍生配置时（When publishing templates, screenshots, or derived configs）：

### 禁止包含 / Never include

- API keys、token、cookie、私钥 / API keys, tokens, cookies, private keys
- 本地绝对路径（`/Users/...`、`C:\...`）/ local absolute paths
- 真实 workspace 名称、slug 或内部 URL / real workspace names, slugs, or internal URLs
- 真实邮箱或账号名 / real emails or account names
- 生产凭据或含密钥的 MCP 配置 / production credentials or MCP configs with secrets

### 应该 / Always

- 用占位符替换密钥（`YOUR_API_KEY`、`<workspace-slug>`）/ replace secrets with placeholders
- 每次 `git push` 前检查所有文件 / review every file before each `git push`
- 凭据使用环境变量和 Multica 运行时配置（绝不粘贴进 Instructions）/ keep credentials in environment variables and Multica runtime config, never paste them into Instructions

## High-privilege Skills / 高权限 Skill

控制浏览器、鼠标、Shell（宽权限）或部署的 Skill 应（Skills that control browsers, mouse, Shell, or deploys should）：

- 只挂载到确实需要的 Agent / mount only to agents that actually need them
- 在共享 workspace 首次使用前由人类审查 / be human-reviewed before first use in a shared workspace
- 在 Agent Instructions 里写明明确边界 / declare explicit boundaries in the Agent Instructions

## Reporting security issues / 上报安全问题

如果发现本仓库存在安全敏感的错误（例如示例中意外包含密钥），请通过私有渠道上报，或开 Issue 时不粘贴密钥，必要时要求清理 git 历史。
If you find a security-sensitive mistake in this repo (e.g. an accidental secret in an example), report it through a private channel, or open an Issue without pasting the secret and, if needed, ask for git history cleanup.

## Agent behavior / Agent 行为

AI Agent 是非确定性的。在破坏性文件操作、生产部署、外部发布等高风险动作之前，必须设置人类门禁，详见 [`docs/zh_CN/gates-and-evidence.md`](docs/zh_CN/gates-and-evidence.md)。
AI agents are non-deterministic. Human gates are required before high-risk actions such as destructive file operations, production deploys, and external publishing — see [`docs/zh_CN/gates-and-evidence.md`](docs/zh_CN/gates-and-evidence.md).
