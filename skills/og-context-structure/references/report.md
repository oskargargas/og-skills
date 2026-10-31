# Report templates

## Report

````markdown
## Context structure: <repo name>

Harness: <running>. Serves: <harnesses>. Launch: repo root. <Each served harness's loading setting, such as Claude Code mode `claude-md-or-agents-md`, Codex `project_doc_max_bytes` 32 KiB.>

### Inventory

| File | Kind | Loads | Chars | ~Tokens |
|---|---|---|---|---|
| `AGENTS.md` | root | startup (all) | 9,018 | 2,577 |
| `packages/api/AGENTS.md` | package | file read (Claude Code, OpenCode, Cursor); pointer (Codex, Pi) | 1,204 | 344 |

Startup, repo-owned: ~<n> tokens (characters ÷ 3.5).

### Findings

1. `MOVE` `AGENTS.md:40-58`: coding rules → `CODING_STANDARDS.md`. Only code tasks need them.
2. `LINK` `CLAUDE.md -> AGENTS.md`: stops Claude Code loading `packages/api/AGENTS.md`.

### Plan

| # | Change | Files | Startup effect |
|---|---|---|---|
| 1 | Move coding rules to `CODING_STANDARDS.md`; add pointer | `AGENTS.md`, `CODING_STANDARDS.md` (new) | −~600 |
| 2 | Remove `CLAUDE.md`; record "Add no `CLAUDE.md`" in the root | `CLAUDE.md`, `AGENTS.md` | +~10 |

### Target tree

```text
AGENTS.md
CODING_STANDARDS.md
packages/api/AGENTS.md
```

### Untouched

- `AGENTS.md:80-95`: og-skill-overrides managed block.
- `AGENTS.md:31`: tracked bug.

### Notes

- Issues inside managed blocks, for the owning skill.

Reply with the numbers to apply, such as "1-3, 5" or "all". Nothing changes until you do.
````

## Final message

````markdown
Applied <n> of <m> plan items.

- `AGENTS.md`: edited, coding rules moved out (item 1).
- `CODING_STANDARDS.md`: created (item 1).

Startup, repo-owned: ~<a> → ~<b> tokens (characters ÷ 3.5). Task costs can rise when topic files load; the prompt below estimates both.

Checks: links resolve, every removed line mapped, untouched content unchanged.
Not fixed (pre-existing or rejected): <list, or "none">.
Removed by accepted items: <verbatim lines, or "none">.

To compare context cost before and after, paste this into a fresh session. I have not run it.

<contents of references/measure-context.md, in a text fence>

Next steps:
- `/eliminate-no-op` checks each remaining line for instructions that change nothing.
  https://github.com/pat-lewczuk/skills/tree/main/skills/eliminate-no-op
  Install: `npx skills add pat-lewczuk/skills --skill eliminate-no-op`
- ContextScope profiles what actually fills the context window, from Claude Code and Codex session transcripts.
  https://github.com/open-mercato/context-scope
````
