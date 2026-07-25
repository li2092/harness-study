#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二卷：逐章 pandoc -> fragment + 手工 TOC/图目录（页码+跳转）-> book.html。
沿用入门卷管线，两处卷二特有：
  1. 章节清单显式列出（排除留档旧版与 SPEC/WRITING-PLAN 等编辑文件）；
  2. 出版前剥离编辑区（章首版本注 + 「审稿日志」「引用来源」两节），并打印剥离报告。
图片下方的「*图 N.M · …*」斜体行升级为 figure+figcaption，收进图目录(LOF) + 写出 figures.json。
用法: python make_book.py [--pages pages.json] [--figpages figpages.json]"""
import subprocess, pathlib, html, sys, json, re, os

def _src():
    """正文 SSOT 目录：mac(~/ClaudeCode) 与 Windows(D:) 自动择一，HARNESS_VOL2 可覆盖。"""
    for p in (os.environ.get("HARNESS_VOL2"),
              str(pathlib.Path.home() / "ClaudeCode/harness-study/volume2"),
              "D:/ClaudeCode/harness-study/volume2"):
        if p and pathlib.Path(p).exists():
            return pathlib.Path(p)
    return pathlib.Path("D:/ClaudeCode/harness-study/volume2")

SRC = _src()
PB = pathlib.Path(__file__).resolve().parent

# 出版章节顺序（显式清单：留档旧版 01-architecture.md / 01-architecture-v3.0.md /
# 02-correct-runtime.md / 03-incident.md 与 SPEC/WRITING-PLAN/README/91-material-index 均不入书）
CHAPTERS = [
    "01-architecture-v4.0.md", "02-correct-runtime-v1.0.md", "03-incident-v2.0.md",
    "04-blueprint.md", "05-run-lifecycle.md", "06-state-persistence.md",
    "07-durable-execution.md", "08-tools-effects.md", "09-interaction.md",
    "10-context-continuity.md", "11-permissions.md", "12-multi-agent.md",
    "13-evidence.md", "14-build.md", "15-review.md",
    "90-artifacts.md", "99-appendix.md",
]

# ===== 编辑区剥离（出版前）=====
# 整节剥离：前两节正文里明写「出版前整体删除」；变更记录是 90-artifacts/99-appendix 的编辑性版本日志
DROP_SECTIONS = ("审稿日志", "引用来源", "变更记录")
# 章首引用块里按行剥离的编辑标记（其余引用块行是给读者的，保留——
# 如 90-artifacts / 99-appendix 开头的用途说明）
EDITORIAL_LINE = re.compile(
    r"编辑工作区|依据 SPEC|SPEC\.md §|留档对照|旧稿 |待用户审|四维评审|章名由|"
    r"随各章过审|待该章过审后补入|样张见|引用规则（SPEC|^> v[\d.]+ ?· ?\d{4}-")

def strip_editorial(md):
    """剥离编辑区，返回 (正文, 报告)。章首引用块按行判定，两节整节剥离。"""
    lines, out, report = md.split("\n"), [], {"head": 0, "sections": []}
    seen_h2 = False
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            name = m.group(1).strip()
            if any(name.startswith(s) for s in DROP_SECTIONS):
                report["sections"].append(name)
                i += 1
                while i < len(lines) and not re.match(r"^##\s+", lines[i]):
                    i += 1
                while out and out[-1].strip() in ("", "---"):  # 收掉遗留分隔线/空行
                    out.pop()
                continue
            seen_h2 = True
        # 章首（第一个 ## 之前）的引用块：只剥编辑标记行
        if not seen_h2 and line.startswith(">") and EDITORIAL_LINE.search(line):
            report["head"] += 1
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out), report

# 图片段 +（紧跟的）「*图 N.M · …*」斜体段 -> figure + figcaption，并收集图目录
FIG_RE = re.compile(
    r'<p><img src="([^"]+)"[^>]*>\s*</p>\s*<p><em>图\s*([\d.]+)\s*·\s*(.*?)</em></p>', re.S)
figures = []
def fig_sub(m):
    src, num, cap = m.group(1), m.group(2), m.group(3).strip()
    fid = "fig-" + num.replace(".", "-")
    figures.append({"num": num, "cap": cap, "id": fid})
    return (f'<figure class="fig" id="{fid}">'
            f'<img src="{src}" alt="图 {num}" />'
            f'<figcaption><span class="fnum">图 {num}</span> · {cap}</figcaption></figure>')

def toc_title(title):
    """目录条目：剥掉标题末尾的「· **…**」加粗标注尾巴。"""
    return re.sub(r"\s*·\s*\*\*.*?\*\*\s*$", "", title).strip()

def fix_dquotes(md):
    """正文（非代码）里的 ASCII 双引号按行配对成弯引号 “ ”。
    pandoc smart 在 CJK 上下文判不准开/闭方向，故双引号自己按出现顺序配对。
    跳过围栏代码块与行内 `code`，保住 JSON/config 里的 ASCII 引号。配对状态每行重置。"""
    fence = re.compile(r"^\s*(`{3,}|~{3,})")
    in_fence, out = False, []
    for line in md.split("\n"):
        if fence.match(line):
            in_fence = not in_fence
            out.append(line); continue
        if in_fence or '"' not in line:
            out.append(line); continue
        segs = re.split(r"(`+[^`]*`+)", line)  # 奇数段=行内代码，原样保留
        op = True  # True=下一个引号画开引号 “
        for i in range(0, len(segs), 2):
            buf = []
            for ch in segs[i]:
                if ch == '"':
                    buf.append("“" if op else "”")
                    op = not op
                else:
                    buf.append(ch)
            segs[i] = "".join(buf)
        out.append("".join(segs))
    return "\n".join(out)

args = sys.argv[1:]
pages = figpages = None
while args and args[0] in ("--pages", "--figpages"):
    val = json.loads(pathlib.Path(args[1]).read_text(encoding="utf-8"))
    if args[0] == "--pages":
        pages = val
    else:
        figpages = val
    args = args[2:]
files = [SRC / a for a in (args or CHAPTERS)]

missing = [f.name for f in files if not f.exists()]
if missing:
    sys.stderr.write(f"[缺文件] {SRC}: {missing}\n"); sys.exit(1)

frags, toc, chap_titles, strip_log = [], [], [], []
for i, f in enumerate(files, 1):
    md = f.read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), f.stem)
    chap_titles.append(toc_title(title))
    md, rep = strip_editorial(md)
    strip_log.append((f.name, rep))
    md = fix_dquotes(md)
    r = subprocess.run(
        ["pandoc", "-f", "markdown-implicit_figures", "-t", "html",
         "--reference-location=document", f"--id-prefix=c{i}-"],
        input=md, capture_output=True, text=True, encoding="utf-8", cwd=str(SRC))
    if r.returncode != 0:
        sys.stderr.write(f"[pandoc fail] {f.name}: {r.stderr[:300]}\n"); sys.exit(1)
    body = FIG_RE.sub(fig_sub, r.stdout)
    frags.append(f'<section id="ch{i}" class="chapter">{body}</section>')
    pg = str(pages[i - 1]) if pages and i - 1 < len(pages) else ""
    toc.append(f'<li><a href="#ch{i}"><span class="ti">{html.escape(toc_title(title))}</span>'
               f'<span class="dots"></span><span class="pg">{pg}</span></a></li>')

# 图目录（顺序 = 图在正文出现顺序）；无图则整页不出
lof = []
for fg in figures:
    pg = str(figpages.get(fg["id"], "")) if figpages else ""
    lof.append(f'<li><a href="#{fg["id"]}"><span class="ti">图 {fg["num"]} · {html.escape(fg["cap"])}</span>'
               f'<span class="dots"></span><span class="pg">{pg}</span></a></li>')

(PB / "figures.json").write_text(json.dumps(figures, ensure_ascii=False), encoding="utf-8")
(PB / "chapters.json").write_text(json.dumps(chap_titles, ensure_ascii=False), encoding="utf-8")

head = (PB / "head.html").read_text(encoding="utf-8")
toc_html = '<nav id="TOC"><ul>' + "".join(toc) + "</ul></nav>"
lof_html = ('<nav id="LOF"><ul>' + "".join(lof) + "</ul></nav>") if lof else ""
doc = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
       + head + "</head><body>" + toc_html + lof_html + "".join(frags) + "</body></html>")
(PB / "book.html").write_text(doc, encoding="utf-8")

if not pages:  # 首遍才打剥离报告，避免刷屏
    print("--- 编辑区剥离 ---")
    for name, rep in strip_log:
        if rep["head"] or rep["sections"]:
            print(f"  {name}: 章首注 {rep['head']} 行" +
                  (f" · 整节 {'/'.join(rep['sections'])}" if rep["sections"] else ""))
print("OK book.html · 章节:", len(files), "· 图:", len(figures),
      "· 图目录:", "有" if lof else "无（正文暂无配图）", "· 页码:", "yes" if pages else "no")
