import focuslib,json,glob,os,re
from collections import Counter
versions=json.load(open('evo/versions_all.json',encoding='utf-8'))
trees={}
for fn in glob.glob('evo/trees/*.json'):
    d=json.load(open(fn,encoding='utf-8')); trees[d.get('_tag')]=d['tree']
# name map from 1.7.1 gfx
def parse_defs(fn):
    items=focuslib.parse_file(fn); out={}
    def walk(xs):
        for k,v in xs:
            if isinstance(v,list):
                if k.lower()=='spritetype':
                    name=focuslib.get1(v,'name'); tex=focuslib.get1(v,'texturefile')
                    if name and tex:
                        name=focuslib.unq(name); tex=focuslib.unq(tex).lower().replace('\\','/')
                        out[name]=tex
                else: walk(v)
    walk(items); return out
D={}
for fn in glob.glob('evo/tmp_interface_*idea*.gfx'):
    D.update(parse_defs(fn))
bytex={}
for n,t in D.items(): bytex.setdefault(os.path.splitext(os.path.basename(t))[0],[]).append(n)
# iterate paths
icons={}
for vi,v in enumerate(versions):
    paths={}
    for x in trees[v['tag']]:
        pth=x['path']
        if not pth.startswith('gfx/interface/ideas/') or not pth.lower().endswith(('.png', '.tga')): continue
        key=os.path.splitext(os.path.basename(pth))[0].lower()
        if key not in paths or (pth.lower().endswith('.png') and not paths[key].lower().endswith('.png')):
            paths[key]=pth
    for key,disp in sorted(paths.items()):
        sha=next(x['sha'] for x in trees[v['tag']] if x['path']==disp)
        if key not in icons:
            icons[key]={'path':disp,'file':os.path.basename(disp),'name':(bytex.get(key) or [None])[0],'first':vi,'last':vi,'runs':[],'shas':set()}
        ic=icons[key]; ic['last']=vi
        if disp.lower().endswith('.png') and not ic['path'].lower().endswith('.png'):
            ic['path']=disp; ic['file']=os.path.basename(disp)
        if ic['runs'] and ic['runs'][-1]['sha']==sha and ic['runs'][-1]['end']==vi-1:
            ic['runs'][-1]['end']=vi
        else:
            ic['runs'].append({'start':vi,'end':vi,'sha':sha,'path':disp})
        ic['shas'].add(sha)
# uses
ideas=json.load(open('idea_defs2.json',encoding='utf-8'))
loc=json.load(open('loc_en.json',encoding='utf-8'))
trans=json.load(open('trans_ideas_merged.json',encoding='utf-8'))
loc_zh=json.load(open('loc_zh_all.json',encoding='utf-8'))

def official_zh(fid):
    def clean(x):
        x=x.replace('\\n',' ').replace('\\"','"')
        x=re.sub(r'§[A-Za-z!]','',x)
        return x.strip()
    raw=loc_zh.get(fid)
    if raw:
        return clean(raw)
    m=re.search(r'(\d+)$',fid)
    if m:
        n,stem=m.group(1),fid[:m.start()]
        for cand in (stem, stem.rstrip('_')+'_1', stem+'1'):
            if cand in loc_zh:
                return clean(loc_zh[cand])+f'（{n}）'
    return ''

manual=json.load(open('idea_manual.json',encoding='utf-8')) if os.path.exists('idea_manual.json') else {}
uses={}
for x in ideas:
    if not x.get('png'): continue
    key=os.path.splitext(os.path.basename(x['png']))[0].lower()
    en=loc.get(x['id']) or x['id'].replace('_',' ').title()
    if '[' in en: en=x['id'].replace('_',' ').title()
    zh=official_zh(x['id']) or manual.get(en, trans.get(en,''))
    row={'tag':x['tag'] or '共享','fid':x['id'],'en':en,'zh':zh,'picture':x['picture']}
    uses.setdefault(key,[]).append(row)
# finalize
out=[]
for key,ic in icons.items():
    ic['variants']=len(ic['shas']); del ic['shas']
    ic['current']=ic['last']==len(versions)-1
    if not ic['name']:
        stem=os.path.splitext(ic['file'])[0]
        ic['name']='GFX_idea_'+stem
    u=uses.get(key,[])
    # dedupe by fid+tag
    seen=set(); uu=[]
    for r in u:
        k=(r['tag'],r['fid'])
        if k in seen: continue
        seen.add(k); uu.append(r)
    ic['uses']=uu
    ic['tags']=sorted({r['tag'] for r in uu if r['tag']!='共享'})
    out.append(ic)
out.sort(key=lambda i:(i['last'],i['path']))
# per-version counts
vs=[]
for vi,v in enumerate(versions):
    vv=dict(v)
    total=sum(1 for i in out if i['first']<=vi<=i['last'])
    added=sum(1 for i in out if i['first']==vi)
    changed=sum(1 for i in out if i['first']<vi and any(r['start']==vi and r['start']>i['first'] for r in i['runs']))
    removed=sum(1 for i in out if i['last']==vi-1)
    vv['counts']={'total':total,'added':added,'changed':changed,'removed':removed}
    vs.append(vv)
data={'versions':vs,'icons':out}
json.dump(data,open('evo_ideas_data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('icons',len(out),'current',sum(1 for i in out if i['current']),'removed',sum(1 for i in out if not i['current']))
print('distinct shas',len({r['sha'] for i in out for r in i['runs']}),'runs',sum(len(i['runs']) for i in out),'multi',sum(1 for i in out if i['variants']>1))
print('with uses',sum(1 for i in out if i['uses']),'use rows',sum(len(i['uses']) for i in out),'missing zh',sum(1 for i in out for u in i['uses'] if not u['zh']))
print('size',os.path.getsize('evo_ideas_data.json'))
print('first',out[0])
