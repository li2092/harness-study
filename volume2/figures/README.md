# 第二卷配图

出图工单见 [`PLAN.md`](./PLAN.md)（Tier 1 十六张 / Tier 2 十三张、跨章分工、图文一致性纠错、待裁决项）。

## 出一张图

```bash
# 1. 复制一张同图型的现成图当骨架
cp t1-flow-5.2-run-states.html t1-<型>-<节>-<slug>.html
# 2. 改内容（信息点须对得上 PLAN 里登记的行号）
# 3. 渲染
~/.venvs/docgen/bin/python _render.py t1-<型>-<节>-<slug>.html t1-<型>-<节>-<slug>.png
```

`_render.py` 走系统 Chrome，3x DPI，截 `.canvas` 元素。**依赖 `~/.venvs/docgen/bin/python`**（带 playwright），不要用系统 python3。

## 命名

`t<层>-<图型>-<节号>-<slug>`。层＝ `t1` Tier 1 / `t2` Tier 2；图型取 PLAN 的九种之一（`matrix` `flow` `sequence` `layered` `cardgrid` `comparison` `timeline` `tree` `analogy`）。

## 样板（已定调，新图照抄结构）

| 文件 | 图型 | 定调了什么 |
|---|---|---|
| `t1-matrix-1.5-contract-grid` | `matrix` | 纯 HTML 表格型：表头承载主场章、格内留空表达"空格本身是发现"、底部延伸带 |
| `t1-flow-5.2-run-states` | `flow` | 内联 SVG 状态机：节点＋编号边＋外挂图例表，"有意不设"的非边做成自足小示意、不画进主图 |
| `t1-sequence-3.4-ten-frames` | `sequence` | 内联 SVG 泳道：横轴帧、纵轴载体、两条轨迹叠加、缺口锚点与缺失证据带 |

## 视觉

`_base.css` 是 jimi-ink 公共底（暖石底 `#f4f0eb` ／ 淡紫网格 ／ 紫 `#6d28d9`），**与正文 PDF 同一套色板**。字体走 `../pdf-build/fonts/` 本地 OFL 文件，不依赖 CDN。

画布固定 1320px 宽。每张图自带 `<style>` 写自己的布局，`_base.css` 只管外壳（canvas／grid-bg／label-type／h1／sub／rule／foot）。

## 硬约束

- **成品有效宽度上限 182mm**（A4 版心）。超宽会触发 Chromium 打印缩放、把整本书等比缩小——第二卷已因宽表踩过一次（正文 14pt 被渲成 9.3pt）。按 1320px 画布出图，印刷宽定 182mm，高度换算：`高(mm) = 图高px / 图宽px × 182`。三张样板分别是 136mm ／ 169mm ／ 168mm，单页放得下。
- **信息忠于原文**。每个信息点要能在正文指出行号，见 PLAN 各条的"信息点"。图文不符是入门卷上一版翻车的原因。
- **脱敏**：三个匿名系统是三个不同项目，不得混为一谈——配套实现项目（Rust harness）／桌面案例项目（TypeScript 桌面 agent）／配套中继服务（TS relay）。公开产品照实具名。

## 接进正文

正文写图片 ＋ 紧跟一行斜体图注，`pdf-build/make_book.py` 自动升级为带编号的 figure 并生成图目录页：

```markdown
![](figures/t1-flow-5.2-run-states.png)

*图 5.2 · run 的七个状态：卡在 running 不是状态，是缺陷*
```

编号规则 `图 <章>.<序>`。图接进正文后，同步删掉该处的 `（配图占位：…）`，并把这一行补进 `99-appendix.md` 第五节图表清单。
