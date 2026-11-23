import json,re
T=json.load(open('evo/tags.json',encoding='utf-8'))
by={t['name']:t for t in T}
old=[t['name'] for t in T if t['name'].startswith('0.')]
old=list(reversed(old))
one=[x['tag'] for x in json.load(open('evo/versions.json',encoding='utf-8'))]
# insert missing 1.x tags at family end
if '1.4.4e' not in one:
    idx=one.index('1.4.3b')+1
    one.insert(idx,'1.4.4e')
if '1.6.3d' not in one:
    idx=one.index('1.6.3c')+1
    one.insert(idx,'1.6.3d')
alltags=old+one
assert len(alltags)==100 and len(set(alltags))==100, (len(alltags),len(set(alltags)))
def ver_of(tag):
    m=re.match(r'^(\d+\.\d+(?:\.\d+)?[a-z]?)',tag)
    return m.group(1) if m else tag
def major_of(v):
    if v.startswith('0.'): return '0'
    m=re.match(r'^(1\.\d+)',v); return m.group(1) if m else v
out=[]
for tag in alltags:
    t=by[tag]; v=ver_of(tag)
    out.append({'tag':tag,'ver':v,'major':major_of(v),'sha':t['commit']['sha']})
json.dump(out,open('evo/versions_all.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(out)); print(out[:4]); print(out[-3:])
