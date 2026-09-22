#!/usr/bin/env python3
"""Retain the Phase 5c assertions with fresh follow-up evidence destinations."""
from pathlib import Path
import json
review = Path(__file__).resolve().parent
checks = (review / 'check-phase-5c.py').read_text()
for before, after in [('metrics-after-phase-5c.json', 'metrics-after-phase-5c-follow-up.json'),
                      ('phase-5c-runtime-results.json', 'phase-5c-follow-up-runtime-results.json'),
                      ('phase-5c-final-labs.log', 'phase-5c-follow-up-labs.log'),
                      ('phase-5c-exit-checks.json', 'phase-5c-follow-up-exit-checks.json')]:
    checks = checks.replace(before, after)
assert all(value == 0 for value in json.loads((review / 'phase-5c-follow-up-results.json').read_text()).values())
exec(compile(checks, str(review / 'check-phase-5c.py'), 'exec'), {'__file__': str(review / 'check-phase-5c.py')})
