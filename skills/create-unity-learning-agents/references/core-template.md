# Core AGENTS Template

Use this as a source for project-specific rules, not a document to copy verbatim. Select the necessary sections and keep detailed current progress in the progress file rather than expanding AGENTS indefinitely.

## Project Positioning and Workspace

- Name the tutorial/topic and its actual learning goal: understanding, retained practice, debugging habits, and a verifiable project.
- State the repository root, active Unity project, and any archived/reference projects. Preserve an established theory/practice split; do not require one for every course.
- Record the verified Unity version and relevant package versions. Recheck them when explaining compatibility issues; do not assume a particular render pipeline or input API.
- Put cross-project management documents at the repository root when that matches the workspace. Default new work to the active Unity root.
- Keep course numbering aligned with the real course list. Distinguish watched content, an omitted exercise, and an entirely deferred topic.

## Codex Responsibilities

- Inspect real scripts, scenes, Prefabs, Inspector references, data, and learning records before conclusions.
- Explain Unity/C#/API principles and the root cause of a problem.
- Review against the exercise goal; distinguish correct behavior, requirement fit, maintainability, and optional production improvements.
- Compare tutorial and learner implementations without treating the tutorial as the only valid approach.
- Maintain the agreed README/progress/notes workflow and Git only when requested.

## Modification Boundary

- Documentation may be updated within the agreed task. Scripts, scenes, Prefabs, materials, animations/controllers, ProjectSettings, Packages, and other runtime-affecting files require explicit authorization.
- Respect an existing read-only project boundary. A request to review or update progress does not authorize rewriting an exercise.
- Examples of authorization include “帮我改”, “直接修复”, or a specific request to configure named Prefabs. Existing authorization applies throughout that scope; do not require another confirmation for each file.
- Without authorization, report location, cause, consequence, and a minimal proposed change. Give precise Inspector object/component/field values when appropriate.
- When repetitive configuration is authorized, preserve the user's sample and verify the resulting references. Record what the user did and what the Agent did separately.

## Before a Lesson or Review

- Read progress, confirm the lesson number and active project, and inspect Git status to separate user edits from generated output.
- For scene-dependent findings, check saved disk state versus current Play Mode/editor state using available evidence. State when live state cannot be inspected.
- For resource-dependent findings, verify paths, importer type, `.meta` GUIDs, and whether the user saved or applied Prefab overrides.
- Do not alter a user's existing changes just to obtain a clean working tree.

## Review and Validation

- At exercise start, record the goal and progress. Respect a request to attempt it independently without hints; review submitted work when asked instead of preemptively supplying the solution.
- Restate the current exercise goal, inspect actual artifacts, then explain findings and the smallest validation step.
- Separate code, scene/Inspector, resource/data, and runtime issues.
- Label the basis of a conclusion: static inspection, compilation, Agent-observed editor/player behavior, or user-reported validation.
- Compilation and logs alone do not prove behavior. Editor behavior does not prove the standalone build. Same-process reload does not prove cross-process persistence.
- Choose tests relevant to the feature: repeated entry/reset, destruction, animation transitions, physics range/layers, async completion, save reload, or another aspect ratio when layout changes.
- If the user explicitly chooses Scene-view/editor triggering for a scoped exercise, assess that scope and document the difference from a Game-view input flow.
- Required checks must pass before marking that scope completed. Keep unrelated optional coverage and accepted limitations visible without treating them as fresh blockers.
- Do not claim every configuration was tested because a representative scene or screenshot worked.

## Learning Records

Adapt existing names rather than creating duplicate tracking systems:

- `README.md`: positioning, quick navigation, environment, and eventual project overview.
- `LearningProgress.md`: real lesson list, state, and next step.
- `Notes/`: misconceptions, root causes, alternatives, verification, and reusable conclusions.
- `CODEX_MEMORY.md`, if used: stable workspace conventions and current handover facts; not hidden personal memory or credentials.
- `Screenshots/`, if useful: requested Inspector/runtime evidence and its index.

Record after each lesson/stage: what was learned or implemented, who did which work, the error and cause, how it was verified, remaining boundaries, and next step.

Use the project's status vocabulary, normally `未开始`, `学习中`, `待复盘`, `已完成`, `已跳过`. Video playback alone does not complete an exercise. Record guidance/answer use honestly.

Preserve learning history. When a conclusion changes, mark the earlier record as a dated snapshot and update the current summary; do not leave “not built” as current after a build was demonstrated. Preserve reasons for skipped or deferred exercises.

## Resources and Repository Boundary

- Exclude Unity-generated folders in every Unity root: Library, Temp, Logs, obj, UserSettings, builds, and confirmed recovery backups.
- Exclude local teaching/third-party assets according to the user's actual resource policy. Keep authored code/data and permitted project files distinct from imported models, audio, textures, plugins, and their metadata.
- Scope ignore patterns to actual paths. Do not ignore all images when requested gameplay screenshots belong in documentation.
- `.gitignore` does not remove already tracked files. Inspect the index and outgoing changes; do not silently rewrite history to remove old assets.
- Moving Unity assets requires their `.meta` files and a reference check. A request for structure-only changes does not authorize editing content; do not relocate caches unnecessarily or delete user-owned source.
- Explain when an asset-excluded source checkout requires separately supplied local resources to run.

## Git and GitHub

- Commit/push/tag/Release only on explicit request. Summarize the intended scope first; messages default to Chinese.
- Inspect status, relevant diffs, the staged diff, and excluded resources. Stage reviewed paths rather than using `git add .`.
- If the user requests batches, group coherent data, gameplay, scene/configuration, and documentation changes with dependencies in mind. Preserve unrelated edits and report what remains local.
- Push to the actual configured remote/branch. Compare HEAD with its remote-tracking ref and inspect status afterward; synchronized commits do not imply a clean working tree.
- Never force-push or rewrite history without explicit authorization; prefer `--force-with-lease` if authorized.
- Use Git for local history and push. Use an available authenticated GitHub CLI/connector for repository/PR/Issue/Release operations when needed. Check actual authentication and capabilities rather than baking in a machine account or protocol.
- A CLI authentication failure does not invalidate another working Git transport. Do not change global Git configuration, credentials, PATH, or remote URLs merely to use a tool; never print tokens or private keys.
- At course end, tags/Release are optional and separately authorized. Verify the actual artifact, UTF-8 body, and attachment contents before reporting publication success.

## Demo Completion and Portfolio

When the user requests a summary or presentation, use the completed project rather than promises:

- Summarize the playable flow, each implemented module, validation evidence, known limits, and reusable pieces.
- Lead README with a short project/value/contribution overview and a representative actual screenshot when useful; keep detailed course records below.
- Distinguish learner-authored logic, Agent-assisted work, and tutorial/third-party assets. Do not invent originality, performance numbers, commercial launch, or a framework that was not built.
- See [project-lifecycle.md](project-lifecycle.md) for conditional batch-configuration, build evidence, screenshot, and portfolio procedures.

## Response Style

- Use Chinese, lead with the conclusion, and explain causes through actual project artifacts.
- Give direct feedback on good and bad habits without imposing advanced architecture on an early exercise.
- After a review, provide one smallest actionable next step; do not reopen an explicitly accepted limitation without new relevant evidence.
