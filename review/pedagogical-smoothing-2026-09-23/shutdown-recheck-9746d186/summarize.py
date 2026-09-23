#!/usr/bin/env python3
"""Summarize complete CTest result sets, retaining individual failure evidence."""
from pathlib import Path
import json,xml.etree.ElementTree as ET

review=Path(__file__).resolve().parent
results=json.loads((review/'results.json').read_text())
summary={};lines=['# Individual test results','', 'All tests use the fresh 9746d186 installation and unchanged test limits.','']
for suite in ['framework-tests','external-echo-tests','labs']:
 path=review/(suite+'.xml')
 if not path.exists():
  summary[suite]={'status':'not run','reason':'see results.json'};continue
 tree=ET.parse(path);cases=tree.findall('.//testcase')
 rows=[]
 for case in cases:
  status='failed' if case.find('failure') is not None or case.find('error') is not None else 'skipped' if case.find('skipped') is not None else 'passed'
  out=case.findtext('system-out','')
  rows.append({'name':case.attrib['name'],'status':status,'seconds':float(case.attrib.get('time','0')),'internal_skip_message':'SKIP:' in out})
 summary[suite]={'total':len(rows),**{k:sum(r['status']==k for r in rows) for k in ['passed','failed','skipped']},'failures':[r['name'] for r in rows if r['status']=='failed'],'internal_skip_messages':[r['name'] for r in rows if r['internal_skip_message']]}
 lines += ['## '+suite,'','| Test | Result | Seconds |','|---|---|---:|']
 lines += [f"| `{r['name']}` | {r['status']} | {r['seconds']:.3f} |" for r in rows]
 lines += ['']
for name,data in results.items():
 if name not in summary:summary[name]={'exit_code':data['exit_code'],'status':'passed' if data['exit_code']==0 else 'failed'}
(review/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(review/'all-tests.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(summary,indent=2))
