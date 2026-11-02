# Portable memory and run records

Use the project's existing record format and memory workflow when available. Otherwise propose these paths in `.ai/agentic.config.json` with the plan:

| Key | Suggested path |
| --- | --- |
| `paths.runs` | `.ai/runs` |
| `paths.memory` | `.ai/memories` |
| `paths.memoryIndex` | `.ai/MEMORY.md` |

Paths are relative to the project root unless absolute. Preserve existing values and unrelated configuration. For an existing `paths.wiki` store, query its index and retain its useful content; propose any migration with the plan rather than silently replacing it.

## Run records

Create one `YYYY-MM-DD-<goal>.md` record after plan acceptance, or at the start of an authorized single task. Include the goal, agent, branch when applicable, Status, Progress, gates and their pass conditions, Decisions, Verification, Open ends and Memories. Progress holds the step table and commits when applicable. Record each gate verdict, decision or correction in one line, using the clock for timestamps. A pipeline's existing run record can serve this purpose.

## Memory

Before classifying a task or making a decision, read the index and the memories relevant to it. At completion, save durable findings that a future agent cannot readily recover from code or existing documentation. Each memory covers one fact, explains when it applies, and cites a dated source. Update an existing memory before adding a duplicate; mark outdated claims as superseded.

Keep one link and a short trigger per memory in the index. In the run record's Memories section, link findings added or changed and any memory that changed the run's decisions. When the index becomes hard to navigate or contains contradictions, suggest consolidation under the project's workflow. Memory setup and consolidation do not require another installed skill.
