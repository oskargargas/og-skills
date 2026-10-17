# Setup

Wire a project so every installed skill honours `.ai/skills/<skill-name>/SKILL.md`. `update` is the same workflow run again: every step is idempotent, and the managed block is rewritten from the current template so a newer skill version refreshes it.

Prompt-driven, not a script: explore, propose, confirm, write.

## 1. Explore

Read what exists, nothing assumed:

- `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md` at the project root. Which exist, and does one already carry the `og-skill-overrides:start` marker?
- `.ai/`, `.ai/skills/`, `.ai/agentic.config.json`. Existing overrides and an existing config (possibly written by the open-mercato `om-setup-agent-pipeline` skill, which uses the same file).
- Installed skills: `.agents/skills/`, `.claude/skills/`, `~/.agents/skills/`, `~/.claude/skills/`. Where this skill itself lives decides the hook script path (see [`hooks.md`](hooks.md)).
- Agent dirs in the project and the home folder: `.claude/`, `.codex/`, `.cursor/`, `.gemini/`, `.github/`.

## 2. Instruction file

Pick the file:

- `CLAUDE.md` exists and `AGENTS.md` does not: write the block to `CLAUDE.md`.
- `AGENTS.md` exists: write the block to `AGENTS.md`. When `CLAUDE.md` also exists and lacks `@AGENTS.md`, add that line, because Claude Code reads `AGENTS.md` only when no `CLAUDE.md` sits in or above the working directory.
- Neither exists: ask which to create. `AGENTS.md` is read by Codex, Cursor, Copilot, Gemini and Claude Code, so recommend it.

Write the block from [`templates/agents-md-block.md`](../templates/agents-md-block.md). Marker present: replace everything between `og-skill-overrides:start` and `og-skill-overrides:end` inclusive. Marker absent: append the block at the end of the file. Show the diff before writing.

## 3. Folders

Create `.ai/skills/` when missing (empty directories are not tracked by git, so add `.ai/skills/.gitkeep`). This is where overrides go. Nothing else is copied.

## 4. Config

`.ai/agentic.config.json` holds values more than one override may need, so each override reads one place instead of repeating a path. It uses the same file and shape as the open-mercato config, so the two coexist.

Format:

- `version`: schema version, `1`.
- `paths.<name>`: a folder (for example `paths.specs`).
- Any other top-level key: any other shared value (a URL, a label vocabulary, a branch name).

Setup creates the file with no keys besides `version`. Keys are proposed only by [`override.md`](override.md), when a specific override needs a shared value. Never guess project folders such as docs or specs here; they may not exist or matter in this project.

- No config: offer to create it from [`templates/agentic.config.json`](../templates/agentic.config.json), which holds only `version`. On no, skip; overrides inline their values.
- Config exists: leave it as it is. Keys written by other tools stay untouched.

## 5. Hooks

Offer the deterministic layer. List the agents exploration found and run [`hooks.md`](hooks.md) for the ones the user picks. On no, skip; the `AGENTS.md` rule alone is a working setup.

## 6. Lockfile

A project-scope install writes `skills-lock.json` at the project root. When it exists and is untracked, say that committing it lets teammates restore the skill with `npx skills experimental_install`. A global install has no lockfile in the project; say that teammates need `npx skills add oskargargas/og-skills --skill og-skill-overrides -g`.

## Done

The instruction file carries the current block, `.ai/skills/` exists, config and hooks are in the state the user chose. Close with one line per item written, and the next step: `/og-skill-overrides override <skill-name> <change>` to write the first override.
