import json,glob,os,collections,sys
S=sys.argv[1]; OUT=sys.argv[2]; NOW=sys.argv[3]
L=lambda p:{os.path.basename(f)[:-5]:json.load(open(f)) for f in glob.glob(S+'/'+p+'/*.json')}
T,P,A=L('tasks'),L('phases'),L('areas')
def tv(i):
  if i=='eb-20': return 3
  for pre,v in [('ai-',2),('arn-',2),('cs-',2),('eb-',2),('va-',2)]:
    if i.startswith(pre): return v
  return {'hb-rewards':2,'hb-save-skill':2,'hb-trim-connectors':2}.get(i,1)
W=[]
def upd(col,i,data,v): W.append({'op':'update','collection':col,'doc_id':i,'data':data,'if_version':v})
def new(col,i,data): W.append({'op':'set','collection':col,'doc_id':i,'data':data})
stamp={'updatedAt':NOW}
# --- areas
old=['coaching-marketing','weekday-programming','class-series','transition-zone']
urls=[u for a in old for u in A[a].get('sourceUrls',[])]
new('areas','coaching',{'name':'Coaching','bucket':'Pickleball','prefix':'co','sourceUrls':urls,'dbBacked':False,'order':min(A[a]['order'] for a in old),'active':True,'paused':False,'tracks':{'marketing':'Marketing','weekday':'Weekday programming','classes':'Class series'},'mergedFrom':old,'createdAt':NOW,'updatedAt':NOW})
for a in old: upd('areas',a,{'active':False,'mergedInto':'coaching',**stamp},1)
upd('areas','ai-consulting',{'active':False,'mergedInto':'ai-builder',**stamp},1)
upd('areas','advisor-path',{'paused':True,**stamp},1)
# --- routines
R=[('r-coach-dropins','Play 2 daytime drop-ins and hand out 5 cards','Weekly','coaching',[],['cm-06']),
   ('r-coach-post',"Post the week's classes in one local group",'Weekly','coaching',[],['cm-07']),
   ('r-coach-review','Ask one student for a review','Weekly','coaching',[],['cm-09']),
   ('r-coach-privates','Offer privates to students finishing a series','Each series','coaching',[],['cm-08']),
   ('r-ebay-pack','Pack and ship sold eBay lots','Mon & Thu nights','card-sales',['Pack sold lots','Mark lots Sold and Shipped in the tracker'],['eb-20','eb-21']),
   ('r-ebay-payouts','Log eBay payouts','Weekly','card-sales',[],['cs-28']),
   ('r-comc-batch','Price a new COMC batch','Each batch','card-sales',['Price each card in the batch','Flag hold and grade candidates','Approve asks and auction picks'],['cs-12','cs-13','cs-14']),
   ('r-tz-setup','Set up a Transition Zone class','Each class','coaching',[T[t]['title'] for t in ['tz-01','tz-02','tz-03','tz-04','tz-05','tz-06']],['tz-01','tz-02','tz-03','tz-04','tz-05','tz-06'])]
rid={}
for n,(i,title,cad,area,items,tids) in enumerate(R):
  new('routines',i,{'title':title,'cadence':cad,'area':area,'items':items,'taskIds':tids,'order':n,'active':True,'lastDone':'','createdAt':NOW,'updatedAt':NOW,'changedBy':'migration'})
  for t in tids: rid[t]=i
# --- tasks
trk={'coaching-marketing':'marketing','weekday-programming':'weekday','class-series':'classes','transition-zone':'classes'}
for i,t in T.items():
  d={}
  if t['area'] in trk: d.update(area='coaching',track=trk[t['area']])
  if t['area']=='ai-consulting': d.update(area='ai-builder',bucket=A['ai-builder']['bucket'],track='consulting',phase='')
  if i in rid and t['status'] not in('done','dropped'): d.update(status='parked',routine=rid[i],nextStep='Tracked in Routines')
  if d: d.update(changedBy='migration',**stamp); upd('tasks',i,d,tv(i))
# apply task changes locally for phase-state calc
for w in W:
  if w['collection']=='tasks': T[w['doc_id']].update(w['data'])
# --- phases
for i,p in P.items():
  if p['area'] in trk: p['area']='coaching'; p['track']=trk[[a for a in trk if i.startswith(A[a]['prefix']+'-')][0]]
openS={'todo','doing','waiting','inbox'}
grp=collections.defaultdict(list)
for i,p in P.items(): grp[(p['area'],p.get('track','main'))].append(i)
state={}
for k,ids in grp.items():
  ids.sort(key=lambda i:P[i].get('order',0)); cur=False
  for i in ids:
    ts=[t for t in T.values() if t.get('phase')==i and t['status']!='dropped']
    op=[t for t in ts if t['status'] in openS]
    if ts and all(t.get('routine') for t in ts if t['status']!='done'): state[i]='routine'; continue
    if not op: state[i]='done' if ts and any(t['status']=='done' for t in ts) or not ts else 'done'
    elif not cur: state[i]='current'; cur=True
    else: state[i]='later'
for i,p in P.items():
  d={'state':state[i],**stamp}
  if p['area']=='coaching': d.update(area='coaching',track=p['track'])
  upd('phases',i,d,1)
# write batches
os.makedirs(OUT,exist_ok=True)
for n in range(0,len(W),50): json.dump(W[n:n+50],open(f'{OUT}/batch{n//50}.json','w'))
print(len(W),'writes'); print({s:list(state.values()).count(s) for s in set(state.values())})
print([i for i in state if state[i]=='current'])
# visible count
vis=[t for t in T.values() if t['status'] in('todo','doing') and t['area'] not in('advisor-path',) and (not t.get('phase') or state.get(t['phase'])=='current')]
print('visible',len(vis),collections.Counter(t['area'] for t in vis))
