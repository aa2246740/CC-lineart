# CC-lineart · 手绘线稿与水彩全场景设计系统（中文完整版）

<p align="center">
  <a href="README.md">🇺🇸/🇨🇳 Bilingual README (中英对照主文档)</a> ·
  <a href="SKILL.md">🤖 智能体技能入口 (SKILL.md)</a> ·
  <a href="references/art-direction.md">🎨 艺术指导规范</a> ·
  <a href="references/drawing-guide.md">📐 绘图与缩放指南</a>
</p>

**CC-lineart** 是一套面向 AI 编程智能体的**手绘 `#141413` 炭黑墨水线稿 + `#FAF9F5` 暖白剪纸填充 + 斑驳水彩块 SVG 与网页全场景设计系统**，灵感源自 `claude.com` 富有纸张温度与人文气息的插画风格。

它最初用于为项目绘制 `64×64` 侧边栏图标；但由于其核心路径生成器（`handify`、`wobbly_circle`、`sparkle`）、水彩与墨水置换滤镜（`#wash`、`#ink`）以及自动化风格质检工具（`scripts/lineart.py lint`）完全确定性且与分辨率无关，智能体可以直接用它来构建**项目图标、AI 产品 Hero 落地页、精品插画商城（市集页）、触感 UI 组件库、空状态插画、系统架构与多智能体拓扑图、杂志感数据可视化图表、开源仓库品牌头图与火漆徽章，以及基于 `pathLength="1"` 的一笔画自绘动效与演示幻灯片**。

<p align="center"><img src="docs/hero.png" width="840" alt="CC-lineart Hero"></p>

---

## 为什么选择 CC-lineart？（三层物理空间隐喻）

大多数 AI 直接生成的 SVG 或网页往往带有强烈的“廉价模板感”：尺规般笔直的 `<rect>` 矩形、完全镜像对称的几何图元、极易失效的外部占位图片链接（Unsplash），以及所有元素平铺在同一个平面上的单调感。

每一件 `CC-lineart` 作品都严格按照自下而上的**三层物理结构**构建：

1. **第一层 — 偏置水彩渲染块 (`<g id="layer-block">`)**  
   由 1～2 个不规则四边形构成的冷暖品牌水彩块（`clay` 陶土红、`sky` 天青蓝、`cactus` 鼠尾草绿、`heather` 薰衣草灰、`plum` 深紫、`mineral` 矿物青、`peach` 杏桃粉、`kraft` 牛皮纸赭石、`olive` 橄榄绿），中心相对主体偏移 `10%–25%`，绝不死板居中。分形噪声滤镜（`#wash`）赋予其水彩渗透纸背的斑驳感，`55%` 不透明度的深色描边模拟水彩干涸时的边缘积水。在大画布（`>= 256px`）上，将一暖一冷两块水彩置于 `isolation: isolate` 组内并以 `mix-blend-mode: multiply` 正片叠底，可自然罩染出丰富的第三色调。
2. **第二层 — 暖白剪纸遮罩层 (`#FAF9F5` / `{PAPER}`)**  
   主体的闭合轮廓填充暖白纸张色 `#FAF9F5`，覆盖在水彩块与后景辅助线之上，同时确保 **≥ 30% 的水彩块外露可见**，并让 **≥ 20% 的线条破出（Break out）水彩边界延伸至留白纸面**。
3. **第三层 — 手绘炭黑钢笔墨线 (`<g id="layer-ink">`, `#141413` / `{INK}`)**  
   采用圆头端点（`stroke-linecap="round"`）与圆角连接，所有直线均通过 `handify()` 转化为带有微弧度的手绘贝塞尔曲线，转角处保留建筑草图式的出锋交叉（`--overshoot`），配合多级线宽层次（主轮廓、内部结构、装饰点缀）与聚拢的不等长星芒（`sparkle`）。

---

## 适用范围与 8 大核心应用场景

> 仓库内全部 12 幅代表性 SVG 作品均通过 `python3 -I scripts/lineart.py lint` 自动化检查（**0 警告**）。

| # | 场景名称 | 适用范围与解决的核心痛点 | 关键工程范式 | 示例与评估目录 |
| :- | :--- | :--- | :--- | :--- |
| **1** | **项目与侧边栏图标 (`64×64`)** | IDE / T3 Code 项目侧边栏图标、CLI 工具图标、分类小角标（支持 `lg` 48px+ 与 `sm` 14–28px 双预设） | 单水彩块偏置 + 暖白剪纸主体 + 28px 缩略图防糊死孔洞检测 | [`motifs/`](motifs/) · [`scripts/lineart.py`](scripts/lineart.py) |
| **2** | **AI 产品 Hero 落地页与主页** | 解决 AI 写网页千篇一律“深色紫光渐变 + 空洞占位图”痛点；适用于 SaaS/AI 工具主页、Bento 特性区、定价区 | 分栏 Hero + `pathLength="1"` 一笔画自绘主视觉 + 水彩主题实时切换 + Bento 悬停水彩视差 + 火漆印章定价卡 | [`examples/pages-hero/`](examples/pages-hero/) · [`EVALUATION.md`](examples/pages-hero/EVALUATION.md) |
| **3** | **精品插画商城与创作者市集页** | 解决 AI 写商城页“没有商品实拍图、白盒卡片无质感”痛点；适用于文创周边店、数字技能包市集、独立商店 | 每个 SKU 专属手绘矢量商品插画 + 倾斜打孔吊牌价签（`$42`）+ 印章角标 + 含手绘空袋插画的实时购物车 | [`examples/pages-storefront/`](examples/pages-storefront/) · [`EVALUATION.md`](examples/pages-storefront/EVALUATION.md) |
| **4** | **触感 UI 组件库与空状态插画** | 零收件箱/空状态面板、新手引导卡、`⌘K` 搜索框、拨杆开关、通知卡片与可交互 Web 工作台 | 页面级共享零尺寸 SVG `<defs>` 滤镜池（`#ui-wash`、`#ui-ink`）+ `vector-effect="non-scaling-stroke"` | [`examples/ui-kit/`](examples/ui-kit/) · [`EVALUATION.md`](examples/ui-kit/EVALUATION.md) |
| **5** | **系统架构与多智能体工作流图** | 技术博客架构图、RFC 拓扑图、多智能体分发与聚合流程、RAG 向量检索流水线 | 冷暖水彩叠色划分逻辑域（告别生硬虚线框）+ 微缩图形符号替代 `<text>` + 穿过卡片背后的 S 形总线 | [`examples/diagrams/`](examples/diagrams/) · [`EVALUATION.md`](examples/diagrams/EVALUATION.md) |
| **6** | **杂志感数据可视化与跑分图表** | 模型发布跑分对比柱状图、能力演进曲线、遥测 KPI 仪表盘与微趋势卡片 | 分级 `handify` 抖动系数（刻度 `1.6`、柱体 `2.8`、曲线 `3.5`、水彩 `5.5`），兼顾手绘温度与数据精度 | [`examples/dataviz/`](examples/dataviz/) · [`EVALUATION.md`](examples/dataviz/EVALUATION.md) |
| **7** | **开源仓库品牌头图与火漆徽章** | GitHub README 顶部 Banner、社交分享卡片、版本发布横幅（`v2.0`）、火漆认证印章 | 中心线双描边剪纸字技法（先画全套 `W + 2t` 粗墨骨，再叠全套 `W` 暖白内芯，交叉处无缝融合） | [`examples/branding/`](examples/branding/) · [`EVALUATION.md`](examples/branding/EVALUATION.md) |
| **8** | **一笔画自绘动效与演示幻灯片** | Keynote / HTML 演示文稿主视觉、三幕式叙事插画、动态书写开场动画 | `pathLength="1"` + `data-step` 顺序落笔动画 + `{PAPER}` 剪纸延迟浮现 + 100% 兼容静态 PNG/PDF 导出 | [`examples/motion-and-slides/`](examples/motion-and-slides/) · [`EVALUATION.md`](examples/motion-and-slides/EVALUATION.md) |

---

## 快速安装与 CLI 常用命令

```bash
# macOS 安装渲染与质检依赖
brew install librsvg imagemagick && pip install Pillow

# Debian / Ubuntu 安装依赖
sudo apt-get install librsvg2-bin imagemagick && pip install Pillow
```

```bash
# 查看内置图标与色板
python3 -I scripts/lineart.py list
python3 -I scripts/lineart.py palette

# 渲染图标（lg 适合 48px+，sm 适合 14-28px 侧边栏）
python3 -I scripts/lineart.py render mac -o out/mac.svg --size lg
python3 -I scripts/lineart.py render mac -o out/mac-sm.svg --size sm --color sky

# 运行机械 + 光栅双重风格质检
python3 -I scripts/lineart.py lint out/mac.svg

# 一键重新生成全部 7 大拓展场景（含 Hero 落地页与精品商城页）
python3 -I examples/pages-hero/generate_hero_page.py
python3 -I examples/pages-storefront/generate_storefront.py
python3 -I examples/ui-kit/generate_ui_kit.py
python3 -I examples/diagrams/generate_diagrams.py
python3 -I examples/dataviz/generate_dataviz.py
python3 -I examples/branding/generate_branding.py
python3 -I examples/motion-and-slides/generate_motion_slides.py
```
