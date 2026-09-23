from pathlib import Path
from datetime import datetime,timezone
import json,os,subprocess
root=Path(__file__).resolve().parents[3]
review=Path(__file__).resolve().parent
work=root/'build/shutdown-recheck-07ca9a29';prefix=work/'install-gcc'
env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1','SNODEC_PREFIX':str(prefix),'BOOK_EXAMPLES_BUILD_DIR':str(work/'examples'),'LD_LIBRARY_PATH':':'.join(sorted({str(p.parent) for p in prefix.rglob('*.so*')}))}
results={}
for name,args in [('checkpoint-repeat',['-R','^exercise-ch13-part-checkpoint$','--repeat','until-fail:40']),('labs',[])]:
 command=['ctest','--test-dir',str(work/'examples'),'--output-on-failure','--no-tests=error','-V',*args,'--output-junit',str(review/(name+'.xml'))]
 start=datetime.now(timezone.utc).isoformat()
 with (review/(name+'.log')).open('w') as log:
  log.write('COMMAND: '+json.dumps(command)+'\nPREFIX: '+str(prefix)+'\n');log.flush()
  result=subprocess.run(command,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 results[name]={'command':command,'exit_code':result.returncode,'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat()}
 (review/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,result.returncode,flush=True)
