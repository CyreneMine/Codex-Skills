# AGENTS.md

## 仓库定位

本仓库用于保存和管理我个人使用的 Codex Skills。

这里的 Skill 主要服务于我的长期学习、项目复盘、代码检查、文档整理和自动化协作流程，不追求一开始就做成通用市场插件。

## Codex 工作原则

在本仓库工作时，你可以：

- 阅读和检查已有 Skill
- 创建新的 Skill 目录
- 更新 `SKILL.md`
- 更新 Skill 相关的 `references/`、`templates/`、`examples/`、`scripts/`
- 更新仓库 README 和 Skill 索引
- 帮我验证 Skill 结构
- 在我明确要求时提交和推送

不要在未经我明确要求时：

- 删除已有 Skill
- 重命名已有 Skill
- 重写 Git 历史
- 自动 commit 或 push
- 提交密钥、Token、账号信息、本机缓存或临时构建目录

## Skill 管理规则

- 每个 Skill 一个独立目录，统一放在 `skills/` 下。
- Skill 目录名使用英文小写短横线。
- 每个 Skill 必须包含 `SKILL.md`。
- 如果有辅助资料，优先放在当前 Skill 目录内部，不要散落到仓库根目录。
- 新增或修改 Skill 后，要同步更新 `skills/README.md`。
- 如果改动会影响安装或调用方式，也要更新根目录 `README.md`。
- 中文文件统一保持 UTF-8。

## 检查要求

修改 Skill 后，至少检查：

- `SKILL.md` frontmatter 是否包含正确的 `name` 和 `description`
- Skill 名称是否和目录名一致
- 文档里的相对链接是否能解析
- 引用的 `references/`、`templates/`、`scripts/` 是否存在
- 是否包含不该提交的本机路径、密钥或临时文件
- 是否能通过官方 Skill 校验脚本

## Git 规则

- 除非我明确说 push，否则不要自动推送。
- commit message 默认使用中文。
- 提交前先总结本次变更。
- push 后确认远程分支状态。

## 回答风格

请使用中文，说明你改了什么、为什么这样管理，以及以后我该怎么复用。
