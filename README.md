# Codex-Skills

这是我的个人 Codex Skills 仓库，用来保存、版本管理和复用自己整理出来的工作流。

当前仓库重点不是发布通用插件，而是把已经验证过、适合自己长期使用的 Skill 保存下来，方便以后在新项目、新对话里继续调用。

## 目录结构

```text
Codex-Skills/
├── AGENTS.md
├── README.md
└── skills/
    ├── README.md
    └── create-unity-learning-agents/
        ├── SKILL.md
        ├── README.md
        ├── agents/
        │   └── openai.yaml
        └── references/
            ├── core-template.md
            ├── topic-guides.md
            └── project-lifecycle.md
```

## Skill 管理规则

- 每个 Skill 使用一个独立目录，目录名使用英文小写短横线，例如 `create-unity-learning-agents`。
- 每个 Skill 必须包含 `SKILL.md`。
- 如果 Skill 依赖模板、参考资料或示例，放在该 Skill 目录下的 `references/`、`templates/`、`examples/` 或 `scripts/` 中。
- 根目录 `README.md` 只记录仓库定位、结构和通用维护方式。
- `skills/README.md` 作为 Skill 索引，每新增或修改一个 Skill 都同步更新。
- 不提交密钥、账号、Token、临时构建目录或本机缓存。
- 文件统一使用 UTF-8，尤其是包含中文说明的 `README.md`、`SKILL.md` 和 `openai.yaml`。

## 安装方式

把需要使用的 Skill 目录复制到本机 Codex Skills 目录：

```powershell
Copy-Item -Recurse `
  -LiteralPath ".\skills\create-unity-learning-agents" `
  -Destination "$env:USERPROFILE\.codex\skills\create-unity-learning-agents"
```

安装后，重新打开 Codex 对话，使用 Skill 名称调用：

```text
使用 $create-unity-learning-agents，为当前 Unity 教程项目生成专属 AGENTS.md
```

## 校验方式

修改 Skill 后，建议使用 Codex 官方 Skill 校验脚本检查结构是否有效。

校验重点：

- `SKILL.md` frontmatter 是否正确。
- 引用文件路径是否存在。
- 中文内容是否仍为 UTF-8。
- 新对话中是否能通过 `$skill-name` 调用。

## 当前 Skill

| Skill | 用途 | 状态 |
| --- | --- | --- |
| [`create-unity-learning-agents`](skills/create-unity-learning-agents/README.md) | 生成或更新 Unity 学习协作规则，覆盖多工程、验证证据、Agent 协助和 Demo 收尾 | 结构与链接已校验；新对话调用待验证 |
