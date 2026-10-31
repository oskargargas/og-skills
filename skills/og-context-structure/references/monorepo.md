# Monorepos

Find packages from nested instruction files or workspace manifests: `pnpm-workspace.yaml`, `package.json` `workspaces`, `turbo.json`, `nx.json`, `lerna.json`, `Cargo.toml` `[workspace]`, `go.work`, `settings.gradle*`, local packages in `Package.swift`, uv workspaces in `pyproject.toml`. List each package with its instruction files.

- Codex and Pi load no `AGENTS.md` below the launch directory; the root line naming package files is their only route.
- Check each root-to-package chain against Codex `project_doc_max_bytes`, and each package file against Claude Code's 40,000-character cut.
