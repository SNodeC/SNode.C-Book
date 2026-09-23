#!/usr/bin/env python3
"""Regression checks for valid-but-wrong references and structural identity drift."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import shutil
import tempfile
import unittest

MODULE = runpy.run_path(str(Path(__file__).with_name('check-chapter-references.py')))
ROOT = MODULE['ROOT']
REVIEW = MODULE['REVIEW']


class ChapterReferences(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        files = ['README.md', 'STRUCTURE.md', 'manuscript/book-files.txt']
        files += (ROOT / 'manuscript/book-files.txt').read_text().splitlines()
        files += [str(p.relative_to(ROOT)) for p in (ROOT / 'companion').rglob('*.md')]
        files += [str(REVIEW / name) for name in ['smoothing-structure.json', 'smoothing-reference-register.json']]
        for name in files:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return MODULE['check'](self.root)

    def test_current_structure(self):
        register = self.root / REVIEW / 'smoothing-reference-register.json'
        data = json.loads(register.read_text())
        self.assertEqual(self.check(), len(data['references']))

    def test_missing_migration_identity(self):
        register = self.root / REVIEW / 'smoothing-reference-register.json'
        data = json.loads(register.read_text())
        data['migration_dispositions'].pop()
        register.write_text(json.dumps(data))
        with self.assertRaises(AssertionError):
            self.check()

    def test_valid_but_wrong_number_even_if_label_is_registered(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text().replace('Chapter 30', 'Chapter 29', 1))
        register = self.root / REVIEW / 'smoothing-reference-register.json'
        data = json.loads(register.read_text())
        ref = next(r for r in data['references'] if r['file'] == 'README.md' and r['text'] == 'Chapter 30')
        ref['text'] = 'Chapter 29'  # A mechanically updated label is insufficient.
        register.write_text(json.dumps(data))
        with self.assertRaisesRegex(AssertionError, 'wrong topic'):
            self.check()

    def test_unregistered_reference(self):
        path = self.root / 'README.md'
        path.write_text(path.read_text() + '\nSee Chapter 29.\n')
        with self.assertRaisesRegex(AssertionError, 'unregistered'):
            self.check()

    def test_reordered_chapters(self):
        path = self.root / 'manuscript/book-files.txt'
        lines = path.read_text().splitlines()
        indices = [i for i, name in enumerate(lines) if '/chapters/' in name]
        a, b = indices[:2]
        lines[a], lines[b] = lines[b], lines[a]
        path.write_text('\n'.join(lines) + '\n')
        with self.assertRaisesRegex(AssertionError, 'order differs'):
            self.check()

    def test_missing_topic_anchor(self):
        path = self.root / 'manuscript/chapters/05-layers-in-practice.md'
        path.write_text(path.read_text().replace('{#reading-public-types-and-components}', ''))
        with self.assertRaisesRegex(AssertionError, 'Missing/ambiguous topic'):
            self.check()


if __name__ == '__main__':
    unittest.main()
