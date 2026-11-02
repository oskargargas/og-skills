"""Exercise setup in temporary projects, including content preservation."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/setup.py'


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='memory setup ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_setup(self, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--root', str(self.root), *args],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode == 0, ok, result.stderr)
        return result

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def write_config(self, value):
        path = self.root / '.ai/agentic.config.json'
        path.parent.mkdir()
        path.write_text(json.dumps(value))

    def check_links(self, document):
        for destination in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            self.assertTrue((document.parent / unquote(destination)).exists(), destination)

    def test_default_layout_preview_apply_and_repeat(self):
        self.run_setup()
        self.assertEqual(self.snapshot(), {})
        self.run_setup('--apply')
        self.assertTrue((self.root / '.ai/runs/.gitkeep').is_file())
        self.assertTrue((self.root / '.ai/memories/.gitkeep').is_file())
        self.check_links(self.root / '.ai/MEMORY.md')
        self.check_links(self.root / 'AGENTS.md')
        config = json.loads((self.root / '.ai/agentic.config.json').read_text())
        self.assertEqual(config, {'version': 1, 'paths': {
            'runs': '.ai/runs', 'memory': '.ai/memories', 'memoryIndex': '.ai/MEMORY.md'}})
        before = self.snapshot()
        self.run_setup('--apply')
        self.assertEqual(self.snapshot(), before)

    def test_existing_content_and_custom_paths_survive(self):
        self.write_config({'version': 1, 'tracker': 'custom', 'paths': {
            'runs': 'records/runs', 'memory': 'knowledge/my memories',
            'memoryIndex': 'indexes/recall.md', 'specs': 'requirements'}})
        index = self.root / 'indexes/recall.md'
        index.parent.mkdir()
        index.write_text('# Existing index\n\nKeep this entry.\n')
        (self.root / 'AGENTS.md').write_text('# Project\n\nKeep this instruction.\n')
        (self.root / 'CLAUDE.md').write_text('# Claude\n\nKeep this too.\n')
        config_before = (self.root / '.ai/agentic.config.json').read_bytes()
        self.run_setup('--apply')
        self.assertEqual((self.root / '.ai/agentic.config.json').read_bytes(), config_before)
        self.assertEqual(index.read_text(), '# Existing index\n\nKeep this entry.\n')
        self.assertIn('Keep this instruction.', (self.root / 'AGENTS.md').read_text())
        self.assertIn('Keep this too.\n\n@AGENTS.md', (self.root / 'CLAUDE.md').read_text())
        self.assertTrue((self.root / 'knowledge/my memories/.gitkeep').exists())
        before = self.snapshot()
        self.run_setup('--apply')
        self.assertEqual(self.snapshot(), before)

    def test_nested_instruction_and_separate_index_links(self):
        self.write_config({'paths': {'memory': 'facts with spaces', 'memoryIndex': 'indexes/deep/recall.md'}})
        self.run_setup('--instruction-file', 'instructions/AGENTS.md', '--apply')
        self.check_links(self.root / 'instructions/AGENTS.md')
        self.check_links(self.root / 'indexes/deep/recall.md')

    def test_claude_only_project(self):
        (self.root / 'CLAUDE.md').write_text('# Existing Claude rules\n')
        self.run_setup('--apply')
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.check_links(self.root / 'CLAUDE.md')

    def test_absolute_store_paths(self):
        self.write_config({'paths': {
            'runs': str(self.root / 'absolute runs'),
            'memory': str(self.root / 'absolute memories'),
            'memoryIndex': str(self.root / 'absolute index/recall.md'),
        }})
        self.run_setup('--apply')
        self.assertTrue((self.root / 'absolute runs/.gitkeep').exists())
        self.check_links(self.root / 'absolute index/recall.md')

    def test_refresh_keeps_surrounding_instructions(self):
        self.run_setup('--apply')
        instructions = self.root / 'AGENTS.md'
        instructions.write_text('Before\n\n' + instructions.read_text().replace('## Memory and run records', '## Outdated') + '\nAfter\n')
        self.run_setup('--apply')
        text = instructions.read_text()
        self.assertTrue(text.startswith('Before\n'))
        self.assertTrue(text.endswith('\nAfter\n'))
        self.assertNotIn('## Outdated', text)
        self.assertEqual(text.count('<!-- og-memory:start'), 1)

    def test_refresh_preserves_project_format_links(self):
        self.run_setup('--apply')
        instructions = self.root / 'AGENTS.md'
        custom = '- Formats: [Run records](.ai/README.md#run-records), [Memories](.ai/README.md#memories).'
        text = re.sub(r'(?m)^- Formats:.*$', lambda _: custom, instructions.read_text())
        text = text.replace('## Memory and run records', '## Outdated')
        instructions.write_text('- Formats: unrelated instructions.\n\n' + text)
        before = self.snapshot()
        self.run_setup()
        self.assertEqual(self.snapshot(), before)
        self.run_setup('--apply')
        refreshed = instructions.read_text()
        self.assertIn(custom, refreshed)
        self.assertIn('- Formats: unrelated instructions.', refreshed)
        self.assertIn('## Memory and run records', refreshed)
        self.assertNotIn('## Outdated', refreshed)
        before = self.snapshot()
        self.run_setup('--apply')
        self.assertEqual(self.snapshot(), before)

    def test_refresh_updates_generated_format_reference(self):
        self.run_setup('--apply')
        instructions = self.root / 'AGENTS.md'
        current = instructions.read_text()
        reference = re.search(r'\[how it works\]\(([^)]+)\)', current).group(1)
        instructions.write_text(current.replace(reference, '../old-install/references/memory.md'))
        self.run_setup('--apply')
        self.assertEqual(instructions.read_text(), current)

    def test_malformed_block_does_not_write_anything(self):
        (self.root / 'AGENTS.md').write_text('<!-- og-memory:start -->\nunfinished\n')
        before = self.snapshot()
        self.run_setup('--apply', ok=False)
        self.assertEqual(self.snapshot(), before)

    def test_invalid_config_does_not_write_anything(self):
        self.write_config({'paths': {'memory': ''}})
        before = self.snapshot()
        self.run_setup('--apply', ok=False)
        self.assertEqual(self.snapshot(), before)

    def test_colliding_paths_do_not_write_anything(self):
        self.write_config({'paths': {'memoryIndex': '.ai/agentic.config.json'}})
        before = self.snapshot()
        self.run_setup('--apply', ok=False)
        self.assertEqual(self.snapshot(), before)

    def test_parent_file_conflict_does_not_write_anything(self):
        self.write_config({'paths': {'runs': 'blocked/runs'}})
        (self.root / 'blocked').write_text('Keep this file.')
        before = self.snapshot()
        self.run_setup('--apply', ok=False)
        self.assertEqual(self.snapshot(), before)


if __name__ == '__main__':
    unittest.main()
