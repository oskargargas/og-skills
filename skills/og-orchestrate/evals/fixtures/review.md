# Eval fixture: expert review of a1b2c3d..e4f5a6b

Reviewer: gpt-6-astra, reasoning high, read-only.

## Findings

### Low

1. `src/db/projects.ts:42`: the list query sorts by `name` without a tie-breaker, so two projects with one name can swap places between pages. Fix: add `id` as the second sort key.
2. `src/api/projects.ts:18`: the `projects.archive` documentation example omits the `not-found` failure. Fix: add it to the example.

Verdict: approve with fixes. Counts: critical 0, high 0, medium 0, low 2.
