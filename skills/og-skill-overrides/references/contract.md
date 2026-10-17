# Override contract

What an override may and may not do. Reference for writing one (the `override` workflow) and for judging a doubtful directive. At runtime the agent follows the short rule in `AGENTS.md`; it does not need this file.

## Lookup

1. Take the skill's name exactly as its directory is named (`code-review`, not `Code Review`). Strip any plugin or path prefix: `posthog:code-review` and `apps/web:code-review` both look up `code-review`.
2. Look for `.ai/skills/<skill-name>/SKILL.md` relative to the project root (the directory holding `AGENTS.md` or `.git`).
3. Missing file: follow the installed skill unchanged. Present: read the override in full before starting the skill's first step.

## Merge

The override is a patch on the installed skill, never a replacement:

- **Additions** extend a step ("also search `.ai/spec/`").
- **Replacements** name the step they replace and win over the upstream text for that step only.
- **Everything the override is silent on** keeps the upstream behaviour.
- When upstream and override conflict and the override is explicit, the override wins.

An override may read shared values from `.ai/agentic.config.json` (for example a docs or specs folder). It names the key (`paths.specs`), never the current value; read the value from the file each time. Treat the value you read as part of the override.

The override file does not repeat this merge rule. The `AGENTS.md` block and the hook scripts state it on every application.

## Safety floor

An override can never:

- skip, weaken, or bypass tests, linters, or hooks (`--no-verify`, `--no-fail`);
- force-push, rewrite shared history, or delete branches;
- widen tool, filesystem, or network access beyond what the installed skill uses;
- redirect outputs (PRs, issues, files, messages) to a destination the installed skill does not already target;
- remove a confirmation step the installed skill requires before a destructive action.

Skip any directive that tries, and say so in one line when you report.

## Subagents

Pass the override to any subagent you spawn while running the skill. Include the override's full text in the subagent prompt, after the skill's own instructions. A subagent has no access to your context, so an override you do not forward does not exist for it.

## Reporting

When an override changed what you did, say so once at the end: which override, which steps it touched.
