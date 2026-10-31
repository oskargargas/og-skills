# Loading facts

## Detect

The running harness names itself in your system prompt; confirm with the environment. Repo markers show what the repo serves, not what runs. Unsure: ask.

| Harness | Environment | Repo marker |
|---|---|---|
| Claude Code | `CLAUDECODE=1`; `AI_AGENT=claude-code_…` | `.claude/`, any `CLAUDE.md` |
| Codex | `CODEX_THREAD_ID` | `.codex/` |
| OpenCode | none documented | `.opencode/`, `opencode.json` |
| Pi | `AI_AGENT=pi`, `PI_CODING_AGENT=true` | `.pi/` |
| Cursor | none documented | `.cursor/`, `.cursorrules` |

`AGENTS.md` is read by all five and marks none.

## Per harness

| Harness | Startup | Nested `AGENTS.md` | Limits | Context hooks |
|---|---|---|---|---|
| Claude Code | See [Claude Code](#claude-code). | On Read of a file in its directory; never while the root holds a `CLAUDE.md`. | Root target 200 lines. On-demand file cut to its first 40,000 characters (150,000 on a 1M window). | `.claude/settings*.json`. Output over 10,000 characters → file path + 2,000-character preview. |
| Codex | One file per directory, project root (`.git`) → launch directory, root first: `AGENTS.override.md`, else `AGENTS.md`, else a `project_doc_fallback_filenames` entry. No project root: launch directory only. | Not loaded; the base prompt says to check for applicable ones. | Chain stops at `project_doc_max_bytes` (32 KiB). | `.codex/hooks.json`, `[hooks]` in `.codex/config.toml`. Output over the handler's `additionalContextLimit` (~2,500 tokens) → file path + head-and-tail preview. |
| OpenCode v2 | `~/.config/opencode/AGENTS.md`, then every `AGENTS.md` from the launch directory up to the project root; files in `opencode.json` `instructions`. | On read or list in its directory. | None documented. | None; JS plugins only. |
| Pi | `<agent-dir>` context file, then per directory from the launch directory up to `/`: first of `AGENTS.override.md`, `AGENTS.md`, `CLAUDE.md`. | Not loaded. | None documented. | None; TypeScript extensions only. |
| Cursor | `AGENTS.md`; `.cursor/rules/*.mdc` with `alwaysApply: true`. | Applies in its directory, combined with parents, nearer wins. | 500-line guidance per rule. | `.cursor/hooks.json` `sessionStart` `additional_context`; no documented limit. |

| Harness | Settings to read | Skill paths: project; user |
|---|---|---|
| Claude Code | `instructionFiles`, `claudeMdExcludes` | `.claude/skills/`; `~/.claude/skills/` |
| Codex | `project_doc_max_bytes`, `project_doc_fallback_filenames`, hook limits (`.codex/config.toml`, `~/.codex/config.toml`) | `.agents/skills/` from the launch directory up to the repo root; `~/.agents/skills/` |
| OpenCode | `opencode.json` `instructions`, `OPENCODE_DISABLE_PROJECT_CONFIG` | `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`; the same under `~/.config/opencode/`, `~/.claude/`, `~/.agents/` |
| Pi | `PI_CODING_AGENT_DIR` (default `~/.pi/agent`) | `.pi/skills/`, `.agents/skills/`; `<agent-dir>/skills/`, `~/.agents/skills/` |
| Cursor | `.cursor/rules` frontmatter, `.cursor/hooks.json` | `.cursor/skills/`, `.agents/skills/`, `.claude/skills/`, `.codex/skills/`; the same under `~` |

- `@path` expands only in Claude Code: relative to the importing file, four hops, never inside backticks, at inline cost. Codex and Pi show it as text; OpenCode does not parse it.
- A hook that prints a file the harness already loads adds a second copy.
- `AGENTS.override.md` shadows `AGENTS.md` in its directory for Codex and Pi; Claude Code and OpenCode ignore it.

## Claude Code

- Project instructions mode: `instructionFiles` under `pluginConfigs."cc-plugin-agents-md@builtin".options`, read from `~/.claude/settings.json`, `--settings` or managed settings, ignored in project settings. `claude-md-or-agents-md` (default): `CLAUDE.md` files, else `AGENTS.md`. `claude-md-and-agents-md`: both. `claude-md`: no `AGENTS.md`. `managed-only`: no project files at launch. `claudeMdExcludes` skips matching paths.
- Default mode startup: every `AGENTS.md` and `.claude/AGENTS.md` in the launch directory and its parents, only while no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists there; otherwise those files instead. Needs v2.1.277+ (v2.1.281+ on Bedrock or with telemetry off).
- A root `CLAUDE.md`, file or symlink, beside `AGENTS.md` also stops nested `AGENTS.md` from loading.
- `~/.claude/CLAUDE.md`, a managed `CLAUDE.md` and `.claude/rules/` never shadow `AGENTS.md`; they load beside it.
- `.claude/rules/**/*.md` without `paths` load at startup; with `paths`, when Claude reads a matching file. Other harnesses ignore them.
- Never read: `AGENTS.override.md`, `AGENTS.local.md`, `.agents/`.
- `disable-model-invocation: true` keeps a skill's description out of context.

## Codex

- `policy.allow_implicit_invocation: false` in `agents/openai.yaml` stops implicit invocation. Whether the description still loads is undocumented: measure it or call it unknown.
