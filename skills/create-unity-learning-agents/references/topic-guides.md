# Unity Tutorial Topic Guides

Select only relevant checks. Combine guides when necessary.

## JSON / Persistence / Save Systems

- Serializer choice and limitations: `JsonUtility`, Newtonsoft.Json, custom serializers.
- Fields/properties/private fields, Dictionary, polymorphism, interfaces, Unity object references.
- `[Serializable]`, encoding, JSON shape, version compatibility.
- `Application.persistentDataPath`, directory creation, file lifecycle, UTF-8.
- Same-run versus cross-run loading.
- Missing, empty, corrupted, manually edited, or old-version files.
- Atomic writes, backup/recovery, save frequency, encryption/checksum, server authority.
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
- Prefab versus scene instance changes.

## Input / New Input System

- Action maps, bindings, generated class, enabled/disabled state.
- Callback lifecycle, performed/canceled behavior, device differences.
- Meaningful action naming and rebinding.
- Verify expected event values and active action map.

## Physics / Character Control

- `Update` versus `FixedUpdate`, Rigidbody ownership, collider setup.
- Force modes, grounded checks, collision layers, triggers.
- Inspector values and runtime velocities/contacts.
- Frame-rate independence and slopes/edges.

## Animation / Animator

- Animator parameters, transitions, exit time, layers, blend trees.
- Animation events, root motion, state names/hashes.
- Verify current state and parameters during Play Mode.

## Prefabs / Scenes / Components

- Asset versus scene instance, overrides, nested Prefabs.
- Missing references, disabled objects/components, lifecycle timing.
- Scene saved state and `.meta` GUID preservation.

## Addressables / Resources / Asset Management

- Address/key correctness, groups, labels, build/update flow.
- Async operation completion, release/unload, reference counts.
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

## Packaging / Course Completion

- Organize reusable code separately from tests/tutorial scripts.
- Preserve `.meta` GUIDs during moves.
- Verify exported `.unitypackage` contents.
- Keep generated artifacts out of Git unless intentionally distributed.
- Create final summary, known-boundary list, semantic tag, and optional Release.

