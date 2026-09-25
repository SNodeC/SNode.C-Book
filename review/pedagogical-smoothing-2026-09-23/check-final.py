#!/usr/bin/env python3
"""Follow-ups 13–16 regression guards over the authoritative Markdown inputs.

These checks protect the specified corrections, not a prose style template.
Fenced code is preserved; fenced Divs are parsed independently of code fences.
The author's later decision withdrew compression, so repeated teaching passages
are not rejected. Human assessment of technical meaning remains in the report.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('polish', HERE/'check-polish.py')
polish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(polish)


def divs(text):
    """Yield attributes, opening line and contents, including nested Markdown."""
    lines = text.splitlines()
    stack = []
    for n, line, code in polish.rows(text):
        if code:
            continue
        opening = re.match(r'^ {0,3}(:{3,})\s*(\{.*\})\s*$', line)
        closing = re.match(r'^ {0,3}(:{3,})\s*$', line)
        if opening:
            stack.append((len(opening[1]), opening[2], n))
        elif closing and stack and len(closing[1]) >= stack[-1][0]:
            _, attrs, start = stack.pop()
            yield attrs, start, '\n'.join(lines[start:n-1])
    if stack:
        raise ValueError('unclosed fenced Div')


def right_aligned_declarations(block):
    """Recognize declaration-shaped type names; ignore literals and expressions.

    A lowercase variable beside * is not sufficient evidence of a declaration.
    Framework/public class names, qualified types and built-in types are useful
    unambiguous signals in these snippets. Rvalue references are excluded.
    """
    clean = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',
                   lambda m: ''.join('\n' if c == '\n' else ' ' for c in m[0]), block)
    types = r'(?:const\s+)?(?:(?:[A-Za-z_]\w*::)+[A-Za-z_]\w*|[A-Z][A-Za-z_]\w*|auto|char|void|int|double|float|bool|long|short|size_t|string)(?:<[^;{}()\n]*>)?'
    return list(re.finditer(r'\b'+types+r'[ \t]+[*&](?![&*])(?=\s*(?:[A-Za-z_]|[,);]))', clean))


def check(root):
    paths = (root/'manuscript/book-files.txt').read_text().splitlines()
    texts = {p: (root/p).read_text() for p in paths}
    errors = []
    def need(condition, message):
        if not condition:
            errors.append(message)
    def ch(n):
        return next(t for p, t in texts.items() if p.startswith(f'manuscript/chapters/{n:02}-'))
    appendix = next(t for p, t in texts.items() if '/appendix-a-' in p)
    need('introduction in Chapter 4' not in appendix, 'Appendix A: stale introduction destination')
    need(bool(re.search(r'source-reading introduction in Chapter 5', appendix)),
         'Appendix A: type/header/component introduction must name Chapter 5')
    need('echo local --port' not in ch(13), 'Ch13: wrong instance command')
    forbidden = ('stream modes', 'connection mode', 'legacy or TLS mode',
                 'Retry is policy, not morality', 'node.js', r'\textsubscript{\texttt{2.0.0}}',
                 'A instance', 'security mode', 'role is named')
    old_roles = ('runtime, role, connection', 'a table of roles', 'locate those roles',
                 'the echo role', 'which roles became active',
                 'The MQTT role still needs endpoint configuration',
                 'an optional role omitted from one deployment',
                 'a role that tried to participate and failed')
    for path, text in texts.items():
        for term in forbidden + old_roles:
            need(not re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', text), f'{path}: old terminology: {term}')
    # Every retained role is reviewable by exact occurrence and one-line reason.
    allow = (root/HERE.relative_to(ROOT)/'terminology-allowlist.md').read_text()
    inventory = allow.split('## Role inventory', 1)[1].split('## Carrier inventory', 1)[0]
    approved = {}
    for line in inventory.splitlines():
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells) == 3 and re.match(r'manuscript/.*:\d+:\d+$', cells[0]):
            need(cells[0] not in approved, 'duplicate role allowance: '+cells[0])
            approved[cells[0]] = cells[1:]
    actual = {}
    for path, text in texts.items():
        for n, line in enumerate(text.splitlines(), 1):
            for hit in re.finditer(r'\broles?\b', line, re.I):
                location = f'{path}:{n}:{hit.start()+1}'
                actual[location] = line.strip().replace('|', ' / ').strip()
    need(set(actual) == set(approved), 'role inventory is missing or has stale occurrences')
    for location in actual.keys() & approved.keys():
        context, reason = approved[location]
        need(context == actual[location] and bool(reason), 'role allowance mismatch: '+location)
    for n in (5, 25):
        boxes = [t for a, _, t in divs(ch(n)) if '.snodec-remember' in a]
        need(len(boxes) == 1 and len(re.findall(r'^\s*[-*+]\s+', boxes[0], re.M)) >= 3,
             f'Ch{n}: at least three recap bullets required')
    need(any('.snodec-note' in a and 'title="Build note"' in a for a, _, _ in divs(ch(20))),
         'Ch20: Build note box missing')
    for path, text in texts.items():
        if not re.match(r'manuscript/chapters/(\d\d-|appendix-a-)', path):
            continue
        boxes = [t for a, _, t in divs(text) if '.snodec-exercise' in a]
        need(len(boxes) == 1, path+': expected one exercise block')
        for block in boxes:
            content = re.split(r'\n\s*\n', block.strip())
            need(bool(content) and bool(re.fullmatch(r'Public (?:answers|solutions).*companion/exercises/[^\s`]+`\.', content[-1], re.S)),
                 path+': answer pointer must be the last exercise content line')
    need('Illustrative role map — not SNode.C configuration syntax' in ch(26),
         'Ch26: illustrative label missing')
    headings = list(re.finditer(r'^### (.*)$', appendix, re.M))
    runtime = next((i for i, h in enumerate(headings) if h[1].startswith('Following a public type into the runtime')), None)
    descriptor = next((i for i, h in enumerate(headings) if h[1].startswith('Observed descriptor populations')), None)
    direct = runtime is not None and descriptor == runtime + 1
    bridge = ''
    if descriptor is not None:
        preceding = appendix[:headings[descriptor].start()].rstrip().split('\n\n')[-1]
        bridge = preceding if not preceding.startswith(('#', '|', '```', '\\index')) else ''
    need(direct or bool(re.search(r'descriptor', bridge, re.I) and re.search(r'runtime|reading|observ', bridge, re.I)),
         'Appendix A: descriptor section needs adjacent runtime reading or a bridge')
    def exercise(text, n):
        block = next(t for a, _, t in divs(text) if '.snodec-exercise' in a)
        match = re.search(rf'^{n}\.\s+(.*?)(?=^\d+\.\s+|^Public (?:answers|solutions)|\Z)', block, re.M | re.S)
        return match[1].strip() if match else ''
    for final_n, old_ch, old_n in ((3, 6, 4), (4, 4, 3)):
        now, old = exercise(ch(32), final_n), exercise(ch(old_ch), old_n)
        need(bool(now and old) and now != old, f'Ch32 Ex{final_n}: repeated earlier question')
        need('acceptance authority' in now and ('observer' in now or 'restart' in now),
             f'Ch32 Ex{final_n}: final architectural interpretation missing')
    need('Part XI checkpoint' in exercise(ch(32), 4), 'Ch32: Part XI synthesis missing')
    for number, target, chapter in ((3, 'model-ownership', 6), (4, 'model-instances', 4)):
        question = exercise(ch(32), number)
        need(target in question and bool(re.search(rf'\bChapter\s+{chapter}\b', question)),
             f'Ch32 Ex{number}: {target} must name Chapter {chapter}')

    # Check navigational cues in their local teaching context. Do not require a
    # fixed sentence, line wrapping, punctuation, or a particular linking verb.
    def section(text, heading):
        match = re.search(r'^### '+re.escape(heading)+r'(?: \{[^}]*\})?\s*\n(.*?)(?=^### |\Z)',
                          text, re.M | re.S)
        return match[1] if match else ''
    def has(text, *patterns):
        return all(re.search(pattern, text, re.I | re.S) for pattern in patterns)
    playground = ch(3).split('cd ~/projects\ncmake -S snodec-playground', 1)[0][-700:]
    need(has(playground, r'Chapter\s+2', r'shortest path', r'fresh playground', r'already|repeat'),
         'Ch3: link repeated build to the earlier shortest path')
    startup = section(ch(4), 'Startup and independent lifetimes')
    opening = startup.split('```', 1)[0]
    need(has(opening, r'init\(\)', r'start\(\)', r'same|above|earlier'),
         'Ch4: identify repeated startup calls')
    need(has(startup, r'(above|earlier|already)[^.]*global protocol singleton'),
         'Ch4: link the repeated context-scope rule')
    comparison = section(ch(7), 'An IPv4/IPv6 comparison').split('```', 1)[0]
    need(has(comparison, r'earlier|above|already', r'alias', r'instance name', r'activation'),
         'Ch7: link the fuller comparison to the earlier aliases')
    unix = section(ch(7), 'Unix domain sockets') + section(ch(7), 'Listening and connecting by path')
    pointers = re.findall(r'Chapter\s+8[^.]*\.', unix)
    need(len(pointers) >= 2 and has(pointers[-1], r'pathname|earlier|above|lifetime'),
         'Ch7: give the later connection pointer its pathname purpose')
    echo = section(ch(12), 'Echo as the smallest transfer microscope').split('```', 1)[0]
    need(has(echo, r'Chapter\s+3', r'complete', r'listing', r'repeat|again', r'transfer'),
         'Ch12: link the repeated snippets to the complete listing')
    paragraphs = re.split(r'\n\s*\n', ch(18))
    framework_index = next((i for i, t in enumerate(paragraphs)
                            if 'InetExpressMiddlewareMountOrderTest.cpp' in t), None)
    framework = ('\n\n'.join(paragraphs[max(0, framework_index-1):framework_index+1])
                 if framework_index is not None else '')
    need(has(framework, r'trace', r'above|earlier', r'/outside', r'404', r'count.*visit|visit.*count'),
         'Ch18: connect framework observations to the earlier trace')
    distinction = next((t for t in re.split(r'\n\s*\n', ch(29)) if 'Throughput asks' in t), '')
    need(has(distinction, r'single run|experiment', r'general|beyond'),
         'Ch29: mark the move from one run to general distinctions')

    # The author replaced FU15's HEAD-only rule with immutable Book-1.0 tags.
    # The book's own release tag remains a separate release step.
    covered = [p for folder in ('manuscript', 'companion', 'ci', '.github')
               for p in (root/folder).rglob('*')
               if p.is_file() and '__pycache__' not in p.parts]
    covered += list((root/'source-baseline').glob('*.env'))
    covered += [root/'source-baseline/SOURCE-VERSION.md']
    for path in covered:
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            # Dependency checkouts use the edition tag; the book clone is separate.
            for match in re.finditer(r'\bgit\s+(?:-C\s+\S+\s+)?(checkout|switch|fetch|clone)\s+([^`\n;]+)', line):
                command, args = match.groups()
                args = args.split(' && ', 1)[0]
                target = None
                branch = re.search(r'--branch(?:=|\s+)([^\s]+)', args)
                if command == 'clone' and branch:
                    target = branch[1]
                elif command in ('checkout', 'switch'):
                    target = next((x for x in args.split() if not x.startswith('-')), None)
                elif command == 'fetch':
                    positions = [x for x in args.split() if not x.startswith('-')]
                    if len(positions) > 1:
                        target = positions[-1]
                if target:
                    target = target.strip('"\'.,')
                    book_clone = (command == 'clone' and target == 'main' and
                                  re.search(r'https://github\.com/SNodeC/SNode\.C-Book(?:\.git)?(?:\s|$)', args))
                    need(target in ('Book-1.0', 'refs/tags/Book-1.0') or book_clone,
                         f'{path.relative_to(root)}:{number}: non-edition repository target {target}')
            literal_ref = re.match(r'\s*ref:\s*([^\s]+)\s*$', line)
            need(not literal_ref or literal_ref[1] in ('Book-1.0', 'refs/tags/Book-1.0'),
                 f'{path.relative_to(root)}:{number}: non-edition repository workflow ref')
    baseline = (root/'source-baseline/book-source-baseline.env').read_text()
    need(re.search(r'^SNODEC_REF=Book-1\.0$', baseline, re.M) and
         not re.search(r'^SNODEC_COMMIT=', baseline, re.M), 'baseline must target Book-1.0')
    need('Clang 13.0 or newer' not in ch(2), 'compiler minimum is not a newer-version guarantee')
    installs = re.findall(r'```sh\n(.*?)\n```', ch(2), re.S)
    need(any('apt install' in block and 'libasio-dev' in block for block in installs),
         'Ch2: optional Asio comparison dependency missing')
    quit_lab = (root/'companion/exercises/ch10/protocol.py').read_text()
    need(r'QUIT\nPING\n' in quit_lab and "== b''" in quit_lab,
         'Ch10: coalesced QUIT/PING closure regression missing')
    for n in (25, 27):
        consumers = [block for block in re.findall(r'```cmake\n(.*?)\n```', ch(n), re.S)
                     if 'my-ipv4-legacy-webapp' in block or 'target_link_libraries(myapp' in block]
        need(bool(consumers) and all('snodec::http-server-express-legacy-in' in block for block in consumers),
             f'Ch{n}: installed Express consumer must use the composed component')
    for path, text in texts.items():
        need(not re.search(r'\bnow\s+(?:exposes|receives|distinguishes|includes?|carries)\b', text, re.I),
             path+': release-notes phrasing')
        need(not re.search(r'\\index\{(?:instance!|Unix-domain sockets(?:!|\}))', text),
             path+': split index heading')
        # Repeated entries in separate discussions are useful. Reject only a
        # repeated directive in one uninterrupted index run (blank lines allowed).
        seen = set()
        for line in text.splitlines():
            directives = re.findall(r'\\index\{(.+)\}', line)
            if directives:
                for key in directives:
                    need(key not in seen, path+': duplicate adjacent index entry '+key)
                    seen.add(key)
            elif line.strip():
                seen.clear()
    for path, text in texts.items():
        for block in re.finditer(r'^ {0,3}```(?:cpp|c\+\+|\{\.cpp(?:\s+[^}\n]*)?\})\n(.*?)\n {0,3}```', text, re.M | re.S):
            for hit in right_aligned_declarations(block[1]):
                line = text.count('\n', 0, block.start(1) + hit.start()) + 1
                need(False, f'{path}:{line}: right-aligned pointer/reference declaration')

    width_spec = importlib.util.spec_from_file_location('width', root/'ci/check-listing-width.py')
    width = importlib.util.module_from_spec(width_spec)
    width_spec.loader.exec_module(width)
    errors.extend(width.violations(root))
    publication = (root/'.github/workflows/book-package.yml').read_text()
    need('name: Verify Pandoc and crossref ABI compatibility' in publication
         and 'run: cmake -S . -B build/ci-book -G Ninja' in publication,
         'publication workflow must configure the shared guarded CMake tool setup')
    local_tools = (root/'production/cmake/SNodeCBookTools.cmake').read_text()
    need('check-publication-tools.py' in local_tools,
         'local CMake path must share the publication version guard')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if args.output:
        args.output.write_text(json.dumps({'status': 'FAIL' if errors else 'PASS', 'errors': errors}, indent=2)+'\n')
    for error in errors:
        print('ERROR: '+error)
    print(f"{'FAIL' if errors else 'PASS'}: final polish regression guards")
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
