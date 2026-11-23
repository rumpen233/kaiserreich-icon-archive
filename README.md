# Kaiserreich 国策 / 民族精神图标档案

一个非官方的静态档案，逐版本追溯 **Kaiserreich（钢铁雄心 4）** 的国策图标（goals）与民族精神图标（ideas）。

数据覆盖 GitHub 上的 **100 个 tag**：从最早的 `0.11_The_Long_Road_Home` 一直到 `1.7.1`。

**在线访问：** <https://rumpen233.github.io/kaiserreich-icon-archive/>

## 页面能做什么

- 按版本查看每个图标的视觉历史，多次重绘会以多格胶片展示
- 在「国策图标」和「民族精神」两个档案之间切换
- 按版本快照浏览：新增、重绘、沿用、本版移除
- 按 TAG 筛选；筛选后卡片和详情表会改用该 TAG 对应的国策/民族精神名称
- 搜索 GFX 名、文件名、TAG、中文名
- 中文名优先使用 1.7.1 官方简中本地化；缺失的编号变体按基础名回退，仍缺则保留机翻/英文

## 统计

| 档案 | 历史图标 | 1.7.1 当前 | 不同画面 | 已移除 |
| --- | ---: | ---: | ---: | ---: |
| 国策 goals | 4,218 | 2,747 | 5,861 | 1,471 |
| 民族精神 ideas | 2,082 | 694 | 3,540 | 1,388 |

- 0.11–0.17 的旧素材为 `.tga`，0.18 起转为 `.png`
- 早期图标名优先取当时的 `interface/KR_goals.gfx`，缺失时才回退文件名
- 民族精神只统计 `gfx/interface/ideas` 下的 PNG/TGA 自有美术，大量通用 DDS 不在本页
- TAG 使用关系基于 `1.7.1` 的国策/民族精神定义

## 目录

```
index.html          静态页面（数据已内嵌）
evo_thumbs/         9,404 张 160×141 WebP 缩略图
data/               构建后的图标、画面、使用关系数据
scripts/            抓取、解析、构建、渲染脚本
```

## 本地打开

直接双击 `index.html` 即可，页面通过相对路径读取 `evo_thumbs/`。

如果浏览器限制本地文件访问，可在项目根目录启动一个静态服务器：

```powershell
python -m http.server 8000
```

然后打开 `http://127.0.0.1:8000/`。

## 重新构建

`scripts/` 保留了主要流水线脚本，但原始素材没有全部放进仓库。完整重建需要：

1. 从 Kaiserreich 仓库按 tag 下载 `gfx/interface/goals`、`gfx/interface/ideas`、`interface/*.gfx`、`common/national_focus`、`common/ideas`
2. 生成 `evo/trees/*.json`、`evo/gfx/*.gfx`、`evo/raw/*`
3. 依次运行 `evo_build.py`、`build_ideas.py`、`evo_render2.py`

更详细的输入输出说明见 [`scripts/README.md`](scripts/README.md)。

## 数据与译名来源

- 图标与定义：GitHub 仓库 [`Kaiserreich/Kaiserreich-HOI4`](https://github.com/Kaiserreich/Kaiserreich-HOI4) 的 100 个 tag
- 官方简中译名：钢铁雄心 4 创意工坊 Kaiserreich 简中本地化 `localisation/simp_chinese`
- 1.7.1 之前的旧版本没有对应的官方简中条目；这些已移除国策不会强行套用 1.7.1 的译名

## 版权说明

这是非官方的学习/存档项目，与 Kaiserreich 开发组无关。

图标、名称与相关素材的版权归 Kaiserreich 团队及原素材作者所有；本仓库不主张对这些素材的所有权，也不将其用于商业用途。若权利人要求，可删除相关内容。
