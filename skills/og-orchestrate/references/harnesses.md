# Spawning a tier in each harness

How to start a subagent of a given tier, family and reasoning level, and how to arm the fallback wake-up that the Waiting section of the skill requires. The ids come from `orchestrate` in `.ai/agentic.config.json`; this file only says where to put them. After every spawn, compare what the harness reports with the brief.

## Pick the route

1. The `t3-code` tools are present (names may carry an `mcp__t3-code__` prefix): use T3 Code for every subagent, own family included. Every spawn under this skill requests a reasoning option, and T3's contract says native subagent tools cannot reliably apply model options.
2. Otherwise read the section for the harness you run in. Each section says which families it reaches. When the family the skill picked is out of reach, use the own-family model and report the skipped cross-family verification.

## T3 Code

Reaches every family that has a provider instance with `canRunChildTask` true.

1. Call `orchestrator_capabilities` once per session. Confirm each configured `providerInstanceId` and model id is listed and `canRunChildTask` is true. Pass `search` for a model the short list omits. Its `inheritedModel` and `inheritedOptions` show the running session's own tier and level for step 1 of the skill.
2. Call `delegate_task` with the brief as `task` and `target: { "providerInstanceId": <family.providerInstanceId>, "model": <tier.family.model>, "options": { <family.reasoningOption>: <reasoning> } }`. Use `mode: "async"` for long work. Give each run its own `clientRequestId`, keep it when you retry the same run, and keep the returned `taskId` for `task_status` and `task_cancel`.
3. Read `providerInstanceId`, `model` and `options` in the result. A mismatch means the option name or model id in the config is wrong. Stop and fix the config.
4. Start a new `delegate_task` for every review round, with the brief, the earlier findings and the responses in the task text.
5. Use `isolation: "worktree"` when the child must not see uncommitted edits, such as a review of a commit range. The worktree starts from the parent's last commit and gets the project's setup. The brief tells the child to check its prerequisites, such as installed dependencies, before it runs checks.
6. Wake-up: while any delegated task runs, keep one `schedule_task` bound to this thread, with `schedule: { "type": "interval", "everyMs": 1800000 }` and a prompt that names the running `taskId`s. Delete it with `delete_scheduled_task` when nothing runs. A task is done only when `task_status` shows `workState: "result_available"` and `hasPendingChildRuns: false`; a completed turn can still have work running behind it. `summary` keeps the first result; read a later turn's result in `latestTerminalSummary`.

## Claude Code, native `Agent` tool

Reaches the `claude` family. The `model` parameter of the `Agent` tool accepts aliases only (`haiku`, `opus`, `fable`), and an alias resolves to the vendor's current version, not to the configured id. The tiers are project agents instead.

1. The project keeps [`templates/claude/`](../templates/claude/) installed as `.claude/agents/worker.md`, `supervisor.md` and `expert.md`. Each file carries the configured full model id in `model` and the reasoning level in `effort`. When the config changes, change the files.
2. Spawn with `subagent_type` set to the tier name and the brief as the prompt. Leave `model` and `effort` off the call; a value on the call replaces the file's.
3. Read `resolvedModel` from the result. The level cannot be read back, and `CLAUDE_CODE_EFFORT_LEVEL` in the environment wins over the file, so the report names the level the file requested.
4. Continue the same agent with `SendMessage` instead of starting a second one. A background subagent dies with the session, so wait for it before the session ends.
5. `isolation: "worktree"` on the `Agent` tool branches from the default branch, not from this session's commit. For a review of a branch, give the child the exact ref to check out, or leave isolation off.
6. Wake-up: start a background `Bash` command that exits when the work shows progress or after 30 minutes, whichever comes first. For example, poll `git ls-remote origin <branch>` until the head moves. Its exit starts a new turn.

The running session's own model and level: the session banner or `/status`, and `CLAUDE_CODE_EFFORT_LEVEL` when set.

## Codex CLI, native `spawn_agent`

Reaches the `codex` family. Read the tool's schema first; it differs by version and configuration.

- The schema exposes `model` and `reasoning_effort`: pass the configured values on the call.
- The schema exposes `agent_type`: use the roles in [`templates/codex/`](../templates/codex/). Copy the three role files to `.codex/agents/`. Add the `[agents.<tier>]` tables to `.codex/config.toml`. Set each role's `model` and `model_reasoning_effort` from the config. Spawn with `agent_type` set to the tier. Check the files against the installed version's config schema before relying on them.
- The schema exposes neither: set `agents.default_subagent_model` and `agents.default_subagent_reasoning_effort` in `.codex/config.toml` to the tier you are about to spawn. One tier per session is the limit of that route; say so in the report.

The running session's own model and level: `model` and `model_reasoning_effort` in the effective config, `--config` overrides included.

Wake-up: no route is recorded for this harness. The status line names what the run waits on, so the user knows when to come back.

## OpenCode v2

Reaches every family its providers cover, so cross-family verification works natively. OpenCode v1 named the tool `task` and the config key `agent`; this route covers v2 only.

1. Copy [`templates/opencode.json`](../templates/opencode.json) into `opencode.json`. It defines one subagent per tier and family, named `<tier>-<family>`.
2. Set each `model` to `<opencodeModel>#<reasoning>`. The `#variant` suffix selects a named bundle of model options, and the catalog's `high` variant is the model's high reasoning level.
3. Before dispatch, check two things in the effective catalog (`opencode models`, plus the project's `provider` overrides in `opencode.json`):
   1. the model lists a variant with exactly that name;
   2. no project override redefines it.
   A family without `opencodeModel`, a model without that variant, or a redefined variant is unsupported on this route. Report it instead of guessing.
4. Spawn with the `subagent` tool: the `<tier>-<family>` agent id, a description, and the brief as the prompt. Set `background` for long work. Keep the returned `sessionID` to continue the same subagent.

The running session's own model and level: the primary agent's `model#variant`.

Wake-up: no route is recorded for this harness. The status line names what the run waits on, so the user knows when to come back.
