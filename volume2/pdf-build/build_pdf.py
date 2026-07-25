#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二卷全书 PDF 一键构建：
  两遍渲染（首遍取各章页码 + 各图页码 → 回填目录/图目录）+ 前页全页填充
  + PDF 书签大纲 + 文档元数据 + 目录/图目录内部跳转链接 + fitz 逐页页眉。
用法: python build_pdf.py [out.pdf]
依赖: pandoc / playwright / PyMuPDF(fitz)。本机解释器见 README。"""
import subprocess, sys, json, pathlib, re
from playwright.sync_api import sync_playwright
import fitz

HERE = pathlib.Path(__file__).resolve().parent
PY = sys.executable
OUT = sys.argv[1] if len(sys.argv) > 1 else str(HERE / "harness-study-运行时架构卷.pdf")
BOOK = (HERE / "book.html")

FRONT = [n for n in ("cover.html", "epigraph.html", "notice.html") if (HERE / n).exists()]
FRONT_LABEL = {"cover.html": "封面", "epigraph.html": "卷首 · 题词", "notice.html": "版权 · 声明"}
FOOTER = ('<div style="font-family:\'Inter\',\'Noto Sans SC\',sans-serif;font-size:8pt;'
          'color:#9a93a6;width:100%;padding:0 14mm;text-align:center;"><span class="pageNumber"></span></div>')
HEADER = "<span></span>"  # 页眉全部改由 fitz 逐页绘制，避免双渲染器错位
BODY_MARGIN = {"top": "20mm", "bottom": "16mm", "left": "14mm", "right": "14mm"}
META = {"title": "Harness Study · Harness 运行时架构（架构与工程卷）", "author": "Jinming Li",
        "subject": "语义正确、可中断、可恢复、可验证的 Agent Harness runtime 怎么造",
        "creator": "Harness Study build pipeline",
        "keywords": "harness, agent, LLM, 智能体, runtime, 运行时架构, durable execution, agent harness"}

def launch(p):
    for ch in ("msedge", "chrome"):
        try:
            return p.chromium.launch(channel=ch)
        except Exception:
            continue
    return p.chromium.launch()

def ready(pg, wait=1800):
    try:
        pg.evaluate("async () => { await document.fonts.ready; }")
    except Exception:
        pass
    pg.wait_for_timeout(wait)

def make_book(pages_json=None, figpages_json=None):
    cmd = [PY, str(HERE / "make_book.py")]
    if pages_json:
        cmd += ["--pages", pages_json]
    if figpages_json:
        cmd += ["--figpages", figpages_json]
    subprocess.run(cmd, check=True)

def render_body(pg, path):
    pg.goto(BOOK.resolve().as_uri(), wait_until="networkidle", timeout=180000)
    ready(pg, 2500)
    pg.pdf(path=path, format="A4", print_background=True, outline=True, tagged=True,
           display_header_footer=True, header_template=HEADER, footer_template=FOOTER, margin=BODY_MARGIN)

make_book()  # 首遍：目录/图目录无页码
body1 = str(HERE / "_body1.pdf")
body2 = str(HERE / "_body2.pdf")
front_pdfs = []
with sync_playwright() as p:
    b = launch(p)
    pg = b.new_page(); render_body(pg, body1); pg.close()

    d1 = fitz.open(body1)
    _ch1 = [(t, n) for (lvl, t, n) in d1.get_toc(simple=True) if lvl == 1]
    chap_pages = [n for (t, n) in _ch1]
    chap_titles = [t for (t, n) in _ch1]
    figs = json.loads((HERE / "figures.json").read_text(encoding="utf-8"))
    texts = [d1[i].get_text("text") for i in range(d1.page_count)]
    figpages = {}  # fig_id -> 正文页码(1-based)
    body_start = chap_pages[0] if chap_pages else 1  # 跳过 TOC/图目录页（它们也含「图 N.M」文本）
    for fg in figs:
        pat = re.compile("图\\s*" + re.escape(fg["num"]) + "\\s*·")
        for i in range(body_start - 1, len(texts)):
            if pat.search(texts[i]):
                figpages[fg["id"]] = i + 1
                break
    pj = str(HERE / "_pages.json"); pathlib.Path(pj).write_text(json.dumps(chap_pages), encoding="utf-8")
    fpj = str(HERE / "_figpages.json"); pathlib.Path(fpj).write_text(json.dumps(figpages), encoding="utf-8")

    make_book(pj, fpj)  # 次遍：目录 + 图目录带页码
    pg = b.new_page(); render_body(pg, body2); pg.close()

    for name in FRONT:  # 前页全页填充
        pg = b.new_page()
        pg.goto((HERE / name).resolve().as_uri(), wait_until="networkidle", timeout=40000)
        ready(pg, 1400)
        fp = str(HERE / ("_fm_" + name + ".pdf"))
        pg.pdf(path=fp, prefer_css_page_size=True, print_background=True,
               margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        pg.close(); front_pdfs.append(fp)
    b.close()

# 合并 + 大纲（前页偏移）+ 元数据
doc = fitz.open(front_pdfs[0])
for fp in front_pdfs[1:]:
    doc.insert_pdf(fitz.open(fp))
nfront = len(front_pdfs)
doc.insert_pdf(fitz.open(body2))

# 修复目录/图目录跳转：Chromium 命名目标(LINK_NAMED)被 fitz 合并丢弃——按页码重建显式 GOTO
chno_re = re.compile(r"ch(\d+)$")
b2 = fitz.open(body2)
for src in range(b2.page_count):
    rel = []  # (link, 正文页码)
    for lk in b2[src].get_links():
        nd = lk.get("nameddest", "")
        m = chno_re.match(nd)
        if m and 1 <= int(m.group(1)) <= len(chap_pages):
            rel.append((lk, chap_pages[int(m.group(1)) - 1]))
        elif nd in figpages:
            rel.append((lk, figpages[nd]))
    if not rel:
        continue
    dst = doc[nfront + src]
    for lk in list(dst.get_links()):
        dst.delete_link(lk)
    for lk, bp in rel:
        dst.insert_link({"kind": fitz.LINK_GOTO, "from": lk["from"],
                         "page": bp - 1 + nfront, "to": fitz.Point(0, 0)})

# 页眉：左=当前章节、右=书名，同基线对齐 + 下方紫色渐变线（全 fitz 绘制，单渲染器保证对齐）
NOTOSC = str(HERE / "fonts" / "NotoSansSC.ttf")  # OFL 中文无衬线
YFONT = fitz.Font(fontfile=NOTOSC)
HDR_RGB = (0x6b / 255, 0x64 / 255, 0x78 / 255)   # --t3 灰
BOOK_TITLE = "Harness Study · 运行时架构"
GRAD_A = (0x6d / 255, 0x28 / 255, 0xd9 / 255)     # --purple
GRAD_B = (0x8b / 255, 0x5c / 255, 0xf6 / 255)     # --purple-soft
HX0, HX1, HSIZE = 40.0, 555.0, 7.5                # 页眉左右边界 + 字号
HY, LINE_Y = 32.0, 41.0                           # 文字基线 + 渐变线 y
def _chap_label(t):
    s = t.split("·")[0].strip()  # 去掉「· 副标题」尾巴，留章名
    s = re.sub(r"（[^）]*）\s*$", "", s).strip()  # 去掉结尾「（年份/注释）」
    w, buf = 0, []  # 按显示宽度截断：CJK 记 2、拉丁记 1
    for c in s:
        cw = 2 if ord(c) > 0x2E80 else 1
        if w + cw > 42:
            buf.append("…"); break
        buf.append(c); w += cw
    return "".join(buf)
def _grad_line(pg, x0, x1, y, h=1.3, n=96):
    seg = (x1 - x0) / n
    for i in range(n):
        f = i / (n - 1)
        col = tuple(GRAD_A[j] + (GRAD_B[j] - GRAD_A[j]) * f for j in range(3))
        pg.draw_rect(fitz.Rect(x0 + i * seg, y, x0 + (i + 1) * seg + 0.6, y + h),
                     color=col, fill=col, width=0)
if chap_pages:
    for src in range(b2.page_count):
        bp = src + 1
        if bp < chap_pages[0]:
            continue  # 目录 / 图目录页不画
        k = 0
        for idx, sp in enumerate(chap_pages):
            if sp <= bp:
                k = idx
            else:
                break
        if bp == chap_pages[k]:
            continue  # 章首页不画运行页眉
        pg = doc[nfront + src]
        pg.insert_text(fitz.Point(HX0, HY), _chap_label(chap_titles[k]),
                       fontfile=NOTOSC, fontname="notosc", fontsize=HSIZE, color=HDR_RGB)
        tw = YFONT.text_length(BOOK_TITLE, fontsize=HSIZE)  # 右对齐：右边界减文字宽
        pg.insert_text(fitz.Point(HX1 - tw, HY), BOOK_TITLE,
                       fontfile=NOTOSC, fontname="notosc", fontsize=HSIZE, color=HDR_RGB)
        _grad_line(pg, HX0, HX1, LINE_Y)

toc = [[1, FRONT_LABEL.get(n, n), i + 1] for i, n in enumerate(FRONT)]
toc.append([1, "目录", nfront + 1])
if figpages:  # 正文暂无配图时不出图目录页，书签也不加
    toc.append([1, "图目录", nfront + 2])
# L1 章级书签用 make_book 落的精简标题，与印刷目录一致；L2/L3 子节原样
clean_titles = json.loads((HERE / "chapters.json").read_text(encoding="utf-8"))
ci = 0
for lvl, title, page in fitz.open(body2).get_toc(simple=True):
    if lvl == 1:
        if ci < len(clean_titles):
            title = clean_titles[ci]
        ci += 1
    toc.append([lvl, title, page + nfront])
doc.set_toc(toc)
doc.set_metadata(META)
try:
    doc.subset_fonts(verbose=False)  # 子集化嵌入字体，大幅瘦身
except Exception as e:
    print("subset_fonts skipped:", e)
doc.save(OUT, garbage=4, deflate=True)
print("OK ->", OUT, "| pages:", doc.page_count, "| figures:", len(figpages), "| bookmarks:", len(toc))
