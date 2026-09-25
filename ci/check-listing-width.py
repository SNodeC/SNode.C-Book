#!/usr/bin/env python3
"""Reject printed fenced-code lines wider than the measured 90-column frame."""
import argparse
from pathlib import Path
import re

LIMIT = 90
ROOT = Path(__file__).resolve().parents[1]


def violations(root):
    errors = []
    for name in (root / 'manuscript/book-files.txt').read_text().splitlines():
        opened = None
        for number, line in enumerate((root / name).read_text().splitlines(), 1):
            if opened:
                marker, raw = opened
                if re.fullmatch(r' {0,3}' + re.escape(marker[0]) + '{' + str(len(marker)) + r',}\s*', line):
                    opened = None
                elif not raw and len(line.expandtabs(4)) > LIMIT:
                    errors.append(f'{name}:{number}: {len(line.expandtabs(4))} columns exceeds {LIMIT}')
            else:
                match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
                if match:
                    opened = (match[1], match[2].strip().startswith('{='))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = violations(args.root)
    print('\n'.join(errors) if errors else f'PASS: printed code fits {LIMIT} columns')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
