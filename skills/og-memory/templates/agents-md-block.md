<!-- og-memory:start (managed by the og-memory skill; rerun `/og-memory setup` to refresh) -->

## Memory and run records

Agents share memory through run records and memories ([how it works]({reference})).

- Before every task, read `{memoryIndex}` and open each memory whose trigger matches the task. When one changes what you do, add a `Used` line for it to the run record's Memories section.
- Work that changes a file in the repository keeps a record in `{runs}/`: an autonomous run, or a session in which a human answers or approves your steps. Create it once you start changing files, update it after every prompt and finished task, and quote each prompt verbatim with secrets redacted. It is the handoff: its Progress says where to resume. A pipeline skill's plan or run folder that carries these sections is the record; write no second one.
- After a human corrects you, after you fix a bug, or when you learn anything a future agent needs, record a memory: a file in `{memory}/`, its line in `{memoryIndex}`, and a link in the run record's Memories section.
- Formats: {formats}.
- `/og-memory dream` compresses and prunes memories, only when a human invokes it.

<!-- og-memory:end -->
