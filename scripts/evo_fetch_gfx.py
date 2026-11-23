# -*- coding: utf-8 -*-
import urllib.request, json, os, re, time, urllib.parse, sys

os.makedirs('evo/gfx', exist_ok=True)
vers = json.load(open('evo/versions.json', encoding='utf-8'))
HDR = {'User-Agent': 'Mozilla/5.0'}

def fetch(url, timeout=90):
    req = urllib.request.Request(url, headers=HDR)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

for i, v in enumerate(vers):
    safe = re.sub(r'[^0-9A-Za-z._-]+', '_', v['tag'])
    out = f'evo/gfx/{safe}.gfx'
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        print('skip', v['ver'], flush=True)
        continue
    tag = urllib.parse.quote(v['tag'])
    urls = [
        f'https://raw.githubusercontent.com/Kaiserreich/Kaiserreich-HOI4/{tag}/interface/kaiserreich/goals.gfx',
        f'https://cdn.jsdelivr.net/gh/Kaiserreich/Kaiserreich-HOI4@{tag}/interface/kaiserreich/goals.gfx',
    ]
    ok = False
    for u in urls:
        try:
            b = fetch(u)
            if len(b) > 10000:
                open(out, 'wb').write(b)
                print('ok', v['ver'], len(b), flush=True)
                ok = True
                break
        except Exception as e:
            print('ERR', v['ver'], str(e)[:80], flush=True)
    if not ok:
        print('FAILED', v['ver'], flush=True)
    time.sleep(0.2)
print('DONE')
