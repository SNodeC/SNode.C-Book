#!/usr/bin/env python3
"""Check the refreshed dossier against the manuscript and collected evidence."""
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
base = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 5m — refine closing material and complete the manuscript audit'], text=True).strip()
def old(path):
    return subprocess.check_output(['git', 'show', f'{base}:{path}'], text=True)

assert all(x == 0 for x in json.loads((REVIEW/'phase-6-entry-results.json').read_text()).values())
entry = json.loads((REVIEW/'phase-6-entry-exit-checks.json').read_text())
assert entry['all_global_numeric_targets_pass'] and entry['numbered_chapters_and_appendix_pedagogy_pass']
assert '100% tests passed, 0 tests failed out of 62' in (REVIEW/'phase-6-entry-labs.log').read_text()
metrics = runpy.run_path(str(ROOT/'ci/manuscript-metrics.py'))['manuscript_metrics'](ROOT, ROOT/'manuscript/book-files.txt')
assert metrics == json.loads((REVIEW/'metrics-after-phase-5m.json').read_text())
assert metrics == json.loads((REVIEW/'metrics-after-phase-6.json').read_text())
protected = ['manuscript','companion','production','ci','packaging','STRUCTURE.md','README.md','AGENTS.md']
assert not subprocess.check_output(['git','diff',base,'--',*protected],text=True)
changed = subprocess.check_output(['git','diff','--name-only',base],text=True).splitlines()
assert all(p.startswith(('review/proposal/','review/proposal-readiness-2026-09-22/')) or p=='review/EDITORIAL-WORK-PLAN.md' for p in changed)

proposal = (ROOT/'review/proposal/book-proposal-package.md').read_text()
evidence = (ROOT/'review/proposal/evidence-sheet.md').read_text()
guide = (ROOT/'review/proposal/sample-chapters.md').read_text()
for header in ['Pitch','Reader and learning path','Comparable titles','Manuscript overview and estimated extent','Revision plan','Author platform and market evidence','Companion material and technical verification']:
    assert '\n# '+header+'\n' in '\n'+proposal
assert proposal.split('## Source-version baseline\n')[1] == old('review/proposal/book-proposal-package.md').split('## Source-version baseline\n')[1]
assert next(l for l in proposal.splitlines() if l.startswith('| **Source baseline**')) == next(l for l in old('review/proposal/book-proposal-package.md').splitlines() if l.startswith('| **Source baseline**'))
assert next(l for l in evidence.splitlines() if l.startswith('- Manuscript baseline:')) == next(l for l in old('review/proposal/evidence-sheet.md').splitlines() if l.startswith('- Manuscript baseline:'))
comps = lambda s: s.split('# Comparable titles\n')[1].split('# Manuscript overview')[0]
assert comps(proposal) == comps(old('review/proposal/book-proposal-package.md'))
bibliography = json.loads((REVIEW/'phase-3-bibliography.json').read_text())
assert len(bibliography['books']) == 5
assert all(b['source'] in proposal for b in bibliography['books'])

plan = json.loads((REVIEW/'phase-5a-approved-structure.json').read_text())
chapter_rows = re.findall(r'^\| (\d+|A) \| (.+) \|$',proposal,re.M)
assert len(chapter_rows) == 31
for (number,title), chapter in zip(chapter_rows,plan['chapters']):
    expected = next(l for l in (ROOT/chapter['path']).read_text().splitlines() if l.startswith('## '))
    expected = re.sub(r' \{#.*','',expected.removeprefix('## '))
    assert number == chapter['new'] and title == expected,(number,title,expected)
toc=(BUILD/'snodec-book.toc').read_text()
pagination=json.loads((REVIEW/'phase-6-manuscript-pagination.json').read_text())
assert all(r['toc_line'] in toc for r in pagination['divisions'])
assert sum(r['pages'] for r in pagination['divisions'])+pagination['preliminary_pages']==pagination['physical_pages']==310
part_rows=proposal.split('## Part plan\n')[1].split('## Chapter plan\n')[0]
page_counts=[int(n) for n in re.findall(r'\| (\d+) \|$',part_rows,re.M)]
assert page_counts == [14]+[r['pages'] for r in pagination['divisions']]
assert '| **Total supplied manuscript** | **30 numbered chapters + appendix** | **310** |' in part_rows
sample_numbers = [1,3,18,28,30]
sample_paths=[next(c['path'] for c in plan['chapters'] if c['new']==str(n)) for n in sample_numbers]
cmake=(ROOT/'review/proposal/CMakeLists.txt').read_text()
assert cmake == old('review/proposal/CMakeLists.txt')
assert re.findall(r'"\$\{MANUSCRIPT_DIR\}/(chapters/[^"]+)"',cmake)==[p.removeprefix('manuscript/') for p in sample_paths]
assert [int(x) for x in re.findall(r'^\| (\d+)\.',guide,re.M)]==sample_numbers
assert not re.search(r'38 chapters|470.page|146,950|final edition will|pre-consolidation|remaining Part revisions|Chapters 35|Parts XI–XII',proposal+evidence+guide)
assert 'prerequisite chain' in proposal and 'without a lecturer' in proposal
assert '[AUTHOR TO SUPPLY]' in proposal and '[AUTHOR TO SUPPLY]' in evidence
assert 'Rhodes' not in proposal+evidence and 'Centre for Biological Control' not in proposal+evidence
assert 'Advanced Technical Institute' not in proposal+evidence

figures=json.loads((REVIEW/'phase-6-repository-figures.json').read_text())
a,b=figures['repositories']
assert [a['repository'],b['repository']]==['SNodeC/snode.c','SNodeC/mqttsuite']
for label,key in [('Commits reachable from the captured `master` head','reachable_commits'),('Stars','stars'),('Forks','forks'),('Watching subscribers','watching_subscribers')]:
    assert f"| {label} | {a[key]:,} | {b[key]:,} |" in proposal
counts=lambda r: (sum(c['type']=='User' for c in r['contributors']),sum(c['type']=='Bot' for c in r['contributors']))
assert '| Contributor accounts returned: User / Bot | %d / %d | %d / %d |' % (*counts(a),*counts(b)) in proposal
assert f"| Published releases | {len(a['releases'])} | {len(b['releases'])} |" in proposal
assert all(not rel['draft'] and not rel['prerelease'] for repo in [a,b] for rel in repo['releases'])
assert all(repo['oldest_api_commit']['parent_count']==0 for repo in [a,b])
assert all(r['collected_at_vienna'].startswith('2026-09-23') for r in figures['requests'])
assert '23 September 2026, 00:58–00:59' in proposal+evidence
assert len(json.loads((REVIEW/'phase-6-author-source-checks.json').read_text()))==3
assert 'Source hygiene checks passed.' in (REVIEW/'phase-6-final-hygiene.log').read_text()
assert 'Source hygiene checks passed.' in (REVIEW/'phase-6-final-extracted-hygiene.log').read_text()

pdfs={}
for name in ['snodec-book','book-proposal-package','book-proposal-sample-package']:
    path=ROOT/'dist/pdf'/(name+'.pdf')
    pages=int(re.search(r'Pages:\s+(\d+)',subprocess.check_output(['pdfinfo',str(path)],text=True))[1])
    assert not re.search(r'Warning|Overfull|Underfull',(BUILD/(name+'.log')).read_text()),name
    pdfs[name]={'pages':pages,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'warnings':0,'bad_boxes':0}
assert pdfs['snodec-book']['pages']==pagination['physical_pages']
with tarfile.open(ROOT/'dist/packages/snodec-book-proposal-package.tar.gz') as archive:
    files=[m for m in archive.getmembers() if m.isfile()]
    for member in files:
        assert archive.extractfile(member).read() == (ROOT/member.name.removeprefix('./')).read_bytes(),member.name
    for source in ['review/proposal/book-proposal-package.md','review/proposal/evidence-sheet.md','review/proposal/sample-chapters.md',*sample_paths]:
        assert source in [m.name.removeprefix('./') for m in files]
result={'scope':'Phase 6 only; manuscript, companion, production and CI unchanged',
        'previous_phase_reverified':True,'entry_check_groups_passed':10,'local_lab_cases_passed':62,
        'required_proposal_sections_passed':True,'chapter_titles_checked':31,'sample_chapters':sample_numbers,
        'part_page_sum':310,'unchanged_verified_comparable_titles':5,'manuscript_metrics_unchanged':True,
        'repository_collection_date_vienna':'2026-09-23','repository_figures_match':True,
        'author_evidence_limits_preserved':True,'pdfs':pdfs,'archive_identical_files':len(files),
        'production_line_delta':0,'test_implementation_line_delta':0}
(REVIEW/'phase-6-exit-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
print('PASS: Phase 6 dossier, dated evidence, unchanged manuscript metrics, PDF builds and package contents.')
