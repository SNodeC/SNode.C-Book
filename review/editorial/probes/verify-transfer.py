#!/usr/bin/env python3
"""Exercise Chapter 15's printed independent peer and carrier failure boundary.

Usage: verify-transfer.py /path/to/transfer
The directory contains ipv4-build and unix-build from the chapter recipe.
"""
from pathlib import Path
import os
import re
import signal
import socket
import subprocess
import sys
import time

root = Path(__file__).resolve().parents[3]
work = Path(sys.argv[1]).resolve()
chapter = next((root / 'manuscript/chapters').glob('15-*.md')).read_text()
peer_code = re.search(r'```python\n(.*?)\n```', chapter, re.S).group(1)
processes = []
logs = []


def wait_ready(family, address):
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        if any(p.poll() is not None for p in processes):
            raise RuntimeError('A listener exited before becoming ready')
        try:
            with socket.socket(family, socket.SOCK_STREAM) as peer:
                peer.settimeout(0.2)
                peer.connect(address)
                with peer.makefile('rb') as reply:
                    assert reply.readline() == b'READY\n'
                return
        except (ConnectionRefusedError, FileNotFoundError, TimeoutError):
            time.sleep(0.02)
    raise TimeoutError(f'Listener not ready: {address}')


try:
    # Preserve the printed port. Refuse to take over an unrelated listener.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.bind(('127.0.0.1', 18090))
    for name, args in [
        ('ipv4', ['--host=127.0.0.1', '--port=18090']),
        ('unix', [f'--sun-path={work / "line.sock"}']),
    ]:
        log = (work / f'{name}-runtime.log').open('w')
        logs.append(log)
        processes.append(subprocess.Popen([
            str(work / f'{name}-build/line-protocol-server'), '--log-level=6',
            'lineprotocolserver', 'local', *args,
        ], stdout=log, stderr=subprocess.STDOUT))
    wait_ready(socket.AF_INET, ('127.0.0.1', 18090))
    wait_ready(socket.AF_UNIX, str(work / 'line.sock'))
    env = dict(os.environ, SNODEC_TRANSFER=str(work))
    subprocess.run([sys.executable, '-c', peer_code], env=env, check=True, timeout=10)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
        peer.settimeout(2)
        try:
            peer.connect(str(work / 'nonexistent.sock'))
        except FileNotFoundError:
            print('Unix missing target: failed before protocol readiness')
        else:
            raise AssertionError('Missing Unix target unexpectedly connected')
    # Independent peers must not share the unfinished command buffer.
    for family, address in [
        (socket.AF_INET, ('127.0.0.1', 18090)),
        (socket.AF_UNIX, str(work / 'line.sock')),
    ]:
        with socket.socket(family, socket.SOCK_STREAM) as first, \
                socket.socket(family, socket.SOCK_STREAM) as second:
            for peer in (first, second):
                peer.settimeout(2)
                peer.connect(address)
            with first.makefile('rb') as a, second.makefile('rb') as b:
                assert a.readline() == b'READY\n'
                assert b.readline() == b'READY\n'
                first.sendall(b'PI')
                second.sendall(b'STATUS\n')
                assert b.readline() == b'OK\n'
                first.sendall(b'NG\n')
                assert a.readline() == b'PONG\n'
        print(f'{family.name}: per-peer partial input remains isolated')
finally:
    for process in processes:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
    for process in processes:
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            raise AssertionError('Listener required forced termination')
    for log in logs:
        log.close()
assert not (work / 'line.sock').exists(), 'Owned Unix socket path remained after shutdown'
print('Both listeners stopped; owned Unix socket pathname cleaned up')
