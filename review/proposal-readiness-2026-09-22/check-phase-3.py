#!/usr/bin/env python3
"""Recheck Phase 3's measurable exits after rebuilding the proposal package.

Publisher-page verification and editorial/visual review are separately documented.
This check does not substitute for the build and lab commands in REPORT.md.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[2]
REVIEW = Path(__file__).resolve().parent
BUILD = ROOT / 'build/proposal-readiness-phase-2'
proposal = (ROOT / 'review/proposal/book-proposal-package.md').read_text()
evidence = (ROOT / 'review/proposal/evidence-sheet.md').read_text()
sections = ['Pitch', 'Reader and learning path', 'Comparable titles',
            'Manuscript overview and estimated extent', 'Revision plan',
            'Author platform and market evidence',
            'Companion material and technical verification']
for section in sections:
    assert f'# {section}\n' in proposal, section
pitch = proposal.split('# Pitch\n', 1)[1].split('\n# ', 1)[0].strip()
assert '\n\n' not in pitch
assert 'without a lecturer' in proposal and 'no SNode.C knowledge' in proposal
assert 'Network and Distributed Systems' in proposal and 'Hagenberg' in proposal
assert '[AUTHOR TO SUPPLY]' in proposal and '[AUTHOR TO SUPPLY]' in evidence
assert len(re.findall(r'^\| \d+ \|', proposal, re.M)) == 38
books = json.loads((REVIEW / 'phase-3-bibliography.json').read_text())['books']
assert 4 <= len(books) <= 6
for book in books:
    for fact in [book['title'], book['publisher'], str(book['year']),
                 book['source'], *book['authors']]:
        assert fact in proposal, fact
metrics = json.loads(subprocess.check_output(
    ['python3', 'ci/manuscript-metrics.py'], cwd=ROOT, text=True))
assert metrics == json.loads((REVIEW / 'metrics-after-phase-3.json').read_text())
pagination = json.loads((REVIEW / 'phase-3-pagination.json').read_text())
assert sum(p['pages'] for p in pagination['parts']) + pagination['front_matter_pages'] == pagination['total_pdf_pages']
for part in pagination['parts']:
    row = next(line for line in proposal.splitlines() if line.startswith('| ' + part['title'] + ' |'))
    assert int(row.split('|')[-2].strip()) == part['pages']
pdfs = {}
for name in ['book-proposal-package', 'book-proposal-sample-package', 'snodec-book']:
    path = ROOT / 'dist/pdf' / (name + '.pdf')
    info = subprocess.check_output(['pdfinfo', str(path)], text=True)
    pages = int(re.search(r'Pages:\s+(\d+)', info)[1])
    log = (BUILD / (name + '.log')).read_text()
    assert not re.search(r'Warning|Overfull|Underfull', log), name
    pdfs[name] = {'pages': pages, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                  'warnings': 0, 'bad_boxes': 0}
assert pdfs['snodec-book']['pages'] == pagination['total_pdf_pages']
archive = ROOT / 'dist/packages/snodec-book-proposal-package.tar.gz'
paths = subprocess.check_output(['git', 'ls-files', 'companion'], cwd=ROOT, text=True).splitlines()
paths += [f'dist/pdf/{name}.pdf' for name in pdfs]
paths += [f'review/proposal/{name}.md' for name in ['book-proposal-package', 'evidence-sheet', 'sample-chapters']]
with tarfile.open(archive) as packed:
    names = packed.getnames()
    assert len(names) == len(set(names))
    assert not any('__pycache__' in n or n.endswith('.pyc') for n in names)
    for name in paths:
        assert packed.extractfile('./' + name).read() == (ROOT / name).read_bytes(), name
result = {'required_sections': sections, 'verified_comparables': len(books),
          'manuscript_metrics_match': True, 'part_pages_sum': pagination['total_pdf_pages'],
          'pdfs': pdfs, 'archive_byte_identical_files': len(paths),
          'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}
(REVIEW / 'phase-3-exit-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
print('PASS: section coverage, recorded bibliography, manuscript metrics, pagination, clean final PDF logs, and archive contents')
print('Reread quality, live publisher verification, actual build execution, labs, and visual review require their separate evidence.')
