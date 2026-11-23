# -*- coding: utf-8 -*-
import json, os, re

data = json.load(open('evo_data.json', encoding='utf-8'))
ideas = json.load(open('evo_ideas_data.json', encoding='utf-8'))
V = data['versions']; I = data['icons']
cur = V[-1]
stats = {
    'versions': len(V),
    'icons': len(I),
    'current': sum(1 for x in I if x['current']),
    'variants': len({r['sha'] for x in I for r in x['runs']}),
    'removed': sum(1 for x in I if not x['current']),
    'changed_icons': sum(1 for x in I if x['variants'] > 1),
}
print(stats)

# compact data: drop per-run path duplication, keep usage cap
for x in I:
    x['uses'] = x['uses'][:180]
json_js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
for x in ideas['icons']:
    x['uses'] = x['uses'][:180]
json_ideas = json.dumps(ideas, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

html = r'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kaiserreich 国策图标演变 · 0.11 → 1.7.1</title>
<style>
:root{
  --bg:#f3efe5; --bg2:#faf7ef; --paper:#fffdf7; --ink:#27231c; --muted:#756d5f;
  --line:#e2d9c8; --line2:#d3c6ae; --gold:#a97728; --gold2:#c89a45;
  --red:#a4483d; --green:#4f7d5d; --blue:#55778c; --shadow:0 8px 26px rgba(73,57,28,.08);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; color:var(--ink); background:
    radial-gradient(900px 420px at 12% -5%, rgba(200,154,69,.20), transparent 60%),
    radial-gradient(800px 380px at 92% 2%, rgba(164,72,61,.10), transparent 60%),
    linear-gradient(180deg,var(--bg2),var(--bg) 460px);
  font-family:"Noto Sans SC","Microsoft YaHei UI","Microsoft YaHei",system-ui,-apple-system,sans-serif;
  line-height:1.6;
}
.wrap{width:min(1280px,calc(100% - 44px));margin:0 auto}
.hero{padding:54px 0 24px}
.kicker{font-size:12px;letter-spacing:.22em;color:var(--gold);font-weight:700}
h1{font-family:"Noto Serif SC","Songti SC",Georgia,serif;font-size:clamp(36px,5vw,64px);
  line-height:1.08;margin:10px 0 12px;letter-spacing:-.02em;font-weight:800}
h1 em{font-style:normal;color:var(--red)}
.lede{max-width:820px;margin:0;color:#5f574a;font-size:16px}
.lede b{color:var(--ink)}
.stats{display:flex;flex-wrap:wrap;gap:12px;margin:26px 0 0}
.stat{background:rgba(255,253,247,.72);border:1px solid var(--line);border-radius:14px;
  padding:10px 16px;min-width:120px;box-shadow:0 3px 12px rgba(73,57,28,.04)}
.stat b{display:block;font-size:26px;line-height:1.1;font-family:"Noto Serif SC",Georgia,serif;color:var(--gold)}
.stat span{font-size:12px;color:var(--muted)}
.typebar{display:flex;gap:10px;margin:24px 0 0;flex-wrap:wrap}
.type{appearance:none;border:1px solid var(--line);background:#fffdf7;color:var(--ink);border-radius:12px;padding:11px 16px;font:inherit;cursor:pointer;display:flex;align-items:baseline;gap:9px;box-shadow:0 2px 0 rgba(80,60,30,.04)}
.type:hover{border-color:#c7ab70}
.type.active{background:var(--ink);color:#fbf4e4;border-color:var(--ink)}
.type small{font-size:11px;letter-spacing:.03em;opacity:.65}
.type.active small{opacity:.8;color:#e8cf9a}
.panel{background:var(--paper);border:1px solid var(--line);border-radius:20px;
  box-shadow:var(--shadow);padding:22px;margin:18px 0}
.panel-head{display:flex;justify-content:space-between;gap:18px;align-items:flex-end;flex-wrap:wrap}
h2{font-family:"Noto Serif SC","Songti SC",Georgia,serif;font-size:22px;margin:0;
  padding-left:12px;border-left:4px solid var(--gold);line-height:1.25}
.panel-head p{margin:0;color:var(--muted);font-size:13px}
.timeline-wrap{overflow-x:auto;padding:18px 2px 6px;scrollbar-width:thin;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 26px,#000 100%);
  mask-image:linear-gradient(90deg,transparent 0,#000 26px,#000 100%)}
.timeline{display:flex;gap:16px;min-width:max-content}
.major{display:flex;flex-direction:column;gap:7px;padding-right:14px;border-right:1px dashed var(--line2)}
.major:last-child{border-right:0}
.major-label{font-size:12px;font-weight:800;color:var(--gold);letter-spacing:.04em;white-space:nowrap}
.major-label span{font-weight:500;color:var(--muted);margin-left:4px}
.vers{display:flex;gap:5px;align-items:flex-end}
.ver{border:1px solid var(--line);background:#fff;color:#4d463a;border-radius:8px;
  padding:5px 8px;font:600 11px/1.2 ui-monospace,Consolas,monospace;cursor:pointer;white-space:nowrap;
  transition:.15s;display:flex;flex-direction:column;gap:2px;align-items:center}
.ver small{font:500 9px/1 ui-monospace,Consolas,monospace;color:var(--muted)}
.ver:hover{border-color:var(--gold2);background:#fffaf0;transform:translateY(-1px)}
.ver.active{background:var(--ink);border-color:var(--ink);color:#fff;box-shadow:0 4px 12px rgba(39,35,28,.22)}
.ver.active small{color:#d9cdb5}
.ver.major-start{border-color:var(--gold2);background:#fff8e8}
.ver.major-start.active{background:var(--gold);border-color:var(--gold)}
.chart-wrap{margin-top:14px;overflow-x:auto;padding-bottom:2px}
.chart{display:flex;align-items:flex-end;gap:4px;height:120px;min-width:760px;
  border-bottom:1px solid var(--line);padding:0 2px}
.bar{flex:1;min-width:8px;display:flex;flex-direction:column;justify-content:flex-end;height:100%;cursor:default}
.bar i{display:block;width:100%;border-radius:3px 3px 0 0}
.bar .a{background:var(--green)} .bar .c{background:var(--gold2)} .bar .r{background:var(--red)}
.chart-note{font-size:11px;color:var(--muted);margin-top:8px}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:11px;color:var(--muted);margin-top:8px}
.legend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:5px}
.toolbar{display:flex;gap:12px;justify-content:space-between;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.tabs{display:flex;background:#f1eadc;border:1px solid var(--line);border-radius:11px;padding:3px}
.tab{border:0;background:transparent;padding:8px 14px;border-radius:8px;font:700 13px/1 inherit;color:#6a6153;cursor:pointer}
.tab.active{background:var(--paper);color:var(--ink);box-shadow:0 2px 7px rgba(73,57,28,.10)}
.search{display:flex;align-items:center;gap:8px;background:#fff;border:1px solid var(--line);
  border-radius:11px;padding:0 12px;height:40px;min-width:min(380px,100%)}
.search input{border:0;outline:0;background:transparent;font:14px inherit;width:320px;max-width:58vw;color:var(--ink)}
.search span{color:var(--muted);font-size:15px}
.search-tools{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.tag-filter{position:relative;flex:none}
.tagbtn{height:40px;border:1px solid var(--line);background:#fff;color:#6a6153;border-radius:11px;
  padding:0 13px;font:700 12px/1 inherit;cursor:pointer;white-space:nowrap}
.tagbtn:hover{border-color:var(--gold2);color:#7a5317}
.tagbtn.active{background:#fff4dc;border-color:var(--gold2);color:#7a5317}
.tagbtn span{display:inline-block;margin-left:5px;padding:2px 6px;border-radius:99px;
  background:#f1eadc;color:#7a6b53;font:700 10px/1.5 ui-monospace,Consolas,monospace}
.tagbtn.active span{background:#f1d9a7;color:#6b4710}
.tagpop{display:none;position:absolute;right:0;bottom:47px;width:356px;max-width:calc(100vw - 34px);
  background:#fffdf8;border:1px solid var(--line2);border-radius:14px;z-index:40;
  box-shadow:0 18px 50px rgba(47,36,18,.22);overflow:hidden}
.tagpop.open{display:block}
.tagpop-head{display:flex;gap:7px;align-items:center;padding:11px;border-bottom:1px solid var(--line)}
.tagpop-head input{flex:1;min-width:0;height:32px;border:1px solid var(--line);border-radius:8px;
  background:#fff;padding:0 9px;outline:0;font:12px inherit;color:var(--ink)}
.tagpop-head input:focus{border-color:var(--gold2)}
.tagpop-head button{border:0;background:transparent;color:var(--red);font:700 11px inherit;cursor:pointer;padding:5px}
.taglist{display:grid;grid-template-columns:1fr 1fr;gap:5px;max-height:286px;overflow:auto;padding:9px}
.tagchip{display:flex;align-items:center;justify-content:space-between;gap:6px;
  border:1px solid #e9dfcc;background:#fff;border-radius:7px;padding:6px 7px;
  font:700 10.5px/1.2 ui-monospace,Consolas,monospace;color:#5f5647;cursor:pointer;text-align:left}
.tagchip:hover{border-color:var(--gold2);background:#fffaf0}
.tagchip.active{background:#fff1d0;border-color:var(--gold);color:#6b4710}
.tagchip b{font-weight:700;color:#9a8f7a;font-size:9.5px}
.tagchip.active b{color:#8a5a12}
.tagnone{grid-column:1/-1;padding:18px 6px;text-align:center;color:var(--muted);font-size:11px}
.tagpop-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;
  padding:9px 11px;border-top:1px solid var(--line);background:#fbf6ea;font-size:10.5px;color:var(--muted)}
.tagdone{border:1px solid var(--gold2);background:#fff4dc;color:#7a5317;border-radius:7px;
  padding:5px 10px;font:700 11px inherit;cursor:pointer}
.tag-active{display:none;gap:5px;align-items:center;flex-wrap:wrap;margin:0 0 12px;
  padding:8px 10px;background:#fffaf0;border:1px solid #efe2c8;border-radius:9px;
  font-size:11px;color:#81735d}
.tag-active.show{display:flex}
.tag-active button{border:1px solid #e4c98f;background:#fff;color:#7a5317;border-radius:99px;
  padding:2px 8px;font:700 10px ui-monospace,Consolas,monospace;cursor:pointer}
.tag-active button:hover{background:#f8e7c4}
.filters{display:flex;gap:7px;flex-wrap:wrap;margin:4px 0 14px}
.chip{border:1px solid var(--line);background:#fff;border-radius:99px;padding:5px 12px;
  font:600 12px/1.2 inherit;color:#6a6153;cursor:pointer}
.chip.active{background:#fff4dc;border-color:var(--gold2);color:#7a5317}
.result-line{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;
  font-size:12px;color:var(--muted);margin-bottom:12px}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:14px}
.card{background:#fff;border:1px solid var(--line);border-radius:13px;overflow:hidden;cursor:pointer;
  transition:.16s;box-shadow:0 2px 8px rgba(73,57,28,.035);position:relative}
.card:hover{transform:translateY(-3px);border-color:var(--gold2);box-shadow:0 10px 24px rgba(94,71,25,.13)}
.card .art{height:164px;background:
  linear-gradient(135deg,#fbf7ed,#f1e9d9);display:flex;align-items:center;justify-content:center;position:relative;border-bottom:1px solid #eee5d3}
.card .art img{width:142px;height:126px;object-fit:contain;image-rendering:auto}
.card .vbadge{position:absolute;right:7px;top:7px;background:rgba(39,35,28,.78);color:#fff;
  font:700 10px/1 ui-monospace,Consolas,monospace;border-radius:99px;padding:4px 7px}
.card .body{padding:11px 12px 12px}
.card .focus{padding:0 0 9px;margin-bottom:8px;border-bottom:1px dashed #eee5d3}
.card .ftag{display:inline-block;margin-right:4px;padding:1px 4px;border-radius:4px;background:#f2e4c6;color:#7a5317;font:700 8.5px/1.45 ui-monospace,Consolas,monospace;vertical-align:1px}
.card .fzh{font:700 15px/1.35 "Noto Serif SC","Songti SC",Georgia,serif;color:var(--ink);
  display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden}
.card .fzh.second{font-size:12.5px;color:#5f574a;font-family:inherit;font-weight:600;margin-top:2px}
.card .fzh.none{color:var(--muted);font-family:inherit;font-size:11.5px;font-weight:500}
.card .fen{font-size:10px;line-height:1.4;color:#8b8170;margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .fcnt{font-size:9.5px;color:var(--gold);margin-top:5px;font-weight:700}
.card h3{margin:0 0 1px;font:700 11.5px/1.3 ui-monospace,Consolas,monospace;word-break:break-all}
.card .file{font-size:10px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .tags{display:flex;gap:4px;flex-wrap:wrap;margin-top:7px;min-height:18px}
.card .tags span{background:#f4eee1;border:1px solid #e9dfcc;color:#6d6352;border-radius:4px;
  padding:1px 4px;font:600 9px/1.5 ui-monospace,Consolas,monospace}
.card .meta{display:flex;justify-content:space-between;gap:6px;margin-top:7px;
  font-size:9.5px;color:#8c8271;border-top:1px dashed #eee5d3;padding-top:6px}
.card .meta b{color:var(--gold);font-weight:700}
.card .state{position:absolute;left:7px;top:7px;border-radius:5px;padding:2px 5px;
  font:700 9px/1.4 inherit;color:#fff;background:var(--green)}
.card .state.removed{background:var(--red)}
.card .state.changed{background:var(--gold)}
.more{text-align:center;margin-top:18px}
.btn{border:1px solid var(--line2);background:#fff;color:#5d5344;border-radius:10px;
  padding:10px 20px;font:700 13px inherit;cursor:pointer}
.btn:hover{border-color:var(--gold);color:var(--gold)}
.empty{padding:50px 20px;text-align:center;color:var(--muted);font-size:14px}
footer{color:#8a806f;font-size:11px;padding:28px 4px 50px;line-height:1.9}
footer code{background:#fff;border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:10px}
.modal{position:fixed;inset:0;background:rgba(39,32,20,.38);backdrop-filter:blur(3px);
  display:none;align-items:center;justify-content:center;padding:22px;z-index:50}
.modal.open{display:flex}
.dialog{background:var(--paper);border:1px solid var(--line2);border-radius:18px;
  width:min(920px,100%);max-height:90vh;overflow:auto;box-shadow:0 30px 80px rgba(35,26,12,.32)}
.dialog-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;
  padding:18px 20px 12px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--paper);z-index:2}
.dialog-head h3{margin:0;font:800 15px/1.35 ui-monospace,Consolas,monospace;word-break:break-all}
.dialog-head p{margin:3px 0 0;font-size:11px;color:var(--muted)}
.x{border:1px solid var(--line);background:#fff;border-radius:9px;width:32px;height:32px;
  font:400 19px/1 inherit;cursor:pointer;color:#6a6153;flex:none}
.dialog-body{padding:16px 20px 20px}
.section-title{font:700 12px/1.4 inherit;color:var(--gold);letter-spacing:.06em;margin:2px 0 10px}
.history{display:flex;gap:10px;overflow-x:auto;padding:2px 0 10px}
.hist{min-width:172px;background:#fff;border:1px solid var(--line);border-radius:11px;padding:10px;text-align:center}
.hist img{width:152px;height:134px;object-fit:contain}
.hist .hl{font:700 10.5px/1.3 ui-monospace,Consolas,monospace;margin-top:4px}
.hist .hs{font-size:10px;color:var(--muted)}
.uses{max-height:54vh;overflow:auto;border:1px solid var(--line);border-radius:11px}
table{border-collapse:collapse;width:100%;font-size:12px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid #eee5d3;vertical-align:top}
th{background:#f6f0e3;color:#6b6150;font-weight:700;position:sticky;top:0;font-size:10.5px}
td.tag{font:700 11px ui-monospace,Consolas,monospace;color:var(--red);white-space:nowrap}
td.id{font:10.5px ui-monospace,Consolas,monospace;color:#756d5f;word-break:break-all}
.note{font-size:11px;color:var(--muted);margin:8px 0 0}
@media(max-width:720px){
  .wrap{width:calc(100% - 24px)} .hero{padding-top:34px}
  .panel{padding:15px;border-radius:15px} .gallery{grid-template-columns:repeat(auto-fill,minmax(164px,1fr))}
  .card .art{height:126px} .card .art img{width:108px;height:96px}
  .card .fzh{font-size:14px}
  .search{width:100%} .search input{width:100%;max-width:none}
  .search-tools{width:100%;justify-content:stretch}
  .tag-filter{width:100%}
  .tagbtn{width:100%;justify-content:center}
  .tagpop{left:0;right:auto;width:100%;max-width:100%}
  .taglist{grid-template-columns:1fr}
}
</style>
</head>
<body>
<header class="hero"><div class="wrap">
  <div class="kicker">KAISERREICH · HOI4 · FOCUS &amp; IDEA ICON ARCHIVE</div>
  <h1 id="heroTitle">国策图标的<em>演变</em></h1>
  <p class="lede" id="heroLede">从 <b>0.11 漫漫归途</b> 到 <b>1.7.1</b>：<b>100 个 GitHub 版本</b>里每一枚 <code>gfx/interface/goals</code> 图标的出现、重绘与消失。浅色时间轴版，卡片直接标出使用它的<b>中文国策名</b>（官方简中优先），点开可看完整视觉史与全部使用国策。</p>
  <div class="stats" id="stats"></div>
  <div class="typebar" id="typebar">
    <button class="type active" data-type="goals">国策图标 <small>goals · 4,218</small></button>
    <button class="type" data-type="ideas">民族精神 <small>ideas · 2,082</small></button>
  </div>
</div></header>

<main class="wrap">
  <section class="panel">
    <div class="panel-head">
      <h2>版本时间轴</h2>
      <p>点击版本 → 查看该版本所有图标的样子；或切到“全量演变”浏览每一枚图标的全部版本。</p>
    </div>
    <div class="timeline-wrap"><div class="timeline" id="timeline"></div></div>
    <div class="chart-wrap"><div class="chart" id="chart"></div></div>
    <div class="legend"><span><i style="background:var(--green)"></i>新增</span><span><i style="background:var(--gold2)"></i>重绘</span><span><i style="background:var(--red)"></i>移除</span><span style="margin-left:auto">条形按数量平方根缩放，0.11 为初始基线</span></div>
  </section>

  <section class="panel">
    <div class="toolbar">
      <div class="tabs">
        <button class="tab active" data-mode="all">全量演变</button>
        <button class="tab" data-mode="snapshot">版本快照</button>
      </div>
      <div class="search-tools">
        <label class="search"><span>⌕</span><input id="search" type="search" placeholder="搜索 GFX 名 / 文件名 / TAG / 国策名…" autocomplete="off"></label>
        <div class="tag-filter">
          <button class="tagbtn" id="tagBtn" type="button" aria-expanded="false">TAG 筛选 <span id="tagBtnLabel">全部</span></button>
          <div class="tagpop" id="tagPop">
            <div class="tagpop-head">
              <input id="tagSearch" type="search" placeholder="搜索 TAG，如 GER / RUS / CHI…" autocomplete="off">
              <button id="tagClear" type="button">清除</button>
            </div>
            <div class="taglist" id="tagList"></div>
            <div class="tagpop-foot"><span id="tagSelInfo">未选择 TAG（显示全部）</span><button class="tagdone" id="tagDone" type="button">完成</button></div>
          </div>
        </div>
      </div>
    </div>
    <div class="filters" id="filters"></div>
    <div class="tag-active" id="tagActive"></div>
    <div class="result-line"><span id="resultCount"></span><span id="resultHint"></span></div>
    <div class="gallery" id="gallery"></div>
    <div class="more"><button class="btn" id="moreBtn">加载更多</button></div>
  </section>

  <footer>
    数据：Kaiserreich/Kaiserreich-HOI4 官方 tag（0.11_The_Long_Road_Home → 1.7.1，共 100 个），逐个版本比对 goals / ideas 目录与对应 gfx；
    中文名优先采用 KR 1.7.1 官方简中译名，缺失时回退机翻；老版本中已移除、1.7.1 无译名的国策保留机翻/英文；部分编号变体官方只译基础名，按“基础名（n）”回退。仅 1.7.1 仍存在的图标显示当前 TAG 使用情况；顶部“TAG 筛选”支持多选，命中任意一个 TAG 即显示。生成时间 2026-11-22。<br>
    民族精神部分仅统计 <code>gfx/interface/ideas</code> 下的 PNG/TGA 自有美术；大量通用 DDS 图标不在本页。0.11–0.17 的旧素材为 .tga，0.18 起转为 .png；早期图标名优先取当时的 KR_goals.gfx，个别缺失时才回退文件名。
    统计按图标身份合并仅大小写不同的路径（如 USA_LIberal → USA_Liberal）；1.7.1 路径层面为 20 新增 / 10 删除，按身份为 19 新增 / 9 删除。
  </footer>
</main>

<div class="modal" id="modal" aria-hidden="true"><div class="dialog" role="dialog" aria-modal="true">
  <div class="dialog-head"><div><h3 id="mTitle"></h3><p id="mSub"></p></div><button class="x" id="mClose" aria-label="关闭">×</button></div>
  <div class="dialog-body">
    <div class="section-title">视觉史 · 从左到右</div>
    <div class="history" id="mHistory"></div>
    <div class="section-title" id="mUseTitle">1.7.1 中还在使用它的国策</div>
    <p class="note" id="mNote"></p>
    <div class="uses" id="mUses"></div>
  </div>
</div></div>

<script>
const GOALS = __DATA_JSON__;
const IDEAS = __IDEAS_JSON__;
let DATA = GOALS, V = DATA.versions, ICONS = DATA.icons;
const $ = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MAJOR_NAME = {'0':'早期版本','1.0':'帝国反击','1.1':'','1.2':'Pour le Mérite','1.3':'蓝色海洋','1.4':'诸俄罗斯','1.5':'美丽新世界','1.6':'Ju 事件','1.7':'十字路口'};
let state = {mode:'all', vi:V.length-1, filter:'all', q:'', shown:96, tags:[], tagQ:''};
let TAG_COUNTS = new Map(), TAG_OPEN = false;

function prep(list){
list.forEach(i => {
  const seen = new Set();
  i._foci = [];
  for (const u of i.uses) {
    if (!seen.has(u.fid)) { seen.add(u.fid); i._foci.push(u); }
  }
  i._s = [i.name, i.file, i.first, i.last, ...i.tags,
    ...i.uses.map(u => u.tag + ' ' + u.fid + ' ' + u.en + ' ' + (u.zh||''))].join(' ').toLowerCase();
});
}
prep(GOALS.icons); prep(IDEAS.icons);
function buildTagCounts(){
  TAG_COUNTS = new Map();
  ICONS.forEach(i => new Set(i.tags || []).forEach(t => {
    if (t) TAG_COUNTS.set(t, (TAG_COUNTS.get(t) || 0) + 1);
  }));
}
let byPath = new Map(ICONS.map(i => [i.path, i]));
const fmt = n => n.toLocaleString('zh-CN');

// stats
function renderStats(){
$('#stats').innerHTML = [
  [V.length, '个 GitHub 版本'],
  [fmt(ICONS.length), '历史图标总数'],
  [fmt(ICONS.filter(x=>x.current).length), '1.7.1 当前图标'],
  [fmt(new Set(ICONS.flatMap(x=>x.runs.map(r=>r.sha))).size), '不同画面版本'],
  [fmt(ICONS.filter(x=>!x.current).length), '已移除图标'],
].map(([a,b])=>`<div class="stat"><b>${a}</b><span>${b}</span></div>`).join('');
}

// timeline
function renderTimeline(){
const groups = [];
for (const v of V) {
  let g = groups[groups.length-1];
  if (!g || g.major !== v.major) { g = {major:v.major, vs:[]}; groups.push(g); }
  g.vs.push(v);
}
$('#timeline').innerHTML = groups.map(g => `
  <div class="major"><div class="major-label">${g.major}${MAJOR_NAME[g.major] ? ' <span>'+MAJOR_NAME[g.major]+'</span>' : ''}</div>
  <div class="vers">${g.vs.map(v => {
    const i = V.indexOf(v);
    return `<button class="ver${v===V[V.length-1]?'':''}${v.ver===g.vs[0].ver?' major-start':''}" data-i="${i}" title="${esc(v.tag)} · 共 ${v.counts.total} 枚（+${v.counts.added} ~${v.counts.changed} -${v.counts.removed}）">${v.ver}<small>${v.counts.total}</small></button>`;
  }).join('')}</div></div>`).join('');
}

// chart
function renderChart(){
const maxTotal = Math.max(...V.slice(1).map(v=>v.counts.added+v.counts.changed+v.counts.removed));
$('#chart').innerHTML = V.map((v,i) => {
  const n = v.counts.added+v.counts.changed+v.counts.removed;
  const h = n ? Math.min(116, 5 + 112 * Math.sqrt(n) / Math.sqrt(maxTotal)) : 2;
  const pr = n ? v.counts.removed/n*100 : 0, pc = n ? v.counts.changed/n*100 : 0;
  const bg = n ? `linear-gradient(to top, var(--red) 0 ${pr}%, var(--gold2) ${pr}% ${pr+pc}%, var(--green) ${pr+pc}% 100%)` : 'var(--line)';
  return `<div class="bar" data-i="${i}" style="height:${h}px;background:${bg}" title="${v.ver}｜新增 ${v.counts.added} · 重绘 ${v.counts.changed} · 移除 ${v.counts.removed}"></div>`;
}).join('');
}

// filters / tabs
function setMode(m){ state.mode=m; state.shown=96; state.filter='all'; document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.mode===m)); renderFilters(); render(); }
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>setMode(t.dataset.mode));
function renderFilters(){
  const all = state.mode==='all';
  const fs = all ? [['all','全部'],['multi','多变体'],['current','当前仍在'],['removed','已移除']]
                 : [['all','全部'],['added','本版新增'],['changed','本版重绘'],['kept','沿用'],['removed','本版移除']];
  $('#filters').innerHTML = fs.map(([k,l])=>`<button class="chip${state.filter===k?' active':''}" data-f="${k}">${l}</button>`).join('');
  document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{state.filter=b.dataset.f;state.shown=96;renderFilters();render();});
}
function renderTagFilter(){
  const sel = new Set(state.tags);
  const n = state.tags.length;
  $('#tagBtn').classList.toggle('active', n > 0);
  $('#tagBtn').setAttribute('aria-expanded', TAG_OPEN ? 'true' : 'false');
  $('#tagBtnLabel').textContent = n === 0 ? '全部' : (n === 1 ? state.tags[0] : `${n} 个`);
  $('#tagPop').classList.toggle('open', TAG_OPEN);
  $('#tagSelInfo').textContent = n ? `已选 ${n} 个 TAG（命中任一）` : '未选择 TAG（显示全部）';
  const active = $('#tagActive');
  if (n) {
    active.classList.add('show');
    active.innerHTML = `已选 TAG（按 1.7.1 使用，命中任一）：` + state.tags.map(t =>
      `<button type="button" data-tag="${esc(t)}" title="移除 ${esc(t)}">${esc(t)} ×</button>`).join('');
  } else {
    active.classList.remove('show');
    active.innerHTML = '';
  }
  const q = state.tagQ.trim().toLowerCase();
  const rows = [...TAG_COUNTS.entries()]
    .filter(([t]) => !q || t.toLowerCase().includes(q))
    .sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0]));
  $('#tagList').innerHTML = rows.length
    ? rows.map(([t,c]) => `<button type="button" class="tagchip${sel.has(t)?' active':''}" data-tag="${esc(t)}">${esc(t)}<b>${fmt(c)}</b></button>`).join('')
    : '<div class="tagnone">没有匹配的 TAG。</div>';
}
function toggleTag(t, on){
  const set = new Set(state.tags);
  if (on) set.add(t); else set.delete(t);
  state.tags = [...set].sort((a,b) => (TAG_COUNTS.get(b)||0) - (TAG_COUNTS.get(a)||0) || a.localeCompare(b));
  state.shown = 96;
  renderTagFilter();
  render();
}
function closeTagPop(){
  TAG_OPEN = false; state.tagQ = '';
  const x = $('#tagSearch'); if (x) x.value = '';
  renderTagFilter();
}
function runAt(icon, vi){ return icon.runs.find(r=>r.start<=vi && vi<=r.end); }
function snapSha(icon, vi){ const r=runAt(icon,vi); return r?r.sha:null; }
function removedAt(icon, vi){ if (runAt(icon,vi)) return null; return icon.runs.find(r=>r.end===vi-1) || null; }
function latestSha(icon){ return icon.runs[icon.runs.length-1].sha; }
function cardFoci(icon){
  if (!state.tags.length) return icon._foci;
  const seen = new Set(), out = [];
  for (const tag of state.tags) {
    for (const u of icon.uses) {
      if (u.tag === tag && !seen.has(u.fid)) { seen.add(u.fid); out.push(u); }
    }
  }
  return out;
}

function filtered(){
  const q = state.q.trim().toLowerCase(), vi = state.vi, all = state.mode==='all';
  let arr = ICONS.filter(i => {
    if (all) {
      if (state.filter==='multi' && i.variants<2) return false;
      if (state.filter==='current' && !i.current) return false;
      if (state.filter==='removed' && i.current) return false;
    } else if (state.filter==='removed') {
      if (!removedAt(i,vi)) return false;
    } else {
      const r = runAt(i,vi);
      if (!r) return false;
      if (state.filter==='added' && i.first!==vi) return false;
      if (state.filter==='changed' && !(i.first!==vi && r.start===vi)) return false;
      if (state.filter==='kept' && (i.first===vi || r.start===vi)) return false;
    }
    if (q && !i._s.includes(q)) return false;
    if (state.tags.length && !i.tags.some(t => state.tags.includes(t))) return false;
    return true;
  });
  const nf = i => cardFoci(i).length;
  arr.sort((a,b)=> all ? (state.tags.length ? (nf(b)-nf(a)) : ((nf(b)>0?1:0)-(nf(a)>0?1:0))) || a.first-b.first || a.name.localeCompare(b.name) : (a.name.localeCompare(b.name)));
  if (!all && state.filter!=='removed') {
    const rank = i => { const r=runAt(i,vi); return !r ? 3 : (i.first===vi ? 1 : (r.start===vi ? 0 : 2)); };
    arr.sort((a,b)=>rank(a)-rank(b) || a.name.localeCompare(b.name));
  }
  return arr;
}

function render(){
  const arr = filtered(), slice = arr.slice(0, state.shown);
  const kind = DATA === IDEAS ? '民族精神' : '国策';
  $('#resultCount').textContent = `${state.mode==='all'?'全量演变':V[state.vi].ver+' 快照'} · ${fmt(arr.length)} 枚图标`;
  const tagHint = state.tags.length ? `；TAG 筛选：${state.tags.join(' / ')}（按 1.7.1 使用，任一）` : '';
  $('#resultHint').textContent = (state.mode==='all'
    ? `每张卡用最后一版画面；中文${kind}名优先展示，角标 ×N 表示共有 N 个不同画面，点开看完整历史`
    : `正在查看 ${V[state.vi].ver} 的图标；点开可看它此前/此后的版本`) + tagHint;
  $('#moreBtn').style.display = arr.length > state.shown ? '' : 'none';
  $('#moreBtn').textContent = `加载更多（剩余 ${fmt(Math.max(0,arr.length-state.shown))}）`;
  if (!slice.length) { $('#gallery').innerHTML = state.tags.length && state.mode==='snapshot' ? '<div class="empty">当前 TAG 筛选基于 1.7.1 的使用情况；这个旧版本里可能没有仍在使用这些 TAG 的图标。试试切回“全量演变”，或清除 TAG 筛选。</div>' : '<div class="empty">没有匹配的图标。试试清空搜索，或切换筛选。</div>'; return; }
  $('#gallery').innerHTML = slice.map(i => {
    const sha = state.mode==='all' ? latestSha(i) : (snapSha(i,state.vi) || (removedAt(i,state.vi)||{}).sha);
    let cls = '', label='';
    if (state.mode==='snapshot') {
      const r = runAt(i,state.vi);
      if (i.first===state.vi) { cls='changed'; label='新增'; }
      else if (r && r.start===state.vi) { cls='changed'; label='重绘'; }
    } else if (!i.current) { cls='removed'; label='已移除'; }
    if (state.mode==='snapshot' && state.filter==='removed') { cls='removed'; label='本版移除'; }
    const foci = cardFoci(i), f1 = foci[0], f2 = foci[1], nf = foci.length;
    const matched = [...new Set(foci.map(u=>u.tag))];
    const badge = u => state.tags.length ? `<span class="ftag">${esc(u.tag)}</span>` : '';
    const focusBlock = f1
      ? `<div class="fzh">${badge(f1)}${esc(f1.zh || f1.en)}</div>${f2?`<div class="fzh second">${badge(f2)}${esc(f2.zh || f2.en)}</div>`:''}
         <div class="fen">${esc(f1.en)}</div>
         <div class="fcnt">${nf>2?`等 ${fmt(nf)} 个${kind}`:`${fmt(nf)} 个${kind}`} · ${state.tags.length ? esc(matched.join(' / ')) : fmt(i.tags.length)+' 个 TAG'}</div>`
      : `<div class="fzh none">${i.current?`1.7.1 未被${kind}引用`:(state.mode==='snapshot'?'本版存在 · 1.7.1 未引用':'已移除 · 无 1.7.1 引用')}</div>`;
    return `<article class="card" data-path="${esc(i.path)}" tabindex="0">
      <div class="art"><img loading="lazy" decoding="async" src="evo_thumbs/${sha}.webp" alt="${esc(i.name)}">
      ${label?`<span class="state ${cls}">${label}</span>`:''}${i.variants>1?`<span class="vbadge">×${i.variants}</span>`:''}</div>
      <div class="body">${focusBlock}<h3>${esc(i.name)}</h3><div class="file">${esc(i.file)}</div>
      <div class="tags">${i.tags.slice(0,4).map(t=>`<span data-tag="${esc(t)}" title="按 ${esc(t)} 筛选">${esc(t)}</span>`).join('')}${i.tags.length>4?`<span class="tagmore">+${i.tags.length-4}</span>`:''}</div>
      <div class="meta"><span>首次 <b>${V[i.first].ver}</b></span><span>最后 <b>${V[i.last].ver}</b></span></div></div></article>`;
  }).join('');
  document.querySelectorAll('.card').forEach(c=>{
    c.onclick = ()=>openModal(c.dataset.path);
    c.onkeydown = e=>{ if(e.key==='Enter'||e.key===' '){e.preventDefault();openModal(c.dataset.path);} };
  });
  document.querySelectorAll('.card .tags [data-tag]').forEach(t=>{
    t.onclick = e=>{
      e.stopPropagation();
      toggleTag(t.dataset.tag, true);
      document.querySelector('.toolbar').scrollIntoView({behavior:'smooth',block:'start'});
    };
  });
}

$('#moreBtn').onclick = ()=>{ state.shown += 96; render(); };
$('#search').oninput = e=>{ state.q=e.target.value; state.shown=96; render(); };
$('#tagBtn').onclick = e=>{
  e.stopPropagation();
  if (TAG_OPEN) { closeTagPop(); return; }
  TAG_OPEN = true;
  renderTagFilter();
  setTimeout(()=>{ const x=$('#tagSearch'); if(x) x.focus(); }, 0);
};
$('#tagSearch').oninput = e=>{ state.tagQ=e.target.value; renderTagFilter(); };
$('#tagSearch').onkeydown = e=>{ if(e.key==='Escape') closeTagPop(); };
$('#tagClear').onclick = ()=>{
  state.tags=[]; state.tagQ=''; state.shown=96;
  const x=$('#tagSearch'); if(x) x.value='';
  renderTagFilter(); render();
};
$('#tagDone').onclick = closeTagPop;
$('#tagList').onclick = e=>{
  const b=e.target.closest('[data-tag]'); if(!b) return;
  toggleTag(b.dataset.tag, !state.tags.includes(b.dataset.tag));
};
$('#tagActive').onclick = e=>{
  const b=e.target.closest('[data-tag]'); if(!b) return;
  toggleTag(b.dataset.tag, false);
};
document.addEventListener('click', e=>{
  const inFilter = e.composedPath().some(n => n.classList && n.classList.contains('tag-filter'));
  if(TAG_OPEN && !inFilter) closeTagPop();
});
$('#timeline').onclick = e=>{
  const b=e.target.closest('.ver'); if(!b) return;
  state.vi = +b.dataset.i; state.mode='snapshot'; state.filter='all'; state.shown=96;
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.mode==='snapshot'));
  document.querySelectorAll('.ver').forEach(x=>x.classList.toggle('active',+x.dataset.i===state.vi));
  renderFilters(); render();
  document.querySelector('.toolbar').scrollIntoView({behavior:'smooth',block:'start'});
};

function openModal(path){
  const i = byPath.get(path); if(!i) return;
  const kind = DATA === IDEAS ? '民族精神' : '国策';
  $('#mTitle').textContent = i.name;
  $('#mSub').textContent = `${i.file} · 首次 ${V[i.first].ver} · 最后 ${V[i.last].ver} · ${i.variants} 个不同画面 · ${i.runs.length} 段`;
  $('#mHistory').innerHTML = i.runs.map((r,n)=>{
    const lab = r.start===r.end ? V[r.start].ver : `${V[r.start].ver} → ${V[r.end].ver}`;
    const sub = n===0 ? '初版' : (r.start>i.runs[n-1].end+1 ? '重新出现' : '重绘');
    return `<div class="hist"><img loading="lazy" src="evo_thumbs/${r.sha}.webp" alt=""><div class="hl">${esc(lab)}</div><div class="hs">${sub}</div></div>`;
  }).join('');
  const uses = state.tags.length ? i.uses.filter(u => state.tags.includes(u.tag)) : i.uses;
  if (uses.length) {
    $('#mUseTitle').textContent = state.tags.length
      ? `1.7.1 中 ${state.tags.join(' / ')} 使用它的${kind}（${uses.length} 条）`
      : `1.7.1 中还在使用它的${kind}（${uses.length} 条 · ${i.tags.length} 个 TAG）`;
    $('#mUses').innerHTML = `<table><thead><tr><th>TAG</th><th>${kind}</th><th>ID</th></tr></thead><tbody>` +
      uses.map(u=>`<tr><td class="tag">${esc(u.tag)}</td><td>${u.zh?esc(u.zh)+'<br><span style="color:#8b8170;font-size:10.5px">'+esc(u.en)+'</span>':esc(u.en)}</td><td class="id">${esc(u.fid)}</td></tr>`).join('') +
      `</tbody></table>`;
    $('#mNote').textContent = state.tags.length
      ? `已按 TAG：${state.tags.join(' / ')} 筛选；清除 TAG 筛选可查看全部使用情况。中文名优先采用 KR 1.7.1 官方简中译名，缺失时回退机翻；保留英文原名核对。`
      : `中文名优先采用 KR 1.7.1 官方简中译名，缺失时回退机翻；保留英文原名核对。同一${kind}可能因多个 TAG 共享而出现多行。`;
  } else {
    $('#mUseTitle').textContent = i.current ? '1.7.1 中的使用情况' : '已移除';
    $('#mUses').innerHTML = `<div class="empty" style="padding:22px">${i.current ? `1.7.1 的${kind}文件中没有引用这枚图标（可能是预留素材）。` : '这枚图标在 1.7.1 已不存在；最后一次出现在 '+V[i.last].ver+'。'}</div>`;
    $('#mNote').textContent = '';
  }
  $('#modal').classList.add('open'); $('#modal').setAttribute('aria-hidden','false');
}
function closeModal(){ $('#modal').classList.remove('open'); $('#modal').setAttribute('aria-hidden','true'); }
$('#mClose').onclick = closeModal;
$('#modal').onclick = e=>{ if(e.target.id==='modal') closeModal(); };
document.addEventListener('keydown', e=>{ if(e.key==='Escape'){ if(TAG_OPEN) closeTagPop(); closeModal(); } });

function scrollTimeline(){
  requestAnimationFrame(()=>{
    const tw=document.querySelector('.timeline-wrap'), a=document.querySelector('.ver.active');
    if(tw&&a) tw.scrollLeft = Math.max(0, a.offsetLeft - tw.clientWidth/2);
  });
}
function setType(t, center=true){
  DATA = t === 'ideas' ? IDEAS : GOALS;
  V = DATA.versions; ICONS = DATA.icons;
  byPath = new Map(ICONS.map(i => [i.path, i]));
  state = {mode:'all', vi:V.length-1, filter:'all', q:'', shown:96, tags:[], tagQ:''};
  TAG_OPEN = false;
  document.querySelectorAll('.type').forEach(b=>b.classList.toggle('active', b.dataset.type===t));
  document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('active', b.dataset.mode==='all'));
  const si = document.querySelector('#search'); if(si) si.value='';
  const tsi = document.querySelector('#tagSearch'); if(tsi) tsi.value='';
  if (t === 'ideas') {
    document.title = '民族精神图标的演变 · Kaiserreich 0.11 → 1.7.1';
    $('#heroTitle').innerHTML = '民族精神的<em>演变</em>';
    $('#heroLede').innerHTML = '从 <b>0.11 漫漫归途</b> 到 <b>1.7.1</b>：<b>100 个 GitHub 版本</b>里每一枚 <code>gfx/interface/ideas</code> 图标的出现、重绘与消失。卡片标出使用它的<b>中文民族精神名</b>（官方简中优先）与 TAG，点开可看完整视觉史。';
  } else {
    document.title = '国策图标的演变 · Kaiserreich 0.11 → 1.7.1';
    $('#heroTitle').innerHTML = '国策图标的<em>演变</em>';
    $('#heroLede').innerHTML = '从 <b>0.11 漫漫归途</b> 到 <b>1.7.1</b>：<b>100 个 GitHub 版本</b>里每一枚 <code>gfx/interface/goals</code> 图标的出现、重绘与消失。浅色时间轴版，卡片直接标出使用它的<b>中文国策名</b>（官方简中优先），点开可看完整视觉史与全部使用国策。';
  }
  renderStats(); renderTimeline(); renderChart(); renderFilters();
  buildTagCounts(); renderTagFilter(); render();
  document.querySelectorAll('.ver').forEach(x=>x.classList.toggle('active',+x.dataset.i===state.vi));
  if(center) scrollTimeline(); else requestAnimationFrame(()=>{const tw=document.querySelector('.timeline-wrap'); if(tw) tw.scrollLeft=0;});
}
document.querySelectorAll('.type').forEach(b=>b.onclick=()=>setType(b.dataset.type, false));
setType('goals', false);
</script>
</body></html>'''

html = html.replace('__DATA_JSON__', json_js).replace('__IDEAS_JSON__', json_ideas)
open('kaiserreich_evolution.html', 'w', encoding='utf-8').write(html)
print('wrote html', os.path.getsize('kaiserreich_evolution.html'))

