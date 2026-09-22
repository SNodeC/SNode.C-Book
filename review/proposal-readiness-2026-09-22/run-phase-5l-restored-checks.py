from pathlib import Path
import concurrent.futures, json, os, subprocess, sys, tarfile
root=Path.cwd(); tag=sys.argv[1]; build=root/'build'/sys.argv[2]; review=root/'review/proposal-readiness-2026-09-22'; prefix=root/'build/ci-fix-2026-09-22/install-gcc'; temp=Path('/tmp')
assert temp.is_dir()
env=os.environ|{'SNODEC_PREFIX':str(prefix),'BOOK_EXAMPLES_BUILD_DIR':str(build),'CMAKE_BUILD_PARALLEL_LEVEL':'4','TMPDIR':str(temp),'TMP':str(temp),'TEMP':str(temp),'SNODEC_BOOK_SMOKE_UNIX_SOCKET':str(temp/f'{tag}-smoke.sock'),'PYTHONDONTWRITEBYTECODE':'1'}
env['LD_LIBRARY_PATH']=':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))
def run(name,cmd,cwd=root):
 with (review/f'{tag}-{name}.log').open('w') as log:
  log.write('COMMAND: '+' '.join(cmd)+'\n'+'\n'.join(k+'='+env[k] for k in ['TMPDIR','TMP','TEMP','SNODEC_BOOK_SMOKE_UNIX_SOCKET','LD_LIBRARY_PATH'])+'\n');log.flush();result=subprocess.run(cmd,env=env,cwd=cwd,stdout=log,stderr=subprocess.STDOUT).returncode
 print(name,result,flush=True);return result
jobs={'hygiene':['bash','ci/check-source-hygiene.sh'],'alignment':['python3','ci/check-source-alignment.py'],'metrics-tests':['python3','ci/test-manuscript-metrics.py'],'companion':['bash','ci/build-companion-examples.sh'],'package':['cmake','--build','build/proposal-readiness-phase-2','--target','proposal','proposal-sample-pdf','proposal-package']}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
 futures={k:pool.submit(run,k,v) for k,v in jobs.items()};results={k:v.result() for k,v in futures.items()}
if results['companion']==0:
 for k,v in {'labs':['ctest','--test-dir',str(build),'--output-on-failure','--no-tests=error','-V'],'teaching':['python3','ci/run-teaching-smoke-tests.py'],'behavior':['bash','ci/run-behavior-smoke-tests.sh'],'lifetime':['python3','ci/run-example-lifetime-tests.py','--prefix',str(prefix),'--build',str(build),'--work',str(root/'build'/f'{tag}-lifetime')]}.items():results[k]=run(k,v)
if results['package']==0:
 dest=root/'build'/f'{tag}-extracted';dest.mkdir(exist_ok=True)
 with tarfile.open(root/'dist/packages/snodec-book-proposal-package.tar.gz') as t:t.extractall(dest,filter='data')
 results['extracted-hygiene']=run('extracted-hygiene',['bash','ci/check-source-hygiene.sh'],dest)
(review/f'{tag}-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(results)
