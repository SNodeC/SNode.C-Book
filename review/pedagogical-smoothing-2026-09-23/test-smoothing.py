#!/usr/bin/env python3
"""Exercise the public file checks with isolated manuscript mutations."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('smoothing',HERE/'check-smoothing.py')
smoothing=importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoothing)

class SmoothingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory()
        cls.root=Path(cls.temp.name)
        shutil.copytree(smoothing.ROOT/'manuscript',cls.root/'manuscript')
        for p in (smoothing.ROOT/'companion/exercises').rglob('README.md'):
            dest=cls.root/p.relative_to(smoothing.ROOT)
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(p,dest)
        cls.review=cls.root/'review/pedagogical-smoothing-2026-09-23'
        cls.review.mkdir(parents=True)
        shutil.copyfile(HERE/'smoothing-structure.json',cls.review/'smoothing-structure.json')
        for name in ('cap-waivers.md', 'floor-waivers.md', 'backmatter-cap-waiver.md'):
            if (HERE/name).exists():
                shutil.copyfile(HERE/name, cls.review/name)
        cls.structure=json.loads((HERE/'smoothing-structure.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_current_files_pass(self):
        self.assertEqual(smoothing.check(self.root)[0],[])

    def test_backmatter_waiver_is_required_and_bounded(self):
        waiver = self.review/'backmatter-cap-waiver.md'
        original = waiver.read_text()
        for replacement in (None, 'No structured approval.', original.replace('812', '813')):
            with self.subTest(waiver=replacement):
                try:
                    if replacement is None:
                        waiver.unlink()
                    else:
                        waiver.write_text(replacement)
                    self.assertTrue(any(e.startswith('2: backmatter') for e in smoothing.check(self.root)[0]))
                finally:
                    waiver.write_text(original)
        path = self.root/'manuscript/backmatter/further-reading.md'
        before = path.read_text()
        try:
            path.write_text(before+'\nExtra\n')
            self.assertTrue(any(e.startswith('2: backmatter 813') for e in smoothing.check(self.root)[0]))
        finally:
            path.write_text(before)

    def test_each_assertion_detects_file_regression(self):
        paths={u['new']:self.root/u['path'] for u in self.structure['chapters']}
        mutations=[
            (1,paths['1'],lambda s:s+'\n'+'padding '*6000),
            (2,self.review/'smoothing-structure.json',lambda s:s.replace('"floor": 2400','"floor": 4000')),
            (3,self.root/'manuscript/book-files.txt',lambda s:s.replace(self.structure['chapters'][0]['path']+'\n','')),
            (4,paths['4'],lambda s:s.replace('**O1.**','**Missing.**')),
            (5,paths['1'],lambda s:s+'\n::: {.snodec-rule}\nExtra rule.\n:::\n'),
            (6,paths['1'],lambda s:s+'\nConfigured roles\n'),
            (6,paths['1'],lambda s:s+'\n### Topic {#configured-role}\n'),
            (7,paths['1'],lambda s:s+'\nRecorded working-tree\n'),
            (8,paths['17'],lambda s:s.replace('title="Build note"','title="Missing"')),
            (9,paths['18'],lambda s:s.replace('<!-- snodec-source: companion/exercises/ch18/dispatch.cpp -->','')),
            (10,paths['21'],lambda s:s.replace('CONNACK','response')),
            (11,paths['27'],lambda s:s.replace('find_package','lookup')),
            (12,paths['29'],lambda s:s.replace(smoothing.first_section(s), '\n```sh\necho premature\n```\n'+smoothing.first_section(s),1)),
            (13,paths['31'],lambda s:s+'\n```text\n'+'line\n'*61+'```\n'),
            (14,paths['32'],lambda s:s.replace('### Worked decision','### Discussion')),
            (15,paths['6'],lambda s:s.replace('peer A','first peer').replace('Peer A','First peer')),
            (16,self.root/'manuscript/frontmatter/conventions.md',lambda s:s.replace('Anonymous instance','Unnamed identity')),
        ]
        for number,path,mutate in mutations:
            with self.subTest(assertion=number):
                original=path.read_text()
                path.write_text(mutate(original))
                try:
                    errors=smoothing.check(self.root)[0]
                    self.assertTrue(any(e.startswith(f'{number}:') for e in errors),errors)
                finally:
                    path.write_text(original)

    def test_diagnostics_skip_objectives(self):
        text='## Title\n\n::: {.snodec-objectives}\n- **O1.** `WrongIdentifier`\n:::\n\n### Entry\n\nThree prose words.\n\n```cpp\ncode\n```\n'
        result=smoothing.diagnostics(text)
        self.assertEqual(result['prose_words_before_first_nonprose_block'],3)
        self.assertNotIn('WrongIdentifier',result['identifier_spellings'])

    def test_nested_fences_count_outer_listing(self):
        self.assertEqual(smoothing.fences('````markdown\n```sh\necho hi\n```\n````\n'),[(0,4,'markdown')])

if __name__=='__main__':
    unittest.main(verbosity=2)
