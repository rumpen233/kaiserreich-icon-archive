# -*- coding: utf-8 -*-
import urllib.request, json, os, re, time
from concurrent.futures import ThreadPoolExecutor, as_completed

API = 'https://api.github.com/repos/Kaiserreich/Kaiserreich-HOI4'
HDR = {'User-Agent': 'lead-evolution'}
vers = json.load(open('evo/versions.json', encoding='utf-8'))

def safe(tag):
    return re.sub(r'[^0-9A-Za-z._-]+', '_', tag)

def one(v):
    out = f"evo/trees/{safe(v['tag'])}.json"
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        return ('skip', v['ver'], 0)
    u = f"{API}/git/trees/{v['sha']}?recursive=1"
    for attempt in range(3):
        try:
            req = urllib.request.Request(u, headers=HDR)
            with urllib.request.urlopen(req, timeout=180) as r:
                b = r.read()
            d = json.loads(b.decode('utf-8'))
            d['_tag'] = v['tag']; d['_ver'] = v['ver']
            json.dump(d, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
            return ('ok', v['ver'], len(d.get('tree', [])))
        except Exception as e:
            if attempt == 2:
                return ('err', v['ver'], str(e)[:60])
            time.sleep(4 + attempt * 6)

with ThreadPoolExecutor(max_workers=4) as ex:
    futs = [ex.submit(one, v) for v in vers]
    for f in as_completed(futs):
        print(*f.result(), flush=True)
print('DONE')
