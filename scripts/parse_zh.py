import re,json
from pathlib import Path
base=Path(r'D:\steam\steamapps\workshop\content\394360\2946487287\localisation\simp_chinese')
pat=re.compile(r'^\s*([A-Za-z0-9_.\-]+):(?:\d+)?\s+"(.*)"\s*$')
loc={}; files=0; bad=0; lines=0
for p in base.rglob('*.yml'):
    files+=1
    try: s=p.read_text(encoding='utf-8-sig')
    except Exception as e: print('ERR',p,e); continue
    for ln in s.splitlines():
        lines+=1
        m=pat.match(ln)
        if m: loc[m.group(1)]=m.group(2)
print('files',files,'lines',lines,'keys',len(loc))
json.dump(loc,open('loc_zh_all.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
# coverage against data
d=json.load(open('evo_data.json',encoding='utf-8'))
fids=set()
for i in d['icons']:
    for u in i['uses']: fids.add(u['fid'])
print('goal uses',sum(len(i['uses']) for i in d['icons']),'unique',len(fids),'loc',sum(1 for f in fids if f in loc))
di=json.load(open('evo_ideas_data.json',encoding='utf-8'))
ifids=set()
for i in di['icons']:
    for u in i['uses']: ifids.add(u['fid'])
print('idea uses',sum(len(i['uses']) for i in di['icons']),'unique',len(ifids),'loc',sum(1 for f in ifids if f in loc))
# all focus ids from focusmap
fm=json.load(open('focusmap_1.7.1.json',encoding='utf-8'))
af=set(fm['focuses'].keys())
print('all focus',len(af),'loc',sum(1 for f in af if f in loc))
