#!/usr/bin/env python3
"""Read-only capture of the author working tree specified by the smoothing pass."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

source = Path('/home/voc/projects/snodec/snode.c')
review = Path(__file__).resolve().parent
def git(*args):
    return subprocess.check_output(['git', '-C', str(source), *args])

files = sorted(git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0'))
state = {
    'source': str(source),
    'head': git('rev-parse', 'HEAD').decode().strip(),
    'status_porcelain_v1': git('status', '--porcelain=v1').decode(),
    'diff_head_binary_sha256': hashlib.sha256(git('diff', 'HEAD', '--binary')).hexdigest(),
    'untracked_nonignored_sha256': [
        {'path': name, 'sha256': hashlib.sha256((source/name).read_bytes()).hexdigest()}
        for name in files if name
    ],
}
tag = sys.argv[1]
path = review / f'framework-freeze-{tag}.json'
path.write_text(json.dumps(state, indent=2) + '\n')
(review/f'framework-untracked-{tag}.sha256').write_text(''.join(
    item['sha256']+'  '+item['path']+'\n' for item in state['untracked_nonignored_sha256']))
if tag != 'P0a':
    previous = json.loads((review/'framework-freeze-P0a.json').read_text())
    if state != previous:
        print('STOP §14: framework freeze changed; see '+str(path))
        sys.exit(1)
print('PASS: framework working-tree freeze '+tag+' recorded'+(' and unchanged' if tag!='P0a' else ''))
