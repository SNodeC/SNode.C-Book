#!/usr/bin/env python3
"""Regression checks for final editorial guards and valid Markdown variants."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('final', HERE/'check-final.py')
final = importlib.util.module_from_spec(spec)
spec.loader.exec_module(final)


class FinalGuards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT/'manuscript', self.root/'manuscript')
        allow = HERE.relative_to(ROOT)/'terminology-allowlist.md'
        (self.root/allow).parent.mkdir(parents=True)
        shutil.copy2(ROOT/allow, self.root/allow)

    def chapter(self, n):
        return next((self.root/'manuscript/chapters').glob(f'{n:02}-*'))

    def replace(self, path, old, new):
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def fails(self, message):
        self.assertTrue(any(message in e for e in final.check(self.root)))

    def test_current_manuscript_including_wrapped_pointers_passes(self):
        self.assertEqual(final.check(self.root), [])

    def test_connection_model_is_not_connection_mode(self):
        p = self.chapter(7)
        p.write_text(p.read_text()+'\nThe connection model remains useful.\n')
        self.assertEqual(final.check(self.root), [])

    def test_actual_connection_mode_is_rejected(self):
        p = self.chapter(7)
        p.write_text(p.read_text()+'\nSelect the connection mode.\n')
        self.fails('old terminology: connection mode')

    def test_wrong_introduction(self):
        p = next((self.root/'manuscript/chapters').glob('appendix-*'))
        self.replace(p, 'source-reading introduction in Chapter 5', 'source-reading introduction in Chapter 4')
        self.fails('stale introduction')

    def test_wrong_instance(self):
        self.replace(self.chapter(13), 'echoserver local --port 8080', 'echo local --port 8080')
        self.fails('wrong instance command')

    def test_role_allowance_is_occurrence_specific(self):
        p = self.chapter(16)
        p.write_text(p.read_text()+'\nThe role has operational needs.\n')
        self.fails('role inventory')

    def test_recap_needs_three_bullets(self):
        self.replace(self.chapter(5), '- The runtime advances', 'The runtime advances')
        self.fails('three recap bullets')

    def test_note_label_is_required(self):
        self.replace(self.chapter(20), 'title="Build note"', 'title="Aside"')
        self.fails('Build note box missing')

    def test_pointer_cannot_have_content_after_it(self):
        self.replace(self.chapter(13), '`companion/exercises/ch13/README.md`.\n:::',
                     '`companion/exercises/ch13/README.md`.\n\nMore exercise content.\n:::')
        self.fails('last exercise content')

    def test_pointer_can_wrap_without_changing_its_paragraph(self):
        self.replace(self.chapter(13), 'are in `companion/exercises/', 'are in\n`companion/exercises/')
        # Refreshing line numbers is irrelevant here: Ch13 has no subsequent role.
        self.assertEqual(final.check(self.root), [])

    def test_illustrative_label_required(self):
        self.replace(self.chapter(26), 'Illustrative role map — not SNode.C configuration syntax', 'Role map')
        self.fails('illustrative label missing')

    def test_copied_lab_does_not_count_as_synthesis(self):
        import re
        source = self.chapter(4).read_text()
        old = re.search(r'^3\. (.*)$', source, re.M)[1]
        p = self.chapter(32)
        p.write_text(re.sub(r'^3\. .*$', '3. '+old, p.read_text(), count=1, flags=re.M))
        self.fails('repeated earlier question')

    def test_div_parser_ignores_code_and_preserves_nested_boxes(self):
        text = ('::: {.snodec-exercise title="Exercises"}\n'
                '```text\n::: {.fake}\n::: \n```\n'
                '::: {.snodec-note}\nNote.\n:::\n'
                'Public answers: `companion/exercises/ch01/README.md`.\n:::\n')
        boxes = list(final.divs(text))
        self.assertEqual(len(boxes), 2)
        self.assertIn('.snodec-exercise', boxes[-1][0])


if __name__ == '__main__':
    unittest.main()
