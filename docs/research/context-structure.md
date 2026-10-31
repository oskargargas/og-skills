# Agent context structure: research

Research date: 2026-10-31. Sources are official documentation and source code unless noted.

## Findings

- Instruction files load at different times in each harness. Check the running harness, the harnesses the repo serves, their effective settings and the launch directory before proposing a move. [1][2][11][12][13]
- Claude imports add content at load time. A conditional pointer can defer material until a task needs it. Path-scoped rules serve matching files. [1]
- Codex reads instructions from the project root to the launch directory, subject to a combined size limit. Nested files below that directory need discovery during work. [2][3]
- Hook output has limits. Large output can leave a preview in context and the full text in a file, so measure what a hook prints. [4][5]
- Keep shared context near the root and package-specific instructions in the package. This community convention depends on each tool's loading behavior. [2][6]
- Keep facts that apply to every task in startup context. Put task-specific rules behind a clear trigger, and let config and tooling own values and enforced rules. Review behavior separately from placement. [1][7]
- Skill invocation settings affect discovery. Claude can hide a skill description from automatic invocation; Codex supports disabling implicit invocation. [8][9]

- Claude Code reads `AGENTS.md` only while no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the launch directory or above. `.claude/rules/` and `~/.claude/CLAUDE.md` load beside it. [1]
- A root `CLAUDE.md` beside `AGENTS.md` stops Claude Code loading nested `AGENTS.md` (user observation, 2026-10-31). The skill therefore removes every `CLAUDE.md` and moves Claude-only lines to `.claude/rules/`.
- OpenCode v2 reads `AGENTS.md` only, from the workspace up to the project root, and loads nested files when the agent reads or lists there. It does not parse `@path` references. [11][12]
- Pi reads one context file per directory from the launch directory up (`AGENTS.override.md`, `AGENTS.md`, then `CLAUDE.md`) and nothing below it. It marks child processes with `AI_AGENT=pi` and `PI_CODING_AGENT=true`. [13]
- Cursor reads root and nested `AGENTS.md` and `.cursor/rules`; `sessionStart` hooks can add context. [14][15]
- No common environment marker identifies the running harness; the system prompt does. Claude Code sets `CLAUDECODE=1`, Codex `CODEX_THREAD_ID`. [16][17]

## Sources

1. [Claude Code memory](https://code.claude.com/docs/en/memory)
2. [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
3. [Codex source](https://github.com/openai/codex)
4. [Claude Code hooks](https://code.claude.com/docs/en/hooks)
5. [Codex hooks](https://learn.chatgpt.com/docs/hooks)
6. [Monorepo guidance](https://agents-md.app/guides/agents-md-for-monorepos/) (community)
7. [eliminate-no-op](https://github.com/pat-lewczuk/skills/tree/main/skills/eliminate-no-op)
8. [Claude Code features overview](https://code.claude.com/docs/en/features-overview)
9. [Codex skills](https://learn.chatgpt.com/docs/build-skills)
10. [Claude Code large codebases](https://code.claude.com/docs/en/large-codebases)
11. [OpenCode instructions (v2 source docs)](https://github.com/anomalyco/opencode/blob/dev/services/www/src/docs/content/instructions.mdx)
12. [OpenCode rules](https://opencode.ai/docs/rules)
13. [Pi configuration and resource loader](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md)
14. [Cursor rules](https://cursor.com/docs/context/rules)
15. [Cursor hooks](https://cursor.com/docs/agent/hooks)
16. [Claude Code environment variables](https://code.claude.com/docs/en/env-vars)
17. [ContextScope](https://github.com/open-mercato/context-scope)
17. [Codex PR #10096: CODEX_THREAD_ID](https://github.com/openai/codex/pull/10096)
