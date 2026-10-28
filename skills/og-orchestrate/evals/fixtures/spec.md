# Eval fixture: project archive

Status: approved, not started. No run folder, branch or pull request exists for it.

## Goal

A project owner can archive a project, and an archived project leaves the project list.

## Implementation plan

### Phase 1

1. 1.1 Add `archived_at` to `projects`, with a migration.
2. 1.2 Repository: `archive(projectId)` and the list query that skips archived projects.
3. 1.3 API endpoint `projects.archive`: input, output, failure codes, access.
4. 1.4 Handler for `projects.archive`, with tests for the owner, a member and a stranger.
5. 1.5 Archive button on the project page.
6. 1.6 Confirmation dialog.
7. 1.7 End-to-end test: archive a project and see it leave the list.
8. 1.8 Documentation: the API reference and the changelog entry.
