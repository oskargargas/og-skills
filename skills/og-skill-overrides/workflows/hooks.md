# Hooks

The `AGENTS.md` rule is advisory: the agent reads it and usually complies. A hook makes the override arrive deterministically, injected by the agent runtime the moment a skill is invoked, whether the model remembered the rule or not. Hooks are optional and per agent.

Input: zero or more agent names from the argument (`hooks`, `hooks codex`, `hooks claude cursor`). No names: detect from the project (`.claude/`, `.codex/`, `.cursor/`, `.gemini/`, `.github/copilot-instructions.md`) and from the user's home (`~/.claude`, `~/.codex`, `~/.cursor`, `~/.gemini`), list what you found, and ask which to wire. Tell the user that any other agent can be added by name: you research its hook docs and wire it when the agent supports context injection.

## Script path

Hook commands run from the project directory. Resolve this skill's `scripts/` folder once:

- Project install (`.agents/skills/og-skill-overrides` exists in the project): use the relative path `.agents/skills/og-skill-overrides/scripts/<hook>.sh`. Teammates get it from `skills-lock.json`.
- Global install: use `$HOME/.agents/skills/og-skill-overrides/scripts/<hook>.sh`. Hook commands run through a shell, so `$HOME` expands. Teammates need the skill installed globally too; say so.

Scripts need `jq` or `python3`. Check `command -v jq python3` and say which was found.

## Scope

Ask once: project scope (settings committed with the repo, every teammate gets it) or user scope (this machine, every project). Default project.

## Claude Code

Two events carry the skill name differently, so register both. Script: `scripts/claude-hook.sh`.

Merge into `.claude/settings.json` (project) or `~/.claude/settings.json` (user). Keep existing hooks; append to the arrays.

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Skill", "hooks": [ { "type": "command", "command": "<path>/claude-hook.sh" } ] }
    ],
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "<path>/claude-hook.sh" } ] }
    ]
  }
}
```

`PreToolUse` fires when the model invokes a skill through the Skill tool. A typed `/skill-name` bypasses it and goes through `UserPromptSubmit` instead. The script returns `hookSpecificOutput.additionalContext` with the override text and never blocks.

## Codex CLI

Codex has no skill tool for local skills: the model reads `SKILL.md` from disk with its shell tool, and the user invokes a skill explicitly with `$skill-name` in the prompt. Script: `scripts/codex-hook.sh`.

Merge into `.codex/hooks.json` (project) or `~/.codex/hooks.json` (user). Hooks are enabled by default since Codex rust-v0.114.0. A project `.codex/` layer must be trusted, and non-managed hooks are reviewed with `/hooks` in the CLI before they run. Tell the user both.

```json
{
  "description": "og-skill-overrides: inject .ai/skills/<name>/SKILL.md on skill use",
  "hooks": {
    "PreToolUse": [
      { "matcher": "^Bash$", "hooks": [ { "type": "command", "command": "<path>/codex-hook.sh", "timeout": 10 } ] }
    ],
    "UserPromptSubmit": [
      { "hooks": [ { "type": "command", "command": "<path>/codex-hook.sh", "timeout": 10 } ] }
    ]
  }
}
```

Limits to state: implicit skill selection shows up only when the model reads the `SKILL.md` through a shell command, which the `PreToolUse` branch catches by matching `.../skills/<name>/SKILL.md` in the command. A skill picked with the `/skills` picker reaches `UserPromptSubmit` only when its `$name` also appears as text.

## Other agents

For an agent not listed above, research before wiring. Use the agent's official docs (`npx ctx7@latest library "<agent>" "hooks"` first, then its docs site or GitHub repo). Answer four questions and show the answers to the user before writing anything:

1. Which hook events exist, and which of them can inject context into the model's turn (an `additionalContext`-style field, or plain stdout that becomes context)?
2. On which event is the skill name visible: a tool-call input that carries a `SKILL.md` path, a prompt that carries a mention sigil, or nothing?
3. Where does the hook config live (project and user scope), and what is the config shape and stdin schema?
4. Any trust or enable step the user has to perform.

Starting points, from research dated 2026-10-17 (verify against current docs before relying on them):

| Agent | Config | Inject on | Skill name visible on |
|---|---|---|---|
| Cursor | `.cursor/hooks.json` | `postToolUse`, `sessionStart` (`additional_context`); `beforeSubmitPrompt` can only allow or block | `postToolUse` of the read tool, when skill loading goes through a read (unverified) |
| Gemini CLI | `.gemini/settings.json` | `BeforeAgent`, `AfterTool` (`hookSpecificOutput.additionalContext`) | `BeforeAgent` prompt text; `AfterTool` read-tool input |
| GitHub Copilot CLI | `.github/hooks/*.json` | `postToolUse`, `sessionStart` (`additionalContext`); `userPromptSubmitted` cannot inject | `postToolUse` of the read tool |

When injection is possible: write the hook script to `.ai/hooks/<agent>-override-hook.sh` in the project (this is the one case where a file is generated into the project, because no shipped script matches that agent), modelled on `scripts/codex-hook.sh` (read stdin JSON, find the skill name, look up `.ai/skills/<name>/SKILL.md`, emit the agent's context field). Register it in the agent's config at the chosen scope. Test it with a hand-made stdin JSON before reporting.

When injection is not possible: say so, name the closest event, and leave the agent on the advisory `AGENTS.md` rule.

## Done

Each wired agent has: the config entry written, the script path verified to exist and be executable, and a dry run with a fake stdin JSON that printed the override text. Report per agent: scope, config file, and any trust step still on the user.
