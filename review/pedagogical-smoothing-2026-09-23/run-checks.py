#!/usr/bin/env python3
"""Run existing checks with the recorded Phase 5m environment and fresh evidence."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

root = Path(__file__).resolve().parents[2]
review = Path(__file__).resolve().parent
tag = sys.argv[1]
if tag == 'P0b':
    raise SystemExit('Original P0b evidence is historical; use P0b-resume.')
suffix = '-resume' if tag == 'P0b-resume' else ''
label = 'P0b' if suffix else tag
build = root/'build/rebaseline-R2-07ca9a29-followup11/examples'
prefix = root/'build/rebaseline-R2-07ca9a29-followup11/install-gcc'
env = os.environ | {
    'SNODEC_PREFIX':str(prefix), 'BOOK_EXAMPLES_BUILD_DIR':str(build),
    'BOOK_BUILD_DIR':'build/rebaseline-R2-07ca9a29-followup11/book',
    'CMAKE_BUILD_PARALLEL_LEVEL':'4', 'TMPDIR':'/tmp','TMP':'/tmp','TEMP':'/tmp',
    'SNODEC_BOOK_SMOKE_UNIX_SOCKET':f'/tmp/smoothing-{tag}.sock',
    'PYTHONDONTWRITEBYTECODE':'1',
    'LD_LIBRARY_PATH':':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')})),
}
def run(name, command, cwd=root):
    with (review/f'{label}-{name}{suffix}.log').open('w') as log:
        log.write('COMMAND: '+' '.join(command)+'\n')
        for key in ['SNODEC_PREFIX','BOOK_EXAMPLES_BUILD_DIR','BOOK_BUILD_DIR','TMPDIR','LD_LIBRARY_PATH']:
            log.write(key+'='+env[key]+'\n')
        log.flush()
        status = subprocess.run(command,cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
    print(name,status,flush=True)
    return status

jobs={
    'metrics':['python3','ci/manuscript-metrics.py'],
    'references':['python3','ci/check-chapter-references.py'],
    'source-alignment':['python3','ci/check-source-alignment.py','--framework','/home/voc/projects/snodec/snode.c'],
    'hygiene':['bash','ci/check-source-hygiene.sh'],
    'companion':['bash','ci/build-companion-examples.sh'],
    'package':['bash','ci/build-book-package.sh'],
}
for path in sorted((root/'ci').glob('test-*.py')):
    jobs[path.stem]=['python3',str(path.relative_to(root))]
with ThreadPoolExecutor(max_workers=5) as pool:
    futures={name:pool.submit(run,name,cmd) for name,cmd in jobs.items()}
    results={name:f.result() for name,f in futures.items()}
# Complete independent entry observations; a failed prerequisite never advances a phase.
if results['companion']==0:
    for name,cmd in {
        'labs':['ctest','--test-dir',str(build),'--output-on-failure','--no-tests=error','-V'],
        'teaching':['python3','ci/run-teaching-smoke-tests.py'],
        'behavior':['bash','ci/run-behavior-smoke-tests.sh'],
        'lifetime':['python3','ci/run-example-lifetime-tests.py','--prefix',str(prefix),'--build',str(build),'--work',str(root/'build'/f'smoothing-{tag}-lifetime')],
    }.items(): results[name]=run(name,cmd)
if results['package']==0:
    dest=root/'build'/f'smoothing-{tag}-extracted';dest.mkdir(exist_ok=True)
    with tarfile.open(root/'dist/packages/snodec-book-proposal-package.tar.gz') as archive:
        archive.extractall(dest,filter='data')
    results['extracted-hygiene']=run('extracted-hygiene',['bash','ci/check-source-hygiene.sh'],dest)
(review/f'{tag}-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
sys.exit(int(any(results.values())))
