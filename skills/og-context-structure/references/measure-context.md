Estimate the context cost of this repo's agent files before and after a change. This is a static estimate from the files, not a runtime measurement. Change no file in the working tree.

Before: the default branch (origin/HEAD, else main, else master). After: the current working tree, uncommitted and untracked files included. If I name other refs, use those. Resolve each ref to a commit SHA.

1. Check out the before SHA in a temporary worktree outside the repo (git worktree add --detach <dir> <sha>). Remove it with git worktree remove when done. Ignored local files, such as CLAUDE.local.md, AGENTS.override.md and .claude/settings.local.json, exist only in the working tree: leave them, and their effect on what loads, out of both sides, and name them.

2. Fix the comparison once and use it for both sides. Harnesses: the one running this prompt, plus each one either side serves: Claude Code (.claude/ or any CLAUDE.md), Codex (.codex/), OpenCode (.opencode/ or opencode.json), Pi (.pi/), Cursor (.cursor/ or .cursorrules). Pick three tasks:
   a. a code change in the directory with the most changed files in the last 100 commits of the after side (git log --name-only);
   b. adding a test in that directory;
   c. writing documentation or an agent instruction file.
   Print a manifest first: the running harness, its version and model; the harnesses compared; launch directory (the repo root); both SHAs and whether the working tree has uncommitted or untracked changes; each compared harness's loading settings (Claude Code: Project instructions, default claude-md-or-agents-md, and claudeMdExcludes; Codex: project_doc_max_bytes, fallback filenames and hook limits; OpenCode: instructions in opencode.json); the three tasks with exact paths; the token method; what is left out.

3. On each side and for each harness, list every repo-owned input that can reach the model, and when it loads:
   - Startup.
     Claude Code, under its Project instructions setting: CLAUDE.md, .claude/CLAUDE.md and CLAUDE.local.md in the launch directory and above, or, where none exists, AGENTS.md and .claude/AGENTS.md; @path imports expanded up to four hops; .claude/rules/**/*.md without paths frontmatter.
     Codex: AGENTS.override.md, else AGENTS.md, else a fallback filename, one per directory from the project root to the launch directory, cut at project_doc_max_bytes.
     OpenCode: every AGENTS.md from the launch directory up to the project root, and files listed in opencode.json instructions.
     Pi: per directory from the launch directory up, the first of AGENTS.override.md, AGENTS.md, CLAUDE.md.
     Cursor: AGENTS.md and .cursor/rules files with alwaysApply: true.
     Every harness: session-start hook output (.claude/settings.json, .codex/hooks.json, .codex/config.toml, .cursor/hooks.json); skill names and descriptions as this harness lists them, or, for another harness or when you cannot see the list, every repo skill it discovers, marked estimated.
     Files above the repo root decide what a harness skips but are left out of the counts.
   - Per event: prompt-submit and tool hooks, with the event that fires each.
   - On demand: nested AGENTS.md (Claude Code on Read, unless the root holds a CLAUDE.md; OpenCode on read or list; Cursor for files in its directory; Codex and Pi only when an instruction says so), nested CLAUDE.md, path-scoped rules, files reached by pointers, skill bodies.

4. Count what reaches context initially, not file size. Hook output over the harness's limit (Claude Code: 10,000 characters; Codex: the handler's additionalContextLimit, about 2,500 tokens by default; other harnesses: none documented, count it all) arrives as a file path plus a preview: count the preview and list the rest as available on read. Count a file a harness skips, shadows or cuts as unreached for that harness. Count a symlinked file once. Follow pointers recursively, count each file once per total, and stop at cycles. To get a hook's output, run its command in that side's checkout only if it just prints; otherwise read the script and estimate.

5. Leave out inputs identical on both sides: system prompt, tools, MCP servers, user-level and parent-directory instructions, rules, memory and skills.

6. Use one characters-to-tokens ratio for both sides. If this session shows a token count for a file that exists on one side (Claude Code: /context lists memory files), derive the ratio from it. Otherwise use characters ÷ 3.5. Round totals to the nearest 100 tokens. Percent is n/a when the before value is 0.

7. Cost each task on each side, per harness, as startup plus what the task loads. Mark each loaded file automatic (the harness loads it) or instructed (an instruction in context tells the agent to read it for that task). If a task path is missing on one side, say so.

Report:
- the manifest;
- per harness, one table: input, when it loads, before, after, difference;
- per harness, startup totals and each task's total, before and after, with the difference in tokens and percent;
- event-hook costs, separately;
- anything cut, shadowed, unreached or available only on read;
- local inputs the before side could not reproduce.
Call every figure a static estimate. No recommendations.
