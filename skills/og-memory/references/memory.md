# Memory and run records

The one definition of how agents share memory in a repository. Every agent follows it through the project's `og-memory` block in `AGENTS.md`. Skills that write memory or run records, such as `og-orchestrate`, follow it and add only their own timing. A project's own format docs extend it, and win where they are explicit.

## The store

Paths come from `paths` in `.ai/agentic.config.json`, written by `/og-memory setup`:

| Key                 | Holds                              | Default         |
| ------------------- | ---------------------------------- | --------------- |
| `paths.runs`        | run records, one per run           | `.ai/runs`      |
| `paths.memory`      | the memories, one file each        | `.ai/memories`  |
| `paths.memoryIndex` | the index agents read before tasks | `.ai/MEMORY.md` |

Paths may be relative to the project root or absolute. Render links relative to the document containing each link. The relative paths in the examples below illustrate the default layout; adapt them to configured paths. No framework, tracker, package manager or other skill is required.

## Run records

A **run record** is the episodic store and the handoff: one file per run or session that changes the repository, named `YYYY-MM-DD-<slug>.md`. Without a project format, it has a header (started, human, agent, branch, Status) and these sections:

- **Goal**: the first prompt, quoted verbatim with secrets redacted.
- **Progress**: the steps and gates as checkboxes, with commits. Another session resumes from the first unchecked one.
- **Log**: `HH:MM Human:` with each later prompt quoted verbatim with secrets redacted, and `HH:MM Agent:` with what was done, times read from the clock.
- **Decisions**, **What changed**, **Verification**, **Open ends**.
- **Memories**: each memory this work added, changed or removed, and its uses.

Create it once you start changing files. Update Progress and Log after every prompt and finished task. A pipeline skill's plan or run folder that carries these sections is the record.

## Memories

A **memory** is one fact a future agent needs and cannot get from the code, the git history or the docs: a bug's cause, a gotcha, an unwritten convention, a better way to do a recurring task. Its file in `paths.memory` is named `YYYY-MM-DD-<slug>.md`, dated when it was created. Without a project format:

```markdown
# <The memory as one sentence>

- Area: <part of the product or codebase>
- Source: <bug, PR, run record or conversation it came from>

<The rule, why it holds, and how to apply it.>
```

Date each claim and cite its source: a PR, a commit with its repository, a run record. A changed claim gets a new dated line, and the old one is marked `(superseded YYYY-MM-DD)`. Keep memories true: update the memory that covers a fact before adding a near-duplicate.

The **index** holds one line per memory, newest first, within 200 lines and 25 000 bytes:

```markdown
- [Title](memories/YYYY-MM-DD-slug.md): when it applies
```

The text after the colon is the **trigger**: the task or area where an agent should open the memory.

## Query, use, record

- **Query**: before a task or a decision, read the index and open each memory whose trigger matches.
- **Use**: when a memory changes what you do, add a line to the run record's Memories section. Opening a memory is not a use.

  ```markdown
  - Used: [Title](../memories/YYYY-MM-DD-slug.md): what it changed
  ```

- **Record**: after a human corrects you, after you fix a bug, or when you learn anything a future agent needs, write the memory, its index line, and an `Added:` or `Changed:` line in the run record's Memories section.

## Permanent docs

A **permanent doc** is where a rule lives once it stops being a memory: agent instructions (`AGENTS.md`, `CLAUDE.md`, a package's own), the standards they point to (coding, testing, review), an ADR or other doc under `docs/`, or a skill's file or its project override in `.ai/skills/<skill>/SKILL.md`. `/og-memory dream` promotes memories into them.

## Consolidation

Only a human starts `/og-memory dream`. Suggest it when the index nears its caps or contradicts itself; never schedule it.
