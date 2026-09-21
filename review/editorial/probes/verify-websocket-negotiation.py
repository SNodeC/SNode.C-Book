#!/usr/bin/env python3
"""Bounded Chapter 24 rehearsal after deploying both echo subprotocol modules.

Usage: verify-websocket-negotiation.py COMPANION_BUILD SCRATCH_CLIENT_BUILD
The scratch client differs only by requesting `editorial-unsupported` instead of
`subprotocol, echo`. No production sources are modified by this harness.
"""
from pathlib import Path
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time

examples = Path(sys.argv[1]).resolve() / 'companion/examples'
unsupported = Path(sys.argv[2]).resolve() / 'http-upgrade-client'
with tempfile.TemporaryDirectory(prefix='snodec-book-ws-') as temporary:
    work = Path(temporary)
    env = dict(os.environ, XDG_CONFIG_HOME=str(work / 'config'))
    with socket.socket() as reservation:
        reservation.bind(('127.0.0.1', 0))
        port = reservation.getsockname()[1]
    flags = ['--monochrom=true', '--log-level=6', 'legacy']
    address = ['--host=127.0.0.1', f'--port={port}']
    server_log = work / 'server.log'
    with server_log.open('w') as log:
        server = subprocess.Popen([
            str(examples / 'HttpUpgrade-Server/http-upgrade-server'),
            *flags, 'local', *address,
        ], stdout=log, stderr=log, env=env)
        try:
            until = time.monotonic() + 5
            while True:
                assert server.poll() is None, server_log.read_text()
                try:
                    with socket.create_connection(('127.0.0.1', port), timeout=0.2):
                        break
                except ConnectionRefusedError:
                    assert time.monotonic() < until, server_log.read_text()
                    time.sleep(0.02)
            for label, executable, expected in [
                ('echo', examples / 'HttpUpgrade-Client/http-upgrade-client', 'accepted'),
                ('unsupported', unsupported, 'rejected'),
            ]:
                output = work / f'{label}.log'
                with output.open('w') as stream:
                    client = subprocess.Popen([str(executable), *flags, 'remote', *address],
                                              stdout=stream, stderr=stream, env=env)
                    try:
                        until = time.monotonic() + 8
                        while client.poll() is None and time.monotonic() < until:
                            if label == 'unsupported' and 'upgrade response: rejected' in output.read_text():
                                break
                            time.sleep(0.02)
                    finally:
                        if client.poll() is None:
                            client.send_signal(signal.SIGINT)
                        try:
                            client.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            client.kill()
                            client.wait()
                            raise AssertionError('Client required forced termination')
                result = output.read_text()
                print(f'--- {label} client ---\n{result}', flush=True)
                assert f'upgrade response: {expected}' in result
                if label == 'echo':
                    assert 'WebSocket echo client received: hello' in result
                    assert 'WebSocket echo client disconnected' in result
                else:
                    assert 'WebSocket echo client connected' not in result
                    assert 'WebSocket echo client received:' not in result
            with socket.create_connection(('127.0.0.1', port), timeout=2) as peer:
                peer.sendall((f'GET /ws HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\n'
                              'Upgrade: websocket\r\nConnection: Upgrade\r\n'
                              'Sec-WebSocket-Version: 13\r\n'
                              'Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\n'
                              'Sec-WebSocket-Protocol: editorial-unsupported\r\n\r\n').encode())
                response = peer.recv(4096).split(b'\r\n\r\n', 1)[0]
                print('Unsupported independent request:', response.decode(), flush=True)
                assert not response.startswith(b'HTTP/1.1 101 ')
                assert b'sec-websocket-protocol: echo' not in response.lower()
        finally:
            server.send_signal(signal.SIGINT)
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
                server.wait()
                raise AssertionError('Server required forced termination')
    result = server_log.read_text()
    print(f'--- server ---\n{result}', flush=True)
    assert result.count('WebSocket echo server connected') == 1
    assert 'WebSocket echo server received: hello' in result
    print('PASS: echo negotiation, hello exchange and closure; unsupported selection has no echo attachment')
