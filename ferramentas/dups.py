import json,re,sys,unicodedata,collections
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
R=json.load(open(sys.argv[1],encoding='utf-8'))
def norm(s):
    s=re.sub(r'\[IMG:[^\]]*\]','',s); s=unicodedata.normalize('NFKD',s.lower())
    s=''.join(ch for ch in s if not unicodedata.combining(ch))
    s=re.sub(r'^[a-z\- ]{3,40}\.\s','',s)  # topic prefix
    return re.sub(r'[^a-z0-9<>=%]+',' ',s).strip()
R=[r for r in R if r['nt']!='Basic-ce046']
fr=[norm(list(r['fields'].values())[0]) for r in R]
bk=[norm(list(r['fields'].values())[1]) if len(r['fields'])>1 else '' for r in R]
v=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),min_df=2)
Xf=v.fit_transform(fr); Sf=cosine_similarity(Xf,dense_output=False)
v2=TfidfVectorizer(analyzer='char_wb',ngram_range=(3,5),min_df=2)
Xb=v2.fit_transform(bk); 
pairs=[]
Sf=Sf.tocoo()
import numpy as np
for i,j,s in zip(Sf.row,Sf.col,Sf.data):
    if i<j and s>=0.55:
        sb=float(cosine_similarity(Xb[i],Xb[j])[0,0])
        pairs.append((round(float(s),2),round(sb,2),i,j))
out=[dict(sf=s,sb=sb,a=R[i]['cid'],b=R[j]['cid'],da=R[i]['deck'].split('::',1)[-1],db=R[j]['deck'].split('::',1)[-1],
  sa=R[i]['state']+('/S' if R[i]['suspended'] else ''),sbst=R[j]['state']+('/S' if R[j]['suspended'] else ''),
  fa=list(R[i]['fields'].values())[0][:200],fb=list(R[j]['fields'].values())[0][:200],
  ba=(list(R[i]['fields'].values())+[''])[1][:200],bb=(list(R[j]['fields'].values())+[''])[1][:200]) for s,sb,i,j in sorted(pairs,reverse=True)]
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(out), collections.Counter((o['sf']>=0.8, o['sb']>=0.5) for o in out))
