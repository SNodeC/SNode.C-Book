#!/usr/bin/env python3
"""Recheck the Part III budgets, teaching contract, scope, preservation and artifacts."""
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
base = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 5c follow-up — remove triple name/component explanation'], text=True).strip()
old = lambda path: subprocess.check_output(['git', 'show', f'{base}:{path}'], text=True)
module = runpy.run_path(str(ROOT / 'ci/manuscript-metrics.py'))
metrics = module['manuscript_metrics'](ROOT, ROOT / 'manuscript/book-files.txt')
assert metrics == json.loads((REVIEW / 'metrics-after-phase-5d.json').read_text())
baseline = json.loads((REVIEW / 'metrics-after-phase-5c-follow-up.json').read_text())
subprocess.run(['python3', 'ci/check-chapter-references.py'], check=True)
changed = {p for p in metrics['files'] if (ROOT / p).read_text() != old(p)}
allowed = {'manuscript/chapters/06-network-families-addresses-ipv4-ipv6-and-unix-sockets.md',
           'manuscript/chapters/07-servers-clients-and-connections.md',
           'manuscript/chapters/08-bluetooth-in-snodec-rfcomm-and-l2cap.md',
           'manuscript/parts/part-03-networking-foundations-in-snodec.md'}
assert changed <= allowed, changed - allowed
assert (ROOT / 'manuscript/book-files.txt').read_text() == old('manuscript/book-files.txt')
ch2 = 'manuscript/chapters/02-preparing-your-environment.md'
protected = lambda text: text.split('### Cloning the framework')[1].split('### Use an out-of-tree build')[0]
assert protected(old(ch2)) == protected((ROOT / ch2).read_text())

def executable_fences(text):
    blocks = []; fence = None; lines = []
    for line in text.splitlines(keepends=True):
        if fence:
            lines.append(line)
            if re.fullmatch(r' {0,3}'+re.escape(fence[0])+'{'+str(len(fence))+r',}[ \t]*', line.rstrip('\r\n')):
                if language in {'cpp','cmake','sh','python','sql','ini'}: blocks.append(''.join(lines))
                fence = None
        elif match := module['FENCE'].match(line):
            fence, info = match.groups(); language = info.strip().split()[0].lstrip('{.').rstrip('}')
            lines = [line]
    assert fence is None
    return Counter(blocks)

before = '\n'.join(old(p) for p in metrics['files'])
after = '\n'.join((ROOT / p).read_text() for p in metrics['files'])
assert executable_fences(before) == executable_fences(after)
for pattern in [r'^\\index\{.*$', r'\{[^}\n]*#fig:[^}\n]+\}', r'<!-- snodec-source:.*?-->']:
    assert Counter(re.findall(pattern,before,re.M)) == Counter(re.findall(pattern,after,re.M))

chapters=[]
for n,budget,headings in [(6,5200,15),(7,3650,10),(8,2200,5)]:
    path = next(p for p in metrics['files'] if f'/chapters/{n:02}-' in p)
    assert re.findall(r'```cpp\n.*?\n```', old(path), re.S) == re.findall(r'```cpp\n.*?\n```', (ROOT/path).read_text(), re.S)
    text = (ROOT / path).read_text(); m=metrics['files'][path]
    assert m['total_words'] <= budget and m['section_count'] <= headings
    assert m['average_section_prose_words'] >= 250
    callouts={}
    for kind in ['objectives','remember','exercise']:
        found = re.findall(r'::: \{\.snodec-'+kind+r'[^\n]*\}\n(.*?)\n:::',text,re.S)
        assert len(found)==1;callouts[kind]=found[0]
    objectives=set(re.findall(r'\*\*(O\d+)\.',callouts['objectives']))
    assert 3 <= len(objectives) <= 5
    tiers=re.findall(r'^\d+\. \*\*(Review|Lab|Design) \((O\d+(?:, O\d+)*)\)',callouts['exercise'],re.M)
    assert [t for t,_ in tiers] == ['Review','Review','Lab','Lab','Design']
    mapped={o for _,ids in tiers for o in ids.split(', ')}
    assert mapped == objectives
    assert len(re.findall(r'^- ',callouts['remember'],re.M)) <= 5
    assert text.index(callouts['objectives']) < text.index('\n### ')
    assert text.index(callouts['remember']) < text.index(callouts['exercise'])
    assert text.rstrip().endswith(':::')
    answers=(ROOT / f'companion/exercises/ch{n:02}/README.md').read_text()
    assert re.findall(r'^## \d+\. (Review|Lab|Design) \((O\d+(?:, O\d+)*)\)',answers,re.M)==tiers
    apparatus=sum(len(s.split()) for s in callouts.values())
    chapters.append({'chapter':n,'path':path,'words_before':baseline['files'][path]['total_words'],
                     'words_after':m['total_words'],'budget':budget,'prose_words':m['prose_words'],
                     'code_words':m['code_words'],'headings':m['section_count'],'heading_ceiling':headings,
                     'average_section_prose_words':m['average_section_prose_words'],
                     'objectives':sorted(objectives),'exercise_mapping':tiers,'apparatus_words':apparatus})
prior=json.loads((REVIEW/'phase-2-exit-checks.json').read_text())
plan=json.loads((REVIEW/'phase-5a-approved-structure.json').read_text())
samples=[]
for sample in prior['sample_chapters']:
    row=next(r for r in plan['chapters'] if sample['chapter'] in r['old'])
    m=metrics['files'][row['path']]
    assert m['prose_words'] <= sample['prose_before']*.8
    assert m['average_section_prose_words'] >= 250
    samples.append({'chapter':row['new'],'prose_reduction_percent':round(100*(1-m['prose_words']/sample['prose_before']),2)})
front=sum(m['total_words'] for p,m in metrics['files'].items() if '/frontmatter/' in p)
openers=sum(m['total_words'] for p,m in metrics['files'].items() if '/parts/' in p)
assert front<=2500 and openers<=1650
assert 'Part III checkpoint' in (ROOT/'manuscript/chapters/08-bluetooth-in-snodec-rfcomm-and-l2cap.md').read_text()
assert 'Part III checkpoint' in (ROOT/'companion/exercises/ch08/README.md').read_text()
intro=(ROOT/'manuscript/chapters/04-the-mental-model-and-layers-in-practice.md').read_text().split('### Reading public types and components')[1].split('### Layers in practice')[0]
assert len(intro.split()) <= 300
# Existing application and lab implementations are reused unchanged.
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'companion/examples','companion/exercises'],text=True).splitlines():
    if Path(path).suffix in {'.cpp','.h','.py'}: assert (ROOT/path).read_text()==old(path),path
# Production formatting stays unchanged in this Part session.
for path in ['production/metadata/metadata.yaml','manuscript/frontmatter/mainmatter.md']:
    assert (ROOT/path).read_text() == old(path)
assert all(value == 0 for value in json.loads((REVIEW/'phase-5d-final-results.json').read_text()).values())
assert '100% tests passed, 0 tests failed out of 22' in (REVIEW/'phase-5d-final-labs.log').read_text()
t=metrics['totals']
assert t['forbidden_phrase_hit_count']==t['closing_perspective_sections']==0
assert t['callout_counts_by_class']['snodec-rule']<=20
assert set(t['fenced_blocks_by_language']) & {'sh','bash','shell','zsh'} == {'sh'}
pdfs={}
for name in ['snodec-book','book-proposal-package','book-proposal-sample-package']:
    p=ROOT/'dist/pdf'/(name+'.pdf')
    pages=int(re.search(r'Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',str(p)],text=True))[1])
    assert not re.search('Warning|Overfull|Underfull',(BUILD/(name+'.log')).read_text()),name
    pdfs[name]={'pages':pages,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'warnings':0,'bad_boxes':0}
with tarfile.open(ROOT/'dist/packages/snodec-book-proposal-package.tar.gz') as archive:
    files=[m for m in archive.getmembers() if m.isfile()]
    for member in files:
        p=ROOT/member.name.removeprefix('./')
        assert archive.extractfile(member).read()==p.read_bytes(),str(p)
    assert any(m.name.endswith('/ch08/selectors.cpp') for m in files)
result={'chapters':chapters,'part_iii_words':sum(c['words_after'] for c in chapters),'part_iii_budget':11050,
        'frontmatter_words':front,'frontmatter_budget':2500,'all_part_openers_words':openers,
        'all_part_openers_budget':1650,'retained_sample_reductions':samples,
        'preserved_executable_configuration_fences':sum(executable_fences(after).values()),
        'preservation_and_scope_checks_passed':True,'pdfs':pdfs,'archive_identical_files':len(files),
        'reserve_used':0,'reserve_remaining':2750,'global_words':t['total_words'],
        'word_delta_from_phase_5c_follow_up':t['total_words']-baseline['totals']['total_words']}
(REVIEW/'phase-5d-exit-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: Part III budgets, pedagogy, mappings, scope, preserved listings, clean final PDFs and package contents.')
print('Execution and editorial/visual review are recorded in separate Phase 5d logs; future Parts are not certified.')
