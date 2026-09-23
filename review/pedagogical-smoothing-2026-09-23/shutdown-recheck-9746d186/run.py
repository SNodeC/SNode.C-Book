#!/usr/bin/env python3
"""Verify the author-accepted new source with restored labs; no editorial changes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,subprocess,tarfile

root=Path(__file__).resolve().parents[3]
review=Path(__file__).resolve().parent
source=Path('/home/voc/projects/snodec/snode.c')
work=root/'build/shutdown-recheck-9746d186'
prefix=work/'install-gcc'
expected='9746d1862b30a5104d3590aaa4ed79752ba9aa6a'
def git(*args):return subprocess.check_output(['git','-C',str(source),*args])
def freeze():
 return {'source':str(source),'head':git('rev-parse','HEAD').decode().strip(),
  'status_porcelain_v1':git('status','--porcelain=v1').decode(),
  'diff_head_binary_sha256':hashlib.sha256(git('diff','HEAD','--binary')).hexdigest(),
  'untracked_nonignored_sha256':[{'path':s,'sha256':hashlib.sha256((source/s).read_bytes()).hexdigest()} for s in sorted(git('ls-files','--others','--exclude-standard','-z').decode().split('\0')) if s]}
def book_hashes():return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for top in ['manuscript','ci','companion'] for p in (root/top).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
before=freeze();assert before['head']==expected and before['status_porcelain_v1']=='',before
(review/'framework-freeze-before.json').write_text(json.dumps(before,indent=2)+'\n')
book_before=book_hashes()
(review/'book-input-hashes-before.json').write_text(json.dumps(book_before,indent=2)+'\n')
work.mkdir(exist_ok=True,parents=True)
(work/'config').mkdir(exist_ok=True)
assert not (work/'source').exists(),'Fresh source export already exists; preserve existing evidence.'
with (work/'source.tar').open('wb') as archive:
 subprocess.run(['git','-C',str(source),'archive',expected],stdout=archive,check=True)
(work/'source').mkdir()
with tarfile.open(work/'source.tar') as archive:archive.extractall(work/'source',filter='data')
(work/'source.tar').unlink()
manifest={p:hashlib.sha256((source/p).read_bytes()).hexdigest() for p in git('ls-files','-z').decode().split('\0') if p}
assert all(hashlib.sha256((work/'source'/p).read_bytes()).hexdigest()==digest for p,digest in manifest.items())
(review/'export-verification.json').write_text(json.dumps({'head':expected,'files':len(manifest),'all_exported_files_match_author_tree':True,'tree_sha256':hashlib.sha256(''.join(f'{v}  {k}\n' for k,v in sorted(manifest.items())).encode()).hexdigest()},indent=2)+'\n')
env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','CMAKE_BUILD_PARALLEL_LEVEL':'8','SNODEC_PREFIX':str(prefix),'BOOK_EXAMPLES_BUILD_DIR':str(work/'examples'),'XDG_CONFIG_HOME':str(work/'config')}
results={}
def run(name,args):
 start=datetime.now(timezone.utc).isoformat()
 with (review/(name+'.log')).open('w') as log:
  log.write('COMMAND: '+json.dumps(list(map(str,args)))+'\nSOURCE: '+expected+'\nPREFIX: '+str(prefix)+'\n');log.flush()
  result=subprocess.run(list(map(str,args)),cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 results[name]={'exit_code':result.returncode,'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat()}
 (review/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,result.returncode,flush=True)
 return result.returncode==0
if run('framework-configure',['cmake','-S',work/'source','-B',work/'framework-gcc','-G','Ninja','-DCMAKE_BUILD_TYPE=Debug','-DSNODEC_BUILD_TESTS=ON','-DSNODEC_BUILD_APPS=ON','-DCMAKE_INSTALL_PREFIX='+str(prefix)]):
 if run('framework-build',['cmake','--build',work/'framework-gcc','--parallel','8']):
  run('framework-inventory',['ctest','--test-dir',work/'framework-gcc','--show-only=json-v1'])
  run('framework-tests',['ctest','--test-dir',work/'framework-gcc','--output-on-failure','--no-tests=error','-V','--output-junit',review/'framework-tests.xml'])
  # A test failure must not suppress the independently requested companion labs.
  if run('framework-install',['cmake','--install',work/'framework-gcc']):
   env['LD_LIBRARY_PATH']=':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))
   if run('external-echo-configure',['cmake','-S',work/'source/examples/echo','-B',work/'external-echo','-G','Ninja','-DCMAKE_BUILD_TYPE=Debug','-DBUILD_TESTING=ON','-DCMAKE_PREFIX_PATH='+str(prefix)]):
    if run('external-echo-build',['cmake','--build',work/'external-echo','--parallel','4']):
     run('external-echo-tests',['ctest','--test-dir',work/'external-echo','--output-on-failure','--no-tests=error','-V','--output-junit',review/'external-echo-tests.xml'])
   if run('companion-build',['bash','ci/build-companion-examples.sh']):
    run('lab-inventory',['ctest','--test-dir',work/'examples','--show-only=json-v1'])
    run('labs',['ctest','--test-dir',work/'examples','--output-on-failure','--no-tests=error','-V','--output-junit',review/'labs.xml'])
    run('teaching-smoke',['python3','ci/run-teaching-smoke-tests.py'])
    run('behavior-smoke',['bash','ci/run-behavior-smoke-tests.sh'])
    run('lifetime-tests',['python3','ci/run-example-lifetime-tests.py','--prefix',prefix,'--build',work/'examples','--work',work/'lifetime'])
after=freeze();(review/'framework-freeze-after.json').write_text(json.dumps(after,indent=2)+'\n')
unchanged=before==after;book_unchanged=book_before==book_hashes()
(review/'preservation.json').write_text(json.dumps({'framework_freeze_unchanged':unchanged,'manuscript_ci_companion_unchanged':book_unchanged},indent=2)+'\n')
assert unchanged and book_unchanged
print('verification finished; no refinement performed',flush=True)
