import focuslib,glob,re,json,os
def unq(x): return focuslib.unq(x) if isinstance(x,str) else x
ideas=[]
for fn in glob.glob('ideas/1.7.1/common/ideas/**/*.txt',recursive=True):
    items=focuslib.parse_file(fn)
    top=focuslib.get1(items,'ideas')
    if not isinstance(top,list): continue
    base=os.path.basename(fn)
    m=re.match(r'^([A-Z0-9]{3})\s+ideas',base)
    ftag=m.group(1) if m and not m.group(1).startswith('00') else None
    for cat,cv in top:
        if cat.lower()!='country' or not isinstance(cv,list): continue
        for iid,iv in cv:
            if not isinstance(iv,list): continue
            pic=focuslib.get1(iv,'picture')
            if not isinstance(pic,str): continue
            pic=unq(pic)
            tag=ftag
            mm=re.match(r'^([A-Z]{3})_',iid)
            if mm and (not tag or tag in ('00','01','02','03','04')): tag=mm.group(1)
            ideas.append({'id':iid,'picture':pic,'tag':tag,'file':os.path.relpath(fn).replace('\\','/'),'ftag':ftag})
print('country ideas',len(ideas),'unique ids',len({x['id'] for x in ideas}))
from collections import Counter
print('tags top',Counter(x['tag'] for x in ideas).most_common(20))
print('pictures unique',len({x['picture'] for x in ideas}))
print('no tag',sum(1 for x in ideas if not x['tag']))
for x in ideas[:10]: print(x)
json.dump(ideas,open('idea_defs.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
