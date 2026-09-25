#!/usr/bin/env python3
"""Reject a Pandoc/pandoc-crossref ABI mismatch, locally and in CI."""
import argparse
import re
import subprocess


def versions(pandoc, crossref):
    active = re.search(r'(?im)^pandoc\s+(\d+(?:\.\d+)+)\b', pandoc)
    built = re.search(r'(?i)built with Pandoc\s+v?(\d+(?:\.\d+)+)\b', crossref)
    if not active or not built:
        raise ValueError('Cannot identify active Pandoc and crossref Pandoc build/ABI versions')
    if active[1] != built[1]:
        raise ValueError(f'Pandoc/crossref mismatch: active Pandoc {active[1]}, crossref built with Pandoc {built[1]}')
    return active[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pandoc', default='pandoc')
    parser.add_argument('--crossref', default='pandoc-crossref')
    args = parser.parse_args()
    outputs = [subprocess.check_output([binary, '--version'], stderr=subprocess.STDOUT, text=True)
               for binary in (args.pandoc, args.crossref)]
    version = versions(*outputs)
    print(f'Publication tool compatibility passed: Pandoc {version}; crossref built with Pandoc {version}')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
