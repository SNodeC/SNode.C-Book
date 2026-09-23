#!/usr/bin/env python3
"""Diagnostic only: process-directed SIGINT, trace recipient, then probe a stalled listener."""
import json, os, signal, socket, subprocess, tempfile, time
from pathlib import Path
review = Path(__file__).resolve().parent
root = review.parents[2]
work = root/'build/shutdown-recheck-9746d186'
prefix = work/'install-gcc'
binary = work/'examples/companion/examples/EchoPair/echoserver'
env = os.environ | {'LD_LIBRARY_PATH': ':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))}
results = []
for trial in range(16):
    trace = review/f'trial-{trial}'
    with tempfile.TemporaryDirectory(dir=work) as home, (review/f'trial-{trial}.stdout').open('w') as output:
        env['XDG_CONFIG_HOME'] = home
        with socket.socket() as reserve:
            reserve.bind(('127.0.0.1', 0)); port = reserve.getsockname()[1]
        command = [str(binary), '--log-level=0', 'echoserver', 'local', '--host=127.0.0.1', f'--port={port}']
        tracer = subprocess.Popen(['strace', '-ff', '-ttt', '-o', str(trace), '-e', 'trace=epoll_pwait,rt_sigprocmask,rt_sigaction', '-e', 'signal=SIGINT', *command], env=env, stdout=output, stderr=subprocess.STDOUT)
        pid = None
        item = {'trial': trial, 'command': command}
        try:
            deadline = time.monotonic()+8
            while pid is None:
                children = Path(f'/proc/{tracer.pid}/task/{tracer.pid}/children').read_text().split()
                if children: pid = int(children[0])
                else:
                    assert time.monotonic()<deadline; time.sleep(.01)
            item['pid'] = pid
            while True:
                try: peer = socket.create_connection(('127.0.0.1', port), .2); break
                except ConnectionRefusedError:
                    assert tracer.poll() is None and time.monotonic()<deadline; time.sleep(.01)
            with peer:
                peer.sendall(b'shutdown-check'); assert peer.recv(14)==b'shutdown-check'
            item['echo_passed'] = True
            item['signal_time'] = time.time()
            os.kill(pid, signal.SIGINT)
            try:
                tracer.wait(timeout=5); item['exit'] = tracer.returncode
            except subprocess.TimeoutExpired:
                item['sigint_timeout_seconds'] = 5
                item['threads'] = []
                for task in sorted(Path(f'/proc/{pid}/task').iterdir()):
                    item['threads'].append({'tid':int(task.name), 'wchan':(task/'wchan').read_text(), 'status':(task/'status').read_text()})
                item['listener_probe_time'] = time.time()
                try:
                    with socket.create_connection(('127.0.0.1', port), 1): pass
                    item['listener_probe_connected'] = True
                except OSError as error: item['listener_probe_error'] = str(error)
                try:
                    tracer.wait(timeout=2); item['exit_after_listener_probe'] = tracer.returncode
                except subprocess.TimeoutExpired: item['listener_probe_did_not_release'] = True
        finally:
            if tracer.poll() is None:
                if pid:
                    try: os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError: pass
                tracer.wait(timeout=3)
            results.append(item)
            (review/'signal-trials.json').write_text(json.dumps(results, indent=2)+'\n')
            print(json.dumps({k:v for k,v in item.items() if k not in {'threads','command'}}), flush=True)
    if 'sigint_timeout_seconds' in item: break
