#!/usr/bin/env python3
"""Recheck the final manuscript budgets, teaching contract, scope, preservation and artifacts."""
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
base = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 5l — refine Part XI and verify the integrated gateway'], text=True).strip()
old = lambda path: subprocess.check_output(['git', 'show', f'{base}:{path}'], text=True)
module = runpy.run_path(str(ROOT / 'ci/manuscript-metrics.py'))
metrics = module['manuscript_metrics'](ROOT, ROOT / 'manuscript/book-files.txt')
assert metrics == json.loads((REVIEW / 'metrics-after-phase-5m.json').read_text())
baseline = json.loads((REVIEW / 'metrics-after-phase-5l.json').read_text())
subprocess.run(['python3', 'ci/check-chapter-references.py'], check=True)
changed = {p for p in metrics['files'] if (ROOT / p).read_text() != old(p)}
allowed = {'manuscript/chapters/appendix-a-reading-and-extending-the-framework.md', 'manuscript/chapters/epilogue.md', 'manuscript/backmatter/further-reading.md'}
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
for pattern in [r'^\\index\{.*$', r'\{[^}\n]*#fig:[^}\n]+\}']:
    assert Counter(re.findall(pattern,before,re.M)) == Counter(re.findall(pattern,after,re.M))

markers_before = Counter(re.findall(r'<!-- snodec-source:.*?-->', before))
markers_after = Counter(re.findall(r'<!-- snodec-source:.*?-->', after))
assert markers_before == markers_after
plan=json.loads((REVIEW/'phase-5a-approved-structure.json').read_text())
heading_ceilings=[5,9,6,15,11,15,10,5,8,7,7,16,7,8,9,6,5,7,7,5,4,8,10,17,10,10,10,6,6,6,10]
chapters=[]
for row,headings in zip(plan['chapters'],heading_ceilings):
    n=row['new']; path=row['path']; budget=4200 if n=='27' else row['total_word_budget']
    assert re.findall(r'```cpp\n.*?\n```', old(path), re.S) == re.findall(r'```cpp\n.*?\n```', (ROOT/path).read_text(), re.S)
    text = (ROOT / path).read_text(); m=metrics['files'][path]
    parsed=json.loads(subprocess.check_output(['pandoc', '-f', 'markdown', '-t', 'json', str(ROOT/path)], text=True))
    rendered_headers=[b for b in parsed['blocks'] if b['t']=='Header' and b['c'][0]>=3]
    assert len(rendered_headers)==m['section_count'], 'A source heading is not parsed as a heading: '+path
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
    solution_dir='appendix-a' if n=='A' else f'ch{int(n):02}'
    answers=(ROOT / f'companion/exercises/{solution_dir}/README.md').read_text()
    assert re.findall(r'^## \d+\. (Review|Lab|Design) \((O\d+(?:, O\d+)*)\)',answers,re.M)==tiers
    apparatus=sum(len(s.split()) for s in callouts.values())
    chapters.append({'chapter':n,'path':path,'words_before':baseline['files'][path]['total_words'],
                     'words_after':m['total_words'],'budget':budget,'prose_words':m['prose_words'],
                     'code_words':m['code_words'],'headings':m['section_count'],'heading_ceiling':headings,
                     'average_section_prose_words':m['average_section_prose_words'],
                     'objectives':sorted(objectives),'exercise_mapping':tiers,'apparatus_words':apparatus})
prior=json.loads((REVIEW/'phase-2-exit-checks.json').read_text())
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
assert 'Part XI checkpoint' in (ROOT/'manuscript/chapters/30-architectural-judgment-choosing-the-right-layer-and-boundary.md').read_text()
assert 'Part XI checkpoint' in (ROOT/'companion/exercises/ch30/README.md').read_text()
intro=(ROOT/'manuscript/chapters/04-the-mental-model-and-layers-in-practice.md').read_text().split('### Reading public types and components')[1].split('### Layers in practice')[0]
assert len(intro.split()) <= 300
# Existing applications, chapter labs and their common harness remain unchanged.
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',base,'companion/examples','companion/exercises'],text=True).splitlines():
    if Path(path).suffix in {'.cpp','.h','.py'}: assert (ROOT/path).read_text()==old(path),path
assert (ROOT/'ci/run-example-lifetime-tests.py').read_text() == old('ci/run-example-lifetime-tests.py')
# Both generated WebSocket lab consumers watch a single canonical input path.
regeneration=next(line for line in (ROOT/'build/proposal-readiness-phase-5m-examples/build.ninja').read_text().splitlines()
                  if ': RERUN_CMAKE ' in line)
for role in ['Server','Client']:
    path=str((ROOT/f'companion/examples/HttpUpgrade-{role}/main.cpp').resolve())
    assert regeneration.split().count(path)==1, path
# Production formatting stays unchanged in this closing-material session.
for path in ['production/metadata/metadata.yaml','manuscript/frontmatter/mainmatter.md']:
    assert (ROOT/path).read_text() == old(path)
assert 'part-xi-checkpoint DEPENDS ch28-lab ch29-lab ch30-lab' in (ROOT/'companion/exercises/ch30/CMakeLists.txt').read_text()
assert all(value == 0 for value in json.loads((REVIEW/'phase-5m-final-results.json').read_text()).values())
assert '100% tests passed, 0 tests failed out of 62' in (REVIEW/'phase-5m-final-labs.log').read_text()
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
    assert any(m.name.endswith('/appendix-a/CMakeLists.txt') for m in files)
# Closing essay is exempt from teaching callouts by the author's approval.
epilogue='manuscript/chapters/epilogue.md'; essay=(ROOT/epilogue).read_text(); em=metrics['files'][epilogue]
assert em['total_words']<=1900 and em['section_count']<=4 and em['average_section_prose_words']>=250
assert not re.search(r'\.snodec-(objectives|remember|exercise)',essay)
assert essay[essay.index('Networking does not become trivial'):]==old(epilogue)[old(epilogue).index('Networking does not become trivial'):]
philosophy=lambda text: text.split('### A philosophical review of the book')[1].split('### Where to go next')[0]
assert philosophy(essay)==philosophy(old(epilogue))
back=sum(m['total_words'] for p,m in metrics['files'].items() if '/backmatter/' in p)
assert back<=1000
assert t['total_words']<=115000
assert t['chapter_headings_level_3_and_deeper']<=550
assert t['average_chapter_section_prose_words']>=250
assert t['fenced_blocks_by_language'].get('text',0)<=250
assert all(t['callout_counts_by_class'][f'snodec-{k}']==31 for k in ['objectives','exercise','remember'])
# Preserve every existing cross-reference identity and topic association.
register='review/proposal-readiness-2026-09-22/phase-5a-reference-register.json'
refs=json.loads((ROOT/register).read_text()); prior_refs=json.loads(old(register))
key=lambda r: (r['file'],r['text'],tuple(r['targets']),tuple(r['source_ids']))
assert not (Counter(map(key,prior_refs['references']))-Counter(map(key,refs['references'])))
assert refs['migration_dispositions']==prior_refs['migration_dispositions']
# Public appendix labs reuse the existing implementations and normal CI discovery.
lab_build=ROOT/'build/proposal-readiness-phase-5m-examples'
inventory=json.loads(subprocess.check_output(['ctest','--test-dir',str(lab_build),'--show-only=json-v1'],text=True))
assert len(inventory['tests'])==62
names={x['name'] for x in inventory['tests']}
assert {'exercise-appendix-a-source-consumer','exercise-appendix-a-carrier-extension'}<=names
assert 'ctest --test-dir build/ci-book-examples --output-on-failure --no-tests=error' in (ROOT/'.github/workflows/companion-examples.yml').read_text()
assert 'appendix-a-lab DEPENDS ch02-lab ch11-lab' in (ROOT/'companion/exercises/appendix-a/CMakeLists.txt').read_text()
parts=[]
for part in plan['parts']:
    rows=[r for r in chapters if r['chapter'] in list(map(str,part['chapters']))]
    budget=part['chapter_words']+(400 if part['part']=='X' else 0)
    total=sum(r['words_after'] for r in rows)
    assert total<=budget
    parts.append({'part':part['part'],'words':total,'budget':budget})
result={'chapters':chapters,'parts':parts,'epilogue':em,'backmatter_words':back,'backmatter_budget':1000,
        'frontmatter_words':front,'frontmatter_budget':2500,'all_part_openers_words':openers,
        'all_part_openers_budget':1650,'retained_sample_reductions':samples,
        'preserved_executable_configuration_fences':sum(executable_fences(after).values()),
        'preservation_and_scope_checks_passed':True,'prior_lifetime_tests_preserved':True,'canonical_entry_dependencies_unique':True,
        'pdfs':pdfs,'archive_identical_files':len(files),'preserved_complete_markers':sum(markers_after.values()),'public_labs':62,
        'reserve_used_this_phase':0,'reserve_used_total':400,'reserve_remaining':2350,
        'global_metrics':t,'word_delta_from_phase_5l':t['total_words']-baseline['totals']['total_words'],
        'numbered_chapters_and_appendix_pedagogy_pass':True,'epilogue_author_exception_pass':True,'all_global_numeric_targets_pass':True}
(REVIEW/'phase-5m-exit-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: all chapter/Part budgets, teaching mappings, essay exception, global targets, scope, preservation, PDFs and package contents.')
print('Runtime and editorial/visual review are recorded in Phase 5m logs; proposal refresh remains Phase 6.')
