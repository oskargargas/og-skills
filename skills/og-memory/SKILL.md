---
name: og-memory
description: Shared agent memory and run records. `setup` creates the store and its AGENTS.md block; `dream` compresses older memories and deletes the ones no longer needed.
argument-hint: "setup | dream [dry-run] [cutoff]"
disable-model-invocation: true
---

# Memory

Run the command the human named, from its file. With no command or an unknown one, list the commands and stop.

| Command | Does                                                                                                   | File                                   |
| ------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------- |
| `setup` | Create or refresh the store: config keys, folders, index, and the managed block in `AGENTS.md`.        | [commands/setup.md](commands/setup.md) |
| `dream` | One pass over older memories: promote, move, merge, compress or delete each, and keep the index short. | [commands/dream.md](commands/dream.md) |

Every command runs only when a human invokes it. The mechanism every agent follows, with or without this skill running, is in [references/memory.md](references/memory.md): read it before any command.

For `dream`, present the plan and final summary in the action groups defined in the command's [Report](commands/dream.md#7-report) section, with project-context upgrades first and deletions last. This also applies to dry runs.
