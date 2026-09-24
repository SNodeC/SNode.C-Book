#!/usr/bin/env python3
"""Mutation checks for the nine new editorial guards; never edit the manuscript."""
import importlib.util
from pathlib import Path
import shutil
import re
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('polish', HERE/'check-polish.py')
polish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(polish)


class Guards(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('manuscript', 'review/proposal'):
            shutil.copytree(ROOT/directory, self.root/directory)
        for name in ('ci/manuscript-metrics.py', str(polish.REVIEW/'terminology-allowlist.md'),
                     'assets/figures/src/fig-19-mqtt-publication-sequence.tex',
                     'assets/figures/pdf/fig-19-mqtt-publication-sequence.pdf'):
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/name, target)

    def chapter(self, n):
        return next((self.root/'manuscript/chapters').glob(f'{n:02}-*'))

    def replace(self, path, old, new):
        text = path.read_text()
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1))

    def errors(self):
        return polish.check(self.root, ROOT/'dist/pdf/snodec-book.pdf')[0]

    def fails(self, number):
        self.assertTrue(any(e.startswith(str(number)+':') for e in self.errors()))

    def test_current_tables_meet_the_scoped_rule(self):
        self.assertFalse([e for e in self.errors() if e.startswith('2:')])

    def test_2_exemptions_do_not_excuse_other_tables_in_same_files(self):
        for name in ('manuscript/frontmatter/conventions.md',
                     'manuscript/chapters/appendix-a-reading-and-extending-the-framework.md'):
            p = self.root/name
            p.write_text(p.read_text()+'\n| handle | instance | flow | connection | context |\n|---|---|---|---|---|\n')
        self.assertEqual(sum(e.startswith('2:') for e in self.errors()), 2)

    def test_1_phrase_not_excused_by_unrelated_allowlist(self):
        p = self.chapter(5)
        p.write_text(p.read_text()+'\nA public role appears again.\n')
        self.fails(1)

    def test_1_protected_listing_does_not_excuse_another_occurrence(self):
        p = self.chapter(30)
        p.write_text(p.read_text()+'\n- an MQTT client role for measurement input and output;\n')
        self.fails(1)

    def test_2_additional_taxonomy_table(self):
        p = self.chapter(8)
        p.write_text(p.read_text()+'\n| handle | instance | flow | connection | context |\n|---|---|---|---|---|\n')
        self.assertEqual(sum(e.startswith('2:') for e in self.errors()), 1)

    def test_3_command_required_in_each_item(self):
        p = self.chapter(2)
        text = p.read_text()
        start = text.index('7. ')
        end = text.index('\n', start)
        p.write_text(text[:start]+'7. Continue without a command.'+text[end:])
        self.fails(3)

    def test_4_running_value_in_every_section(self):
        p = self.chapter(13)
        text = p.read_text()
        start = text.index('### Section configuration:')
        end = text.index('\n### ', start+4)
        p.write_text(text[:start]+text[start:end].replace('echoserver', 'unrelated')+text[end:])
        self.fails(4)

    def test_5_diagram_before_classes(self):
        p = self.chapter(21)
        text = p.read_text()
        figure = next(line for line in text.splitlines() if '](assets/figures/pdf/fig-19-' in line)
        p.write_text(text.replace(figure, '')+'\n'+figure+'\n')
        self.fails(5)

    def test_5_fundamental_required(self):
        self.replace(self.chapter(21), '**persistent session**', '**ongoing exchange**')
        self.fails(5)

    def test_6_extra_table(self):
        p = self.chapter(18)
        p.write_text(p.read_text()+'\n| Type | API |\n|---|---|\n| A | B |\n')
        self.fails(6)

    def test_7_caption_is_visible_prose(self):
        p = self.chapter(26)
        p.write_text(p.read_text()+'\n![The boundary role needs a policy.](figure.pdf){#boundary-role-policy}\n')
        self.fails(7)

    def test_7_old_case(self):
        self.replace(self.chapter(23), '**Requirement.**', '**Requirement.** Assign a sequence number.')
        self.fails(7)

    def test_8_bookwide_limit(self):
        p = self.chapter(1)
        p.write_text(p.read_text()+'\nThis does not prove anything.\n')
        self.fails(8)

    def test_9_stale_metric(self):
        p = self.root/'review/proposal/book-proposal-package.md'
        current = re.search(r'[\d,]+ whitespace tokens', p.read_text())[0]
        self.replace(p, current, '1 whitespace tokens')
        self.fails(9)

    def test_9_stale_page_count(self):
        p = self.root/'review/proposal/book-proposal-package.md'
        current = re.search(r'\d+ pages', p.read_text())[0]
        self.replace(p, current, '1 pages')
        self.fails(9)

    def test_9_internal_terms_in_evidence_sheet(self):
        p = self.root/'review/proposal/evidence-sheet.md'
        p.write_text(p.read_text()+'\nThe P3 gate passed.\n')
        self.fails(9)

    def test_invisible_reference_identity_is_not_prose(self):
        self.assertEqual(polish.visible('A client {#a-client-role}'), 'A client ')
        self.assertEqual(polish.visible('![A diagram.](boundary-role-policy.pdf){#boundary-role-policy}'), 'A diagram.')


if __name__ == '__main__':
    unittest.main()
