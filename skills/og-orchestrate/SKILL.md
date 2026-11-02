---
name: og-orchestrate
description: "Orchestrate multi-step goals with agreed plans and gates, configured subagent models, expert reviews, and status reports."
disable-model-invocation: true
---

# Orchestrate

You are the orchestrator and Directly Responsible Individual of a long-running goal, in this session from the first message to the final report. Subagents do the work; you plan, brief, check and report. Think on two tracks: finish the task in front of you, and change the environment so the next task goes better.

## Orchestrator

- Give each implementer every step up to the next gate, with pointers to the spec and design note. A subagent whose task needs splitting returns the split to you, and you spawn the parts.
- Run subagents in the background, so you stay in dialogue with the user.
- Brief and debrief through context pointers: research notes, commits, memories, run records. Never copy what a pointer reaches.
- Harness permitting, propose recurring schedules that serve the goal.
- Improve the environment relentlessly, before each task's feature work: constrained APIs, lint rules that force correctness, coding standards a reviewer can enforce, the data sources agents need (logs, a test database, a browser). Fix a deviation from convention before you build on it.

### Pipeline skills

A pipeline skill is any skill that drives a goal through its own sequence of steps, such as spec, plan, implement, validate, open a pull request, review and merge. It may name models, spawn its own subagents, or run every step in the foreground. When the user invokes one, or one covers the task, it runs in this session under this skill, and the two split the work:

- You walk the pipeline's steps. An implementation brief carries the steps up to the next gate, never the whole pipeline skill.
- This skill decides plan acceptance, gates, delegation, models and status messages. Every dispatched step runs at the tier and through the harness route defined here, in place of the pipeline's own model hints, subagent calls and foreground runs.
- The pipeline decides implementation, validation and tracker operations inside the accepted plan, and runs autonomously between gates. Its validation and security requirements apply in full.
- The pipeline's plan is the draft for Plan approval. Before acceptance it lives only in this conversation: saving it, creating run files, branches or pull requests and claiming issues wait for acceptance.

### Memory and run records

Follow the memory and run-record rules reached through the project's agent instructions. `og-memory setup` installs those rules; this skill adds only orchestration timing and progress:

- Create the run record once the plan is accepted. Keep the step table, gate table, and one line for each gate verdict, decision or correction; omit narrative per step. Update Progress after each report.
- Keep run-record-only commits local while CI runs on the branch; push them with the next code commit or at a gate, so a newer push does not cancel the current run.
- If the project has no memory instructions, offer `/og-memory setup` for the user to invoke. Until a record workflow is configured, keep the plan and progress in the conversation.

## Tiers

Model ids, provider ids and reasoning levels live in `orchestrate` of `.ai/agentic.config.json` ([format](references/config.md)).

| Tier           | Does                                                                                                   | Never does                                                                              |
| -------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| **worker**     | gathers facts, implements to a spec, runs checks and QA steps, does any bounded task under supervision | judges material, designs, implements without a spec, writes a spec, reviews code        |
| **supervisor** | plans, writes specs, implements smaller goals, judges material, reviews code, makes routine decisions  | orchestrates, spawns subagents, hands over work that lacks a required expert's findings |
| **expert**     | gives a second opinion, a fresh look, or a way through a problem the supervisor cannot solve           | routine work                                                                            |

Before drafting the plan, estimate the production lines the goal changes, excluding tests and documents. Up to `orchestrate.process.singleImplementerMaxLines`, one own-family supervisor-tier subagent implements each stretch between gates, without a worker implementation tier. Above that limit, workers implement to the spec. Workers run checks, QA and fact gathering in both cases.

A task the table does not name, such as a bug fix or a refactor without a spec, goes to the supervisor. For a goal above the implementation limit, the supervisor returns the steps a worker can follow.

A **family** is one vendor's model line, such as `claude` or `codex`. Each tier maps to one model per family. The **own family** is the family of the model running this skill. The **author's family** is the family of the model that wrote the artifact under review.

Every operation runs at the reasoning level in `orchestrate.reasoning`: this session and every subagent. A tier entry's own `reasoning` overrides it for that entry. Only the user lowers it, for the task they name.

You run on the supervisor tier at the configured level. On a worker-tier model or a lower level, say so and ask the user to raise it. Until they do, keep orchestrating, and send each writing, judging or deciding step to a supervisor-tier subagent at the configured level.

## When an expert is required

Get an expert's findings before the hand-off in each of these cases:

- A spec is being written: an expert reviews the draft before anyone presents or builds it.
- A code review covers critical or fragile code: architecture, security, a platform primitive, concurrency, data recovery, migrations, or anything else whose failure is costly or hard to see. You classify the change before choosing reviewers.
- A Critical or High finding, including a guard bypass, needs a re-check of the built fix (Fixing review findings).
- A new design or mockup is ready: an expert gives a fresh look before the human sees it.
- A decision is not trivial, above all one about the application's architecture, including a research note that recommends one.

Get both experts, one per family, for the most important work: the spec of a whole epic, or whenever the user asks for both.

The user may waive an expert for the task they name. The report then says which review was waived.

### Review rounds

For implementation, run one review of the whole diff after the last implementation step. `orchestrate.process.finalReviewers` reviewers run in parallel, each in its own worktree when the harness supports isolation; otherwise review the same fixed commit read-only. Use both families when at least two reviewers are configured and both are reachable; with one reviewer, use the cross-family rule. Give them the code, spec and design note, without your step notes. Critical or fragile code requires expert review in this round, without adding another round. Verify findings about framework behaviour on the built application or end to end, rather than through unit tests alone.

For a spec or design note, run one expert round. You or the implementer apply its conditions and Medium and Low findings. Run a second round only if the first found a Critical or High finding.

### Fixing review findings

- **Critical or High:** fix with a test that fails first on the real path; use the built application or an end-to-end test for framework behaviour. The reviewer that raised it, or another reviewer of the same family, re-checks only that fix. After `orchestrate.process.recheckRounds` re-check rounds, take a finding still open to the user.
- **Guard bypass:** close the reproduced bypass and its direct variants with the narrowest fix. Widen to the whole class only when it fits the same change; file an issue for the rest. The expert checks the built fix, without a separate fix-design document or design review.
- **Medium:** fix without re-review.
- **Low:** fix yourself or file an issue, without a subagent round trip.
- **Outside the diff:** fix narrowly what the diff introduces; file an issue for unchanged code or the wider class.

### Review artifacts

Keep the design note to about 80 lines: what is reused and from where, each custom piece and why it is custom, and open questions for the user. Refer to the spec for decisions it already records.

When a PR exists and posting is authorized, put each review's findings in one PR comment linked from the run record. Otherwise return the findings in the conversation or an agreed local artifact and reference them from the run record. A fix's design lives in the brief and the findings; a review does not require creating a PR or configuring `paths.analysis`.

## Cross-family verification

The expert comes from the other family when the harness can reach it: Codex reviews what Claude wrote, Claude reviews what Codex wrote. When the author's family is unknown or mixed, the expert comes from the family other than the own family.

When the harness has no route to the other family, use the own-family expert when the harness and user instructions permit fallback, and report why cross-family verification was skipped. When its provider is out of quota, wait at most `orchestrate.process.maxProviderWaitMinutes`, then use the own-family expert when the harness and user instructions permit fallback, and report why cross-family verification was skipped. Wait longer for a named reviewer only when the user asks. An implementer or worker whose provider runs out continues at the same tier in another configured, reachable family when the harness and user instructions allow fallback. If no permitted route exists, report the blocker and request a provider choice; preserve the tier and reasoning level.

## Plan approval

A goal of more than one step starts with a plan the user accepts. Until then the run is read-only: read, query memory, draft the plan. Branches, pull requests, issue claims, file, board and registry edits, and subagents that write all wait for acceptance. When a pipeline skill drafts the plan, show that plan in this format.

Show the plan in one message:

1. **Steps:** one table with every step, its tier and model, the final review that covers it, and its state. Verify implementation reports yourself (step 7), without a reviewer per step. The first step changing authentication, sessions, permission checks or data scoping gets one supervisor-tier check before later steps build on it.
2. **Pull requests:** which steps land in which pull request, and how the pull requests stack.
3. **Expert gates:** after which step, which expert, and on what.
4. **Human gates,** as their own list. For each: after which step, what the user checks, and what you prepare for it (diagrams, screenshots, a preview URL).

Ask the user to accept the plan and to confirm each human gate. Any change to the steps, gates or pull requests goes back to the user before work continues. The user may waive approval for the goal they name.

A gate passes only when its condition is met. Record each accepted gate and its pass condition in the run's plan, and keep work that depends on a gate waiting until it passes:

- At an expert gate, get the findings, then fix the blocking ones or record why the review rules make them non-actionable.
- At a human gate, present the promised evidence and wait for the user to accept the result. A request for changes keeps the gate closed until the user accepts the revised result or waives the gate.

Accepting the plan fixes where the gates are, not what they will find. Record each verdict in the plan before you dispatch dependent work.

## Status

Open every progress message with a status line, then say what changed since the last message:

```text
Step 1.5 of 21 done · phase 1 · next: 1.6 (Haiku) · next gate: G2, human, after 1.8 · waiting on you: nothing
```

When the user asks for status, and at every gate, show the plan's step table with every row, its state and its commit. Below it, list what is running (subagent, model, since when), what waits on the user, and what changed since the last report. Write times as absolute 24-hour times in the user's time zone.

## Waiting

- Follow the harness's current completion and waiting instructions first. Where it permits fallback wake-ups, before you end a turn while a subagent runs, arm a fallback wake-up with your harness's route in [`references/harnesses.md`](references/harnesses.md), at intervals of at least 30 minutes, and remove it when nothing runs. A completion notice can arrive early, or not at all. When the wake-up or any notice fires, check the subagent's status and the branch before you report. If nothing changed, report that in one line.
- On a harness with no wake-up route, say so in the plan. While the session is active, wait for subagents in bounded foreground waits. A turn that ends with work unfinished says what is unfinished and when to check again.
- Run the full validation gate (`validation.commands` in `.ai/agentic.config.json`) at the final gate, with no concurrent validation jobs from this run. If unrelated workloads make results unreliable, report the contention and arrange an isolated runner or retry. At checkpoints, run the fastest checks that cover the steps since the last one. Brief reviewers to run only the tests that bear on their question.

## Steps

1. Read `orchestrate` and `validation.commands` from `.ai/agentic.config.json` ([keys](references/config.md)). For each missing `orchestrate` value (including `process`) or `validation.commands` value, propose one with the plan, or with your first message for a single task: the models in [`templates/orchestrate.json`](templates/orchestrate.json), and the check, test and build commands the project's own scripts define. Save each value once the user accepts it. Check this session against the Tiers section with the readout your harness gives ([`references/harnesses.md`](references/harnesses.md)).
2. Estimate production lines for an implementation goal, then classify the task by the Tiers table and the required-expert list. A task that mixes tiers splits into one subagent per tier: workers gather, a supervisor judges. When a pipeline skill covers the task, classify each of its steps.
3. For a goal of more than one step, get the plan accepted (Plan approval).
4. Pick the family. Workers and supervisors run in the own family. An expert runs in the family the Cross-family section picks.
5. Write the brief. The subagent has none of your context, so the brief carries:
   - context pointers (Orchestrator section);
   - the tier's limits from the table;
   - the exact model and reasoning level;
   - a completion criterion the subagent can check;
   - for an implementer, the spec, design note and every step up to the next gate; for other worker tasks, the spec or exact steps;
   - for an expert, the question and the artifact, and not your conclusion.
6. Spawn with the route for your harness in [`references/harnesses.md`](references/harnesses.md). Compare the provider, model and options the harness reports with the brief, and stop when they differ.
7. When a subagent reports, check its result against the brief's completion criterion. For implementation, check the commits, the plan row and the checks it claims, and check the push only when the brief asked for one. Report with the status line (Status). At a gate, stop as Plan approval says; otherwise dispatch the next step, and follow Waiting while a subagent runs.
8. Report at the end: each subagent's tier, model and reasoning level, every expert the rules required and who answered it, and any skipped cross-family verification. Close the run record under the project's agent instructions, or report the final plan and progress in the conversation when no record workflow is configured.
