---
name: og-skill-overrides
description: Project overrides for installed skills. Before following any skill, check `.ai/skills/<skill-name>/SKILL.md`; when present, apply it on top of the skill (safety rules still win) and forward it to subagents. Also use when the user wants to set up overrides in a project, create or edit an override for a skill, wire agent hooks for overrides, or manage `.ai/agentic.config.json`.
---

Overrides let a project customise an installed skill without editing it, so `npx skills update` keeps working. The override lives at `.ai/skills/<skill-name>/SKILL.md` and is read on top of the installed skill.

## Route

Pick one branch by the argument the user passed, or by context when they passed none:

| Argument | Branch | Read |
|---|---|---|
| none, and you are about to follow another skill | apply the override | nothing more: read `.ai/skills/<skill-name>/SKILL.md`, apply it on top, safety rules win, forward it to subagents |
| none, bare invocation | help | [`references/help.md`](references/help.md) |
| `help` | help | [`references/help.md`](references/help.md) |
| `setup` | wire the project | [`workflows/setup.md`](workflows/setup.md) |
| `update` | rerun setup, refresh the `AGENTS.md` block | [`workflows/setup.md`](workflows/setup.md) |
| `override <skill-name> <what to change>` | create or edit one override | [`workflows/override.md`](workflows/override.md) |
| `hooks [agent...]` | deterministic hook layer per agent | [`workflows/hooks.md`](workflows/hooks.md) |

No recognised argument: infer the branch from the request. "Make code-review also look in `.ai/spec`" is `override`. "Set this repo up for overrides" is `setup`. "Add the hook for Codex" is `hooks`. When two branches fit, name the one you picked in your first line and proceed.

## Paths

- Project root: the directory holding `.git`, or `AGENTS.md` when there is no `.git`.
- This skill's own folder: resolve from this file's location. Templates and scripts are referenced relative to it, so the project never needs a copy.
- Shared project values: `.ai/agentic.config.json`, created by `setup`, read by overrides.
