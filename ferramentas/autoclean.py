import re, difflib
def split_answer(back):
    """separa resposta x explicação (Medway indenta explicação com 4+ espaços)"""
    lines=back.split('\n'); ans=[]; exp=[]
    dash = bool(lines) and lines[0].lstrip().startswith('-')
    for i,l in enumerate(lines):
        if not l.strip(): continue
        if exp or (i>0 and ans and (re.match(r'^\s{3,}\S',l) or (dash and not l.lstrip().startswith('-')))):
            exp.append(l.strip())
        else: ans.append(l.rstrip())
    return [a for a in ans if a.strip()], [x for x in exp if x]
def fill_from_cloze(front, first):
    if '__' not in front: return None
    f=re.sub(r'_{2,}',' ',front); f=re.sub(r'\s+',' ',f).strip(); b=re.sub(r'\s+',' ',first).strip().lstrip('-').strip()
    if difflib.SequenceMatcher(None,f.lower(),b.lower()).ratio()<0.6: return None
    sm=difflib.SequenceMatcher(None,f,b,autojunk=False); parts=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op in('insert','replace'):
            seg=b[j1:j2].strip(' ,.;')
            if len(seg)>1: parts.append(seg)
    if not parts: return None
    out=' / '.join(parts)
    return out[0].upper()+out[1:]
def clean(front, back, prefix=None):
    imgs_f=re.findall(r'\[IMG:[^\]]+\]',front)
    if prefix: front=re.sub(r'^'+re.escape(prefix)+r'\.\s*','',front.strip())
    front=re.sub(r'\s+\n','\n',front).strip()
    imgs_b=re.findall(r'\[IMG:[^\]]+\]',back); back_t=re.sub(r'\[IMG:[^\]]+\]','',back)
    ans,exp=split_answer(back_t)
    comment=''
    first=ans[0] if ans else ''
    fill=fill_from_cloze(front,first) if len(ans)==1 else None
    if fill: ans=[fill]
    ans=[a.strip() for a in ans]
    if len(ans)==1: ans=[ans[0].lstrip('-').strip().rstrip('.')]
    exp_txt=' '.join(exp)
    if exp_txt: comment=exp_txt  # explicação Medway vai para o campo oculto Comentário
    new_back='\n'.join(ans)
    if imgs_b: new_back+='\n'+'\n'.join(imgs_b)
    return front,new_back,comment,bool(fill)
