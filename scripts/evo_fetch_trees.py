# -*- coding: utf-8 -*-
import urllib.request, json, os, re, time, sys

API = 'https://api.github.com/repos/Kaiserreich/Kaiserreich-HOI4'
HDR = {'User-Agent': 'lead-evolution'}
os.makedirs('evo/trees', exist_ok=True)

def get(u, timeout=180):
    req = urllib.request.Request(u, headers=HDR)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode('utf-8'))

if os.path.exists('evo/tags.json'):
    tags = json.load(open('evo/tags.json', encoding='utf-8'))
else:
    tags = get(API + '/tags?per_page=100')
    json.dump(tags, open('evo/tags.json', 'w', encoding='utf-8'), ensure_ascii=False)

# official 1.x releases only, sorted by semantic version
from packaging.version import Version, InvalidVersion
rel = []
for t in tags:
    name = t['name']
    m = re.match(r'^(1\.\d+(?:\.\d+)?[a-z]?)(?:_|$)', name)
    if not m:
        continue
    try:
        v = Version(m.group(1))
    except InvalidVersion:
        continue
    rel.append({'tag': name, 'ver': str(v), 'version': v, 'sha': t['commit']['sha']})
rel.sort(key=lambda x: x['version'])
print('versions', len(rel))
for x in rel:
    print(x['ver'], x['tag'], x['sha'][:8])
json.dump([{k: v for k, v in x.items() if k != 'version'} for x in rel],
          open('evo/versions.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

for i, x in enumerate(rel):
    safe = re.sub(r'[^0-9A-Za-z._-]+', '_', x['tag'])
    out = f'evo/trees/{safe}.json'
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print('skip', x['ver'], flush=True)
        continue
    u = f"{API}/git/trees/{x['sha']}?recursive=1"
    for attempt in range(4):
        try:
            d = get(u)
            d['_tag'] = x['tag']
            d['_ver'] = x['ver']
            json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
            print('ok', i + 1, '/', len(rel), x['ver'], len(d.get('tree', [])), flush=True)
            break
        except Exception as e:
            print('ERR', x['ver'], e, flush=True)
            time.sleep(10 * (attempt + 1))
    time.sleep(1)
print('DONE')
