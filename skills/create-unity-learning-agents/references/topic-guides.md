# Unity Tutorial Topic Guides

Select only relevant checks. Combine guides when necessary.

## JSON / Persistence / Save Systems

- Serializer choice and limitations: `JsonUtility`, Newtonsoft.Json, custom serializers.
- Fields/properties/private fields, Dictionary, polymorphism, interfaces, Unity object references.
- `[Serializable]`, encoding, JSON shape, version compatibility.
- `Application.persistentDataPath`, directory creation, file lifecycle, UTF-8.
- Same-run versus cross-run loading.
- Missing, empty, corrupted, manually edited, or old-version files.
- Save timing and defaults versus mutable saves. Consider atomic writes, recovery, migration, or trust boundaries only when they are relevant to the requested course scope.
- Inspect actual JSON files, not Console output alone.

## PlayerPrefs

- Supported primitive types, key naming, overwrite behavior, `Save()` timing.
- Lists/Dictionaries/custom data decomposition.
- Same-run versus cross-run verification and platform storage paths.
- Client-local security boundary and stale keys.

## UI / UGUI

- Canvas render mode, anchors, pivots, layout groups, scaling, safe area.
- Inspector references, EventSystem, raycast blocking, interactable state.
- Different resolutions/aspect ratios and localization text overflow.
- Prefab versus scene instance changes, Prefab Mode preview environment versus runtime Canvas.
- CanvasGroup alpha, object lifetime, raycast blocking, and hide callbacks are separate states.
- Scaled versus unscaled UI time when gameplay is paused; show/hide and input after returning.

## Input / New Input System

- Action maps, bindings, generated class, enabled/disabled state.
- Callback lifecycle, performed/canceled behavior, device differences.
- Meaningful action naming and rebinding.
- Verify expected event values and active action map.
- Inspect the actual input implementation and Active Input Handling setting; an installed Input System package does not mean scripts use Action maps.

## Physics / Character Control

- `Update` versus `FixedUpdate`, Rigidbody ownership, collider setup.
- Force modes, grounded checks, collision layers, triggers.
- Inspector values and runtime velocities/contacts.
- Frame-rate independence and slopes/edges.

## Animation / Animator

- Animator parameters, transitions, exit time, layers, blend trees.
- Animation events, root motion, state names/hashes.
- Shared base controller versus Override Controller, per-variant clip/event mapping, and reused Prefab dependencies.
- Verify current state and parameters during Play Mode.

## Prefabs / Scenes / Components

- Asset versus scene instance, overrides, nested Prefabs.
- Missing references, disabled objects/components, lifecycle timing.
- Scene saved state and `.meta` GUID preservation.

## Addressables / Resources / Asset Management

- Address/key correctness, groups, labels, build/update flow.
- Async operation completion, release/unload, reference counts.
- Resource path case and imported type; file existence alone does not prove a Sprite or other expected asset can be loaded.
- Editor simulation versus built player behavior.
- Artifact size and platform build verification.

## Networking / Multiplayer

- Client/server authority, ownership, synchronization direction.
- Host/client differences, disconnect/reconnect, latency.
- Never trust client-only authoritative values.
- Verify with multiple instances, not a single local path.

## Data Structures / Reflection / Generic Managers

- Public/private fields, properties, generic arguments, assignability.
- `Activator.CreateInstance` constraints and parameterless constructors.
- Nulls, unsupported types, recursion, circular references.
- Save/load symmetry and concrete versus interface types.

## Gameplay Systems

- Expected behavior versus actual behavior.
- Lifecycle, object ownership, state transitions, reset/re-entry behavior.
- Test repeated actions, edge cases, scene reload, and object destruction.
- Scheduled/coroutine work versus blocking execution; wave generation, alive counts, reset, and duplicate entry.
- Physics query origin, shape/range, layers, target selection, and damage-target consistency.
- Death animation versus logical death, attack cooldown scope, and game-over input/time state.

## Data-Driven Gameplay / Spreadsheet Configuration

- Inspect the user's sample, field schema, IDs, relationships, source resource hierarchy, and requested target count.
- Match spreadsheet, JSON, and C# names/types; preserve unrelated cells, formulas, formatting, and source assets.
- Validate resource keys, valid upgrade links, level/category combinations, and loader index-versus-ID assumptions.
- Record Agent-generated rows/configuration separately from user-authored examples; static data checks are not runtime coverage.

## Navigation / Multi-Module Practice

- NavMesh references, Agent settings, actual reachable paths, stopping distance, and target lifetime.
- Initialization order across UI, player, camera, protection zone, enemies, and level counters.
- Scene selection data versus loaded scene, repeated button clicks, async callback lifetime, and reset after return.
- Layer number versus layer bitmask, shared preview/gameplay Prefab use, and world position versus rotated direction.

## Packaging / Course Completion

- Organize reusable code separately from tests/tutorial scripts.
- Preserve `.meta` GUIDs during moves.
- Verify exported `.unitypackage` contents.
- Keep generated artifacts out of Git unless intentionally distributed.
- Distinguish compilation, editor behavior, the actual built-player run, and user-provided evidence.
- Create the requested summary and known-boundary list. Tags and Releases are optional and require explicit authorization.
- For multiple Unity roots, authorized batch work, or project presentation, see [project-lifecycle.md](project-lifecycle.md).
