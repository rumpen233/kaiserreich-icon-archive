# 构建脚本说明

页面是纯静态 HTML，构建分成「抓取 → 解析/建库 → 渲染」三段。

## 主要脚本

| 脚本 | 作用 |
| --- | --- |
| `evo_fetch_trees.py` / `evo_fetch_trees_par.py` | 按 tag 抓取 GitHub 递归 tree |
| `evo_fetch_gfx.py` | 抓取各版本 `interface/**/goals.gfx`、`ideas*.gfx` |
| `evo_download.py` / `evo_download_ideas.py` | 按画面 SHA 下载 goals / ideas 原始素材 |
| `evo_build.py` | 建立 goals 的版本/画面/使用关系，输出 `evo_data.json` |
| `build_ideas.py` | 建立 ideas 的版本/画面/使用关系，输出 `evo_ideas_data.json` |
| `evo_render2.py` | 读取两份数据和缩略图，生成 `index.html` |
| `idea_parse.py` / `idea_map.py` | 解析 idea 定义并匹配 `GFX_idea_*` |
| `parse_zh.py` | 解析官方简中 yml，生成 `loc_zh_all.json` |
| `make_versions_all.py` | 生成 100 个版本的 `versions_all.json` |

## 输入目录约定

脚本默认在项目根目录运行，并读取：

```
evo/tags.json
evo/versions_all.json
evo/trees/<safe_tag>.json
evo/gfx/<safe_tag>.gfx
evo/raw/<sha>.png|.tga
evo_thumbs/<sha>.webp
focusmap_1.7.1.json
loc_en.json
loc_zh_all.json
trans.json
trans_ideas_merged.json
idea_manual.json
```

这些中间文件体积较大，没有全部上传到仓库。`data/` 中保留了最终建库结果，因此只改页面样式或文案时，可以直接改 `evo_render2.py` 后重新渲染，不必重新抓取。

## 渲染

```powershell
python evo_render2.py
```

输出文件名为 `kaiserreich_evolution.html`；发布到 GitHub Pages 时可重命名为 `index.html`。

## 说明

- 0.11–0.17 是 `.tga`，0.18 起是 `.png`
- 早期 goals 的 gfx 定义文件是 `interface/KR_goals.gfx`，不是 `interface/kaiserreich/goals.gfx`
- ideas 以 **basename stem** 合并旧国家目录中的重复素材
- 官方简中只覆盖 1.7.1；老版本已移除条目没有官方译名
