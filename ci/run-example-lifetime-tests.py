#!/usr/bin/env python3
"""Focused SSE lifetime and WebSocket echo checks; no external services.

Build test-only copies of the three SSE examples with a weak response observer
and /test/retained endpoint. The production subscription path stays unchanged.
The observer never owns a response. This makes idle retention observable without
adding a diagnostic API or counter to the teaching programs. --baseline-ref tests
an earlier book revision as a negative control, expecting that idle retention.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'companion/exercises/ch20'))
from wire import echo_exchange
spec = importlib.util.spec_from_file_location('book_smoke', ROOT / 'ci/run-behavior-smoke-tests.py')
smoke = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = smoke
spec.loader.exec_module(smoke)


def port_number():
    with socket.socket() as peer:
        peer.bind(('127.0.0.1', 0))
        return peer.getsockname()[1]


def instrument_sse(work, prefix, baseline):
    source = work / 'fixture-source'
    source.mkdir(parents=True, exist_ok=True)
    examples = ['SSE-Server', 'MiniGateway', 'MiniGateway-Extended']
    for name in examples:
        destination = source / name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(ROOT / 'companion/examples' / name, destination)
        if baseline:
            for path in destination.iterdir():
                if path.is_file():
                    relative = f'companion/examples/{name}/{path.name}'
                    path.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{baseline}:{relative}']))
        target = destination / ('main.cpp' if name == 'SSE-Server' else 'MiniGatewayWeb.cpp')
        content = target.read_text()
        anchor = '#include <web/http/http_utils.h>'
        assert content.count(anchor) == 1
        content = content.replace(anchor, anchor + '''
#include <algorithm>
#include <vector>
namespace { std::vector<std::weak_ptr<express::Response>> observedResponses; }
''')
        anchor = 'if (acceptsEventStream(req)) {'
        assert content.count(anchor) == 1
        content = content.replace(anchor, anchor + '\n                    observedResponses.emplace_back(res);')
        anchor = 'app.get("/events",'
        assert content.count(anchor) == 1
        content = content.replace(anchor, '''app.get("/test/retained", [](const auto&, const auto& response) {
                response->json({{"responses", std::count_if(observedResponses.begin(), observedResponses.end(),
                    [](const auto& observer) { return !observer.expired(); })}});
            });
            ''' + anchor)
        target.write_text(content)
    (source / 'CMakeLists.txt').write_text('cmake_minimum_required(VERSION 3.14)\nproject(BookLifetimeFixtures LANGUAGES CXX)\n' +
                                        ''.join(f'add_subdirectory({name})\n' for name in examples))
    build = work / 'fixture-build'
    for command in [['cmake', '-S', str(source), '-B', str(build), f'-DCMAKE_PREFIX_PATH={prefix}'],
                    ['cmake', '--build', str(build), '--parallel', '4']]:
        subprocess.run(command, check=True, timeout=180)
    return build


def open_events(port):
    peer = socket.create_connection(('127.0.0.1', port), timeout=3)
    reader = peer.makefile('rb')
    peer.sendall((f'GET /events HTTP/1.1\r\nHost: localhost:{port}\r\n'
                  'Accept: text/event-stream\r\n\r\n').encode())
    assert b' 200 ' in reader.readline()
    while True:
        line = reader.readline()
        assert line, 'SSE connection ended inside the response header'
        if line in (b'\r\n', b'\n'):
            break
    event = read_event(reader)
    return peer, reader, event


def read_event(reader):
    fields = {}
    while True:
        line = reader.readline()
        assert line, 'SSE connection ended before an event boundary'
        line = line.strip()
        if not line:
            if fields:
                return json.loads(fields[b'data'])
        elif b':' in line:
            key, value = line.split(b':', 1)
            fields[key] = value.strip()


def close_event(peer, reader, reset=False):
    reader.close()
    if reset:
        peer.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
    peer.close()


def response_count(port):
    return smoke.json_get(port, '/test/retained')['responses']


def expect_count(port, expected):
    deadline = time.monotonic() + 4
    while True:
        actual = response_count(port)
        if actual == expected:
            return
        assert time.monotonic() < deadline, f'Retained response owners: {actual}; expected {expected}'
        time.sleep(0.02)


def test_sse(build, name, baseline):
    port = port_number()
    role = 'legacy' if name == 'SSE-Server' else 'web'
    executable = {'SSE-Server': 'sse-server', 'MiniGateway': 'minigateway',
                  'MiniGateway-Extended': 'minigateway-extended'}[name]
    args = ['--log-level=3', role, 'local', '--host=127.0.0.1', f'--port={port}']
    if name != 'SSE-Server':
        args += ['mqtt-uplink', '--disabled']
    if name == 'MiniGateway-Extended':
        args += ['measurement-input', '--disabled']
    process = smoke.start_process(build / name / executable, name, args)
    opened = []
    try:
        smoke.wait_for_tcp('127.0.0.1', port, process)
        # Seed the initially empty capstone model before any idle-disconnect check.
        status, _, payload = smoke.raw_http(port, '/simulate', method='POST')
        smoke.assert_status(status, 200, '/simulate')
        sequence = json.loads(payload)['sequence']
        survivor = open_events(port)
        opened.append(survivor)
        assert survivor[2]['sequence'] == sequence
        expect_count(port, 1)
        for wave in range(3):
            churn = [open_events(port) for _ in range(8)]
            opened.extend(churn)
            expect_count(port, 9)
            for index, (peer, reader, _) in enumerate(churn):
                close_event(peer, reader, reset=index % 2 == 1)
            del opened[1:]
            if baseline:
                time.sleep(0.3)
                assert response_count(port) == 9, 'Negative control did not exhibit the expected retention'
                print(f'EXPECTED FAILURE confirmed: {name} retains eight idle disconnected responses', flush=True)
                return
            expect_count(port, 1)
            print(f'PASS: {name} idle FIN/RST churn wave {wave + 1}, only the live observer retained', flush=True)
        status, _, payload = smoke.raw_http(port, '/simulate', method='POST')
        smoke.assert_status(status, 200, '/simulate')
        assert read_event(survivor[1]) == json.loads(payload)
        close_event(*survivor[:2])
        opened.clear()
        expect_count(port, 0)
        print(f'PASS: {name} surviving observer receives the next measurement; final idle cleanup releases all responses', flush=True)
    finally:
        for peer, reader, _ in opened:
            close_event(peer, reader)
        process.stop()


def test_websocket(build):
    port = port_number()
    binary = build / 'companion/examples/HttpUpgrade-Server/http-upgrade-server'
    process = smoke.start_process(binary, 'websocket-echo', ['--log-level=3', 'legacy', 'local',
                                                          '--host=127.0.0.1', f'--port={port}'])
    try:
        smoke.wait_for_tcp('127.0.0.1', port, process)
        client = build / 'companion/examples/HttpUpgrade-Client/http-upgrade-client'
        result = subprocess.run([str(client), '--log-level=6', 'legacy', 'remote',
                                 '--host=127.0.0.1', f'--port={port}'],
                                capture_output=True, text=True, timeout=10, env=smoke.smoke_env())
        assert result.returncode == 0, result.stdout + result.stderr
        assert 'WebSocket echo client received: hello' in result.stdout + result.stderr
        print('PASS: unchanged teaching client receives hello and closes', flush=True)
        with socket.create_connection(('127.0.0.1', port), timeout=3) as peer:
            echo_exchange(peer)
        print('PASS: WebSocket text/binary type, exact bytes, NUL/non-UTF8 binary, empty/sequential/fragmented messages, interleaved ping and close', flush=True)
    finally:
        process.stop()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', type=Path, required=True)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--baseline-ref')
    args = parser.parse_args()
    args.prefix = args.prefix.resolve()
    args.build = args.build.resolve()
    args.work = args.work.resolve()
    smoke.SNODEC_PREFIX = args.prefix
    smoke.LOG_DIR = args.work / 'runtime-logs'
    args.work.mkdir(parents=True, exist_ok=True)
    if not args.baseline_ref:
        for component in ['WebSocketEchoServerSubprotocol', 'WebSocketEchoClientSubprotocol']:
            subprocess.run(['cmake', '--install', str(args.build), '--prefix', str(args.prefix),
                            '--component', component], check=True, timeout=30)
    fixtures = instrument_sse(args.work, args.prefix, args.baseline_ref)
    failures = []
    with tempfile.TemporaryDirectory(prefix='snodec-example-lifetime-config-') as config:
        os.environ['XDG_CONFIG_HOME'] = config
        for name in ['SSE-Server', 'MiniGateway', 'MiniGateway-Extended']:
            try:
                test_sse(fixtures, name, args.baseline_ref)
            except Exception as error:
                failures.append(f'{name}: {error}')
                print(f'FAIL: {failures[-1]}', flush=True)
        if not args.baseline_ref:
            try:
                test_websocket(args.build)
            except Exception as error:
                failures.append(f'WebSocket: {error}')
                print(f'FAIL: {failures[-1]}', flush=True)
    assert not failures, failures
    print('All selected example lifetime/echo checks passed.', flush=True)


if __name__ == '__main__':
    main()
