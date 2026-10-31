# og-skills

Agent skills by Oskar Gargas. Install with the [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add oskargargas/og-skills --skill og-skill-overrides
```

## Skills

### og-skill-overrides

Customise installed skills per project without editing them, so `npx skills update` keeps working.

A project keeps overrides at `.ai/skills/<skill-name>/SKILL.md`. Each override is a patch applied on top of the installed skill: explicit changes win, the installed skill's safety rules always win, and overrides are forwarded to subagents. Shared values such as a docs or specs folder live in `.ai/agentic.config.json`, the same file the [open-mercato skills](https://github.com/open-mercato/skills) use.

Nothing is copied into the project beyond a short managed block in `AGENTS.md`, the `.ai/` files you create, and optional hook entries. Templates, scripts and the contract stay inside the installed skill folder, so an update to the skill updates every project.

Commands (`/og-skill-overrides <command>`):

| Command | Does |
|---|---|
| `help` | show the commands |
| `setup` | wire the project: `AGENTS.md` block, `.ai/` folders, optional `.ai/agentic.config.json`, optional hooks |
| `update` | rerun setup, refresh the managed block |
| `override <skill> <change>` | create or extend an override for an installed skill |
| `hooks [agent ...]` | add a deterministic hook that injects the override on skill invocation (Claude Code and Codex built in; other agents researched on request) |

Background research with sources is in [`docs/research/`](docs/research/).

### og-orchestrate

```sh
npx skills add oskargargas/og-skills --skill og-orchestrate
```

Run a multi-step goal as its orchestrator. The session agrees a plan and its gates with you, sends every step to a subagent at a configured model tier (worker, supervisor, expert), asks an expert from the other model family (Claude or Codex) for a second opinion on specs, risky reviews and architecture decisions, and opens every progress message with a status line.

Model ids, provider ids and reasoning levels live in the `orchestrate` section of `.ai/agentic.config.json`; [`templates/orchestrate.json`](skills/og-orchestrate/templates/orchestrate.json) is the starting point. Spawn routes are described for T3 Code, Claude Code, Codex CLI and OpenCode v2. Pipeline skills such as the open-mercato `om-auto-*` family run under it step by step.

### og-context-structure

```sh
npx skills add oskargargas/og-skills --skill og-context-structure
```

Run `/og-context-structure` to restructure a project's agent context: root and nested `AGENTS.md`, topic files, rules and context hooks. It detects the harness it runs in (Claude Code, Codex, OpenCode, Pi, Cursor) and the harnesses the repo serves, reports what loads when in each, and proposes a lean, `AGENTS.md`-only layout as a numbered plan. It edits only the items you accept, following `technical-writing` and `writing-for-agents`, then prints a prompt that estimates context cost before and after, and suggests `/eliminate-no-op` and [ContextScope](https://github.com/open-mercato/context-scope) as next steps.

## Layout

Each skill lives once in `skills/<name>/`, which is where the skills CLI installs from. To use a skill while working in this repo, `.agents/skills/<name>` (Codex) and `.claude/skills/<name>` (Claude Code) are symlinks to that folder, so both agents load the same files. `og-orchestrate` and `og-context-structure` are linked this way.

## License

MIT
