# Help

Show this to the user verbatim when they invoke the skill with no argument and no skill is being applied, or with `help`.

```
og-skill-overrides: customise installed skills per project without editing them.

Overrides live at .ai/skills/<skill-name>/SKILL.md and are applied on top of
the installed skill. Safety rules in the installed skill always win.

Usage: /og-skill-overrides <command> [args]

  help                              this text
  setup                             wire this project: AGENTS.md rule, .ai/ folders,
                                    optional .ai/agentic.config.json, optional agent hooks
  update                            rerun setup; refreshes the AGENTS.md block from the
                                    installed skill version
  override <skill-name> <change>    create or extend .ai/skills/<skill-name>/SKILL.md
                                    e.g. override code-review "also look for specs in .ai/spec"
  hooks [agent ...]                 add a deterministic hook that injects overrides;
                                    built in: claude, codex. Other agents: researched on request

Shared values (a specs folder, a tracker URL, ...) are offered for
.ai/agentic.config.json when an override needs them, so later overrides can
read them from one place.
```

After showing it, ask which command to run, or do the obvious one when the request already says.
