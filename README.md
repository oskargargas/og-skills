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

## License

MIT
