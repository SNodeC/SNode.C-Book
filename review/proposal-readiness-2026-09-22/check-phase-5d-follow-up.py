#!/usr/bin/env python3
"""Run Phase 5d checks with fresh evidence and the authorized include relocation."""
from pathlib import Path
review = Path(__file__).resolve().parent
import subprocess
root = review.parents[1]
chapter = 'manuscript/chapters/06-network-families-addresses-ipv4-ipv6-and-unix-sockets.md'
base_ref = subprocess.check_output(['git', 'rev-parse', ':/proposal-readiness: phase 5d — refine Part III and verify endpoint-family labs'], text=True).strip()
base = subprocess.check_output(['git', 'show', base_ref + ':' + chapter], text=True)
a = base.index(r'\index{datagram sockets}'); b = base.index('::: {.snodec-remember', a)
block = base[a:b].replace('That keeps the connection and protocol model established in the preceding chapters available while endpoint identity changes.', 'It builds on the context/factory separation and event-loop execution established in Chapters 3–5 while endpoint identity changes. Chapter 7 develops connection lifetimes in detail.')
expected = (base[:a] + base[b:]).replace('### Unix domain sockets {#unix-domain-sockets}\n\n', '### Unix domain sockets {#unix-domain-sockets}\n\n' + block)
assert (root / chapter).read_text() == expected
checks = (review / 'check-phase-5d.py').read_text()
for name in ['metrics-after-phase-5d.json', 'phase-5d-final-results.json', 'phase-5d-final-labs.log', 'phase-5d-exit-checks.json']:
    checks = checks.replace(name, name.replace('phase-5d', 'phase-5d-follow-up').replace('-final', ''))
# The author explicitly moved the Unix header excerpt before the address examples.
# Preserve every excerpt byte-for-byte, allowing order changes only in Chapter 6.
old = "assert re.findall(r'```cpp\\n.*?\\n```', old(path), re.S) == re.findall(r'```cpp\\n.*?\\n```', (ROOT/path).read_text(), re.S)"
new = "assert (Counter if n == 6 else list)(re.findall(r'```cpp\\n.*?\\n```', old(path), re.S)) == (Counter if n == 6 else list)(re.findall(r'```cpp\\n.*?\\n```', (ROOT/path).read_text(), re.S))"
assert old in checks
checks = checks.replace(old, new)
exec(compile(checks, str(review / 'check-phase-5d.py'), 'exec'), {'__file__': str(review / 'check-phase-5d.py')})
