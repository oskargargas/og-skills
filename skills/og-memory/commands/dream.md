# Dream

One pass over older memories. The goal is fewer, shorter memories: each one is promoted into a permanent doc, moved, merged, compressed, deleted or kept, and the index ends within its caps. Terms (memory, index, trigger, use, permanent doc) are defined in [the reference](../references/memory.md).

Arguments:

- `dry-run`: stop after step 3 and return the plan in the conversation, without changing files or branches.
- A cutoff (a date or a number of days): replaces the default of 14 days.

## 1. Open the pass

1. Read today's date from the clock. For an applied pass in a Git repository, use `chore/memory-dream-YYYY-MM-DD` unless the human chose a branch or an existing working branch should be retained. Without Git, work in the named project directory. A dry run changes no branch.
2. For an applied pass, create the run record `<paths.runs>/YYYY-MM-DD-memory-dream.md` in the project's run-record format, with the human's prompt as its Goal and secrets redacted. For a dry run, keep this information in the conversation.
3. **In scope** are the memories whose file-name date is more than 14 days before today, or before the human's cutoff. Newer memories change only as merge targets.
4. Write the index size (`wc -lc <paths.memoryIndex>`) and the number of memories in scope into the record.

Done when the record, or the dry-run response, names the cutoff, the scope count and the index size.

## 2. Count uses

For each memory in scope, count the run records that use it:

Search the configured runs folder, including untracked records, for `Used:` entries whose link resolves to that memory. Count distinct run records, not mentions. Resolve each link relative to its record; custom paths and filenames need not match the default layout. Use a filesystem search when Git is absent.

Note the date of the oldest record with a `Used` line. A memory created before it has no usage history, so its zero says nothing.

Done when every memory in scope has a count, and the record states the date usage history starts.

## 3. Plan one action per memory

Read each memory in scope, the memories that share its area or trigger, and the code or doc it describes. Read a run record or transcript only to check what a memory claims.

First compare it with its closest memory:

- **repeats**: the same rule. Merge.
- **changes**: the newer source says something different. The rule with the later source date wins, whatever order you read them in.
- **ends**: the rule stopped holding. Delete it, or compress it to what still applies.
- **unrelated**: judge it on its own.

Then pick its action:

| Action   | When                                                                                                              |
| -------- | ----------------------------------------------------------------------------------------------------------------- |
| Promote  | Its rule applies to most tasks: used in 3 or more runs across different areas. Into a permanent doc.              |
| Move     | Only one skill or package needs it: used in 3 or more runs, all there. Into that skill's or package's doc.        |
| Merge    | It repeats another memory.                                                                                        |
| Delete   | A permanent doc holds its rule, the code or docs make it obvious, it was about one finished task, or it is wrong. |
| Compress | It stays, and its file holds more than the rule, the reason and how to apply it.                                  |
| Keep     | It stays as it is.                                                                                                |
| Ask      | You cannot tell whether it still holds.                                                                           |

- Use counts point at candidates; the content decides the action.
- Age is a question, not a verdict. A memory unused for 30 days or more, with usage history, is a delete candidate: confirm against the code or docs that it no longer earns its place. When you cannot confirm it either way, plan Ask.
- Before you delete a memory because the code contradicts it, read the code.
- Keep is a full outcome. A pass that keeps everything, each with a reason, has succeeded.

Write the plan into the record, or the conversation for a dry run, as tables in the action-group order defined under [Report](#7-report): memory, use count, action, target (for promote, move and merge), reason in a few words. Use the same groups in the human-facing dry-run summary.

Done when every memory in scope has exactly one action and a reason. With `dry-run`, report the plan to the human and stop.

## 4. Apply the plan

- **Promote** and **Move**: write the rule into the target doc in that doc's own style, in the section where a reader of that doc would look for it. Then delete the memory.
- **Merge**: into the oldest file. Fold the others' Sources into its `Source` line, then delete them.
- **Compress**: keep the title sentence, `Area`, `Source`, and a body holding the rule, why it holds and how to apply it, in as few lines as carry them. Drop superseded dated lines and the story of how it was found; retain provenance needed by the project, especially when no version history exists. Keep the rule's meaning exact.
- **Delete**: remove the file and its index line.
- **Links**: memories are cited from run records, specs, ADRs, docs and code comments. For every memory you promoted, moved, merged or deleted, search project files, including untracked files, for links to that memory and point each link at the doc or memory that holds the rule now. Where nothing holds it, replace the link with plain text naming the memory and its deletion date. Leave `<commit>:` paths as they are.
- **Index**: rewrite the lines of the memories you changed, newest first. While the index exceeds 200 lines or 25 000 bytes, shorten triggers to the task or area alone. If useful entries still exceed the caps, record the remaining excess under Open ends and ask for a consolidation decision; preserve useful memories rather than deleting them to meet a size limit.

Done when every planned action except Ask is applied and the project-file search finds no link to a removed file.

## 5. Ask

Put every Ask in one message to the human: the memory, what you checked, what is unclear. Apply each answer as the action it implies. Record unanswered ones under Open ends.

Done when every Ask has an answer or sits under Open ends.

## 6. Verify

1. Resolve local Markdown links in the index and links to changed memories from project documents relative to each containing file. Check that their targets exist, including links across custom folder layouts. Record broken links present before the pass under Open ends.

2. `wc -lc <paths.memoryIndex>` is within 200 lines and 25 000 bytes.
3. Run the repository's fast check when one exists; otherwise inspect changed Markdown and verify links.

Done when the checks pass or each unresolved check is reported under Open ends. Report a partial result if the index still exceeds its caps.

## 7. Report

In the record, under What changed: the count per action, each promoted, moved, merged, compressed and deleted memory with its reason, and the index size before and after. Set its Status.

Present the plan and the human-facing summary in these groups, in order:

1. **Upgraded to project instructions**: Promote and Move. For each, show the proposed instruction, its destination file and section, and why it belongs there. In an applied pass, show the instruction actually added. If none qualify, say so explicitly.
2. **Keep**: memories retained as they are, with a short reason.
3. **Compress**: memories shortened, with the rule that remains.
4. **Merge**: duplicates combined, with their destination memory.
5. **Unresolved**: Ask entries, with what remains uncertain.
6. **Delete**: memories removed, with the reason and the existing rule location when applicable.

Give each group's count; empty groups other than upgrades may be omitted. Distinguish proposed actions in a dry run from applied changes. A useful promotion candidate that lacks the required usage evidence may be mentioned in the first group as a recommendation, clearly separate from selected Promote/Move actions. Preserve its selected action in the plan.

Leave the changes uncommitted for the human to review in the diff, unless they asked for a commit or a pull request. Reply with the counts, the index size before and after, and the open Asks.
