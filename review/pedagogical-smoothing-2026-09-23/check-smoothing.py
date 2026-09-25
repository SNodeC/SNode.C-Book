#!/usr/bin/env python3
"""Assert PROMPT §12 against raw manifest inputs; emit reproducible diagnostics.

Optional waiver files contain a fenced JSON list with chapter, reason, rows,
completion_evidence, and recovery_chapters (floors only). No waiver is in use.
Diagnostic identifiers are unique monospace C++-like spellings per 1,000 prose
words, not a claim that every spelling is new to the reader. Split baseline
units use the approved headings; their apparatus remains in its original half.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SPEC = importlib.util.spec_from_file_location('metrics', ROOT/'ci/manuscript-metrics.py')
METRICS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(METRICS)
DEPRECATED = ('configured role', 'registered instance', 'configuration instance',
              'runtime-visible role', 'endpoint role', 'configured endpoint',
              'named endpoint', 'lower family', 'communication family',
              'lower communication family', 'peer episode', 'connection episode',
              'server instance', 'client instance')
PROVENANCE = ('recorded working-tree', 'source identity', 'must not be presented',
              'handshake claims', 'Existing consumers',
              'source tree recorded for this edition', 'For this edition')
CANONICAL = ('endpoint handle', 'instance', 'named instance', 'anonymous instance',
             'flow', 'flow handle', 'connection', 'context', 'factory',
             'network family', 'transport form', 'connection variant', 'carrier',
             'role', 'acceptance', 'accepted state')


def pattern(term):
    return r'\b' + re.escape(term).replace(r'\ ', r'[\s-]+').replace(r'\-', r'[\s-]+').replace('family', 'famil(?:y|ies)') + r's?\b'


def fences(text):
    result, opened = [], None
    for i, line in enumerate(text.splitlines()):
        if opened:
            start, marker, language = opened
            if re.fullmatch(r' {0,3}'+re.escape(marker[0])+'{'+str(len(marker))+r',}\s*', line):
                result.append((start, i, language))
                opened = None
        else:
            match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
            if match:
                opened = (i, match[1], match[2].strip())
    if opened:
        raise ValueError('unclosed fence')
    return result


def body(text):
    # Discard objectives and chapter title; retain the opening teaching paragraph.
    objectives = re.search(r'::: \{\.snodec-objectives[^\n]*\n.*?\n:::[ \t]*\n', text, re.S)
    if objectives:
        text = text[objectives.end():]
    return text.split('::: {.snodec-remember', 1)[0]


def first_section(text):
    sections = re.split(r'^### .+$', body(text), flags=re.M)
    return sections[1] if len(sections) > 1 else sections[0]


def diagnostics(text):
    b = body(text)
    lines = b.splitlines()
    blocked = set()
    for start, end, _ in fences(b):
        blocked.update(range(start, end+1))
    prose = '\n'.join(line for i, line in enumerate(lines) if i not in blocked)
    identifiers = sorted(set(re.findall(r'`([A-Za-z_]\w*(?:::\w+)*(?:\(\))?)`', prose)))
    clusters = []
    for sentence in re.split(r'(?<=[.!?])\s+|\n\n', prose):
        nouns = re.findall(r'\b(?:boundar(?:y|ies)|roles?|surfaces?|polic(?:y|ies)|carriers?|owners?|ownership|observations?)\b', sentence, re.I)
        if len(nouns) >= 3:
            clusters.append({'nouns': nouns, 'passage': sentence.strip()})
    opening = []
    for line in lines:
        if re.match(r'\s*(?:`{3,}|~{3,}|\||!\[|:::)', line):
            break
        if line and not re.match(r'\s*(?:#|\\index|<span)', line):
            opening.append(line)
    blocks = [p.strip() for p in re.split(r'\n\s*\n', b) if p.strip()]
    return {'identifier_density_per_1000_prose_words': round(1000*len(identifiers)/max(1,len(prose.split())),2),
            'identifier_spellings': identifiers,
            'identifier_spellings_in_first_400_words': sorted(set(re.findall(r'`([A-Za-z_]\w*(?:::\w+)*(?:\(\))?)`', ' '.join(prose.split()[:400])))),
            'prose_words_before_first_nonprose_block': len(' '.join(opening).split()),
            'abstract_noun_clusters': clusters,
            'context_terms': {term: len(re.findall(pattern(term), prose, re.I)) for term in ('communication role','server instance','client instance','role')},
            'fenced_tokens': METRICS.measure(text)['code_words'],
            'last_three_blocks_before_recap': blocks[-3:]}


def check(root):
    review = root/'review/pedagogical-smoothing-2026-09-23'
    structure = json.loads((review/'smoothing-structure.json').read_text())
    metrics = METRICS.manuscript_metrics(root, root/'manuscript/book-files.txt')
    texts = {p:(root/p).read_text() for p in metrics['files']}
    units = structure['chapters']
    missing = [u['path'] for u in units if u['path'] not in texts]
    if missing:
        return ['3: missing manifest units: '+', '.join(missing)], metrics, structure, texts
    chapters = {u['new']:texts[u['path']] for u in units}
    errors = []
    def need(condition, number, message):
        if not condition:
            errors.append(f'{number}: {message}')
    total = metrics['totals']['total_words']
    need(107338 <= total <= 115000, 1, f'total {total} outside absolute budget')
    waivers = {}
    for kind in ('floor', 'cap'):
        p = review/f'{kind}-waivers.md'
        entries = []
        if p.exists():
            match = re.search(r'```json\s*\n(.*?)\n```', p.read_text(), re.S)
            need(bool(match),2,f'{kind} waiver needs structured evidence')
            if match:
                entries = json.loads(match[1])
        waivers[kind] = {str(w['chapter']):w for w in entries}
    for u in units:
        n = metrics['files'][u['path']]['total_words']
        for kind, fails in [('floor',n<u['floor']),('cap',n>u['cap'])]:
            if fails:
                w = waivers[kind].get(u['new'],{})
                fields = ['reason','rows','completion_evidence'] + (['recovery_chapters'] if kind=='floor' else [])
                need(all(w.get(f) for f in fields),2,f"Ch{u['new']} {n} outside {kind} {u[kind]} without complete waiver")
        need(n <= u['cap']*1.05,2,f"Ch{u['new']} exceeds absolute 105% cap")
    for group,lo,hi in [('frontmatter',2280,2430),('parts',1356,1456),('backmatter',781,800)]:
        n=sum(m['total_words'] for p,m in metrics['files'].items() if f'/{group}/' in p)
        waived = False
        if group == 'backmatter' and hi < n <= 812:
            p = review/'backmatter-cap-waiver.md'
            match = re.search(r'```json\s*\n(.*?)\n```', p.read_text(), re.S) if p.exists() else None
            try:
                w = json.loads(match[1]) if match else {}
                waived = (w.get('group') == group and w.get('original_cap') == hi
                          and w.get('approved_cap') == 812 and bool(w.get('authority'))
                          and bool(w.get('reason')))
            except (ValueError, AttributeError):
                waived = False
        need(lo<=n<=hi or waived,2,f'{group} {n} outside {lo}..{hi} without the explicit 812-token author waiver')
    epilogue=next(t for p,t in texts.items() if p.endswith('/epilogue.md'))
    need(1338<=len(epilogue.split())<=1438,2,'epilogue floor/cap')
    expected=[str(n) for n in range(1,33)]+['A']
    paths=[u['path'] for u in units]
    need([u['new'] for u in units]==expected,3,'ordered 32 chapters plus A')
    need([p for p in texts if p in paths]==paths,3,'manifest unit order')
    disk={str(p.relative_to(root)) for p in (root/'manuscript/chapters').glob('*.md') if p.name!='epilogue.md'}
    need(disk==set(paths),3,'orphan/missing chapter files')
    for u in units:
        t=chapters[u['new']]
        need(re.findall(r'^- \*\*O([123])\.\*\*',t,re.M)==list('123'),4,f"Ch{u['new']} objectives")
        need(t.count('.snodec-remember')==1 and t.count('.snodec-exercise')==1,4,f"Ch{u['new']} recap/exercises")
        tiers=re.findall(r'^([1-5])\. \*\*(Review|Lab|Design)\b',t,re.M)
        need(tiers==list(zip('12345',['Review','Review','Lab','Lab','Design'])),4,f"Ch{u['new']} tier order")
        answer=root/'companion/exercises'/('appendix-a' if u['new']=='A' else f"ch{int(u['new']):02}")/'README.md'
        need(answer.exists(),4,f'missing {answer}')
        if answer.exists():
            need(len(re.findall(r'^## [1-5][. )]',answer.read_text(),re.M))==5,4,f'{answer} answer sections')
    for p in structure['parts']:
        t=chapters[str(p['chapters'][-1])].split('.snodec-exercise',1)[-1]
        need(bool(re.search(r'Part '+p['part']+r'\b[^\n]*checkpoint',t,re.I)),4,f"Part {p['part']} ending checkpoint")
    need(all('TODO(P3-apparatus)' not in t for t in texts.values()),4,'manuscript apparatus placeholder')
    need(not any('TODO(P3-apparatus)' in p.read_text() for p in (root/'companion/exercises').rglob('README.md')),4,'answer placeholder')
    need(metrics['totals']['callout_counts_by_class']['snodec-rule']<=20,5,'rule box ceiling')
    for p,t in texts.items():
        # These IDs are immutable reference identities, not learner vocabulary.
        clean=t
        for identity in ('#configured-endpoints-and-activation-flows',
                         '#from-configured-roles-to-visible-runtime-behavior',
                         '#carrier-and-protocol-decisions', '#choosing-the-carrier-at-each-boundary',
                         '#the-lower-family-transfer-model', '#designing-for-lower-family-transfer',
                         '#fig:snodec-lower-family-transfer', r'\ref{fig:snodec-lower-family-transfer}',
                         'assets/figures/pdf/fig-04-lower-family-transfer-model.pdf'):
            clean=clean.replace(identity, '')
        for term in DEPRECATED:
            need(not re.search(pattern(term),clean,re.I),6,f'{p}: deprecated {term}')
        if p.endswith('/conventions.md'):
            clean=re.sub(r'^\| \*\*Carrier\*\*.*$', '', clean, flags=re.M)
        if p not in [units[20]['path'],units[21]['path']]:
            need(not re.search(r'\bcarriers?\b',clean,re.I),6,f'{p}: carrier outside allowance')
        if p!=units[1]['path']:
            for phrase in PROVENANCE:
                need(not re.search(pattern(phrase),t,re.I),7,f'{p}: provenance {phrase}')
    for n in (17,18,19,21,22):
        b=body(chapters[str(n)])
        match=re.search(r'::: \{\.snodec-note title="Build note"\}.*?\n:::',b,re.S)
        need(bool(match),8,f'Ch{n} missing Build note')
        if match:
            tail=b[match.end():]
            need(not fences(tail),8,f'Ch{n} listing after Build note')
            need(any(line.strip() and not line.startswith(('#','\\',':::')) for line in tail.splitlines()),8,f'Ch{n} no transition after Build note')
    t=chapters['18']; table=re.search(r'^\|',t,re.M)
    need('dispatch.cpp' in t and table and t.index('dispatch.cpp')<table.start() and '<!-- snodec-source: companion/exercises/ch18/dispatch.cpp -->' in t[:table.start()],9,'dispatch marked listing before first table')
    need(all(word in re.split(r'^\|', first_section(chapters['21']), maxsplit=1, flags=re.M)[0] for word in ('CONNECT','CONNACK','SUBSCRIBE','SUBACK','PUBLISH')),10,'MQTT first-section conversation')
    need(all(word in first_section(chapters['27']) for word in ('find_package','target_link_libraries')),11,'minimal CMake consumer first')
    need(not any(lang=='sh' for _,_,lang in fences(first_section(chapters['29']))),12,'Ch29 opens with shell commands')
    need(all(end-start-1<=60 for start,end,_ in fences(chapters['31'])),13,'Ch31 fence exceeds 60 lines')
    t=chapters['30'];lines=t.splitlines();blocks=fences(t)
    for (_,end,_),(start,_,_) in zip(blocks,blocks[1:]):
        between=lines[end+1:start]
        need(any(line.strip() and not re.match(r'\s*(?:#|\\index|:::|<!--|<span)',line) for line in between),13,f'Ch30 adjacent listings at {end+1}/{start+1}')
    need(len(re.findall(r'^### Worked decision',chapters['32'],re.M))>=3,14,'three worked decisions')
    t=body(chapters['6']); first=fences(t)[0][0];before='\n'.join(t.splitlines()[:first])
    need(all(re.search(s,before,re.I) for s in ('peer A','peer B','retry timer','queued callback','wait','dispatch','timeout','cleanup')),15,'event-loop thought experiment before source')
    need('### Observed descriptor populations' in chapters['A'] and '### Observed descriptor populations' not in chapters['6'],15,'descriptor population section placement')
    glossary=texts['manuscript/frontmatter/conventions.md'].split('### Vocabulary',1)[-1]
    need(all(re.search(pattern(term),glossary,re.I) for term in CANONICAL),16,'incomplete canonical glossary')
    return errors,metrics,structure,texts


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    parser.add_argument('--diagnostics',type=Path)
    args=parser.parse_args()
    errors,metrics,structure,texts=check(args.root.resolve())
    print(f"Total {metrics['totals']['total_words']}; distance to wish {112338-metrics['totals']['total_words']:+d}; 16 assertion groups")
    backmatter = sum(m['total_words'] for p,m in metrics['files'].items() if '/backmatter/' in p)
    if backmatter > 800 and not any(e.startswith('2: backmatter') for e in errors):
        print(f'Backmatter {backmatter}/800: explicit author waiver permits at most 812; global ceiling remains 115000')
    if args.diagnostics:
        oldfiles=subprocess.check_output(['git','show','c7b76c1:manuscript/book-files.txt'],cwd=args.root,text=True).splitlines()
        records=[]
        for u in structure['chapters']:
            old=u['old'][0]
            prefix='appendix-a' if old=='A' else f'{int(old):02}-'
            path=next(p for p in oldfiles if p.startswith('manuscript/chapters/'+prefix))
            before=subprocess.check_output(['git','show',f'c7b76c1:{path}'],cwd=args.root,text=True)
            if u['new'] in ('4','5'):
                split=before.index('### Reading public types and components')
                before=before[:split] if u['new']=='4' else before[split:]
            if u['new'] in ('25','26'):
                split=before.index('### From applications to systems')
                before=before[:split] if u['new']=='25' else before[split:]
            a,b=diagnostics(before),diagnostics(texts[u['path']])
            records.append({'chapter':u['new'],'old':old,'path':u['path'],'before':a,'after':b,'fenced_token_delta':b['fenced_tokens']-a['fenced_tokens']})
        args.diagnostics.write_text(json.dumps({'baseline':'c7b76c1','definition':__doc__,'chapters':records},indent=2)+'\n')
    for error in errors: print('ERROR',error)
    print('PASS' if not errors else f'FAIL ({len(errors)} findings)')
    return bool(errors)

if __name__=='__main__':
    raise SystemExit(main())
