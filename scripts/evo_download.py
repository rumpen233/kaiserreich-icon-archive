# -*- coding: utf-8 -*-
import json, os, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
import requests, urllib3
from threading import local
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.makedirs('evo/raw', exist_ok=True)
os.makedirs('evo_thumbs', exist_ok=True)
assets = json.load(open('evo_assets.json', encoding='utf-8'))
_tl = local()

def session():
    if not hasattr(_tl, 's'):
        s = requests.Session()
        s.verify = False
        s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        _tl.s = s
    return _tl.s

def work(a):
    sha = a['sha']
    ext = os.path.splitext(a['path'])[1].lower() or '.png'
    raw = f'evo/raw/{sha}{ext}'
    th = f'evo_thumbs/{sha}.webp'
    if os.path.exists(th) and os.path.getsize(th) > 200:
        return ('skip', sha)
    if not (os.path.exists(raw) and os.path.getsize(raw) > 200):
        tag = urllib.parse.quote(a['tag'])
        p = urllib.parse.quote(a['path'])
        urls = [
            f'https://cdn.jsdelivr.net/gh/Kaiserreich/Kaiserreich-HOI4@{tag}/{p}',
            f'https://raw.githubusercontent.com/Kaiserreich/Kaiserreich-HOI4/{tag}/{p}',
        ]
        b = None
        for u in urls:
            try:
                r = session().get(u, timeout=(6, 12))
                if r.status_code == 200 and len(r.content) > 200:
                    b = r.content
                    break
            except Exception:
                pass
        if not b:
            return ('fail', sha)
        open(raw, 'wb').write(b)
    try:
        im = Image.open(raw).convert('RGBA')
        im.thumbnail((160, 141), Image.LANCZOS)
        canvas = Image.new('RGBA', (160, 141), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((160 - im.width) // 2, (141 - im.height) // 2))
        canvas.save(th, 'WEBP', quality=87, method=4)
    except Exception:
        return ('bad', sha)
    return ('ok', sha)

print('assets', len(assets), flush=True)
done = 0
fails = []
with ThreadPoolExecutor(max_workers=16) as ex:
    futs = {ex.submit(work, a): a for a in assets}
    for f in as_completed(futs):
        st, sha = f.result()
        done += 1
        if st in ('fail', 'bad'):
            fails.append((st, sha))
        if done % 50 == 0:
            print(done, '/', len(assets), 'fails', len(fails), flush=True)
print('DONE', done, 'fails', len(fails), flush=True)
json.dump(fails, open('evo_fails.json', 'w'), ensure_ascii=False)
