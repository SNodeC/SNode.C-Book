#!/usr/bin/env python3
"""Rerun Phase 0 exit evidence before starting Phase 1, from the repository root."""
import json
from pathlib import Path
import re
import subprocess
import tempfile

report = Path(__file__).resolve().parent
root = report.parents[1]
subprocess.run(['python3', '-B', 'ci/test-manuscript-metrics.py'], cwd=root, check=True)
with tempfile.TemporaryDirectory() as directory:
    fresh = Path(directory) / 'metrics.json'
    subprocess.run(['python3', 'ci/manuscript-metrics.py', '--output', str(fresh)], cwd=root, check=True)
    assert fresh.read_bytes() == (report / 'metrics-after-phase-0.json').read_bytes()
assert (report / 'metrics-before.json').read_bytes() == (report / 'metrics-after-phase-0.json').read_bytes()
print('PASS: fresh metrics and saved before/after measurements are byte-identical')
m = json.loads((report / 'metrics-before.json').read_text())
paths = [root / s for s in (root / 'manuscript/book-files.txt').read_text().splitlines() if s.strip()]
assert len(paths) == m['file_count'] == 62
assert sum(len(re.findall(r'\S+', p.read_text())) for p in paths) == m['totals']['total_words'] == 151924
print('PASS: independent whitespace-token count across 62 manifest files: 151924')
assert sum(len(re.findall(r'^#{3,6}\s', p.read_text(), re.M)) for p in paths if p.parent.name == 'chapters') == 1020
print('PASS: independent chapter heading count: 1020')
for label, expected in [('text', 478), ('cpp', 205)]:
    assert sum(len(re.findall(r'^```' + label + r'\s*$', p.read_text(), re.M)) for p in paths) == expected
    print(f'PASS: independent {label} fence count: {expected}')
for label, expected in [('remember', 38), ('rule', 30), ('exercise', 0)]:
    assert sum(len(re.findall(r'^:{3,}\s+\{\.snodec-' + label + r'\b', p.read_text(), re.M)) for p in paths) == expected
    print(f'PASS: independent snodec-{label} count: {expected}')
assert sum(len(re.findall(r'^#{1,6} Closing perspective\b', p.read_text(), re.M | re.I)) for p in paths) == 15
print('PASS: independent closing-section count including attributed headings: 15')
for item in m['files'].values():
    assert item['total_words'] == item['prose_words'] + item['code_words']
    assert item['code_words'] == item['code_content_words'] + item['fence_marker_words']
print('PASS: word partitions balance in all 62 files')
assert not subprocess.check_output(['git', 'diff', 'SNode.C-2.0', '--', 'manuscript/'], cwd=root)
print('PASS: manuscript diff from SNode.C-2.0 is empty')
for path, item in m['files'].items():
    for label, hits in item['forbidden_phrase_hits'].items():
        for hit in hits:
            print(f'GUARD HIT: {path}:{hit["line"]}: {label}')
scope_commit = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 0 — record author scope revision'], cwd=root, text=True).strip()
for path in ['AGENTS.md', 'review/EDITORIAL-WORK-PLAN.md', str(report.relative_to(root) / 'PROMPT.md')]:
    subprocess.run(['git', 'cat-file', '-e', scope_commit + ':' + path], cwd=root, check=True)
print('PASS: scope instructions and prompt exist in the separate scope-revision commit')
assert 'Author scope revision — proposal readiness, 2026-09-22' in (root / 'AGENTS.md').read_text()
assert 'Author scope revision — proposal readiness, 2026-09-22' in (root / 'review/EDITORIAL-WORK-PLAN.md').read_text()
assert '| Phase | Status | Commit | Date | Evidence |' in (report / 'REPORT.md').read_text()
print('PASS: scope revision references and phase status table exist')
subprocess.run(['git', 'diff', '--check'], cwd=root, check=True)
print('PASS: git diff --check')
