#!/usr/bin/env python3
"""Follow-up 12's nine manuscript/proposal assertions; no framework mutations.

Raw manifest inputs are authoritative. Historical review records and companion
sources are not reader prose. Exact protected-listing exceptions must be in the
terminology allowlist. Sentence diagnostics ignore code, tables, headings and
invisible reference identities, but retain figure captions and exercise prose.
Metrics come from the existing measurement authority; PDF extent from pdfinfo.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REVIEW = HERE.relative_to(ROOT)
VERIFY = re.compile(r"\b(does|do|did|can|cannot|could|will|would) ?(not|n't)? (by itself |alone |merely |yet )?(prove|establish|demonstrate|show)s?\b|\b(is|are) not (proof|evidence)\b|\bcannot (prove|establish|demonstrate)\b", re.I)
NOUNS = re.compile(r'\b(?:boundar(?:y|ies)|roles?|surfaces?|polic(?:y|ies)|carriers?|owners?|ownership|observations?|responsibilit(?:y|ies)|contracts?)\b', re.I)
FORBIDDEN = ('public role', 'role header', 'role file', 'the role is a',
             'selects a role', 'role-level', 'context role', 'protocol role',
             'server role', 'client role', 'communication role')
INTERNAL = re.compile(r'\b(?:wish|floors?|gates?|FOLLOWUP|P0a|P[0-7])\b|P[−-]1|107,338|112,338', re.I)


def rows(text):
    """Yield source line, text, in-code flag, respecting longer outer fences."""
    fence = None
    for n, line in enumerate(text.splitlines(), 1):
        if fence:
            yield n, line, True
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
                fence = None
        else:
            match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
            if match:
                fence = match[1]
            yield n, line, bool(fence)
    if fence:
        raise ValueError('unclosed code fence')


def visible(line):
    line = re.sub(r'!?\[([^\]]*)\]\([^)]*\)(?:\{[^}]*\})?', r'\1', line)
    line = re.sub(r'\\(?:ref|index)\{[^}]*\}|\{#[^}]*\}', '', line)
    return line


def sentences(text):
    lines = ['' if code or re.match(r'^\s*(?:\||#|\\index|:::|<!--)', line)
             else visible(line) for _, line, code in rows(text)]
    # Blank lines and sentence punctuation terminate a sentence; retain offsets.
    prose = '\n'.join(lines)
    for match in re.finditer(r'.+?(?:(?<=[.!?])(?=\s)|(?=\n\s*\n)|\Z)', prose, re.S):
        sentence = match[0].strip()
        if sentence:
            yield prose.count('\n', 0, match.start()) + 1, sentence


def tables(text):
    block, start = [], 0
    for n, line, code in list(rows(text)) + [(0, '', False)]:
        if not code and line.lstrip().startswith('|'):
            if not block:
                start = n
            block.append(line)
        elif block:
            yield start, '\n'.join(block)
            block = []


def chapter(texts, number):
    return next((p, t) for p, t in texts.items()
                if p.startswith(f'manuscript/chapters/{number:02}-'))


def sections(text):
    return re.split(r'^### .+$', text, flags=re.M)[1:]


def check(root, pdf):
    spec = importlib.util.spec_from_file_location('metrics', root/'ci/manuscript-metrics.py')
    metrics_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(metrics_module)
    metrics = metrics_module.manuscript_metrics(root, root/'manuscript/book-files.txt')
    texts = {p: (root/p).read_text() for p in metrics['files']}
    errors = []
    def need(ok, group, message):
        if not ok:
            errors.append(f'{group}: {message}')

    allowtext = (root/REVIEW/'terminology-allowlist.md').read_text()
    exceptions = json.loads(re.search(r'```json\n(.*?)\n```', allowtext, re.S)[1])
    consumed = set()
    for path, text in texts.items():
        for n, line, code in rows(text):
            for term in FORBIDDEN:
                pattern = r'\b' + re.escape(term).replace(r'\ ', r'[\s-]+') + r's?\b'
                if re.search(pattern, visible(line), re.I):
                    approved = [(i, e) for i, e in enumerate(exceptions)
                                if e['path'] == path and e['text'] == line.strip() and e['reason'] and code]
                    need(bool(approved), 1, f'{path}:{n}: {term}')
                    for i, _ in approved:
                        need((i, n) not in consumed, 1, 'repeated protected phrase on one line')
                        consumed.add((i, n))
    need({i for i, _ in consumed} == set(range(len(exceptions))), 1, 'unused phrase exception')
    need(len(consumed) == len(exceptions), 1, 'duplicated protected exception')

    for path, text in texts.items():
        if path.startswith('manuscript/chapters/04-'):
            continue
        for n, table in tables(text):
            names = [name for name in ('handle', 'instance', 'flow', 'connection', 'context', 'factory')
                     if re.search(r'\b' + (r'factor(?:y|ies)' if name == 'factory' else name + 's?') + r'\b', table, re.I)]
            need(len(names) < 5, 2, f'{path}:{n}: repeated taxonomy {names}')

    path, text = chapter(texts, 2)
    box = re.search(r'::: [^\n]*title="Shortest path to Chapter 3"[^\n]*\n(.*?)\n:::', text, re.S)
    items = re.findall(r'^\d+\. (.*?)(?=^\d+\. |\Z)', box[1] if box else '', re.M | re.S)
    need(len(items) >= 6, 3, 'shortest-path box needs six or more numbered items')
    for i, item in enumerate(items, 1):
        need(bool(re.search(r'`(?:mkdir|cd|git|export|cmake|cp|python|\./|ctest|ls|test|grep)\b[^`]*`', item)),
             3, f'shortest-path item {i} lacks a command')

    path, text = chapter(texts, 13)
    for i, section in enumerate(sections(text)[1:], 2):
        need('echoserver' in section and bool(re.search(r'8080|18091|18092|local\.port', section)),
             4, f'Ch13 section {i} loses the running port')

    path, text = chapter(texts, 21)
    first = sections(text)[0]
    first_table = first.find('| Shared concern |')
    figure = re.search(r'!\[.*?\]\(([^)]*mqtt-publication-sequence\.pdf)\)', first)
    fallback = re.search(r'```text\n(.*?)\n```', first, re.S)
    diagram = figure or fallback
    need(first_table >= 0 and diagram is not None and diagram.start() < first_table,
         5, 'MQTT sequence must precede the first class table')
    diagram_text = ''
    if figure:
        source = root/'assets/figures/src'/Path(figure[1]).with_suffix('.tex').name
        need(source.exists() and (root/figure[1]).is_file(), 5, 'MQTT figure source or built PDF missing')
        diagram_text = source.read_text() if source.exists() else ''
    elif fallback:
        diagram_text = fallback[1]
    for token in ('Subscriber', 'Broker', 'Publisher', 'CONNECT', 'CONNACK', 'SUBSCRIBE', 'SUBACK'):
        need(token in diagram_text, 5, 'sequence missing ' + token)
    need(diagram_text.count('PUBLISH') >= 2, 5, 'sequence needs incoming and forwarded PUBLISH')
    for pattern in (r'topic.*filter', r'`\+`', r'`#`', r'QoS 0', r'QoS 1', r'QoS 2',
                    r'retained message', r'keep-alive', r'PINGREQ', r'PINGRESP',
                    r'clean session', r'persistent session', r'MQTT 3\.1\.1'):
        need(bool(re.search(pattern, first, re.I)), 5, 'MQTT fundamentals missing ' + pattern)

    path, text = chapter(texts, 18)
    box = re.search(r'::: [^\n]*title="Routing API reference"[^\n]*\n(.*?)\n:::', text, re.S)
    need(bool(box), 6, 'routing reference box missing')
    outside = text[:box.start()] + text[box.end():] if box else text
    remaining = list(tables(outside))
    need(len(remaining) <= 1, 6, 'more than one routing table outside reference box')
    need(not remaining or '| Concern | HTTP layer | Express-like layer |' in remaining[0][1],
         6, 'remaining table is not the HTTP/Express comparison')

    _, text = chapter(texts, 23)
    worked = re.search(r'^### Worked change:.*?\n(.*?)(?=^### |\Z)', text, re.M | re.S)
    need(bool(worked), 7, 'worked decision missing')
    need(not re.search(r'sequence (?:number|owner|authority)', worked[1] if worked else '', re.I),
         7, 'worked decision repeats sequence ownership')
    for label in ('Requirement', 'Options', 'Decision', 'Consequence', 'Test'):
        need(worked and f'**{label}.**' in worked[1], 7, 'worked decision missing ' + label)
    for number in (23, 26):
        path, text = chapter(texts, number)
        for n, sentence in sentences(text):
            hits = NOUNS.findall(sentence)
            need(len(hits) < 3, 7, f'{path}:{n}: abstraction stack {hits}: {sentence}')

    count = sum(len(VERIFY.findall(t)) for t in texts.values())
    need(count <= 46, 8, f'verification constructions: {count} > 46')

    proposal_paths = sorted((root/'review/proposal').glob('*.md'))
    for path in proposal_paths:
        need(not INTERNAL.search(path.read_text()), 9, f'{path.relative_to(root)}: internal revision term')
    package = (root/'review/proposal/book-proposal-package.md').read_text()
    evidence = (root/'review/proposal/evidence-sheet.md').read_text()
    totals = metrics['totals']
    try:
        info = subprocess.check_output(['pdfinfo', str(pdf)], text=True)
        pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    except (OSError, subprocess.CalledProcessError, TypeError):
        pages = None
        need(False, 9, 'cannot read rebuilt PDF extent')
    expected = {
        'total': totals['total_words'], 'fenced': totals['code_words'],
        'prose': totals['prose_words'], 'pages': pages,
        'headings': totals['chapter_headings_level_3_and_deeper'],
        'section_average': totals['average_chapter_section_prose_words'],
        'text_fences': totals['fenced_blocks_by_language'].get('text', 0),
    }
    for label, source, pattern, actual in (
        ('extent', package, r'([\d,]+) (?:total )?whitespace tokens', expected['total']),
        ('fenced tokens', package, r'including ([\d,]+) fenced tokens', expected['fenced']),
        ('pages', package, r'(\d+) pages', pages),
        ('headings', package, r'(\d+) chapter subheadings', expected['headings']),
        ('section average', package, r'average ([\d.]+) prose words per section', expected['section_average']),
        ('text fences', package, r'(\d+) text fences', expected['text_fences']),
        ('evidence extent', evidence, r'([\d,]+) whitespace tokens', expected['total']),
        ('evidence prose', evidence, r'([\d,]+) are prose', expected['prose']),
        ('evidence fences', evidence, r'([\d,]+) occur in fences', expected['fenced']),
        ('evidence pages', evidence, r'(\d+) pages', pages)):
        values = re.findall(pattern, source)
        need(bool(values) and all(float(v.replace(',', '')) == actual for v in values),
             9, f'{label}: {values} differs from current {actual}')
    need('105,000' not in package and '115,000 words' in package, 9, 'length ceiling/old stretch target')
    for name, pattern, actual in (
        ('chapters', r'(\d+) (?:numbered )?chapters', len([p for p in texts if re.search(r'/\d\d-',p) and '/chapters/' in p])),
        ('objectives', r'(?<![\d–-])(\d+) objectives', sum(len(re.findall(r'^- \*\*O\d+\.',t,re.M)) for t in texts.values())),
        ('exercises', r'(\d+) mapped exercises', sum(len(re.findall(r'^\d+\. \*\*(?:Review|Lab|Design)',t,re.M)) for t in texts.values())),
        ('rule boxes', r'(\d+) rule boxes', totals['callout_counts_by_class']['snodec-rule'])):
        matches = re.findall(pattern, package + '\n' + evidence)
        need(bool(matches) and all(int(v) == actual for v in matches), 9, f'{name}: {matches} differs from {actual}')
    return errors, {'assertion_groups': 9,
                    'group_status': {str(i): ('FAIL' if any(e.startswith(str(i)+':') for e in errors) else 'PASS') for i in range(1, 10)},
                    'verification_constructions': count,
                    'proposal_metrics': expected, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--pdf', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    errors, data = check(root, args.pdf or root/'dist/pdf/snodec-book.pdf')
    if args.output:
        args.output.write_text(json.dumps(data, indent=2)+'\n')
    for error in errors:
        print('ERROR: ' + error)
    passed = sum(v == 'PASS' for v in data['group_status'].values())
    print(f"{'FAIL' if errors else 'PASS'}: {passed}/9 polish assertion groups pass; {data['verification_constructions']} verification constructions")
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
