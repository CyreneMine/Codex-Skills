# create-unity-learning-agents

用于为新的 Unity 教程学习项目生成专属 `AGENTS.md`。

这个 Skill 继承了 PlayerPrefs 学习项目中形成的协作流程：

- 先阅读真实项目文件，再判断问题。
- 默认不直接修改 Unity 运行相关代码。
- 检查教程练习时区分代码、场景、Inspector、运行验证。
- 每完成一课或一个阶段，维护 README、LearningProgress 和 Notes。
- Git commit/push 必须由用户明确要求。
- 文档和提交信息默认使用中文。

## 调用示例

```text
使用 $create-unity-learning-agents，为当前 Unity JSON 持久化教程项目生成专属 AGENTS.md
```

```text
使用 $create-unity-learning-agents，为当前 Unity 动画系统教程生成 AGENTS.md
```

## 适用主题

已内置以下主题方向的检查规则：

- JSON / 持久化 / 存档系统
- PlayerPrefs
- UGUI
- Input System
- 物理和角色控制
- Animator / 动画系统
- Prefab / Scene / Component
- Addressables / Resources
- 网络同步
- 反射 / 泛型管理器
- 通用 Gameplay 系统

## 文件说明

- `SKILL.md`：Skill 主说明和执行流程。
- `agents/openai.yaml`：Codex 界面展示信息。
- `references/core-template.md`：AGENTS 通用模板来源。
- `references/topic-guides.md`：不同 Unity 教程主题的专项检查规则。
