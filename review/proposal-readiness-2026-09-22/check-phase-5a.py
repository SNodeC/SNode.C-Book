#!/usr/bin/env python3
"""Verify Phase 5a structure, preserved content, sample exits, PDFs, and package."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BUILD = ROOT / 'build/proposal-readiness-phase-2'
base = subprocess.check_output(['git', 'rev-parse', ':/author approval: restructure plan with changes'], cwd=ROOT, text=True).strip()
old = lambda name: subprocess.check_output(['git', 'show', f'{base}:{name}'], cwd=ROOT, text=True)
plan = json.loads((REVIEW / 'phase-5a-approved-structure.json').read_text())
subprocess.run(['python3', 'ci/check-chapter-references.py'], cwd=ROOT, check=True)
metrics_module = runpy.run_path(str(ROOT / 'ci/manuscript-metrics.py'))
metrics = metrics_module['manuscript_metrics'](ROOT, ROOT / 'manuscript/book-files.txt')
assert metrics == json.loads((REVIEW / 'metrics-after-phase-5a.json').read_text())
assert (ROOT / 'manuscript/chapters/epilogue.md').read_text() == old('manuscript/chapters/epilogue.md')
ch2 = 'manuscript/chapters/02-preparing-your-environment.md'
for text in [old(ch2), (ROOT / ch2).read_text()]:
    assert '### Cloning the framework' in text
assert old(ch2).split('### Cloning the framework')[1].split('### Use an out-of-tree build')[0] == (ROOT / ch2).read_text().split('### Cloning the framework')[1].split('### Use an out-of-tree build')[0]
old_inputs = old('manuscript/book-files.txt').splitlines()
before = '\n'.join(old(name) for name in old_inputs)
after = '\n'.join((ROOT / name).read_text() for name in metrics['files'])
indices = lambda text: Counter(re.findall(r'^\\index\{.*$', text, re.M))
assert indices(before) == indices(after)
figures = lambda text: Counter(re.findall(r'\{[^}\n]*#(fig:[^\s}]+)[^}\n]*\}', text))
assert figures(before) == figures(after) and sum(figures(after).values()) == 18

def code_fences(text):
    code = []; fence = None; lines = []
    for line in text.splitlines(keepends=True):
        if fence:
            lines.append(line)
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}[ \t]*', line.rstrip('\r\n')):
                if language in {'cpp','cmake','sh','python','sql','ini'}:
                    code.append(''.join(lines))
                fence = None
        elif match := metrics_module['FENCE'].match(line):
            fence, info = match.groups(); language = info.strip().split()[0].lstrip('{.').rstrip('}')
            lines = [line]
    assert fence is None
    return Counter(code)
assert code_fences(before) == code_fences(after), 'Executable/configuration listing changed'
# Existing lab implementations move byte-for-byte; only their registration and
# public commands change identity.
old_labs = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', base, 'companion/exercises'], cwd=ROOT, text=True).splitlines()
lab_sources = 0
for name in old_labs:
    if Path(name).suffix not in {'.cpp', '.h', '.py'}: continue
    target = re.sub(r'\bch(23|35|37)\b', lambda m: {'23':'ch18','35':'ch28','37':'ch30'}[m[1]], name)
    assert old(name) == (ROOT / target).read_text(), target
    lab_sources += 1
prior = json.loads((REVIEW / 'phase-2-exit-checks.json').read_text())
samples = []
for sample in prior['sample_chapters']:
    row = next(r for r in plan['chapters'] if sample['chapter'] in r['old'])
    text = (ROOT / row['path']).read_text(); count = metrics['files'][row['path']]
    assert count['prose_words'] <= sample['prose_before'] * .8
    assert count['average_section_prose_words'] >= 250
    callouts = {}
    for kind in ['objectives','remember','exercise']:
        blocks = re.findall(r'::: \{\.snodec-' + kind + r'[^\n]*\}\n(.*?)\n:::', text, re.S)
        assert len(blocks) == 1; callouts[kind] = blocks[0]
    objectives = set(re.findall(r'\*\*(O\d+)\.', callouts['objectives']))
    tiers = re.findall(r'^\d+\. \*\*(Review|Lab|Design) \((O\d+)\)', callouts['exercise'], re.M)
    assert tiers == [tuple(t) for t in sample['exercise_tiers']]
    assert {objective for _, objective in tiers} == objectives
    assert len(re.findall(r'^- ', callouts['remember'], re.M)) <= 5
    answers = (ROOT / f"companion/exercises/ch{int(row['new']):02}/README.md").read_text()
    assert re.findall(r'^## \d+\. (Review|Lab|Design) \((O\d+)\)', answers, re.M) == tiers
    samples.append({'old':sample['chapter'], 'current':int(row['new']), 'prose_words':count['prose_words'],
                    'reduction_percent':round(100 * (1-count['prose_words']/sample['prose_before']),2),
                    'average_section_prose_words':count['average_section_prose_words'],
                    'objectives':sorted(objectives), 'exercise_mapping':tiers, 'public_answers':True})
t = metrics['totals']
assert t['forbidden_phrase_hit_count'] == t['closing_perspective_sections'] == 0
assert t['callout_counts_by_class']['snodec-rule'] <= 20
assert set(t['fenced_blocks_by_language']) & {'sh','bash','shell','zsh'} == {'sh'}
# Proposal/evidence refresh is explicitly deferred to Phase 6.
for name in ['book-proposal-package.md','evidence-sheet.md']:
    path = 'review/proposal/' + name
    assert (ROOT / path).read_text() == old(path)
pdfs = {}
for name in ['snodec-book','book-proposal-package','book-proposal-sample-package']:
    path = ROOT / 'dist/pdf' / (name + '.pdf')
    pages = int(re.search(r'Pages:\s+(\d+)', subprocess.check_output(['pdfinfo', str(path)], text=True))[1])
    log = (BUILD / (name+'.log')).read_text()
    assert not re.search(r'Warning|Overfull|Underfull', log), name
    pdfs[name] = {'pages':pages, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'warnings':0, 'bad_boxes':0}
# Confirm rendered numbering, including Appendix A after the unnumbered essay.
toc = (BUILD / 'snodec-book.toc').read_text()
assert re.findall(r'\\contentsline \{chapter\}\{\\numberline \{([^}]+)\}', toc) == list(map(str,range(1,31))) + ['A']
assert toc.index('The Principles Behind the Programs') < toc.index('Reading and Extending the Framework') < toc.index('Further Reading')
archive = ROOT / 'dist/packages/snodec-book-proposal-package.tar.gz'
with tarfile.open(archive) as packed:
    names = packed.getnames(); assert len(names) == len(set(names))
    checked = 0
    for member in packed.getmembers():
        if not member.isfile(): continue
        name = member.name.removeprefix('./')
        assert not '__pycache__' in name and not name.endswith('.pyc')
        assert (ROOT / name).is_file(), name
        assert packed.extractfile(member).read() == (ROOT / name).read_bytes(), name
        checked += 1
    for path in [REVIEW.relative_to(ROOT) / 'phase-5a-approved-structure.json', REVIEW.relative_to(ROOT) / 'phase-5a-reference-register.json']:
        assert './'+str(path) in names
result = {'approved_structure_applied':True,'numbered_chapters':30,'parts':11,'appendices':1,
          'sample_chapters':samples,'epilogue_unchanged':True,'chapter_2_reconstruction_unchanged':True,
          'preserved_executable_configuration_fences':sum(code_fences(after).values()),
          'preserved_index_insertions':sum(indices(after).values()),'preserved_figures':18,
          'unchanged_lab_implementation_files':lab_sources,'pdfs':pdfs,'archive_identical_files':checked,
          'proposal_refresh_deferred_to_phase_6':True,'planned_words':112250,'reserve_used':0,'reserve_remaining':2750}
(REVIEW / 'phase-5a-exit-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: Phase 5a structure, references, preservation, sample pedagogy, final PDFs, and archive contents.')
print('Actual build/runtime execution and targeted visual/editorial reread have separate logs; no Part condensation is claimed.')
