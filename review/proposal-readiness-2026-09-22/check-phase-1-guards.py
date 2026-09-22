#!/usr/bin/env python3
"""Exercise all authoring-note guards through the actual hygiene script."""
from pathlib import Path
import runpy
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
metrics = runpy.run_path(str(root / 'ci/manuscript-metrics.py'))
with tempfile.TemporaryDirectory() as directory:
    fixture = Path(directory)
    (fixture / 'ci').mkdir()
    (fixture / 'manuscript/chapters').mkdir(parents=True)
    for name in ('check-source-hygiene.sh', 'manuscript-metrics.py'):
        shutil.copyfile(root / 'ci' / name, fixture / 'ci' / name)
    # Case folding and line wrapping must not let reader-facing notes escape.
    text = '\n\n'.join(name.upper().replace(' ', '\n', 1) for name in metrics['FORBIDDEN'])
    (fixture / 'manuscript/chapters/10-fixture.md').write_text(text + '\n')
    (fixture / 'manuscript/book-files.txt').write_text('manuscript/chapters/10-fixture.md\n')
    result = subprocess.run(['bash', str(fixture / 'ci/check-source-hygiene.sh')], capture_output=True, text=True)
    print(result.stdout + result.stderr, end='')
    assert result.returncode == 1, result.returncode
    for name in metrics['FORBIDDEN']:
        assert f'forbidden authoring phrase: {name}' in result.stderr, name
    print('PASS: actual hygiene entry point rejects all nine case-varied, line-wrapped guards')
