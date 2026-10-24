# create-unity-learning-agents

为 Unity 教程学习项目生成或维护专属 `AGENTS.md`，把已验证的协作经验带到下一门课程。

规则来源涵盖持久化学习和综合实践：先读真实工程，保留用户修改边界，区分静态检查与实际运行，记录独立实现和 Agent 协助，再按授权维护 Git 与作品资料。它不会因为一次调用就自动重组工程、代写功能或发布成果。

## 这次补充的工作流

- **多工程管理：** 识别 Git 根目录、理论参考工程与当前实践工程，保留只读边界和 `.meta` 引用。
- **按目标验收：** 区分代码、编译、Editor、独立包、用户反馈及截图；必要验证完成后更新对应进度，专项边界另记。
- **重复配置与分工：** 以用户样板批量制作动画覆盖、Prefab 引用和表格数据，记录规则、范围与检查结果。
- **资源与 Git：** 各工程生成目录和本地教学素材排除；按实际需求分批提交，推送后核对提交同步并报告本地保留改动。
- **Demo 收尾：** 用户请求时整理功能、模块、截图和简历材料；README 顶部突出玩法、完成情况和个人贡献。
- **尊重学习选择：** 已接受的练习边界、跳过原因和不同于教程的有效实现，不反复当成必须修复的问题。

## 调用示例

```text
使用 $create-unity-learning-agents，为当前 Unity JSON 持久化教程项目生成专属 AGENTS.md。
```

```text
使用 $create-unity-learning-agents，更新当前理论与实践双工程的 AGENTS.md，保留理论工程只读和教学素材不上传的约定。
```

```text
使用 $create-unity-learning-agents，把这个已完成 Demo 的验证、Agent 分工和作品总结流程整理进现有 AGENTS.md，保留已有有效规则。
```

## 文件说明

- [SKILL.md](SKILL.md)：入口、适用范围、生成流程和修改边界。
- [agents/openai.yaml](agents/openai.yaml)：Codex 界面信息与默认提示。
- [core-template.md](references/core-template.md)：项目规则的通用来源。
- [topic-guides.md](references/topic-guides.md)：持久化、UI、输入、物理、动画、资源、数据与 Gameplay 等专项检查。
- [project-lifecycle.md](references/project-lifecycle.md)：按需使用的双工程、批量配置、验证证据、Git 分批和 Demo 展示指南。

## 校验范围

本次更新核对官方 Skill 结构校验、引用链接、UTF-8、界面元数据以及仓库版与本机安装版的一致性。结构校验不等同于在新对话中完成实际调用；后续课程继续用真实项目验证生成规则是否合适。
