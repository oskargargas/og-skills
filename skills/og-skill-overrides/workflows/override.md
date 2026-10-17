# Override a skill

Create or extend `.ai/skills/<skill-name>/SKILL.md` so an installed skill behaves differently in this project. Input: a skill name and a description of the change, from the argument or from the conversation.

## 1. Resolve the skill

Run `scripts/find-skill.sh <skill-name> <project-root>` (path relative to this skill's folder).

- Exact match: note the SKILL.md path. Read it. You need the step the change touches, and the skill's safety rules, so the override names real steps and stays inside the [contract](../references/contract.md).
- `NOMATCH` with suggestions: tell the user the name was not found and offer the closest suggestion ("Did you mean `code-review`?"). Use it once they confirm, or when the typo is unambiguous and you say which name you took.
- `NOMATCH` with no suggestions: say the skill is not installed for this user and stop. An override for an absent skill never fires.

## 2. Turn the request into a patch

Write the change as a patch against the installed skill, not a rewrite:

- Name the step it touches, using the installed skill's own heading or step number ("Step 2, Identify the spec source").
- State the addition or replacement in one or two sentences. One bullet per change; no restating what the installed skill already does.
- Do not restate the merge rule (override wins where explicit, safety rules still win). The `AGENTS.md` block and the hooks carry it; the override file holds only the changes.
- Check the change against the safety floor in the contract. A change that would weaken it is refused with one line explaining why, and the rest of the override is still written.

## 3. Pull shared values into the config

This is the only place config keys are proposed. Anything in the change that looks shared (a folder, a URL, a label vocabulary, a tracker, a branch name) belongs in `.ai/agentic.config.json`, so a second override can reuse it. Propose only the values this change uses. The format is in [`setup.md`](setup.md) under "Config".

- Config exists and already holds the value: reference it in the override by key ("the folder in `paths.specs` of `.ai/agentic.config.json`"). Never write the current value next to the key; the value can change and the override must not go stale.
- Config exists without the value: offer to add it. On yes, add the key and reference it. On no, inline the value.
- No config: offer to create it from [`templates/agentic.config.json`](../templates/agentic.config.json) with this value added. On no, inline the value.

## 4. Write the file

- New override: fill [`templates/override-skill.md`](../templates/override-skill.md). `{{changes}}` is the patch from step 2, `{{config-refs}}` lists each config key the override uses, one line each: what it holds and any convention the change relies on (a subfolder, a file-name pattern). Drop the section when there are none. No prose outside the two sections.
- Existing override: read it, add the change under `## Changes` without rewriting the rest, and keep its config section in sync.

Show the resulting file to the user before writing.

## 5. Check the wiring

Done when the file exists and the project is wired: `AGENTS.md` carries the `og-skill-overrides` block. When it does not, say so and offer `setup`. Without the block, only agents whose always-loaded skill description mentions overrides will find the file.

Example, from the request "make code-review also look in `.ai/spec` for specs":

```markdown
---
name: code-review
extends: code-review
description: Project override applied on top of the installed `code-review` skill.
---

## Changes

- Step 2, Identify the spec source: also search the folder in `paths.specs` of `.ai/agentic.config.json` for a file matching the branch name or feature, with the same priority as `docs/`, `specs/`, and `.scratch/`.

## Shared values

- `paths.specs` in `.ai/agentic.config.json`: this project's feature specs folder.
```
