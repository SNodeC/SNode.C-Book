#!/usr/bin/env python3
"""Bounded diagnostics with unchanged five-second grace and no wake-up traffic."""
from pathlib import Path
import json, os, signal, socket, subprocess, tempfile, time, statistics
review=Path(__file__).resolve().parent
root=review.parents[2]
work=root/'build/shutdown-recheck-07ca9a29'
prefix=work/'install-gcc'
binary=work/'examples/companion/examples/EchoPair/echoserver'
env=os.environ|{'LD_LIBRARY_PATH':':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))}
trials=[]
for index in range(100):
    mode='disabled' if index%2==0 else 'default'
    with tempfile.TemporaryDirectory(dir=work) as home, tempfile.TemporaryFile() as output:
        env['XDG_CONFIG_HOME']=home
        with socket.socket() as reserve:
            reserve.bind(('127.0.0.1',0));port=reserve.getsockname()[1]
        command=[str(binary), *(['--log-level=0'] if mode=='disabled' else []), 'echoserver','local','--host=127.0.0.1',f'--port={port}']
        proc=subprocess.Popen(command,env=env,stdin=subprocess.DEVNULL,stdout=output,stderr=subprocess.STDOUT)
        trial={'index':index,'mode':mode,'pid':proc.pid,'command':command,'idle_delay_seconds':[0,.002,.01][index%3]}
        try:
            deadline=time.monotonic()+8
            while True:
                try: peer=socket.create_connection(('127.0.0.1',port),.2);break
                except ConnectionRefusedError:
                    assert proc.poll() is None and time.monotonic()<deadline
                    time.sleep(.01)
            with peer:
                payload=b'shutdown-check\x00\xff'
                peer.sendall(payload);received=b''
                while len(received)<len(payload):
                    chunk=peer.recv(len(payload)-len(received));assert chunk;received+=chunk
                assert received==payload
                workers=[]
                for task in Path(f'/proc/{proc.pid}/task').iterdir():
                    if int(task.name)!=proc.pid:
                        mask=next(line.split()[1] for line in (task/'status').read_text().splitlines() if line.startswith('SigBlk:'))
                        workers.append({'tid':int(task.name),'blocked_mask':mask,'sigint_blocked':bool(int(mask,16)&(1<<(signal.SIGINT-1)))})
                trial['workers']=workers
                assert workers and all(w['sigint_blocked'] for w in workers)
            time.sleep(trial['idle_delay_seconds'])
            started=time.monotonic();proc.send_signal(signal.SIGINT)
            proc.wait(timeout=5)
            trial['shutdown_seconds']=time.monotonic()-started
            trial['returncode']=proc.returncode
            assert proc.returncode==254
            trial['passed']=True
        except Exception as error:
            trial['passed']=False;trial['error']=repr(error)
            if proc.poll() is None:
                with (review/f'stress-{index}-backtrace.log').open('w') as out:
                    subprocess.run(['gdb','-q','-batch','-ex','set pagination off','-ex',"p (int) 'core::EventLoop::eventLoopState'",'-ex',"p (int) 'core::EventLoop::stopsig'",'-ex','thread apply all bt 12','-p',str(proc.pid)],stdout=out,stderr=subprocess.STDOUT,timeout=15)
        finally:
            if proc.poll() is None:proc.kill();proc.wait()
            output.seek(0);contents=output.read()
            if not trial['passed'] or index in [0,1]:
                (review/f'stress-{index}.log').write_bytes(contents)
            trials.append(trial)
            (review/'sigint-stress.json').write_text(json.dumps(trials,indent=2)+'\n')
        if not trial['passed']:break
summary={'trials':len(trials),'passed':sum(t['passed'] for t in trials),'failed':sum(not t['passed'] for t in trials),'grace_seconds':5,'logging_modes':['disabled','default'],'maximum_shutdown_seconds':max([t.get('shutdown_seconds',0) for t in trials]),'median_shutdown_seconds':statistics.median([t.get('shutdown_seconds',0) for t in trials])}
(review/'sigint-stress-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
