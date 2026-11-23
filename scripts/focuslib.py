import re, os, glob, json, sys

def strip_comments(txt):
    out=[]
    for line in txt.splitlines():
        q=False; res=''
        for ch in line:
            if ch=='"': q=not q
            if ch=='#' and not q: break
            res+=ch
        out.append(res)
    return '\n'.join(out)

TOK=re.compile(r'"[^"]*"|[A-Za-z0-9_.\-]+|[{}]|=')
def tokenize(txt):
    return TOK.findall(strip_comments(txt))

def parse_block(toks,i):
    # toks[i] == '{'
    assert toks[i]=='{'
    i+=1; items=[]
    while i<len(toks) and toks[i]!='}':
        key=toks[i]; i+=1
        if i>=len(toks) or toks[i]!='=':
            # skip stray
            continue
        i+=1
        if i>=len(toks): break
        if toks[i]=='{':
            val,i=parse_block(toks,i)
        else:
            val=toks[i]; i+=1
        items.append((key,val))
    return items,i+1

def parse_file(path):
    toks=tokenize(open(path,encoding='utf-8-sig',errors='replace').read())
    items=[]; i=0
    while i<len(toks):
        if toks[i]=='{': i+=1; continue
        key=toks[i]; i+=1
        if i<len(toks) and toks[i]=='=':
            i+=1
            if i<len(toks) and toks[i]=='{':
                val,i=parse_block(toks,i)
            else:
                val=toks[i] if i<len(toks) else None; i+=1
            items.append((key,val))
    return items

def get(items,key):
    return [v for k,v in items if k==key]
def get1(items,key):
    vs=get(items,key); return vs[0] if vs else None

def unq(s): return s[1:-1] if s and s.startswith('"') else s

def collect_tags(block):
    tags=set()
    if isinstance(block,list):
        for k,v in block:
            if k=='tag' and isinstance(v,str): tags.add(unq(v))
            elif isinstance(v,list): tags |= collect_tags(v)
    return tags
