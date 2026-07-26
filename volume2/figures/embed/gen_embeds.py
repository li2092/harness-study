#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二卷正文表格 -> jimi-ink 风格 PNG 嵌入图（无图号，不进图目录）。

用法:
  python gen_embeds.py extract   # 一次性：从章节 md 抽表 -> sources.md + html + png + 回写 md
  python gen_embeds.py regen     # 日常：从 sources.md 再生成 html + png（正文 md 不动）

规则:
  - 编辑区（审稿日志/引用来源/变更记录，出版时 strip_editorial 剥离）里的表格不抽取，保留 md 原表。
  - 超高表（canvas 高 > MAX_H px，超出 A4 单页可容高度）按行拆成多张续图，每张重复表头。
  - 单元格内联语法：**粗体** `代码` *强调*；ASCII 双引号按出现顺序配对弯化（同 make_book.fix_dquotes）。
  - 表格内容的 SSOT 在 sources.md；改表先改它，再跑 regen。"""
import sys, re, html, json, pathlib, math

HERE = pathlib.Path(__file__).resolve().parent
VOL2 = HERE.parent.parent
CHAPTERS = [
    "01-architecture-v4.0.md", "02-correct-runtime-v1.0.md", "03-incident-v2.0.md",
    "04-blueprint.md", "05-run-lifecycle.md", "06-state-persistence.md",
    "07-durable-execution.md", "08-tools-effects.md", "09-interaction.md",
    "10-context-continuity.md", "11-permissions.md", "12-multi-agent.md",
    "13-evidence.md", "14-build.md", "15-review.md",
    "90-artifacts.md", "99-appendix.md",
]
DROP_SECTIONS = ("审稿日志", "引用来源", "变更记录")  # 与 pdf-build/make_book.py 保持一致
MAX_H = 1750   # canvas px；A4 版心 182mm 宽显示 1320px 图 → 单页最多容 ~1894px 高
TARGET_H = 1550  # 拆分后每张的目标高度

# ---------- 单元格内联语法 ----------
def curl_quotes(s):
    out, op = [], True
    for ch in s:
        if ch == '"':
            out.append("“" if op else "”"); op = not op
        else:
            out.append(ch)
    return "".join(out)

def cell_html(s):
    s = s.strip()
    codes = []
    def stash(m):
        codes.append(m.group(1)); return f"\x00{len(codes)-1}\x00"
    s = re.sub(r"`([^`]+)`", stash, s)
    s = curl_quotes(s)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub("\x00(\\d+)\x00", lambda m: "<code>" + html.escape(codes[int(m.group(1))], quote=False) + "</code>", s)
    return s

def split_row(line):
    line = line.strip()
    if line.startswith("|"): line = line[1:]
    if line.endswith("|"): line = line[:-1]
    return [c.replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]

# ---------- HTML 模板 ----------
def table_html(header, aligns, rows, cont=False, wrap="break"):
    """wrap="break"：保英文词完整（overflow-wrap:break-word）；列的 min-content 撑爆画布时
    由 build() 检测溢出、单表回退 wrap="any"（anywhere，逐字符可断）。"""
    ow = "anywhere" if wrap == "any" else "break-word"
    ncol = len(header)
    fs, pad = (28, "13px 17px") if ncol <= 4 else (26, "12px 14px") if ncol == 5 else (23, "9px 11px")
    # 短列不折行（显示宽：CJK 记 2、拉丁记 1，全列最长 ≤10 单位）——防"图 5.2"/"5.8/7.6"被拦腰断
    def disp_w(s):
        return sum(2 if ord(c) > 0x2E80 else 1 for c in s)
    padded = [(r + [""] * ncol)[:ncol] for r in rows]
    nowrap = [max(disp_w(c.strip()) for c in col) <= 10 for col in zip(header, *padded)]
    def sty(a, nw):
        return f'text-align:{a}' + (';white-space:nowrap' if nw else '')
    ths = "".join(f'<th style="{sty(a, nw)}">{cell_html(c)}</th>'
                  for c, a, nw in zip(header, aligns, nowrap))
    trs = []
    for r in padded:
        trs.append("<tr>" + "".join(f'<td style="{sty(a, nw)}">{cell_html(c)}</td>'
                                    for c, a, nw in zip(r, aligns, nowrap)) + "</tr>")
    note = '<div class="cont">（续上表）</div>' if cont else ""
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<link rel="stylesheet" href="../_base.css">
<style>
  .canvas{{width:1320px;padding:24px 26px;background:var(--bg)}}
  .cont{{font-family:var(--f-label);font-size:19px;font-weight:700;color:var(--t3);
    letter-spacing:.08em;margin:0 0 12px 2px}}
  table{{border-collapse:collapse;width:100%;background:var(--card);
    font-family:var(--f-body);font-size:{fs}px;line-height:1.6;color:var(--t2)}}
  th,td{{border:1px solid var(--divider);padding:{pad};vertical-align:top;overflow-wrap:{ow}}}
  th{{font-family:var(--f-head);font-weight:700;color:var(--purple-dark);
    background:rgba(109,40,217,.08);border-bottom:2.5px solid var(--purple)}}
  tr:nth-child(even) td{{background:rgba(26,20,40,.022)}}
  td b{{color:var(--t1);font-weight:700}}
  td em{{color:var(--purple-dark);font-style:normal;font-weight:600}}
  th code,td code{{font-family:"JetBrains Mono","LXGW WenKai",monospace;font-size:.9em;
    background:#efeae2;padding:1px 6px;border-radius:4px;color:var(--purple-dark)}}
</style></head>
<body><div class="canvas">{note}<table><thead><tr>{ths}</tr></thead><tbody>{"".join(trs)}</tbody></table></div></body></html>
"""

# ---------- 抽取 ----------
def parse_align(sep_cells):
    out = []
    for c in sep_cells:
        c = c.strip()
        if c.startswith(":") and c.endswith(":"): out.append("center")
        elif c.endswith(":"): out.append("right")
        else: out.append("left")
    return out

def extract_tables(md_lines):
    """返回 [(start, end, lines)]，end 为开区间；排除编辑区。"""
    res, section, i = [], "", 0
    while i < len(md_lines):
        l = md_lines[i]
        m = re.match(r"^##\s+(.+?)\s*$", l)
        if m: section = m.group(1).strip()
        if l.startswith("|") and i + 1 < len(md_lines) and re.match(r"^\|[\s:|-]+\|?\s*$", md_lines[i + 1]):
            j = i
            while j < len(md_lines) and md_lines[j].startswith("|"): j += 1
            if not any(section.startswith(s) for s in DROP_SECTIONS):
                res.append((i, j, md_lines[i:j]))
            i = j; continue
        i += 1
    return res

# ---------- sources.md ----------
def parse_sources():
    src = (HERE / "sources.md").read_text(encoding="utf-8").splitlines()
    entries, i = [], 0
    while i < len(src):
        m = re.match(r"^##\s+(tb-[\w.-]+)\s+·\s+(\S+)", src[i])
        if m:
            j = i + 1
            while j < len(src) and not src[j].startswith("|"): j += 1
            k = j
            while k < len(src) and src[k].startswith("|"): k += 1
            entries.append((m.group(1), m.group(2), src[j:k]))
            i = k; continue
        i += 1
    return entries

# ---------- 渲染（批量，2x DPI）----------
def render_all(jobs):
    """jobs: [(html_path, png_path)]；返回 {png_path: (canvas_css_height, 表格是否横向溢出)}"""
    from playwright.sync_api import sync_playwright
    meas = {}
    with sync_playwright() as p:
        b = None
        for ch in ("msedge", "chrome"):
            try:
                b = p.chromium.launch(channel=ch); break
            except Exception:
                continue
        b = b or p.chromium.launch()
        pg = b.new_page(device_scale_factor=2)
        for hp, pp in jobs:
            pg.goto(pathlib.Path(hp).resolve().as_uri(), wait_until="networkidle", timeout=20000)
            try:
                pg.evaluate("async () => { await document.fonts.ready; }")
            except Exception:
                pass
            pg.wait_for_timeout(180)
            el = pg.query_selector(".canvas")
            el.screenshot(path=str(pp))
            meas[str(pp)] = tuple(pg.evaluate(
                "() => { const c = document.querySelector('.canvas'), t = document.querySelector('table');"
                " return [c.offsetHeight, t ? t.getBoundingClientRect().right >"
                " c.getBoundingClientRect().right - 26 + 1 : false]; }"))
        b.close()
    return meas

def build(entries):
    """entries: [(tid, chapter, tbl_lines)] -> 渲染全部，超高自动拆分。返回 {tid: [png 名列表]}。"""
    plans = {}
    for tid, _ch, lines in entries:
        header = split_row(lines[0])
        aligns = (parse_align(split_row(lines[1])) + ["left"] * len(header))[:len(header)]
        rows = [split_row(l) for l in lines[2:]]
        plans[tid] = [header, aligns, rows, "break"]

    def write_parts(tid, parts):
        header, aligns, _rows, wrap = plans[tid]
        jobs = []
        for name, rows, cont in parts:
            hp = HERE / f"{name}.html"
            hp.write_text(table_html(header, aligns, rows, cont=cont, wrap=wrap), encoding="utf-8")
            jobs.append((hp, HERE / f"{name}.png"))
        return jobs

    result = {tid: [tid] for tid in plans}
    jobs = []
    for tid in plans:
        jobs += write_parts(tid, [(tid, plans[tid][2], False)])
    meas = render_all(jobs)

    # 保词模式撑爆画布的，单表回退 anywhere
    redo = [tid for tid in plans if meas[str(HERE / f"{tid}.png")][1]]
    for tid in redo:
        plans[tid][3] = "any"
        meas.update(render_all(write_parts(tid, [(tid, plans[tid][2], False)])))
    if redo:
        print(f"  [回退 anywhere] {' '.join(redo)}")

    # 超高的拆分（按行数均分，迭代到全部达标）
    for tid, (h, a, rows, _w) in plans.items():
        hh = meas[str(HERE / f"{tid}.png")][0]
        if hh <= MAX_H: continue
        nparts = max(2, math.ceil(hh / TARGET_H))
        while True:
            per = math.ceil(len(rows) / nparts)
            chunks = [rows[k:k + per] for k in range(0, len(rows), per)]
            names = [f"{tid}{chr(97 + n)}" for n in range(len(chunks))]
            jobs = write_parts(tid, [(nm, ck, n > 0) for n, (nm, ck) in enumerate(zip(names, chunks))])
            hs = render_all(jobs)
            if all(v[0] <= MAX_H for v in hs.values()) or per == 1:
                (HERE / f"{tid}.html").unlink(missing_ok=True)
                (HERE / f"{tid}.png").unlink(missing_ok=True)
                result[tid] = names
                print(f"  [拆分] {tid} 高 {hh}px -> {len(chunks)} 张")
                break
            nparts += 1
    return result

# ---------- 主流程 ----------
def do_extract(dry=False):
    entries, src_out = [], ["# 第二卷 · 正文表格嵌入图源（SSOT）", "",
        "> 由 `gen_embeds.py extract` 生成。**之后改表格内容请改本文件**，再跑 `python gen_embeds.py regen`；",
        "> 正文 md 里只留 `figures/embed/*.png` 引用。编辑区（审稿日志/变更记录）表格未抽取，仍在正文 md。", ""]
    replaces = {}  # chapter -> [(start, end, [png names])]
    for ch in CHAPTERS:
        p = VOL2 / ch
        lines = p.read_text(encoding="utf-8").splitlines()
        tabs = extract_tables(lines)
        chno = ch.split("-")[0]
        for n, (s, e, tl) in enumerate(tabs, 1):
            tid = f"tb-{chno}-{n}"
            entries.append((tid, ch, tl))
            src_out += [f"## {tid} · {ch} · 原 L{s + 1}", ""] + tl + [""]
            replaces.setdefault(ch, []).append((s, e, tid))
        # 断言：表格块后不能紧跟图注行（防 FIG_RE 抢配图图注）
        for s, e, _t in tabs:
            nxt = next((l for l in lines[e:e + 2] if l.strip()), "")
            assert not nxt.startswith("*图 "), f"{ch} L{e}: 表格后紧跟图注，需人工处理"
    (HERE / "sources.md").write_text("\n".join(src_out), encoding="utf-8")
    print(f"抽取 {len(entries)} 张表 -> sources.md")

    result = build(entries)
    if dry:
        print("[dry] 只生成 sources.md + html + png，正文 md 未改")
        return

    for ch, reps in replaces.items():
        p = VOL2 / ch
        lines = p.read_text(encoding="utf-8").splitlines()
        for s, e, tid in sorted(reps, reverse=True):
            imgs = []
            for nm in result[tid]:
                imgs += [f"![](figures/embed/{nm}.png)", ""]
            lines[s:e] = imgs[:-1]
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  [回写] {ch}: {len(reps)} 处")

def do_regen():
    entries = [(tid, ch, tl) for tid, ch, tl in parse_sources()]
    result = build(entries)
    print(f"再生成 {len(entries)} 张表（拆分 {sum(1 for v in result.values() if len(v) > 1)} 张）")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "regen"
    if mode == "extract":
        do_extract(dry="--dry" in sys.argv)
    else:
        do_regen()
