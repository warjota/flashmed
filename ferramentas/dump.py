import sqlite3, json, re, html, sys, collections, datetime
db=sys.argv[1]; out=sys.argv[2]
c=sqlite3.connect(db)
decks={r[0]:r[1].replace('\x1f','::') for r in c.execute('select id,name from decks')}
nts={r[0]:r[1] for r in c.execute('select id,name from notetypes')}
fields=collections.defaultdict(list)
for ntid,o,n in c.execute('select ntid,ord,name from fields order by ntid,ord'): fields[ntid].append(n)
def clean(s):
    s=re.sub(r'<br\s*/?>|</div>|</p>|</li>','\n',s,flags=re.I)
    s=re.sub(r'<img[^>]*src="([^"]+)"[^>]*>',r'[IMG:\1]',s,flags=re.I)
    s=re.sub(r'<[^>]+>','',s); s=html.unescape(s)
    return re.sub(r'\n\s*\n+','\n',s).strip()
rev=collections.defaultdict(list)
for cid,ease,ivl,t,typ,tm in c.execute('select cid,ease,ivl,id,type,time from revlog'):
    rev[cid].append((ease,ivl,t,typ,tm))
rows=[]
for cid,nid,did,typ,queue,ivl,reps,lapses,cmod,data in c.execute('select id,nid,did,type,queue,ivl,reps,lapses,mod,data from cards'):
    nmid,mod,flds,tags=c.execute('select mid,mod,flds,tags from notes where id=?',(nid,)).fetchone()
    f=flds.split('\x1f')
    r=rev[cid]
    rows.append(dict(cid=cid,nid=nid,deck=decks[did],nt=nts.get(nmid,nmid),
        fields={fields[nmid][i] if i<len(fields[nmid]) else i:clean(x) for i,x in enumerate(f)},
        raw_len=sum(len(x) for x in f),
        created=datetime.datetime.fromtimestamp(nid/1000).isoformat()[:10],
        note_mod=datetime.datetime.fromtimestamp(mod).isoformat()[:16],
        state={0:'new',1:'learn',2:'review',3:'relearn'}[typ], suspended=queue==-1,
        ivl=ivl,reps=reps,lapses=lapses,tags=tags.strip(),
        answers=[e for e,*_ in r], first_review=(datetime.datetime.fromtimestamp(min(x[2] for x in r)/1000).isoformat()[:16] if r else None),
        avg_time_s=round(sum(x[4] for x in r)/len(r)/1000,1) if r else None, data=data))
json.dump(rows,open(out,'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(rows))
