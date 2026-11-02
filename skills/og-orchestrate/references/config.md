# The `orchestrate` section of `.ai/agentic.config.json`

Edit this section to change providers, models or reasoning levels. [`templates/orchestrate.json`](../templates/orchestrate.json) is the complete example and the starting point.

| Key                                    | Holds                                                                                                                                              |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `reasoning`                            | The default reasoning level, a value every listed model accepts, such as `high`.                                                                   |
| `families.<family>.providerInstanceId` | The provider instance that runs this family in T3 Code, as `orchestrator_capabilities` lists it.                                                   |
| `families.<family>.reasoningOption`    | The name of the model option that carries the reasoning level for this family in T3 Code: `effort` for Claude, `reasoningEffort` for Codex.        |
| `tiers.<tier>.<family>.model`          | The model id for this tier in this family, as the provider's catalog spells it.                                                                    |
| `tiers.<tier>.<family>.reasoning`      | Optional. Overrides `reasoning` for this one entry.                                                                                                |
| `tiers.<tier>.<family>.opencodeModel`  | Optional. The `provider/model` id OpenCode uses for the same model, without a `#variant`. Required for a family the project runs through OpenCode. |

Rules:

- `reasoning` applies to every operation: the running session and every subagent. A tier entry's own `reasoning` overrides it for that entry.
- The three tiers are `worker`, `supervisor` and `expert`. Every tier names a model in every family the project uses.
- A family key is the vendor's line (`claude`, `codex`), not a harness. Harnesses are in [`harnesses.md`](harnesses.md).
- A model id that the catalog no longer lists fails step 6 of the skill. Fix the config, not the skill.

## Process

`orchestrate.process` controls implementation batching, review rounds and provider fallback. Propose missing values with the plan; the template supplies starting values, not hardcoded limits.

| Key                         | Holds                                                                                                                  |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `singleImplementerMaxLines` | Maximum estimated production lines changed, excluding tests and documents, for supervisor-tier implementation without workers. |
| `finalReviewers`            | Positive integer: reviewers reviewing the whole implementation diff in parallel.                                               |
| `recheckRounds`             | Non-negative integer: maximum re-check rounds for Critical and High fixes before taking an open finding to the user.                         |
| `maxProviderWaitMinutes`    | Non-negative number: maximum wait for a provider out of quota before a permitted fallback; `0` means immediate fallback.                            |

## Other keys the skill reads

| Key                                               | Holds                                                                                                     |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `engine.stepReview`                               | Optional integration: if a pipeline engine supports this key, use `final` for the single final review. Otherwise ignore it.             |
| `validation.commands`                             | The full validation gate: an array of shell commands run in order at the final gate, all must pass.       |

Memory paths and record formats come from the project's agent instructions, installed by `og-memory setup`; this skill does not define them.

Other skills may share these keys. Add a missing key next to the existing ones and leave the rest of the file as it is.
