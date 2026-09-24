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
        source = self.chapter(6).read_text()
        block = next(t for a, _, t in final.divs(source) if '.snodec-exercise' in a)
        old = re.search(r'^4\.\s+(.*?)(?=^\d+\. |^Public |\Z)', block, re.M | re.S)[1].strip()
        p = self.chapter(32)
        p.write_text(re.sub(r'^3\. .*$', lambda _: '3. '+old, p.read_text(), count=1, flags=re.M))
        self.fails('repeated earlier question')

    def test_swapped_model_references_are_rejected(self):
        self.replace(self.chapter(32), 'observations from Chapter 6', 'observations from Chapter 4')
        self.fails('model-ownership must name Chapter 6')
        self.replace(self.chapter(32), 'Use the Chapter 4 model observations', 'Use the Chapter 6 model observations')
        self.fails('model-instances must name Chapter 4')

    def test_article_and_residual_terminology(self):
        p = self.chapter(5)
        p.write_text(p.read_text()+'\nA instance has a security mode. The role is named web.\n')
        for term in ('A instance', 'security mode', 'role is named'):
            self.fails('old terminology: '+term)

    def test_link_checks_allow_synonyms_and_soft_wrapping(self):
        self.replace(self.chapter(3), 'If you followed Chapter 2’s shortest path, this build already exists;',
                     'Chapter 2’s shortest path has already created this build;')
        self.replace(self.chapter(12), 'repeated here to show the transfer boundary',
                     'shown again here\nto locate the transfer boundary')
        errors = final.check(self.root)
        self.assertFalse([e for e in errors if e.startswith(('Ch3:', 'Ch12:'))])

    def test_each_required_link_is_guarded(self):
        for number, old, new, message in (
            (3, 'fresh playground', 'playground', 'Ch3: link repeated build'),
            (4, 'The same `init()` and `start()` calls seen above now take their places in the startup sequence.',
                'Call `init()` and `start()` during startup.', 'Ch4: identify repeated startup'),
            (4, 'As noted above, it should', 'It should', 'Ch4: link the repeated context'),
            (7, 'earlier IPv4/IPv6 alias pair', 'IPv4/IPv6 pair', 'Ch7: link the fuller comparison'),
            (7, 'Chapter 8 adds connection-lifetime reasoning to these pathname endpoints; its bind, local and remote views remain distinct.',
                'Chapter 8 develops this connection model in detail.', 'Ch7: give the later connection pointer'),
            (12, 'complete Chapter 3 listing', 'complete listing', 'Ch12: link the repeated snippets'),
            (18, 'trace followed above', 'trace', 'Ch18: connect framework observations'),
            (29, 'Beyond this single run, the general benchmarking distinctions still apply.', '',
                 'Ch29: mark the move')):
            with self.subTest(chapter=number, guard=message):
                p = self.chapter(number)
                original = p.read_text()
                self.replace(p, old, new)
                self.fails(message)
                p.write_text(original)

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
