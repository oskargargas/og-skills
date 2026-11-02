#!/usr/bin/env python3
"""Preview or apply the shared memory layout using only the Python standard library."""

import argparse
import json
import os
from pathlib import Path
import re
from urllib.parse import quote


SKILL = Path(__file__).resolve().parents[1]
DEFAULTS = {
    "runs": ".ai/runs",
    "memory": ".ai/memories",
    "memoryIndex": ".ai/MEMORY.md",
}
START = "<!-- og-memory:start"
END = "<!-- og-memory:end -->"


def link(target, document):
    return quote(Path(os.path.relpath(target, document.parent)).as_posix(), safe="/.")


def plan_setup(root, instruction_file=None):
    """Return proposed file contents. Validate everything before writing anything."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"Project directory does not exist: {root}")
    config_path = root / ".ai/agentic.config.json"
    config = json.loads(config_path.read_text()) if config_path.exists() else {"version": 1}
    if not isinstance(config, dict):
        raise ValueError("Configuration must be an object")
    paths = config.setdefault("paths", {})
    if not isinstance(paths, dict):
        raise ValueError("Configuration paths must be an object")
    for key, default in DEFAULTS.items():
        paths.setdefault(key, default)
        if not isinstance(paths[key], str) or not paths[key].strip():
            raise ValueError(f"paths.{key} must be a nonempty path")
    resolved = {key: (root / paths[key]).resolve() for key in DEFAULTS}
    runs, memory, index = (resolved[key] for key in DEFAULTS)
    if runs == memory or index == runs or index == memory:
        raise ValueError("Runs, memories and index must use distinct paths")
    for folder in (runs, memory):
        if folder.exists() and not folder.is_dir():
            raise ValueError(f"Expected a folder: {folder}")
    if index.exists() and not index.is_file():
        raise ValueError(f"Expected an index file: {index}")

    if instruction_file:
        instructions = root / instruction_file
    else:
        instructions = next(
            (root / name for name in ("AGENTS.md", "CLAUDE.md") if (root / name).exists()),
            root / "AGENTS.md",
        )
    instructions = instructions.resolve()
    outputs = (config_path, instructions, index, runs / ".gitkeep", memory / ".gitkeep")
    if len(set(outputs)) != len(outputs):
        raise ValueError("Configuration, instructions, index and folder placeholders must use distinct files")
    for path in outputs:
        for parent in path.parents:
            if parent in outputs or (parent.exists() and not parent.is_dir()):
                raise ValueError(f"Expected a parent folder: {parent}")
    reference = SKILL / "references/memory.md"
    block = (SKILL / "templates/agents-md-block.md").read_text().strip()
    values = {key: paths[key] for key in ("runs", "memory", "memoryIndex")}
    values.update(reference=link(reference, instructions), formats=f"[Memory and run records]({link(reference, instructions)})")
    for key, value in values.items():
        block = block.replace("{" + key + "}", value)
    original = instructions.read_text() if instructions.exists() else ""
    if START in original or END in original:
        if original.count(START) != 1 or original.count(END) != 1:
            raise ValueError("Expected exactly one complete og-memory block")
        pattern = re.compile(r"<!-- og-memory:start[^\n]*-->.*?<!-- og-memory:end -->", re.S)
        if not pattern.search(original):
            raise ValueError("Malformed og-memory block")
        updated = pattern.sub(lambda _: block, original)
    else:
        updated = (original.rstrip() + "\n\n" if original.strip() else "") + block + "\n"

    proposals = {instructions: updated}
    # Avoid rewriting an existing config solely to change its formatting.
    if not config_path.exists() or json.loads(config_path.read_text()) != config:
        proposals[config_path] = json.dumps(config, indent=2) + "\n"
    for folder in (runs, memory):
        keep = folder / ".gitkeep"
        if not keep.exists():
            proposals[keep] = ""
    if not index.exists():
        proposals[index] = (
            f"# Memory\n\nOne line per memory in [the memory folder]({link(memory, index)}/). "
            f"Format and rules: [Memory and run records]({link(reference, index)}).\n"
        )
    # Preserve Claude instructions while making the shared AGENTS block reachable.
    claude = root / "CLAUDE.md"
    if instructions == root / "AGENTS.md" and claude.exists():
        content = claude.read_text()
        if not re.search(r"(?m)^\s*@(?:\./)?AGENTS\.md\s*$", content):
            proposals[claude] = content.rstrip() + "\n\n@AGENTS.md\n"
    changes = {}
    for path, content in proposals.items():
        if path.exists() and not path.is_file():
            raise ValueError(f"Expected a file: {path}")
        if not path.exists() or path.read_text() != content:
            changes[path] = content
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--instruction-file", help="Chosen instruction file, relative to project root")
    parser.add_argument("--apply", action="store_true", help="Write the previewed setup")
    args = parser.parse_args()
    try:
        changes = plan_setup(args.root, args.instruction_file)
        for path, content in changes.items():
            print(f"{'Write' if args.apply else 'Would write'} {path}")
            if args.apply:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
        if not changes:
            print("Memory setup is already current.")
    except (ValueError, OSError) as error:
        parser.exit(1, f"Memory setup failed: {error}\n")


if __name__ == "__main__":
    main()
