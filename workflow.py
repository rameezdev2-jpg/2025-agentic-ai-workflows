from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from common import save, records
class State(TypedDict,total=False):
    tenant:str
    message:str
    route:str
    answer:str
    citations:list[str]
    handoff:bool
    ticket_id:int
POLICIES={'refund':'Refunds can be requested within thirty days. An agent must approve any payment action.', 'shipping':'Standard shipping takes three to five business days.'}
def classify(state):
    text=state['message'].lower()
    # The graph is deterministic and testable; no untrusted text can invoke tools.
    if any(w in text for w in ['human','refund','cancel','password','ignore','delete']): return {'route':'handoff'}
    if 'order' in text: return {'route':'orders'}
    return {'route':'knowledge'}
def knowledge(state):
    for term,policy in POLICIES.items():
        if term in state['message'].lower(): return {'answer':policy,'citations':['policy:'+term],'handoff':False}
    return {'answer':'I could not find supporting policy. A human will review your question.','citations':[],'handoff':True}
def orders(state):
    # Only records belonging to the authenticated tenant are visible to this tool.
    data=records(state['tenant'],'order')
    if not data: return {'answer':'No order is available in your account. A human will review.','citations':[],'handoff':True}
    return {'answer':'Your latest order status is '+data[-1]['status'],'citations':['order:'+str(data[-1]['id'])],'handoff':False}
def handoff(state):
    return {'answer':'This request requires a human support agent. No external action has been taken.','citations':[],'handoff':True}
def persist(state):
    ticket=save(state['tenant'],'ticket',{'message':state['message'],'answer':state['answer'],'handoff':state['handoff'],'citations':state['citations'],'route':state['route'],'status':'pending_human' if state['handoff'] else 'answered'})
    return {'ticket_id':ticket}
builder=StateGraph(State)
for name,fn in [('classify',classify),('knowledge',knowledge),('orders',orders),('handoff',handoff),('persist',persist)]: builder.add_node(name,fn)
builder.add_edge(START,'classify')
builder.add_conditional_edges('classify',lambda state:state['route'],{'knowledge':'knowledge','orders':'orders','handoff':'handoff'})
for name in ['knowledge','orders','handoff']: builder.add_edge(name,'persist')
builder.add_edge('persist',END)
graph=builder.compile()
