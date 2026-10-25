# Codex-Skills

这是我的个人 Codex Skills 仓库，用来保存、版本管理和复用自己整理出来的工作流。

当前仓库重点不是发布通用插件，而是把已经验证过、适合自己长期使用的 Skill 保存下来，方便以后在新项目、新对话里继续调用。

## 目录结构

```text
Codex-Skills/
├── AGENTS.md
├── README.md
└── skills/
    ├── README.md                       # 按用途分类的技能索引
    ├── create-unity-learning-agents/    # Unity 学习与协作
    └── archive-authorized-courses/      # 学习资料与离线归档
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        └── scripts/
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

把需要使用的 Skill 目录复制到本机 Codex Skills 目录。例如首次安装课程归档技能：

```powershell
$skillName = "archive-authorized-courses"
$skillSource = Join-Path (Get-Location) "skills\$skillName"
$skillDestination = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
if (Test-Path -LiteralPath $skillDestination) { throw "目标已存在，请先对比已安装版本。" }
Copy-Item -Recurse -LiteralPath $skillSource -Destination $skillDestination
```

安装后重新打开对话，按名称调用：

```text
使用 $archive-authorized-courses，把我已有观看权限的课程整理为离线学习资料。
使用 $create-unity-learning-agents，为当前 Unity 教程项目生成专属 AGENTS.md。
```

技能本身不包含账号或课程文件，也不会提供额外观看权限。

## 校验方式

修改 Skill 后，建议使用 Codex 官方 Skill 校验脚本检查结构是否有效。

校验重点：

- `SKILL.md` frontmatter 是否正确。
- 引用文件路径是否存在。
- 中文内容是否仍为 UTF-8。
- 新对话中是否能通过 `$skill-name` 调用。

## 当前 Skill

目录保持 `skills/<skill-name>/` 平铺，分类由索引维护，避免改变已有安装路径。

| 分类 | Skill | 用途 | 验证状态 |
| --- | --- | --- | --- |
| Unity 学习与协作 | [`create-unity-learning-agents`](skills/create-unity-learning-agents/README.md) | 生成或更新 Unity 学习协作规则，覆盖多工程、运行证据和 Demo 收尾 | 结构与链接已校验；新对话调用待验证 |
| 学习资料与离线归档 | [`archive-authorized-courses`](skills/archive-authorized-courses/SKILL.md) | 授权课程的 HLS、配套资料、动态文字、去重续传、校验和离线目录 | 官方结构校验与 6 项本地合成测试通过；新对话调用及真实站点重新回归待验证 |

完整说明与脚本入口见 [分类索引](skills/README.md)。
