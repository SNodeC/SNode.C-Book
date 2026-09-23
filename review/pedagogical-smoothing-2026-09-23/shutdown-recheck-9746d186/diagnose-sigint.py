#!/usr/bin/env python3
"""Separate controlled reproduction; never changes the lab harness or framework."""
from pathlib import Path
import json,os,signal,socket,subprocess,tempfile,time
root=Path(__file__).resolve().parents[3];review=Path(__file__).resolve().parent
work=root/'build/shutdown-recheck-9746d186';prefix=work/'install-gcc'
binary=work/'examples/companion/examples/EchoPair/echoserver'
env=os.environ|{'LD_LIBRARY_PATH':':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))}
trials=[]
for trial in range(8):
 with tempfile.TemporaryDirectory(dir=work) as home, (review/f'sigint-{trial}.log').open('w') as log:
  env['XDG_CONFIG_HOME']=home
  with socket.socket() as reserved:reserved.bind(('127.0.0.1',0));port=reserved.getsockname()[1]
  command=[str(binary),'--log-level=0','echoserver','local','--host=127.0.0.1',f'--port={port}']
  proc=subprocess.Popen(command,env=env,stdout=log,stderr=subprocess.STDOUT,stdin=subprocess.DEVNULL)
  try:
   deadline=time.monotonic()+8
   while True:
    try:peer=socket.create_connection(('127.0.0.1',port),.2);break
    except ConnectionRefusedError:
     assert proc.poll() is None and time.monotonic()<deadline
     time.sleep(.03)
   with peer:
    peer.sendall(b'shutdown-check');assert peer.recv(14)==b'shutdown-check'
   proc.send_signal(signal.SIGINT)
   try:
    proc.wait(timeout=5);trials.append({'trial':trial,'exit':proc.returncode,'command':command})
   except subprocess.TimeoutExpired:
    with (review/'sigint-backtrace.log').open('w') as out:
     result=subprocess.run(['gdb','-q','-batch','-ex','set pagination off','-ex',"p (int) 'core::EventLoop::eventLoopState'",'-ex',"p (int) 'core::EventLoop::stopsig'",'-ex','thread apply all bt 12','-p',str(proc.pid)],stdout=out,stderr=subprocess.STDOUT,timeout=15)
    trials.append({'trial':trial,'echo_passed':True,'sigint_timeout_seconds':5,'gdb_exit':result.returncode,'command':command});break
  finally:
   if proc.poll() is None:proc.kill();proc.wait()
(review/'sigint-diagnosis.json').write_text(json.dumps(trials,indent=2)+'\n')
