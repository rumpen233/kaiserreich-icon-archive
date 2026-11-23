import focuslib,glob,json,os,re
ideas=json.load(open('idea_defs.json',encoding='utf-8'))
tree=json.load(open('evo/trees/1.7.1.json',encoding='utf-8'))['tree']
pngs={x['path'].lower():x['path'] for x in tree if x['path'].startswith('gfx/interface/ideas/') and x['path'].lower().endswith('.png')}
def defs(fn):
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
 d=defs(fn); D.update(d)
print('gfx defs',len(D))
used={}
for x in ideas:
 pic=x['picture']
 names=[]
 if pic.startswith('GFX_'): names=[pic]
 else: names=['GFX_idea_'+pic, pic]
 hit=None
 for n in names:
  if n in D and D[n] in pngs: hit=D[n]; break
 if not hit:
  cand=f'gfx/interface/ideas/{pic}.png'.lower()
  if cand in pngs: hit=pngs[cand]
 x['png']=hit
 used[hit]=used.get(hit,0)+1
print('ideas mapped',sum(1 for x in ideas if x['png']),'of',len(ideas),'unique png',len(used))
print('unmapped pics',len({x['picture'] for x in ideas if not x['png']}))
from collections import Counter
print([p for p,c in Counter(x['picture'] for x in ideas if not x['png']).most_common(15)])
json.dump(ideas,open('idea_defs2.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
