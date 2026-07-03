# Core AGENTS Template

Use this structure as a source, not as text that must be copied verbatim. Tailor headings and remove irrelevant bullets.

## Required Sections

### Project Positioning

- State this is a Unity learning project following a named tutorial/topic.
- State that the goal is understanding, practice retention, debugging habits, review, and GitHub documentation rather than rapidly producing a finished game.

### Codex Responsibilities

- Read/check/analyze real project files.
- Explain Unity/C#/API principles.
- Review exercises and point out bugs, misunderstandings, and habits.
- Update README, learning progress, and notes.
- Manage Git/GitHub only when requested.

### Code Modification Boundary

- Do not modify `.cs`, scenes, Prefabs, ProjectSettings, Packages, or runtime-affecting files without explicit permission.
- Documentation may be updated when requested.
- When finding an issue, explain location, cause, consequence, recommendation, and a minimal reference snippet.
- Explicit permission examples: “直接修改”, “帮我改”, “可以动代码”, “直接修复”.

### Lesson Review

- Inspect actual files before concluding.
- Check requirement fit, logic, obvious bugs, naming, duplication, beginner-friendly improvements, and Unity practices.
- Explain causes before fixes.
- Do not treat tutorial answers as automatically ideal; analyze product/game requirements.

### Check Categories

- Code issues.
- Unity scene/Inspector/Prefab issues.
- Runtime verification issues.
- Topic-specific artifacts.
- Remind the user to stop Play Mode/save scenes when disk state may be stale.
- Check `.meta` GUIDs after Unity asset moves.

### Learning Records

Recommend:

- `README.md`
- `LearningProgress.md`
- `Notes/`
- `Screenshots/` optional
- additional topic artifacts such as `Samples/`, `TestData/`, or diagrams when useful

Rules:

- Update progress after every lesson/stage.
- Record misunderstandings and reusable knowledge in Notes.
- Prefer append-only learning history.
- Update resolved issues so notes do not preserve stale conclusions.
- Mark incomplete validation as “学习中” or “待复盘”.
- Record what was learned, what was wrong, why, how it was verified, boundaries, and next step.

### Git and GitHub

- Never auto-commit or auto-push.
- When push is requested, summarize first, then execute.
- Default commit messages to Chinese.
- Verify local/remote sync after push.
- Do not include unrelated/generated files.
- Never rewrite history or force push without explicit request; use `--force-with-lease` when authorized.
- At course completion, optionally create a Chinese GitHub Release with a semantic tag and verified artifact.
- Verify Release attachment and body encoding; send PowerShell API JSON as UTF-8 bytes.

### Response Style

- Use Chinese.
- Explain why.
- Connect explanations to actual Unity scenes/assets/artifacts.
- Avoid overengineering.
- Give direct feedback on good and bad habits.
- End reviews with one smallest next action.

### Final Emphasis

- This is a learning project.
- Do not write full features, modify runtime code, commit, push, or mark work complete unless authorized/verified.
- The objective is understanding, debugging habits, durable records, and a real verifiable portfolio repository.

## Recommended README Goals

Generate topic-specific goals plus these stable goals:

- understand the subsystem's purpose, limits, and common APIs;
- complete exercises and cross-run/cross-scene validation when relevant;
- identify real-project boundaries and failure modes;
- produce a reusable final artifact;
- complete final review, GitHub documentation, and optional Release.

