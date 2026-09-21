#!/usr/bin/env python3
"""Bounded Chapter 33 service and Chapter 34 measurement rehearsal.

Usage: verify-service.py SCRATCH_DIRECTORY
Requires its service-install/bin/echoserver and an available systemd user manager.
Uses a uniquely named transient unit, temporary paths, and an isolated SNode.C
configuration base. It does not install or enable the printed persistent unit.
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
chapter = next((root / 'manuscript/chapters').glob('33-*.md')).read_text()
benchmark = next((root / 'manuscript/chapters').glob('34-*.md')).read_text()
config_text = re.search(r'```ini\n(daemonize=false.*?)\n```', chapter, re.S).group(1)
unit_text = re.search(r'```ini\n(\[Unit\].*?)\n```', chapter, re.S).group(1)
peer_code = re.search(r"python3 - <<'PY'\n(.*?)\nPY", chapter, re.S).group(1)
benchmark_code = re.search(r'```python\n(.*?)\n```', benchmark, re.S).group(1)
binary = work / 'service-install/bin/echoserver'
config = work / 'service-echo.conf'
config.write_text(config_text + '\n')
unit = f'snodec-book-editorial-echo-{os.getpid()}.service'
unit_file = work / unit
unit_file.write_text(unit_text.replace('%h/.local/snodec-book/bin/echoserver', str(binary))
                     .replace('%h/.config/snodec-book/echo.conf', str(config))
                     .replace('WorkingDirectory=%h', f'WorkingDirectory={work}') + '\n')
env = dict(os.environ, XDG_CONFIG_HOME=str(work / 'service-user-base'))


def command(*args, check=True):
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20)
    if result.stdout:
        print(result.stdout, end='', flush=True)
    if check:
        result.check_returncode()
    return result


def exchange_ready():
    until = time.monotonic() + 8
    while time.monotonic() < until:
        try:
            subprocess.run([sys.executable, '-c', peer_code], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
            return
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            time.sleep(0.05)
    raise AssertionError('Installed echo did not become ready')


def no_listener():
    try:
        with socket.create_connection(('127.0.0.1', 18093), timeout=1):
            raise AssertionError('Listener unexpectedly available')
    except ConnectionRefusedError:
        pass


with socket.socket() as reservation:
    reservation.bind(('127.0.0.1', 18093))
command('systemd-analyze', '--user', 'verify', str(unit_file))
print('Printed unit syntax verified with temporary executable/configuration paths', flush=True)
with (work / 'service-foreground.log').open('w') as log:
    process = subprocess.Popen([str(binary), '--config-file', str(config)], env=env, stdout=log, stderr=log)
    try:
        exchange_ready()
        print('Installed foreground exchange passed', flush=True)
        command(sys.executable, '-c', benchmark_code)
    finally:
        process.send_signal(signal.SIGINT)
        process.wait(timeout=10)
no_listener()
started = False
try:
    command('systemd-run', '--user', '--unit', unit, '--property=Type=exec',
            '--property=Restart=on-failure', '--property=RestartSec=2s',
            '--property=TimeoutStopSec=10s', '--property=StandardOutput=journal',
            '--property=StandardError=journal', '--property=UnsetEnvironment=XDG_CONFIG_HOME',
            f'--property=WorkingDirectory={work}', '/usr/bin/env',
            f'XDG_CONFIG_HOME={env["XDG_CONFIG_HOME"]}', str(binary), '--config-file', str(config))
    started = True
    exchange_ready()
    first_pid = command('systemctl', '--user', 'show', unit, '--property=MainPID', '--value').stdout.strip()
    command('systemctl', '--user', 'restart', unit)
    exchange_ready()
    next_pid = command('systemctl', '--user', 'show', unit, '--property=MainPID', '--value').stdout.strip()
    assert first_pid != next_pid and next_pid != '0'
    print('Supervised start/restart exchange passed; process identity changed', flush=True)
    config.write_text(config_text.replace('port=18093', 'port=invalid') + '\n')
    command('systemctl', '--user', 'restart', unit, check=False)
    time.sleep(0.3)
    no_listener()
    print('Invalid port rejected without a listener', flush=True)
    config.write_text(config_text + '\n')
    command('systemctl', '--user', 'restart', unit)
    exchange_ready()
    print('Restored configuration recovers the service', flush=True)
    command('journalctl', '--user', '-u', unit, '--no-pager', '-n', '18')
finally:
    config.write_text(config_text + '\n')
    if started:
        command('systemctl', '--user', 'stop', unit, check=False)
        command('systemctl', '--user', 'reset-failed', unit, check=False)
no_listener()
print('Service stopped; listener absent; no boot enablement or persistent unit installed', flush=True)
