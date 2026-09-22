#!/usr/bin/env python3
"""Run the unchanged Phase 5a exits against the explicitly authorized author baseline.

Only the metrics input and result destination differ; historical checks and
outputs are preserved. Use this prerequisite gate before starting Phase 5b.
"""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
historical = json.loads((HERE / 'metrics-after-phase-5a.json').read_text())
authorized = json.loads((HERE / 'metrics-after-author-seam-edits.json').read_text())
record = json.loads((HERE / 'author-seam-baseline.json').read_text())
assert {p for p in authorized['files'] if authorized['files'][p] != historical['files'][p]} == set(record['changed_manuscript_files'])
for key, delta in [('total_words', -5), ('prose_words', -5), ('code_words', 0)]:
    assert authorized['totals'][key] - historical['totals'][key] == delta
register = json.loads((HERE / 'phase-5a-reference-register.json').read_text())
ref = next(r for r in register['references'] if 'R275' in r['source_ids'])
assert ref['source_ids'] == ['R275', 'R276']
assert set(ref['targets']) == {'configuration-philosophy-in-snodec', 'application-and-instance-configuration-in-detail'}
assert sum('R276' in r['source_ids'] for r in register['references']) == 1
check = HERE / 'check-phase-5a.py'
source = check.read_text()
source = source.replace('metrics-after-phase-5a.json', 'metrics-after-author-seam-edits.json')
source = source.replace('phase-5a-exit-checks.json', 'phase-5a-author-seam-exit-checks.json')
exec(compile(source, str(check), 'exec'), {'__file__': str(check), '__name__': '__main__'})
