---
name: og-context-structure
description: Restructure a repo's agent context files into a lean layout, applying only the plan items you accept.
disable-model-invocation: true
---

# Context structure

Analyse where agent instructions live, when they load and how tersely they read; restructure on acceptance.

## Principles (ranked; the higher wins)

1. **Accept first.** Edit nothing until the user accepts plan items by number.
2. **Lose nothing.** A moved instruction keeps its scope, trigger and path targets, and reaches at least the harnesses it reached. Every removed line has a destination or an accepted removal.
3. **Single source.** Each meaning lives once, in the narrowest file every task needing it reaches. Config and tooling own values and enforced rules; prose names the key or command. Split only when most tasks skip the split-out part.
4. **Reach.** Every-session content reaches the initial context of every served harness, within its limits.
5. **Lean.** One word over two, one sentence over two. Rules, not workflow. State the target, not the ban.
6. **Structure only.** Whether a line changes behaviour is `eliminate-no-op`'s job.

## Target structure

### Harnesses

- **Running**: the harness executing this skill, detected per `references/loading.md`. It sets which settings and skill paths you read.
- **Served**: the running one plus each with a repo marker. Load and limit checks cover each; harness-specific files (`.claude/rules/`) are proposed only for one. Propose no new hook, plugin or extension.

### Files

| File | Holds |
|---|---|
| Root `AGENTS.md` | What every task needs, under 200 lines: facts not findable by looking (conventions, gotchas, reasons); undiscoverable commands, or where they are defined; conditional pointers; config location and needed keys, no values; recorded decisions; other skills' managed blocks. In a monorepo, one line saying packages carry their own `AGENTS.md`. |
| Package `AGENTS.md` | What applies only inside the package: commands, framework, tests, constraints. Nothing the root says. |
| Topic file | One topic: coding standards, testing, glossary, domain, writing. A standards file lists rules; a procedure gets its own file or a project skill. Keep existing names; else repo-wide at the root in upper case (`TESTING.md`), agent-only under `docs/agents/`. Rules shared by some packages live here, pointed to by each. |
| `.ai/agentic.config.json` or harness config | Paths, settings, model ids, command lists. Move a value here only when two or more files quote it. |
| `.claude/rules/*.md` | Claude-only lines. No `paths`: every session; `paths`: matching files. Keep existing ones; drop lines the root repeats. |

With no context files, say so; propose a root `AGENTS.md` only for facts not findable by looking.

### AGENTS.md only

Every harness reads `AGENTS.md`. Any `CLAUDE.md` shadows it for Claude Code, root and nested (`references/loading.md`). Remove every one:

| Found | Plan |
|---|---|
| `CLAUDE.md` symlink, any depth | Remove. |
| `CLAUDE.md` or `.claude/CLAUDE.md` beside `AGENTS.md` | Shared lines → `AGENTS.md`, Claude-only lines → `.claude/rules/claude.md`, delete. |
| `CLAUDE.md` without `AGENTS.md` | `git mv` to `AGENTS.md`; Claude-only lines → `.claude/rules/claude.md`, or for a nested file `.claude/rules/<dir>.md` with `paths: <dir>/**`. |
| `CLAUDE.local.md` | Move to a gitignored `.claude/rules/local.md`. |
| `CLAUDE.md` above the repo root; Claude Code mode `claude-md` or `managed-only`; Claude Code below v2.1.277 | `LOAD` finding naming the user's fix. Edit nothing. |

Record in the root: "Add no `CLAUDE.md`; Claude Code reads this file."

### Pointers

| Form | Use |
|---|---|
| Conditional pointer | Default for a topic file: one line until it fires, read by every harness. Trigger first, one per branch, path in backticks: `Read \`TESTING.md\` before you write or change tests.` |
| `@path` import | None in `AGENTS.md`: only Claude Code expands it, at inline cost. Replace with a pointer. |
| Context hook | Keep an existing one only when its content must be in every session and fits the harness's hook limit; else propose a pointer and removing the hook entry. |

### Untouched

- Managed blocks (`<!-- name:start … -->` … `<!-- name:end -->`, or a heading naming the owning skill): byte-identical, in place. Issues go to Notes.
- Lines recording a tracked bug, workaround or known issue: verbatim.
- Recorded user decisions. When one blocks a proposal, the item quotes it; acceptance updates both.
- Config files and values, except an accepted removal of one identified context-hook entry; the rest stays byte-identical.
- Installed skills (any harness's skill directories, `skills-lock.json` entries) and `.ai/skills/`.
- `AGENTS.override.md`, anything under `~` or above the repo root, symlink targets outside the repo.
- `.cursor/rules/`, `.github/copilot-instructions.md`, `GEMINI.md`: inventory and `DUP` notes only.

## Workflow

### 1. Analyse (read-only)

Read `references/loading.md`. Name the running and served harnesses. Assume launch at the repo root and say so. Read, skipping `node_modules`, `.git`, build output and installed skills:

- every `AGENTS.md`, `.claude/AGENTS.md`, `AGENTS.override.md`, `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md` in the repo and above its root, with symlink targets, and every file they reach by pointer, link or `@path`, recursively, each once;
- `.claude/rules/**` and `.cursor/rules/**`, with `paths` and `globs`;
- each served harness's settings and hooks (`references/loading.md`), and what each context hook prints (read the script, measure the output);
- project skills, `skills-lock.json`, `.ai/skills/`, `.ai/agentic.config.json`;
- enforcing tooling: linter, formatter, `tsconfig.json`, pre-commit, CI, `package.json` scripts, `Makefile`;
- workspace manifests; with those or nested instruction files, read `references/monorepo.md`.

Per file, record path, kind, load time per served harness (startup, folder read, pointer, hook event), characters, and tokens as characters ÷ 3.5.

| Tag | Finding |
|---|---|
| `MOVE` | Wrong tier or file. |
| `SPLIT` / `MERGE` | Mixed topics, or one topic in two files. |
| `DUP` | One meaning twice, including prose restating config or tooling. |
| `POINTER` | Missing or weak pointer, broken link, import that should be a pointer. |
| `LOAD` | Shadowed, cut, previewed or unreached in a served harness. |
| `LINK` | A `CLAUDE.md` file or symlink, a broken symlink. |
| `TRIM` | Wording longer than its meaning. |

A reference to a missing path gets two options: fix the target or drop the line.

Done when every inventoried file has a load time and size, and every proposed move names source, destination and route.

### 2. Report

Show the report from `references/report.md`, nothing more, and end the turn. Plan numbers match finding numbers where one finding makes one change. An item names its dependencies ("needs 2") and any load-time change ("every session → when tests change"). A `TRIM` item covers one file with one before/after sample. A recorded-decision line is its own item when the user rejected a proposal that would return.

### 3. Accept

Apply only accepted numbers. On a change request, or an accepted item that needs an unaccepted one, revise, show only changed items, and wait. When the user rejects an item a later run would repeat, offer to record the decision in the root.

### 4. Implement

1. Find `technical-writing`, `unslop` and `writing-for-agents` in the running harness's skill paths (`references/loading.md`). Read each in full, with the files it points to, before the first edit. If one is missing, offer `npx skills add cursor/plugins --skill technical-writing --skill unslop` and `npx skills add mattpocock/skills --skill writing-for-agents`, and wait; if declined, write to principle 5 and say so at the end.
2. Snapshot every inventoried file, with type and symlink target, outside the repo.
3. Apply accepted items: move text, then tighten it. Keep a move map, source `file:line` → destination `file:line`, many-to-one allowed. Rewrite relative paths and incoming references; leave a pointer where text left. Rename with `git mv`. Commit nothing.

Done when every accepted item is applied and nothing else differs from the snapshot.

### 5. Verify

Against the snapshot:

- Every removed line is in the move map or an accepted removal, and meets principle 2.
- Every pointer, link, backticked path and symlink in changed files resolves (`find -L . -type l` lists broken links).
- No `@path` outside backticks in any `AGENTS.md`. No removed `CLAUDE.md` remains.
- Untouched files and blocks are byte-identical and in place.
- Sizes are within each served harness's limits (`references/loading.md`).

Fix failures the accepted items introduced; report the rest. Delete the snapshot.

### 6. Final message

Fill the final-message template in `references/report.md`. It ends with `references/measure-context.md` verbatim in a `text` fence, never run, and the `eliminate-no-op` and ContextScope next steps.
