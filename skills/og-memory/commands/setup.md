# Setup

Create or refresh the memory store in this repository, so every agent follows [the mechanism](../references/memory.md). Every step is idempotent: run it again after a skill update, and the managed block is rewritten from the current template.

Explore, propose, confirm, write. Show the human every change before you write it. Existing authorization to apply setup covers the writes; otherwise wait for confirmation. Resolve the project root from Git, or from the directory the human names when Git is absent.

## 1. Explore

Read what exists, nothing assumed:

- `.ai/agentic.config.json`: which of `paths.runs`, `paths.memory` and `paths.memoryIndex` are set.
- The folders and index those keys name, or the defaults. Also look for an older store under another name (`lessons/`, `wiki/`, `sessions/`, a `MEMORY.md` elsewhere).
- `AGENTS.md`, `CLAUDE.md`, `.claude/CLAUDE.md`: which exist, whether one carries the `og-memory:start` marker, and which unmanaged lines already state the memory or run-record rules.
- Format docs the project already has for run records or memories, such as a README in `.ai/`.
- Where this skill is installed (`.agents/skills/og-memory/`, `.claude/skills/og-memory/`, or a home folder), for the block's link to the reference.

Done when you can name, for each config key, folder, index and instruction file, whether it exists, is missing, or holds an older store.

## 2. Config

Add each missing key with its default from [the store table](../references/memory.md#the-store), or the path of an older store the human chooses to keep. Leave every other key as it is. With no config file, create it as `{ "version": 1, "paths": { … } }`.

## 3. Folders and index

- Create the runs and memory folders when missing, each with a `.gitkeep`. The defaults reproduce the shared layout: `.ai/runs/`, `.ai/memories/`, and `.ai/MEMORY.md`. Other `.ai/` folders belong to their project workflows and are not required by this skill.
- Create the index when missing, with a header that links the memory format:

  ```markdown
  # Memory

  One line per memory in <link to configured memory folder>. Format and rules: <link to format doc or reference>.
  ```

- An older store: offer to move it into these paths, and name the files whose links would need repointing. Move it only when the human agrees.

## 4. Instruction file

Pick the file:

- `AGENTS.md` exists: write the block there. When `CLAUDE.md` also exists and lacks `@AGENTS.md`, add that line, since Claude Code reads `AGENTS.md` only when no `CLAUDE.md` sits in or above the working directory.
- Only `CLAUDE.md` exists: write the block there.
- Neither exists: ask which to create, and recommend `AGENTS.md`, which most agents read.

Fill [`templates/agents-md-block.md`](../templates/agents-md-block.md):

- `{runs}`, `{memory}`, `{memoryIndex}`: the configured paths.
- `{reference}`: a link to this skill's `references/memory.md`, relative to the instruction file. A skill installed outside the repository can use a relative path outside it. Re-run setup if the installation moves.
- `{formats}`: links to the project's own format docs for run records and memories, or to the reference when it has none.

Compute all Markdown links relative to the file that contains them, including the index links. Encode spaces and other URL characters in link destinations. Keep filesystem paths in backticks as configured.

For the config, folders, missing index and managed instruction block, use the bundled helper after exploring:

```sh
python3 <skill-folder>/scripts/setup.py --root <project-root>
python3 <skill-folder>/scripts/setup.py --root <project-root> --apply
```

The first command previews without writing. The second applies the approved changes. Pass `--instruction-file` for a chosen instruction file relative to the project root. The helper preserves existing config values and index contents, and refreshes only its managed block. Reconcile unmanaged rules and project format links as described below; the helper does not migrate an older store or edit unrelated instructions.

Place it:

- Marker present: replace everything from `og-memory:start` to `og-memory:end`.
- Marker absent: put the block where the file's existing memory or run-record rules sit, and remove those rules, since the block now holds them. Keep any line that says something the block does not, outside the block. With no such rules, append the block at the end.

Done when the file holds exactly one block, filled with this repository's paths, and no unmanaged line repeats a rule the block states.

## 5. Verify

- Each configured path exists.
- Every link in the block resolves from the instruction file's folder.
- Run the repository's fast check when one exists. Use its configured commands rather than requiring a particular runtime or package manager. For a documentation-only repository without a check, inspect the generated Markdown and parse the config.

Close with one line per item written or left as it was, and the next step: work as usual, and run `/og-memory dream` once memories pile up.
