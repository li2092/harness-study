# 第二卷 PDF 构建管线

沿用入门卷管线（`Agent-Z/docs/learn-harness/explainers/what-is-harness/v0.4/pdf-build/`），同一套视觉语言。

## 一键构建

```bash
~/.venvs/docgen/bin/python build_pdf.py
```

输出 `harness-study-运行时架构卷.pdf`。传参可改文件名：`build_pdf.py out.pdf`。

**依赖**：`pandoc`（`/opt/homebrew/bin/pandoc`）、`playwright`、`PyMuPDF(fitz)`。本机只有 `~/.venvs/docgen/bin/python` 三样齐全，**不要用系统 python3**。

## 管线两步

1. **`make_book.py`** — 逐章 pandoc → HTML 片段，拼 `book.html`（含目录 + 图目录）。同时写出 `figures.json`、`chapters.json`。
2. **`build_pdf.py`** — 两遍渲染：首遍取各章/各图页码 → 回填目录 → 次遍出正文；再合并前页（封面/题词/版权）、重建目录跳转、用 fitz 逐页绘页眉、落书签与元数据、子集化字体。

## 正文来源（SSOT）

`../`（即 `harness-study/volume2/`）。章节顺序由 `make_book.py` 的 `CHAPTERS` 显式列出——**留档旧版**（`01-architecture.md`、`01-architecture-v3.0.md`、`02-correct-runtime.md`、`03-incident.md`）与编辑文件（`SPEC.md`、`WRITING-PLAN.md`、`README.md`、`91-material-index.md`）**不入书**。

环境变量 `HARNESS_VOL2` 可覆盖正文目录（默认按 mac `~/ClaudeCode/...` → Windows `D:/ClaudeCode/...` 顺序探测）。

## 编辑区剥离（卷二特有）

正文每章带编辑工作区，出版前剥离，规则在 `make_book.py` 顶部两处，要调就改那里：

- `DROP_SECTIONS` — 整节删除：`## 审稿日志`、`## 引用来源`（正文里明写"出版前整体删除"）。
- `EDITORIAL_LINE` — 章首引用块里**按行**删除的编辑标记（版本注、`依据 SPEC`、`留档对照`、`待用户审` 等）。按行而非整块，是因为 `90-artifacts.md` / `99-appendix.md` 开头的引用块里混着给读者看的用途说明，不能整块删。

首遍构建会打印剥离报告（每章删了几行章首注、删了哪些整节），**每次改完正文都扫一眼**，防止误删或漏删。

## 配图

正文里写成图片 + 紧跟一行斜体图注，管线自动升级为 `figure` 并收进图目录：

```markdown
![](figures/5-3-state-machine.svg)

*图 5.3 · run 七状态转移图*
```

编号规则 `图 <章>.<序>`。当前正文只有 `（配图占位：…）` 文字占位、**尚无实际图片**，故图目录页不生成（有图后自动出现）。

## 字体

`fonts/` 五套 OFL 字体（67MB，gitignore 不入库）。缺失时从入门卷管线拷：

```bash
cp -R ~/ClaudeCode/Agent-Z/docs/learn-harness/explainers/what-is-harness/v0.4/pdf-build/fonts .
```
