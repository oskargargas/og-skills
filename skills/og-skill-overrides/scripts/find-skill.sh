#!/usr/bin/env bash
# Locate an installed skill by name across the usual agent skill directories.
#
# Usage: find-skill.sh <skill-name> [project-root]
#
# Prints one line per match: "<name>\t<path-to-SKILL.md>".
# When nothing matches exactly, prints "NOMATCH" and then close names
# (prefix, substring, or small edit distance) so the caller can suggest
# a correction. Exit 0 on exact match, 1 otherwise.
set -euo pipefail

name="${1:?skill name required}"
root="${2:-$PWD}"
home="${HOME}"
claude_home="${CLAUDE_CONFIG_DIR:-$home/.claude}"
codex_home="${CODEX_HOME:-$home/.codex}"

dirs=(
  "$root/.agents/skills"
  "$root/.claude/skills"
  "$root/.codex/skills"
  "$root/.cursor/skills"
  "$home/.agents/skills"
  "$claude_home/skills"
  "$codex_home/skills"
  "$home/.cursor/skills"
  "$home/.gemini/skills"
  "$home/.copilot/skills"
)
# Claude Code plugin cache: skills live under <plugin>/<version>/skills/<name>
while IFS= read -r d; do dirs+=("$d"); done < <(find "$claude_home/plugins/cache" -maxdepth 4 -type d -name skills 2>/dev/null || true)

seen=""
all_names=()
exact=0
for d in "${dirs[@]}"; do
  [ -d "$d" ] || continue
  for s in "$d"/*/; do
    [ -f "$s/SKILL.md" ] || continue
    n="$(basename "$s")"
    real="$(cd "$s" && pwd -P)"
    if [ "$n" = "$name" ] && [ "${seen#*|$real|}" = "$seen" ]; then
      seen="$seen|$real|"
      printf '%s\t%s\n' "$n" "$real/SKILL.md"
      exact=1
    fi
    all_names+=("$n")
  done
done

[ "$exact" = 1 ] && exit 0

echo "NOMATCH"
lname="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]' | tr ' _' '--')"
printf '%s\n' "${all_names[@]}" | sort -u | awk -v q="$lname" '
function lev(a, b,   i, j, la, lb, c, d, p, m) {
  la = length(a); lb = length(b)
  for (j = 0; j <= lb; j++) d[0, j] = j
  for (i = 1; i <= la; i++) {
    d[i, 0] = i
    for (j = 1; j <= lb; j++) {
      c = (substr(a, i, 1) == substr(b, j, 1)) ? 0 : 1
      m = d[i-1, j] + 1
      if (d[i, j-1] + 1 < m) m = d[i, j-1] + 1
      if (d[i-1, j-1] + c < m) m = d[i-1, j-1] + c
      d[i, j] = m
    }
  }
  return d[la, lb]
}
{
  n = tolower($0)
  if (index(n, q) || index(q, n) || lev(n, q) <= 3) print $0
}'
exit 1
