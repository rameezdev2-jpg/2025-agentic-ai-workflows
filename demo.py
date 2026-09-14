"""Repeatable local demo; its temporary database is independent of your app data."""
import json, os, tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from app import app
scratch=Path(tempfile.mkdtemp(prefix='portfolio-demo-'))
os.environ['DATABASE_PATH']=str(scratch/'demo.sqlite3')
os.environ['API_KEYS_JSON']='{"local-demo-key":"demo"}'
os.environ['TENANT_ROLES_JSON']='{"demo":"operator"}'
os.environ.pop('LLM_ENDPOINT',None)
os.environ['DAILY_QUOTA']='20'
client=TestClient(app)
H={'Authorization':'Bearer local-demo-key'}
result={'grounded':client.post('/support',headers=H,json={'message':'What is the shipping time?'}).json(),'handoff':client.post('/support',headers=H,json={'message':'Please refund my order'}).json()}
Path('docs/demo-output.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
