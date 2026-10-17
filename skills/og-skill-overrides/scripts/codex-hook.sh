#!/usr/bin/env bash
# Codex CLI hook: inject a project override when a skill is used.
#
# Codex has no skill tool for local skills: the model reads SKILL.md from disk
# with the shell tool, and users invoke a skill explicitly with "$name" in the
# prompt. Register for both:
#   PreToolUse       matcher "^Bash$"  -> tool_input.command mentions .../skills/<name>/SKILL.md
#   UserPromptSubmit                   -> prompt contains "$name"
#
# Reads the hook JSON from stdin, looks for .ai/skills/<name>/SKILL.md under the
# project root, and when found returns it as hookSpecificOutput.additionalContext
# (PreToolUse ignores plain stdout, so JSON is used for both). Never blocks.
set -uo pipefail

input="$(cat)"

json_get() {
  if command -v jq >/dev/null 2>&1; then
    printf '%s' "$input" | jq -r "$1 // empty" 2>/dev/null
  else
    printf '%s' "$input" | python3 -c '
import json, sys
data = json.load(sys.stdin)
for p in sys.argv[1].strip(".").split("."):
    data = data.get(p) if isinstance(data, dict) else None
print(data if isinstance(data, str) else "")' "$1" 2>/dev/null
  fi
}

event="$(json_get .hook_event_name)"
cwd="$(json_get .cwd)"
[ -n "$cwd" ] || cwd="$PWD"
cwd="$(cd "$cwd" 2>/dev/null && pwd -P || printf '%s' "$cwd")"

names=""
case "$event" in
  PreToolUse)
    [ "$(json_get .tool_name)" = "Bash" ] || exit 0
    cmd="$(json_get .tool_input.command)"
    # every ".../skills/<name>/SKILL.md" mentioned in the command
    names="$(printf '%s\n' "$cmd" | grep -oE 'skills/[A-Za-z0-9._-]+/SKILL\.md' | sed -E 's#skills/([^/]+)/SKILL\.md#\1#' | sort -u)"
    ;;
  UserPromptSubmit)
    prompt="$(json_get .prompt)"
    names="$(printf '%s\n' "$prompt" | grep -oE '(^|[^A-Za-z0-9_])\$[A-Za-z0-9._-]+' | sed -E 's#.*\$##' | sort -u)"
    ;;
  *) exit 0 ;;
esac

[ -n "$names" ] || exit 0

root="$(cd "$cwd" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || printf '%s' "$cwd")"
context=""
while IFS= read -r name; do
  [ -n "$name" ] || continue
  [ "$name" = "og-skill-overrides" ] && continue
  file=""
  for candidate in "$cwd/.ai/skills/$name/SKILL.md" "$root/.ai/skills/$name/SKILL.md"; do
    [ -f "$candidate" ] && { file="$candidate"; break; }
  done
  [ -n "$file" ] || continue
  context="${context}Project override for skill \`$name\` found at ${file#"$root"/}. Apply it on top of the installed skill: explicit override wins, installed safety rules still win, forward this text to any subagent you spawn.

$(cat "$file")

"
done <<< "$names"

[ -n "$context" ] || exit 0

if command -v jq >/dev/null 2>&1; then
  jq -n --arg ev "$event" --arg ctx "$context" \
    '{hookSpecificOutput: {hookEventName: $ev, additionalContext: $ctx}}'
else
  python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":sys.argv[1],"additionalContext":sys.argv[2]}}))' "$event" "$context"
fi
exit 0
