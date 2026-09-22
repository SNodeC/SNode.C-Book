#!/usr/bin/env python3
"""Recheck Phase 2 editorial exits and preservation against its entry snapshot."""
import json
from pathlib import Path
import re
import runpy
import subprocess

root = Path(__file__).resolve().parents[2]
report = Path(__file__).resolve().parent
metrics = runpy.run_path(str(root / 'ci/manuscript-metrics.py'))
current = metrics['manuscript_metrics'](root, root / 'manuscript/book-files.txt')
assert current == json.loads((report / 'metrics-after-phase-2.json').read_text())
before = json.loads((report / 'metrics-before-phase-2.json').read_text())
base = subprocess.check_output(['git', 'rev-parse', ':/author edit: restore epilogue closing'], cwd=root, text=True).strip()
numbers = ('01', '03', '23', '35', '37')
records = []


def fences(text):
    result, start, fence = [], None, None
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', line.rstrip('\r\n')):
                result.append(''.join(lines[start:i + 1]))
                fence = None
        elif match := metrics['FENCE'].match(line):
            start, fence = i, match[1]
    assert fence is None
    return result


for name, result in current['files'].items():
    old = subprocess.check_output(['git', 'show', base + ':' + name], cwd=root, text=True)
    text = (root / name).read_text()
    number = Path(name).name[:2]
    if number not in numbers or Path(name).parent.name != 'chapters':
        assert text == old, f'Unexpected manuscript edit: {name}'
        continue
    original = before['files'][name]
    assert result['prose_words'] <= original['prose_words'] * .8, name
    assert result['average_section_prose_words'] >= 250, name
    assert result['callout_counts_by_class']['snodec-objectives'] == 1
    assert result['callout_counts_by_class']['snodec-remember'] == 1
    assert result['callout_counts_by_class']['snodec-exercise'] == 1
    objectives = re.search(r'::: \{\.snodec-objectives[^\n]*\}\n(.*?)\n:::', text, re.S)
    remember = re.search(r'::: \{\.snodec-remember[^\n]*\}\n(.*?)\n:::', text, re.S)
    exercises = re.search(r'::: \{\.snodec-exercise[^\n]*\}\n(.*?)\n:::\s*$', text, re.S)
    assert objectives and remember and exercises
    assert objectives.start() < text.index('\n### ')
    assert remember.end() < exercises.start()
    assert 1 <= len(re.findall(r'^- ', remember[1], re.M)) <= 5
    objective_ids = set(re.findall(r'\*\*(O\d+)\.', objectives[1]))
    assert 3 <= len(objective_ids) <= 5
    tiers = re.findall(r'^\d+\. \*\*(Review|Lab|Design) \((O\d+)\)', exercises[1], re.M)
    assert 3 <= len(tiers) <= 5
    assert {tier for tier, _ in tiers} == {'Review', 'Lab', 'Design'}
    assert {objective for _, objective in tiers} == objective_ids
    assert (root / f'companion/exercises/ch{number}/README.md').is_file()
    for pattern in (r'<!-- snodec-source: .*? -->', r'^\\index\{.*$', r'!\[.*?\]\(.*?\)\{.*?\}'):
        assert re.findall(pattern, old, re.M) == re.findall(pattern, text, re.M), name
    if number == '35':
        assert fences(old) == fences(text), 'Chapter 35 listing changed'
    records.append({'chapter': int(number), 'prose_before': original['prose_words'],
                    'prose_after': result['prose_words'],
                    'reduction_percent': round(100 * (1 - result['prose_words'] / original['prose_words']), 2),
                    'average_section_prose_words': result['average_section_prose_words'],
                    'objectives': len(objective_ids), 'exercise_tiers': tiers})
assert len(records) == 5
assert current['totals']['forbidden_phrase_hit_count'] == 0
assert current['totals']['closing_perspective_sections'] == 0
assert current['totals']['callout_counts_by_class']['snodec-rule'] <= 20
assert set(current['totals']['fenced_blocks_by_language']) & {'sh', 'bash', 'shell', 'zsh'} == {'sh'}
ch1 = next(root.glob('manuscript/chapters/01-*')).read_text()
comparison = ch1.split('### Where SNode.C fits: two echo servers\n')[1].split('\n### ')[0]
assert len(comparison.split()) <= 1200
assert not subprocess.check_output(['git', 'diff', base, '--', 'manuscript/book-files.txt'], cwd=root)
output = {'sample_chapters': records, 'comparison_words': len(comparison.split()),
          'chapter_35_fences_identical': True, 'other_manuscript_files_identical': True,
          'sample_source_markers_index_entries_figures_preserved': True}
(report / 'phase-2-exit-checks.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps(output, indent=2))
print('PASS: editorial thresholds, objectives/exercise coverage, public answer paths, and preservation')
print('Build, run, visual review, and answer quality need the separate evidence logs and ledger.')
