#!/usr/bin/env python3
"""Independent observation of the checkpoint payload log before/after normal shutdown."""
from pathlib import Path
import json,os,sys
review=Path(__file__).resolve().parent
root=review.parents[2]
work=root/'build/shutdown-recheck-07ca9a29'
os.environ['SNODEC_PREFIX']=str(work/'install-gcc')
sys.path.insert(0,str(root/'companion/exercises'))
from lab_support import connect,free_port,receive,running
binary=str(work/'examples/companion/examples/EchoPair/echoserver')

def inspect(contents):
    try: records=[json.loads(line) for line in contents.splitlines()]
    except json.JSONDecodeError as error: return {'complete_json':False,'error':str(error),'payload_record':False}
    context=[r for r in records if r.get('instance')=='echoserver' and r.get('boundary')=='context' and r.get('origin')=='application']
    matched=any(r['level']=='debug' and 'part-v-checkpoint' in r['message'] and r.get('connection') for r in context)
    return {'complete_json':True,'record_count':len(records),'context_count':len(context),'payload_record':matched}

rows=[]
for trial in range(40):
    port=free_port()
    args=['--log-level=2','--log-format=json','--log-component-level=echo=info','--log-instance-level=echoserver=debug','echoserver','local','--host=127.0.0.1',f'--port={port}']
    retained=None
    try:
        with running(binary,args) as (process,log):
            # Keep this file readable after the unchanged harness removes its temp directory.
            retained=log.open()
            with connect(port,process) as peer:
                payload=b'part-v-checkpoint';peer.sendall(payload);assert receive(peer,len(payload))==payload
            before=log.read_text()
        retained.seek(0);after=retained.read()
        row={'trial':trial,'returncode':process.returncode,'before':inspect(before),'after':inspect(after)}
        assert process.returncode==254 and row['after']['payload_record'],row
        if trial==0 or not row['before']['payload_record']:
            (review/f'checkpoint-{trial}-before.log').write_text(before)
            (review/f'checkpoint-{trial}-after.log').write_text(after)
        rows.append(row)
        (review/'checkpoint-observations.json').write_text(json.dumps(rows,indent=2)+'\n')
    finally:
        if retained: retained.close()
summary={'trials':len(rows),'payload_present_before':sum(r['before']['payload_record'] for r in rows),'payload_missing_before':sum(not r['before']['payload_record'] for r in rows),'payload_present_after':sum(r['after']['payload_record'] for r in rows),'normal_sigint_shutdowns':sum(r['returncode']==254 for r in rows)}
(review/'checkpoint-observations-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
