from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from common import identity, records
from workflow import graph
app=FastAPI(title='Agentic Customer Support')
class Message(BaseModel):
    message:str=Field(min_length=1,max_length=4000)
@app.get('/health')
def health(): return {'status':'ok','orchestration':'LangGraph','routing':'deterministic baseline'}
@app.post('/support')
def support(body:Message,tenant=Depends(identity)):
    result=graph.invoke({'tenant':tenant,'message':body.message})
    return {k:v for k,v in result.items() if k!='tenant'}
@app.get('/tickets')
def tickets(tenant=Depends(identity)): return records(tenant,'ticket')
