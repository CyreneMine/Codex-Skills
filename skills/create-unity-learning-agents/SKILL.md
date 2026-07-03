---
name: create-unity-learning-agents
description: Create or update a tailored AGENTS.md for a long-running Unity tutorial or learning repository. Use when the user starts a new Unity course/project, wants the same mentoring/documentation/Git workflow reused across tutorial series, asks to generate project collaboration rules, or wants an existing AGENTS.md adapted to a new topic such as JSON persistence, UI, animation, input, physics, networking, asset management, or gameplay systems.
---

# Create Unity Learning AGENTS

Generate a project-specific `AGENTS.md` that turns a Unity tutorial repository into a durable learning workflow.

## Workflow

1. Inspect the current project before writing:
   - Read an existing `AGENTS.md` or similarly named rule file when present.
   - Inspect `README.md`, learning-progress files, top-level directories, Unity version, Git status, and representative scripts.
   - Use the user's stated course topic and directory/course list as the primary scope.
2. Determine the output:
   - Default to `<project-root>/AGENTS.md`.
   - If the user explicitly requests another filename, use it.
   - Do not overwrite an existing `AGENTS.md` blindly; preserve useful project-specific rules and adapt them.
3. Build the document from [core-template.md](references/core-template.md).
4. Add a concise topic-specific section using [topic-guides.md](references/topic-guides.md).
5. Tailor concrete names:
   - Replace generic topic names with the actual tutorial topic.
   - Mention real expected artifacts and validation methods.
   - Keep unknown details generic or mark them as future decisions.
6. Write the file directly unless the user asks for a draft only.
7. Validate the result:
   - Ensure it says not to modify code without explicit permission.
   - Ensure each completed lesson updates learning records.
   - Ensure Git commit/push is opt-in and commit messages default to Chinese.
   - Ensure checks distinguish code, Unity scene, runtime, and topic-specific artifacts.
   - Ensure unfinished validation cannot be recorded as completed.
8. Do not commit or push unless explicitly requested.

## Generation Principles

- Write in Chinese unless the user requests otherwise.
- Preserve the user's mentor-style workflow: inspect real files, explain causes, identify good and bad habits, and give one smallest next step.
- Prefer a practical document of roughly 180-320 lines. Remove sections that are irrelevant to the project.
- Keep course-specific checks concrete, but avoid prematurely requiring advanced architecture.
- Treat documentation files as editable by default; treat code, scenes, Prefabs, ProjectSettings, and Packages as protected unless explicitly allowed.
- Include final-course GitHub practices: Chinese commit messages, optional Release, artifact verification, and UTF-8 Release body handling.

## Topic Selection

Use the closest guide in [topic-guides.md](references/topic-guides.md). Combine guides when the course spans multiple topics.

If the topic is new or absent, derive checks around:

- the core API or engine subsystem;
- real artifacts produced by the feature;
- Unity scene/Inspector configuration;
- same-run versus cross-run or cross-scene validation;
- common lifecycle, reference, serialization, platform, and performance boundaries;
- expected final reusable artifact.

## Output Summary

After writing, briefly report:

- created/updated path;
- selected topic-specific checks;
- whether existing rules were preserved;
- that the user should invoke this skill again for the next tutorial project.

