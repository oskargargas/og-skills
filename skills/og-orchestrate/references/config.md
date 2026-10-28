# The `orchestrate` section of `.ai/agentic.config.json`

The skill reads this section. A project edits it to change providers, models or reasoning levels. [`templates/orchestrate.json`](../templates/orchestrate.json) is the complete example and the starting point.

| Key                                    | Holds                                                                                                                                              |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `reasoning`                            | The default reasoning level, a value every listed model accepts, such as `high`.                                                                   |
| `families.<family>.providerInstanceId` | The provider instance that runs this family in T3 Code, as `orchestrator_capabilities` lists it.                                                   |
| `families.<family>.reasoningOption`    | The name of the model option that carries the reasoning level for this family in T3 Code: `effort` for Claude, `reasoningEffort` for Codex.        |
| `tiers.<tier>.<family>.model`          | The model id for this tier in this family, as the provider's catalog spells it.                                                                    |
| `tiers.<tier>.<family>.reasoning`      | Optional. Overrides `reasoning` for this one entry.                                                                                                |
| `tiers.<tier>.<family>.opencodeModel`  | Optional. The `provider/model` id OpenCode uses for the same model, without a `#variant`. Required for a family the project runs through OpenCode.  |

Rules:

- `reasoning` applies to every operation: the running session and every subagent. A tier entry's own `reasoning` overrides it for that entry.
- The three tiers are `worker`, `supervisor` and `expert`. Every tier names a model in every family the project uses.
- A family key is the vendor's line (`claude`, `codex`), not a harness. Harnesses are in [`harnesses.md`](harnesses.md).
- A model id that the catalog no longer lists fails step 6 of the skill. Fix the config, not the skill.

## Other keys the skill reads

| Key                   | Holds                                                                                              |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| `paths.wiki`          | The wiki folder, relative to the repository root, such as `.ai/wiki`.                              |
| `validation.commands` | The full validation gate: an array of shell commands run in order at the final gate, all must pass. |

Other skills may share these keys. Add a missing key next to the existing ones and leave the rest of the file as it is.
