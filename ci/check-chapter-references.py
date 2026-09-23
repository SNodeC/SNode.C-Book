#!/usr/bin/env python3
"""Check current chapter references against approved topic identities, not just ranges.

When prose is revised, review its intended topic and update the occurrence register.
Do not regenerate target identities from the edited numbers: that would certify a
valid-but-wrong number. Historical proposal/review snapshots are outside this check.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = Path('review/pedagogical-smoothing-2026-09-23')
REFERENCE = re.compile(
    r'\bChapters?\s+\d+(?:(?:\s*(?:--?|[–—]|through|to|,\s*(?:(?:and|then)\s+)?|and)\s*)\d+)*'
    r'|\bAppendix A|\b(?:[Tt]he )?section “[^”]+”|\b(?:[Tt]he )?source-reading introduction', re.I)


def check(root=ROOT):
    plan = json.loads((root / REVIEW / 'smoothing-structure.json').read_text())
    register = json.loads((root / REVIEW / 'smoothing-reference-register.json').read_text())
    manifest = (root / 'manuscript/book-files.txt').read_text().splitlines()
    chapters = [p for p in manifest if re.match(r'manuscript/chapters/(?:\d\d-|appendix-)', p)]
    assert chapters == [r['path'] for r in plan['chapters']], 'Approved chapter order differs'
    assert len(manifest) == len(set(manifest)), 'Duplicate manuscript input'
    assert sorted(n for row in plan['chapters'] for n in row['old']) == sorted(list(map(str, range(1, 31))) + ['4', '24', 'A'])
    assert [r['new'] for r in plan['chapters']] == list(map(str, range(1, 33))) + ['A']
    actual_chapters = {str(p.relative_to(root)) for p in (root / 'manuscript/chapters').glob('*.md')}
    assert actual_chapters == {p for p in manifest if '/chapters/' in p}, 'Unlisted or missing chapter'
    assert len([p for p in manifest if '/parts/' in p]) == 12, 'Eleven Parts plus epilogue opener required'
    actual_parts = [p for p in manifest if '/parts/' in p][:11]
    assert actual_parts == [p['path'] for p in plan['parts']], 'Approved Part order differs'
    for part in plan['parts']:
        assert (root / part['path']).read_text().startswith('# ' + part['title'] + '\n')
        start = manifest.index(part['path'])
        next_part = next((i for i in range(start + 1, len(manifest)) if '/parts/' in manifest[i]), len(manifest))
        members = [r for r in plan['chapters'] if r['path'] in manifest[start:next_part]]
        assert [r['new'] for r in members] == list(map(str, part['chapters'])), 'Chapter in wrong Part'
    anchors = defaultdict(list)
    owners = {}
    for row in plan['chapters']:
        path = row['path']; text = (root / path).read_text()
        assert re.search(r'^## ' + re.escape(row['title']) + r' \{#', text, re.M), path
        owners[path] = row['new']
        for anchor in re.findall(r'\{#([^}\s]+)', text):
            anchors[anchor].append(path)
    for anchor, topic in plan['topic_anchors'].items():
        assert anchors[anchor] == [topic['path']], f'Missing/ambiguous topic: {anchor}'
        assert owners[topic['path']] == topic['chapter'], f'Topic in wrong chapter: {anchor}'
        approved = plan['old_to_new'][str(topic['old_chapter'])]
        assert topic['chapter'] in approved
    paths = ['README.md', 'STRUCTURE.md'] + manifest
    paths += sorted(str(p.relative_to(root)) for p in (root / 'companion').rglob('*.md'))
    expected = defaultdict(list)
    for ref in register['references']:
        expected[ref['file']].append(ref)
    assert set(expected) <= set(paths), 'Registered reference in missing/unscanned file'
    checked = 0
    for path in paths:
        text = (root / path).read_text()
        matches = list(REFERENCE.finditer(text))
        assert len(matches) == len(expected[path]), f'{path}: unregistered/removed reference; review its intended topic'
        for match, ref in zip(matches, expected[path]):
            label = ' '.join(match[0].split())
            where = f'{path}:{text.count(chr(10), 0, match.start()) + 1}'
            assert label == ref['text'], f'{where}: changed reference; expected {ref["text"]!r}, got {label!r}'
            destinations = {plan['topic_anchors'][a]['chapter'] for a in ref['targets']}
            if label.lower().startswith('chapter'):
                numbers = re.findall(r'\d+', label)
                if len(numbers) == 2 and re.search(r'–|--?|through|to', label):
                    numbers = list(map(str, range(int(numbers[0]), int(numbers[1]) + 1)))
                assert set(numbers) == destinations - {'A'}, f'{where}: reference names the wrong topic'
            elif label.lower() == 'appendix a':
                assert destinations == {'A'}, f'{where}: wrong appendix topic'
            elif 'source-reading introduction' in label.lower():
                assert destinations == {'5'}, f'{where}: main-path orientation moved out of reach'
            else:
                assert len(ref['targets']) == 1, f'{where}: ambiguous section target'
                anchor = ref['targets'][0]
                heading = re.search(r'^### (.*?) \{#' + re.escape(anchor) + r'\}', (root / plan['topic_anchors'][anchor]['path']).read_text(), re.M)
                assert heading and f'“{heading[1]}”' in label, f'{where}: section title differs from intended topic'
            checked += 1
    dispositions = register['migration_dispositions']
    assert Counter(r['id'] for r in dispositions) == Counter(f'R{i:03}' for i in range(1, 375))
    assert all(r['evidence'] for r in dispositions)
    print(f'Chapter references passed: 32 chapters + Appendix A, {len(plan["topic_anchors"])} stable topics, '
          f'{checked} current references, 374 old-reference dispositions.')
    return checked


if __name__ == '__main__':
    try:
        check()
    except (AssertionError, KeyError, OSError, ValueError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
