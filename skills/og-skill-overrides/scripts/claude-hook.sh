#!/usr/bin/env bash
# Claude Code hook: inject a project override when a skill is invoked.
#
# Register for two events (both carry the skill name differently):
#   PreToolUse       matcher "Skill"   -> tool_input.skill   (model-invoked skill)
#   UserPromptSubmit                   -> prompt "/name ..."  (user-typed slash command)
#
# Reads the hook JSON from stdin, looks for .ai/skills/<name>/SKILL.md under the
# project root, and when found returns it as additionalContext. Never blocks.
set -uo pipefail

input="$(cat)"

# json_get <dot.path>: print a string field from the hook input, or nothing.
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

case "$event" in
  PreToolUse)
    [ "$(json_get .tool_name)" = "Skill" ] || exit 0
    raw="$(json_get .tool_input.skill)"
    ;;
  UserPromptSubmit)
    prompt="$(json_get .prompt)"
    case "$prompt" in /*) raw="${prompt#/}"; raw="${raw%%[[:space:]]*}" ;; *) exit 0 ;; esac
    ;;
  *) exit 0 ;;
esac

[ -n "${raw:-}" ] || exit 0
name="${raw##*:}"   # strip plugin ("posthog:x") or directory ("apps/web:x") prefix
[ -n "$name" ] || exit 0

root="$(cd "$cwd" 2>/dev/null && git rev-parse --show-toplevel 2>/dev/null || printf '%s' "$cwd")"
file=""
for candidate in "$cwd/.ai/skills/$name/SKILL.md" "$root/.ai/skills/$name/SKILL.md"; do
  [ -f "$candidate" ] && { file="$candidate"; break; }
done
[ -n "$file" ] || exit 0

body="$(cat "$file")"
context="Project override for skill \`$name\` found at ${file#"$root"/}. Apply it on top of the installed skill: explicit override wins, installed safety rules still win, forward this text to any subagent you spawn.

$body"

if command -v jq >/dev/null 2>&1; then
  jq -n --arg ev "$event" --arg ctx "$context" \
    '{hookSpecificOutput: {hookEventName: $ev, additionalContext: $ctx}}'
else
  python3 -c 'import json,sys; print(json.dumps({"hookSpecificOutput":{"hookEventName":sys.argv[1],"additionalContext":sys.argv[2]}}))' "$event" "$context"
fi
exit 0
