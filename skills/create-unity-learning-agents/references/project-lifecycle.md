# Project Lifecycle: Learning, Practice, and Demo Handover

Read only the sections needed for the requested project rules. These are conditional workflows, not permission to perform every operation or a universal acceptance checklist.

## 1. Theory-to-Practice Workspaces

For a course with separate theory and practice projects:

- Discover each Unity root before naming it. Record which is active and which is archived/read-only; keep repository-wide documents outside both.
- Keep the older project available for reference, and apply new gameplay work to the active project. A directory restructure needs its own authorization.
- For authorized structure-only moves, preserve Assets, Packages, ProjectSettings, authored support files, and corresponding metadata. Move with `git mv` or an equivalent safe operation; inspect GUID references afterward.
- Inspect actual generated folders before excluding or removing them. Do not discard user source or treat every unfamiliar directory as a cache.
- Keep .gitignore scoped across all Unity roots. Explain the correct Unity Hub project path after a move; the repository root itself may not be a Unity project.
- Record course numbering changes, explicit topic deferrals, and exercise omissions without changing “watched” into “independently implemented”.

## 2. Authorized Repetitive Configuration

Use when the user asks for batch setup based on a manually prepared example, such as Animator overrides, Prefab references, or spreadsheet data.

### Establish the rule from real artifacts

- Inspect the user's saved/applied baseline, hierarchy, public/serialized fields, source clips, metadata, and data columns before generating more entries.
- Confirm numbering and the exact target set from files, not an ambiguous message. Ask only for a rule that cannot be inferred from the provided example.
- Derive variants from the working original when appropriate; do not duplicate a full Animator graph when an Override Controller preserves the intended shared behavior.
- Check shared Prefab use: adding player logic to a preview role can introduce dependencies on a game-only UI or manager. Explain the dependency and propose the smallest change within authorization.

### Verify the result

- For animation: override clip mapping, base controller, state parameters, animation-event receiver, and Prefab binding.
- For Prefabs: object identity, parent hierarchy, local coordinates, serialized field references, GUIDs, and enabled state.
- For data: field names/types, unique IDs, valid upgrade/relationship IDs, row counts, and resource path spelling/case. Check the table, JSON, and C# class when all are part of the request.
- Preserve formulas, formatting, and unrelated cells when editing a workbook. A JSON conversion is not a general-purpose export tool unless such a tool was actually implemented.
- Resource paths must resolve to the expected imported type, not merely to an existing filename. For example, an unsliced Multiple texture is different from a loadable Single Sprite.
- Distinguish successful writes/static mapping checks from Unity import and actual animation/gameplay execution.

### Keep an attribution record

A useful record states: the user made the original and first variant; the Agent filled the identified remaining variants; both followed a specified mapping rule; static and runtime checks are listed separately.

Record configuration counts as configuration counts. A model/animation Cartesian product is not the same number of independently designed AI behaviors. Use “Agent-assisted” honestly; do not describe automated steps as manual work or invent a productivity percentage.

## 3. Evidence and Completion

Keep the source and scope of each result:

| Evidence | What it supports | What it does not establish alone |
| --- | --- | --- |
| Static file/reference inspection | Paths, fields, layers, links, saved configuration | Successful scene behavior |
| C# compilation | No compiler errors in the selected target | Player build or gameplay acceptance |
| Editor/Play Mode observation | The observed interaction in that editor state | Standalone/platform behavior |
| Agent-operated built player | The actual exercised menu/battle/return sequence | Every scene, character, or data combination |
| User report or supplied screenshot | The reported outcome and visible state | Exhaustive coverage, timing, sound, or performance |
| Same-process reward/re-entry check | That reward flow or reset in this run | Cross-process persistence or clean first-run behavior |

- Complete a lesson when its required goal and necessary checks are satisfied. Keep relevant optional coverage, accepted limitations, and untested combinations separate.
- Do not reset old progress merely because a new optional test was proposed. Do not close every old pending item from one successful package or screenshot.
- When the user accepts a learning-only limitation, record it and stop treating it as an unresolved mandatory repair. A new problem may be reviewed on its own evidence.
- Date old snapshots and correct the current summary. A changed wave count or parameter can explain differences between old notes and a later package.

## 4. Authorized Git Batches

- Verify the actual repository, branch, remote, status, and existing staged changes. Scope authorization to this repository; do not mix another project's edits into the push.
- Inspect generated folders and local teaching resources, including their `.meta` files. Exclude confirmed local-only imports, build output, and recovery backups without deleting them.
- Inspect outgoing changes as well as ignore rules: ignored-but-tracked files are still tracked. Do not silently untrack authored managers or rewrite old history.
- Separate coherent batches where useful: data/exclusions; gameplay/UI logic; scenes/Prefab configuration/build settings; documentation/screenshots. This is an example, not a required four-commit structure.
- Stage exact reviewed paths and inspect each staged diff. Keep Unity-generated serialization formatting distinct from logic changes; do not rewrite protected code solely to silence whitespace checks.
- Leave unrelated local configuration edits untouched and outside the commit; name them in the result. A successful push may leave those edits in the working tree.
- If the push fails because the remote advanced, inspect divergence and preserve both histories; never force-push to bypass it. If authentication fails, diagnose the transport without printing secrets or changing user-wide configuration.
- After pushing, verify local HEAD against the intended remote-tracking ref and report the commits actually sent, including earlier pending commits if relevant.

## 5. Finished Demo and Portfolio

Use only when the user requests project presentation, screenshots, a summary, or career material.

### Gather actual evidence

- Locate the real build and launch it through available supported tools. Do not equate a generated project file or compile command with packaging.
- Avoid changing game code or overwriting saves to make a screenshot. If ordinary play can award currency or otherwise alter progress, record that effect rather than calling the run read-only.
- Use original runtime screenshots; preserve watermarks. If overlays obstruct the frame, ask the user to hide them rather than modifying unrelated desktop state without authorization.
- Accept user-supplied victory/build/upgrade frames when those actions are difficult to capture. Clearly distinguish user-provided and Agent-captured images.
- Store images in a requested/project-appropriate documentation folder. Give each a meaningful filename and index with source, depicted feature, and relevant limitations. Preserve supplied originals; if copying them, hashes can confirm identical bytes.
- Keep model/audio/texture source assets and build binaries excluded according to the user's policy. Gameplay screenshots are a separate documented artifact, not a reason to add all imported resources.

### Write for the intended reader

- README top: project name/type, one-sentence gameplay, delivered platform/status, two or three concrete capabilities, personal contribution, and a representative screenshot when useful. Put course tables and detailed verification below.
- Project overview: playable flow, actual systems, implementation choices, evidence links, and known boundaries.
- Module summary: actual UI, data, scenes, camera, player, enemies, level management, and towers only where implemented. For each, state responsibility, main mechanism, a useful debugging lesson, and validation scope.
- Resume/interview wording: concrete responsibilities and outcomes, tutorial basis, third-party art, and Agent contribution. Use counts only when they clarify scope; never invent commercial release, performance gains, original art, or advanced systems not in the code.
- Prefer one overview and a focused module document over automatically producing many redundant files. Honor existing documentation names and the user's desired format.
- Verify relative links and image files. Update README/progress/workspace handover so current status agrees with the actual package and summary.
- Release, public binaries, and external messages require their own authorization; a screenshot/summary request alone does not grant them.
