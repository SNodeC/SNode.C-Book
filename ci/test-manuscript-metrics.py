#!/usr/bin/env python3
"""Regression fixtures for the manuscript measurement contract."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('metrics', Path(__file__).with_name('manuscript-metrics.py'))
metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metrics)


class MetricsTests(unittest.TestCase):
    def test_fences_hide_fake_structure_and_phrases(self):
        text = ('## Chapter\n### First\nTwo words\n'
                '````cpp\n### fake\n```\nChapter 9 the chapter should\n'
                '::: {.snodec-rule}\n`````\n'
                '~~~sh\necho hello\n~~~\n'
                '### Second\nThree more words\n')
        result = metrics.measure(text)
        self.assertEqual(result['total_words'], len(text.split()))
        self.assertEqual(result['prose_words'] + result['code_words'], result['total_words'])
        self.assertEqual(result['heading_counts_by_level']['3'], 2)
        self.assertEqual(result['fenced_blocks_by_language'], {'cpp': 1, 'sh': 1})
        self.assertEqual(result['section_prose_words'], 5)
        self.assertEqual(result['average_section_prose_words'], 2.5)
        self.assertEqual(result['code_content_words'] + result['fence_marker_words'], result['code_words'])
        self.assertEqual(result['forbidden_phrase_hit_count'], 0)
        self.assertEqual(result['manual_chapter_references'], [])
        self.assertEqual(result['callout_counts_by_class']['snodec-rule'], 0)

    def test_wrapped_phrases_locations_and_word_boundaries(self):
        result = metrics.measure('The chapter\nshould explain Chapter\n29.\n'
                                 'role roles boundary boundaries visible invisible\n')
        self.assertEqual(result['forbidden_phrase_hits']['the chapter should'],
                         [{'line': 1, 'match': 'The chapter\nshould'}])
        self.assertEqual(result['manual_chapter_references'], [{'line': 2, 'match': 'Chapter\n29'}])
        self.assertEqual(len(result['term_occurrences']['role']), 1)
        self.assertEqual(len(result['term_occurrences']['boundary/boundaries']), 2)
        self.assertEqual(len(result['term_occurrences']['visible']), 1)

    def test_callouts_and_closing_headings(self):
        result = metrics.measure('### Closing perspective\n'
                                 '::: {.snodec-remember title="What to remember"}\n'
                                 '- Useful item\n:::\n'
                                 '::: {.snodec-objectives}\n- Explain a behavior\n:::\n'
                                 ':::: {.snodec-exercise}\nDo something\n::::\n'
                                 'The phrase Closing perspective is prose.\n')
        self.assertEqual(len(result['closing_perspective_sections']), 1)
        self.assertEqual(result['callout_counts_by_class']['snodec-remember'], 1)
        self.assertEqual(result['callout_counts_by_class']['snodec-exercise'], 1)
        self.assertEqual(result['callout_counts_by_class']['snodec-objectives'], 1)

    def test_unclosed_fence_fails(self):
        with self.assertRaisesRegex(ValueError, 'unclosed'):
            metrics.measure('```cpp\nunclosed\n')

    def test_manifest_authority_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'manuscript/chapters').mkdir(parents=True)
            chapter = 'manuscript/chapters/01-one.md'
            (root / chapter).write_text('## Title\n### Section\nhello\n')
            (root / 'manuscript/chapters/not-in-book.md').write_text('ignored words')
            manifest = root / 'manuscript/book-files.txt'
            manifest.write_text('# comment\n\n' + chapter + '\n')
            result = metrics.manuscript_metrics(root, manifest)
            self.assertEqual(result['file_count'], 1)
            self.assertEqual(result['totals']['total_words'], 5)
            manifest.write_text(chapter + '\n' + chapter + '\n')
            with self.assertRaisesRegex(ValueError, 'unique'):
                metrics.manuscript_metrics(root, manifest)


if __name__ == '__main__':
    unittest.main(verbosity=2)
