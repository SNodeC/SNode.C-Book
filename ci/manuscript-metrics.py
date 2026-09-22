#!/usr/bin/env python3
"""Deterministic source metrics over the ordered manuscript inputs; standard library only."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re

CLASSES = ('remember', 'rule', 'note', 'warning', 'checklist', 'exercise', 'objectives')
FORBIDDEN = {
    'in the manuscript': r'\bin\s+the\s+manuscript\b',
    'manuscript material': r'\bmanuscript\s+material\b',
    'the chapter should': r'\bthe\s+chapter\s+should\b',
    'the book should': r'\bthe\s+book\s+should\b',
    'this chapter should': r'\bthis\s+chapter\s+should\b',
    'published edition': r'\bpublished\s+edition\b',
    'should be presented as': r'\bshould\s+be\s+presented\s+as\b',
    'useful for Chapter 29': r'\buseful\s+for\s+Chapter\s+29\b',
    'the benchmarking tone should be': r'\bthe\s+benchmarking\s+tone\s+should\s+be\b',
}
TERMS = {
    'role': r'\brole\b',
    'boundary/boundaries': r'\bboundar(?:y|ies)\b',
    'visible': r'\bvisible\b',
    'is not a': r'\bis\s+not\s+a\b',
    'does not prove': r'\bdoes\s+not\s+prove\b',
    'does not by itself': r'\bdoes\s+not\s+by\s+itself\b',
}
FENCE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
HEADING = re.compile(r'^ {0,3}(#{1,6})\s+(.+?)\s*$')


def locations(text, pattern):
    return [{'line': text.count('\n', 0, m.start()) + 1, 'match': m.group()}
            for m in re.finditer(pattern, text, re.IGNORECASE)]


def measure(text):
    headings = Counter({str(n): 0 for n in range(1, 7)})
    callouts = Counter({'snodec-' + name: 0 for name in CLASSES})
    fences = Counter()
    prose_lines = []
    code_words = marker_words = section_words = sections = 0
    closing = []
    fence = None
    in_section = False
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        words = len(line.split())
        if fence:
            code_words += words
            prose_lines.append('\n' if line.endswith('\n') else '')
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' +
                            str(len(fence)) + r',}[ \t]*', line.rstrip('\r\n')):
                marker_words += words
                fence = None
            continue
        opening = FENCE.match(line)
        if opening:
            fence, info = opening.groups()
            if fence[0] == '`' and '`' in info:
                raise ValueError(f'invalid backtick fence at line {number}')
            language = info.strip().split()[0] if info.strip() else '(unlabelled)'
            if language.startswith('{'):
                language = language.lstrip('{.').rstrip('}')
                language = language or '(unlabelled)'
            fences[language] += 1
            code_words += words
            marker_words += words
            prose_lines.append('\n' if line.endswith('\n') else '')
            continue
        prose_lines.append(line)
        heading = HEADING.match(line)
        if heading:
            level = len(heading[1])
            headings[str(level)] += 1
            in_section = level >= 3
            sections += int(in_section)
            if re.match(r'Closing\s+perspective(?:\s|$)', heading[2], re.IGNORECASE):
                closing.append({'line': number, 'heading': heading[2]})
        elif in_section:
            section_words += words
        if re.match(r'^ {0,3}:{3,}\s*\{', line):
            for name in callouts:
                callouts[name] += len(re.findall(r'\.' + name + r'(?=[\s}])', line))
    if fence:
        raise ValueError('unclosed fenced block')
    prose = ''.join(prose_lines)
    total = len(text.split())
    forbidden = {name: locations(prose, pattern) for name, pattern in FORBIDDEN.items()}
    return {
        'total_words': total,
        'prose_words': total - code_words,
        'code_words': code_words,
        'code_content_words': code_words - marker_words,
        'fence_marker_words': marker_words,
        'heading_counts_by_level': dict(headings),
        'section_count': sections,
        'section_prose_words': section_words,
        'average_section_prose_words': round(section_words / sections, 2) if sections else None,
        'callout_counts_by_class': dict(callouts),
        'fenced_blocks_by_language': dict(sorted(fences.items())),
        'closing_perspective_sections': closing,
        'forbidden_phrase_hits': forbidden,
        'forbidden_phrase_hit_count': sum(map(len, forbidden.values())),
        'term_occurrences': {name: locations(prose, pattern) for name, pattern in TERMS.items()},
        'manual_chapter_references': locations(prose, r'\bChapter\s+\d+\b'),
    }


def manuscript_metrics(root, manifest):
    paths = [line.strip() for line in manifest.read_text().splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('manifest must contain nonempty, unique input paths')
    files = {path: measure((root / path).read_text(encoding='utf-8')) for path in paths}
    totals = {key: sum(item[key] for item in files.values()) for key in
              ('total_words', 'prose_words', 'code_words', 'code_content_words',
               'fence_marker_words', 'forbidden_phrase_hit_count')}
    for key in ('heading_counts_by_level', 'callout_counts_by_class', 'fenced_blocks_by_language'):
        counts = Counter()
        for item in files.values():
            counts.update(item[key])
        totals[key] = dict(sorted(counts.items()))
    chapters = [item for path, item in files.items() if Path(path).parent == Path('manuscript/chapters')]
    totals['chapter_headings_level_3_and_deeper'] = sum(item['section_count'] for item in chapters)
    totals['chapter_section_prose_words'] = sum(item['section_prose_words'] for item in chapters)
    n = totals['chapter_headings_level_3_and_deeper']
    totals['average_chapter_section_prose_words'] = round(totals['chapter_section_prose_words'] / n, 2) if n else None
    totals['closing_perspective_sections'] = sum(len(item['closing_perspective_sections']) for item in files.values())
    totals['term_occurrence_counts'] = {name: sum(len(item['term_occurrences'][name]) for item in files.values()) for name in TERMS}
    totals['manual_chapter_reference_count'] = sum(len(item['manual_chapter_references']) for item in files.values())
    expected = {
        'total_words': (151922, totals['total_words']),
        'chapter_headings_level_3_and_deeper': (1020, n),
        'closing_perspective_sections': (15, totals['closing_perspective_sections']),
        'snodec-remember': (38, totals['callout_counts_by_class']['snodec-remember']),
        'snodec-rule': (30, totals['callout_counts_by_class']['snodec-rule']),
        'text_fences': (478, totals['fenced_blocks_by_language'].get('text', 0)),
        'cpp_fences': (205, totals['fenced_blocks_by_language'].get('cpp', 0)),
        'snodec-exercise': (0, totals['callout_counts_by_class']['snodec-exercise']),
    }
    return {
        'schema_version': 1,
        'manifest': manifest.relative_to(root).as_posix(),
        'file_count': len(files),
        'definitions': {
            'words': 'Python str.split whitespace tokens in raw UTF-8 manuscript inputs, including markup.',
            'partition': 'prose_words + code_words = total_words. code_words includes opening/closing fence lines; code_content_words excludes them.',
            'structure': 'ATX headings and fenced Div classes outside backtick/tilde code fences; languages preserve source labels. No Markdown rendering.',
            'sections': 'Each chapter heading at level 3–6 starts a non-overlapping section. Count non-code body tokens until the next heading; exclude heading lines and chapter preambles. Empty parent sections count. Chapters include the epilogue.',
            'phrases': 'Case-insensitive whole words outside code fences; whitespace may span lines. Singular role and exact visible; boundary and boundaries combined. Raw inline markup remains.',
            'forbidden': 'Nine non-overlapping guards cover the five named examples and seven guard phrases; hit locations are source line numbers. Similar phrasing still needs editorial review.',
            'manual_references': 'Literal Chapter followed by an integer outside code fences; source line and matched text recorded, including self-references. Ranges/plural Chapters require editorial review.',
        },
        'totals': totals,
        'requested_baseline_comparison': {key: {'expected': a, 'actual': b, 'delta': b-a} for key, (a, b) in expected.items()},
        'files': files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, help='JSON destination; otherwise stdout')
    args = parser.parse_args()
    root = args.root.resolve()
    result = manuscript_metrics(root, root / 'manuscript/book-files.txt')
    output = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(output, encoding='utf-8')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
