---
name: create-unity-learning-agents
description: Create or update Chinese AGENTS.md collaboration rules for Unity tutorial and learning repositories. Use when starting a course, adapting an existing learning workflow to another project, or carrying lessons from practice into project rules, including multiple Unity projects and demo handover.
---

# Create Unity Learning AGENTS

Turn the project's actual learning workflow into maintainable, project-specific `AGENTS.md` rules.

## Workflow

1. Inspect before writing:
   - Read existing collaboration rules, README, learning progress, notes, and workspace memory when present.
   - Identify the Git root and each Unity root using real directories, `ProjectVersion.txt`, package manifests, representative scripts, and Git status.
   - Distinguish an archived theory project from the active practice project when that split exists. Do not assume the repository root is a Unity project.
   - Use the user's course list, current progress, accepted limitations, and existing authorization as the primary scope. Do not infer titles, completion, or missing runtime results.
2. Choose the output:
   - Default to `<repository-root>/AGENTS.md`; honor an explicit alternative.
   - Preserve useful existing rules, especially modification boundaries, read-only projects, resource exclusions, and learning decisions.
   - This skill writes collaboration rules. Reorganizing Unity assets, configuring Prefabs, generating data, building the game, or publishing a portfolio requires the corresponding user request.
3. Read [core-template.md](references/core-template.md) as the shared source, then select relevant sections of [topic-guides.md](references/topic-guides.md).
4. For theory-to-practice transitions, repetitive Agent-assisted work, authorized Git batches, or a finished Demo, read [project-lifecycle.md](references/project-lifecycle.md). Include only the sections that apply.
5. Tailor the rules:
   - Use actual project names, paths, versions, course numbers, artifacts, and validation methods.
   - Mark unknowns as unknown; do not copy an old project's machine paths, repository owner, authentication state, or tutorial-specific counts.
   - Resolve obsolete current-state claims while preserving historical snapshots with their date and scope.
6. Write the file directly unless the user requests a draft. Update related learning documents only within the user's agreed scope; do not generate every possible deliverable automatically.
7. Validate:
   - Code and Unity assets remain protected unless already authorized; do not ask again for permission the user has already granted for the same scope.
   - Lesson records distinguish independent work, tutorial guidance, Agent configuration, static inspection, user-reported results, and direct runtime observation.
   - Required validation is complete before marking the corresponding scope completed. Optional coverage gaps stay explicit without blocking unrelated completed work.
   - Git remains opt-in, messages default to Chinese, and project-specific resource exclusions are preserved.
   - Paths, course numbers, document links, and the active-project designation are consistent.
8. Commit, push, tag, or publish only when explicitly requested. Honor the actual repository's branch and workflow.

## Generation Principles

- Write generated project rules in Chinese unless requested otherwise.
- Preserve mentor-style collaboration: inspect real artifacts, explain causes, separate requirement failures from optional improvements, and give one smallest next step.
- Keep the document proportional to the course. Remove irrelevant sections rather than enforcing a fixed length or advanced architecture.
- Documentation is editable within the agreed learning workflow. Treat scripts, scenes, Prefabs, controllers, ProjectSettings, and Packages as protected runtime artifacts.
- Respect explicit choices such as deferring a topic, using an alternative implementation, manually triggering an editor test, or accepting a known limitation. Record the scope and reason instead of repeatedly reopening the decision.
- Do not equate compilation with runtime correctness, video completion with exercise completion, screenshots with exhaustive testing, or configuration counts with independent behaviors.
- Carry forward reusable decision rules, not every past bug or a fixed list of project-specific fixes.

## Topic Selection

Use the closest topic guide, combining only relevant checks. For an absent topic, derive checks from:

- the subsystem and actual produced artifacts;
- scene, Inspector, serialization, and lifecycle dependencies;
- same-run, scene re-entry, cross-process, or built-player behavior as relevant;
- evidence needed for this lesson's goal and separate optional boundaries;
- the useful final reusable artifact.

## Output Summary

Briefly report the updated path, preserved rules, added checks, and remaining unknowns. Mention local edits or exclusions left outside any requested commit. For another tutorial, the user can invoke this skill again to adapt the rules; do not imply the current project's rules apply unchanged.
