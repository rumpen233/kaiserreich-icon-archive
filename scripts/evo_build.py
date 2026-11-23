# -*- coding: utf-8 -*-
import json, os, re, glob, sys
from collections import defaultdict, OrderedDict
from focuslib import parse_file, get1, unq

TAGDIR = 'gfx/interface/goals/'
vers_raw = json.load(open('evo/versions_all.json', encoding='utf-8'))

def safe(tag):
    return re.sub(r'[^0-9A-Za-z._-]+', '_', tag)

def display_ver(tag):
    m = re.match(r'^(\d+\.\d+(?:\.\d+)?[a-z]?)', tag)
    return m.group(1) if m else tag

def major_of(ver):
    m = re.match(r'^(1\.\d+)', ver)
    return '0' if ver.startswith('0.') else (m.group(1) if m else ver)

versions = []
for v in vers_raw:
    tag = v['tag']
    p = f'evo/trees/{safe(tag)}.json'
    if not os.path.exists(p):
        print('MISSING TREE', tag); sys.exit(1)
    d = json.load(open(p, encoding='utf-8'))
    files = {}
    for e in d['tree']:
        if e['type'] == 'blob' and e['path'].startswith(TAGDIR) and e['path'].lower().endswith(('.png', '.tga')):
            files[e['path']] = e['sha']
    versions.append({'tag': tag, 'ver': display_ver(tag), 'major': major_of(display_ver(tag)),
                     'sha': v['sha'], 'files': files, 'tree': d['tree']})

print('versions', len(versions))
for v in versions:
    print(v['ver'], len(v['files']))

# ---- gfx names per version ----
def load_gfx(path):
    if not os.path.exists(path):
        return {}
    items = parse_file(path)
    st = get1(items, 'spriteTypes')
    out = {}
    if isinstance(st, list):
        for k, b in st:
            if k.lower() != 'spritetype' or not isinstance(b, list):
                continue
            name = tex = None
            for kk, vv in b:
                if kk == 'name' and isinstance(vv, str):
                    name = unq(vv)
                elif kk.lower() == 'texturefile' and isinstance(vv, str):
                    tex = unq(vv)
            if name and tex:
                out[tex.replace('\\', '/').lower()] = name
    return out

for v in versions:
    v['gfx'] = load_gfx(f"evo/gfx/{safe(v['tag'])}.gfx")
    print('gfx', v['ver'], len(v['gfx']))

# ---- per icon path groups (case-insensitive) ----
groups = {}
for v in versions:
    for p in v['files']:
        groups.setdefault(os.path.splitext(p.lower())[0], set()).add(p)
print('path groups', len(groups))

# ---- usage at 1.7.1 ----
focus = json.load(open('focusmap_1.7.1.json', encoding='utf-8'))['focuses']
loc_en = json.load(open('loc_en.json', encoding='utf-8'))
trans = json.load(open('trans.json', encoding='utf-8'))
loc_zh = json.load(open('loc_zh_all.json', encoding='utf-8'))

def official_zh(fid):
    def clean(x):
        x = x.replace('\\n', ' ').replace('\\"', '"')
        x = re.sub(r'§[A-Za-z!]', '', x)
        return x.strip()
    raw = loc_zh.get(fid)
    if raw:
        return clean(raw)
    m = re.search(r'(\d+)$', fid)
    if m:
        n, stem = m.group(1), fid[:m.start()]
        for cand in (stem, stem.rstrip('_') + '_1', stem + '1'):
            if cand in loc_zh:
                return clean(loc_zh[cand]) + f'（{n}）'
    return ''


uses_by_gfx = defaultdict(list)
for fid, f in focus.items():
    icons = f.get('icons') or []
    tags = f.get('tags') or ['GENERIC']
    en = loc_en.get(fid) or fid.replace('_', ' ')
    zh = official_zh(fid) or trans.get(en) or ''
    for g in icons:
        for tag in tags:
            uses_by_gfx[g].append({'tag': tag, 'fid': fid, 'en': en, 'zh': zh})

cur = versions[-1]
cur_name_by_tex = {}
for tex, name in cur['gfx'].items():
    # prefer non-shine, shortest name
    cur_name_by_tex.setdefault(tex, name)

def texkey(p):
    return p.replace('\\', '/').lower()

icon_data = []
run_list = []
for key in sorted(groups):
    variants = sorted(groups[key])
    seq = []
    for i, v in enumerate(versions):
        hits = [p for p in variants if p in v['files']]
        if hits:
            hits.sort(key=lambda q: (0 if q.lower().endswith('.png') else 1, q))
            seq.append((i, v['files'][hits[0]], hits[0]))
    if not seq:
        continue
    p = seq[-1][2]
    # runs: consecutive version indices with same sha
    runs = []
    for i, sha, rpath in seq:
        if runs and runs[-1]['sha'] == sha and runs[-1]['end'] == i - 1:
            runs[-1]['end'] = i
        else:
            runs.append({'start': i, 'end': i, 'sha': sha, 'path': rpath})
    # variant count = distinct sha
    shas = []
    for r in runs:
        if r['sha'] not in shas:
            shas.append(r['sha'])
    first = seq[0][0]; last = seq[-1][0]
    # name: current gfx if texture exists, else latest version where mapped
    name = cur_name_by_tex.get(texkey(p))
    if not name:
        for i in range(len(versions) - 1, -1, -1):
            if p in versions[i]['files']:
                name = versions[i]['gfx'].get(texkey(p))
                if name:
                    break
    if not name:
        name = os.path.splitext(os.path.basename(p))[0]
    # usage: all names for this texture in current version
    names = sorted({g for g, n in cur['gfx'].items() if n == name}) if name else []
    # if same texture has multiple names, gather all
    same_tex_names = [n for g, n in cur['gfx'].items() if g == texkey(p)]
    all_names = sorted(set(same_tex_names)) or [name]
    uses = []
    seen = set()
    for g in all_names:
        for u in uses_by_gfx.get(g, []):
            key = (u['tag'], u['fid'])
            if key in seen:
                continue
            seen.add(key); uses.append(u)
    uses.sort(key=lambda u: (u['tag'], u['fid']))
    tags = sorted({u['tag'] for u in uses})
    icon = {
        'path': p,
        'file': os.path.basename(p),
        'name': name,
        'first': first,
        'last': last,
        'current': last == len(versions) - 1,
        'runs': runs,
        'variants': len(shas),
        'uses': uses,
        'tags': tags,
    }
    icon_data.append(icon)
    for r in runs:
        run_list.append({'sha': r['sha'], 'start': r['start'], 'end': r['end'], 'path': r.get('path', p)})

print('icons', len(icon_data), 'runs', len(run_list))
print('current', sum(1 for x in icon_data if x['current']), 'removed', sum(1 for x in icon_data if not x['current']))
print('with uses', sum(1 for x in icon_data if x['uses']))

# per-version diff counts
prev = {}
for i, v in enumerate(versions):
    curset = {p.lower(): sha for p, sha in v['files'].items()}
    added = [p for p in curset if p not in prev]
    removed = [p for p in prev if p not in curset]
    changed = [p for p in curset if p in prev and prev[p] != curset[p]]
    v['counts'] = {'total': len(curset), 'added': len(added), 'changed': len(changed), 'removed': len(removed)}
    prev = curset

# compact versions for HTML
vout = []
for i, v in enumerate(versions):
    vout.append({'tag': v['tag'], 'ver': v['ver'], 'major': v['major'], 'counts': v['counts']})

for x in icon_data:
    for r in x['runs']:
        r.pop('path', None)
data = {'versions': vout, 'icons': icon_data}
json.dump(data, open('evo_data.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('wrote evo_data.json', os.path.getsize('evo_data.json'))

# list assets needed
assets = {}
for r in run_list:
    assets.setdefault(r['sha'], {'sha': r['sha'], 'tag': versions[r['start']]['tag'], 'ver': versions[r['start']]['ver'], 'path': r['path']})
json.dump(list(assets.values()), open('evo_assets.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('assets', len(assets))
