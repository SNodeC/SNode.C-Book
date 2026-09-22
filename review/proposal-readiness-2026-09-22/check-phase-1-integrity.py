#!/usr/bin/env python3
"""Check Phase 1 metrics and preservation against the pre-phase manuscript."""
import json
from pathlib import Path
import re
import runpy
import subprocess

root = Path(__file__).resolve().parents[2]
report = Path(__file__).resolve().parent
base = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 0 — unescape stored prompt'], cwd=root, text=True).strip()
metrics = runpy.run_path(str(root / 'ci/manuscript-metrics.py'))
fresh = metrics['manuscript_metrics'](root, root / 'manuscript/book-files.txt')
assert fresh == json.loads((report / 'metrics-after-phase-1.json').read_text())
t = fresh['totals']
assert t['forbidden_phrase_hit_count'] == 0
assert t['closing_perspective_sections'] == 0
assert t['callout_counts_by_class']['snodec-rule'] <= 20
assert set(t['fenced_blocks_by_language']) & {'bash', 'shell', 'sh', 'zsh'} == {'sh'}
print('PASS: fresh metrics match saved Phase 1 metrics; all four hygiene thresholds pass')


def code_blocks(text):
    result, body, fence, language = [], [], None, ''
    for line in text.splitlines(keepends=True):
        if fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', line.rstrip('\r\n')):
                result.append((language, ''.join(body)))
                fence = None
            else:
                body.append(line)
        else:
            m = metrics['FENCE'].match(line)
            if m:
                fence, language = m[1], m[2].strip()
                body = []
    assert fence is None
    return [(('sh' if k in ('sh', 'shell', 'bash') else k), v) for k, v in result if k not in ('text', 'markdown')]


records = []
for name in (root / 'manuscript/book-files.txt').read_text().splitlines():
    old = subprocess.check_output(['git', 'show', base + ':' + name], cwd=root, text=True)
    new = (root / name).read_text()
    assert code_blocks(old) == code_blocks(new), name
    old_headings = re.findall(r'^#{1,6} .+$', old, re.M)
    assert [h for h in old_headings if not re.match(r'^### Closing perspective', h)] == re.findall(r'^#{1,6} .+$', new, re.M), name
    for pattern in (r'<!-- snodec-source: .*? -->', r'^\\index\{.*$', r'!\[.*?\]\(.*?\)\{.*?\}'):
        assert re.findall(pattern, old, re.M) == re.findall(pattern, new, re.M), name
    assert not re.search(r'^```(?:bash|shell|zsh)\s*$', new, re.M), name
    records.append({'file': name, 'changed': old != new, 'code_and_structure_preserved': True})
assert not subprocess.check_output(['git', 'diff', base, '--', 'manuscript/book-files.txt'], cwd=root)
result = {'ordered_inputs_unchanged': True, 'checks': ['executable and raw-LaTeX fence contents', 'source markers', 'index entries', 'figures', 'all headings except Closing perspective', 'shell labels including nested Markdown example'], 'files': records}
(report / 'phase-1-integrity.json').write_text(json.dumps(result, indent=2) + '\n')
print('PASS: all 62 inputs preserve code, source markers, index entries, figures and non-closing headings')
print('PASS: manuscript input order is unchanged; shell labels are sh, including nested example')
