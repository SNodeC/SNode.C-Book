#!/usr/bin/env python3
"""Validate Phase 4 planning arithmetic, inventory coverage, and untouched manuscript.

This validates the proposed plan only. Phase 5a must implement the separate
intent-aware cross-reference check after author approval.
"""
import collections
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
plan = json.loads((REVIEW / 'phase-4-plan-data.json').read_text())
inv = json.loads((REVIEW / 'phase-4-reference-inventory.json').read_text())
metrics = json.loads(subprocess.check_output(
    ['python3', 'ci/manuscript-metrics.py'], cwd=ROOT, text=True))
assert metrics == json.loads((REVIEW / 'metrics-after-phase-3.json').read_text())
assert metrics == json.loads((REVIEW / 'metrics-after-phase-4.json').read_text())
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only', '--', 'manuscript'], cwd=ROOT)
rows = plan['chapters'] + plan['support']
sources = [p for row in rows for p in row['source_files']]
assert collections.Counter(sources) == collections.Counter(metrics['files'].keys())
assert sorted(n for row in plan['chapters'] for n in row['old']) == list(range(1, 39))
assert [r['new'] for r in plan['chapters']] == [str(n) for n in range(1, 31)] + ['A']
for row in rows:
    current = sum(metrics['files'][p]['total_words'] for p in row['source_files'])
    code = sum(metrics['files'][p]['code_words'] for p in row['source_files'])
    assert row['current_total_words'] == current
    assert row['current_fenced_words'] == code
    assert row['prose_allowance_with_all_current_fences'] == row['total_word_budget'] - code
    assert row['total_word_budget'] > code
assert sum(r['current_total_words'] for r in rows) == metrics['totals']['total_words']
assert sum(r['total_word_budget'] for r in rows) == plan['planned_total_words'] == 112250
headings = sum(r.get('heading_ceiling', 0) for r in rows)
assert headings == 269 and headings <= 550
assert plan['planned_total_words'] <= 115000
samples = json.loads((REVIEW / 'phase-2-exit-checks.json').read_text())['sample_chapters']
for sample in samples:
    row = next(r for r in plan['chapters'] if sample['chapter'] in r['old'])
    assert row['prose_allowance_with_all_current_fences'] <= sample['prose_before'] * .8
refs = inv['chapter_references']
covered = 0
for path, data in metrics['files'].items():
    for ref in data['manual_chapter_references']:
        number = int(ref['match'].split()[1])
        assert any(r['file'] == path and r['line'] == ref['line'] and number in r['old_chapters'] for r in refs), (path, ref)
        covered += 1
assert covered == inv['metrics_singular_references_covered'] == 276
register = (REVIEW / 'phase-4-reference-map.md').read_text()
for ref in refs:
    assert f"| {ref['id']} |" in register
    lines = (ROOT / ref['file']).read_text().splitlines()
    text = ' '.join('\n'.join(lines[ref['line'] - 1:ref['line'] + 2]).split())
    assert ref['text'] in text, ref['id']
for item in inv['index_entries']:
    assert '\\index{' + item['key'] + '}' in (ROOT / item['file']).read_text()
assert len(inv['figures']) == 18
for figure in inv['figures']:
    assert (ROOT / figure['asset']).is_file()
    assert figure['label'] in (ROOT / figure['file']).read_text()
text = (REVIEW / 'RESTRUCTURE-PLAN.md').read_text()
assert 'awaiting author approval' in text
assert len(re.findall(r'^\| (?:XI|X|IX|VIII|VII|VI|V|IV|III|II|I) / ', text, re.M)) == 11
for row in plan['chapters']:
    assert f"| {row['new']} | {row['part']} | {row['title']} |" in text
    assert f"| {row['total_word_budget']:,} | {row['prose_allowance_with_all_current_fences']:,} | {row['heading_ceiling']} |" in text
result = {'status': 'awaiting author approval', 'manuscript_unchanged': True,
          'manuscript_files_accounted_once': len(sources), 'old_chapters_mapped': 38,
          'proposed_numbered_chapters': 30, 'parts_with_checkpoints': 11,
          'planned_words': 112250, 'net_reduction_planned': 34700,
          'unallocated_words_to_hard_ceiling': 2750, 'chapter_heading_ceiling': headings,
          'sample_prose_budget_ceilings_preserve_phase_2_reductions': True,
          'singular_manuscript_references_covered': covered,
          'reference_occurrences': len(refs), 'references_requiring_treatment': sum(r['changed'] for r in refs),
          'index_insertions': len(inv['index_entries']),
          'unique_index_keys': len(set(i['key'] for i in inv['index_entries'])),
          'figures': len(inv['figures']), 'manual_page_marks': len(inv['manual_page_marks'])}
(REVIEW / 'phase-4-plan-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
print('PASS: planning arithmetic and inventory; no manuscript edits. This is not author approval or proof of executed condensation.')
