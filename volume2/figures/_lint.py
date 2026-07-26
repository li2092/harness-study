#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图稿静态检查：用浏览器实测几何，抓四类肉眼容易漏的问题。
用法: python _lint.py [fig.html ...]   不传参则检查目录下全部 t*.html

  1. 遮挡——文字被后绘制的图形盖住（SVG 按文档顺序绘制，后写的 rect 会压住先写的 text）
  2. 出界——文字超出 viewBox
  3. 溢框——文字超出它所属 <g> 里的那个 rect
  4. 短箭头——带 marker-end 的路径短于 20px，渲染出来只剩一个箭头尖
"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
files = [pathlib.Path(a) for a in sys.argv[1:]] or sorted(HERE.glob("t*.html"))

JS = r"""() => {
  const out = {occluded: [], outside: [], overflow: [], shortArrow: [], overridden: []};
  const svg = document.querySelector('svg');
  if (!svg) return out;
  const vb = svg.viewBox.baseVal;
  const texts = [...svg.querySelectorAll('text')];
  const all = [...svg.querySelectorAll('*')];
  const idx = el => all.indexOf(el);

  const label = t => (t.textContent || '').trim().slice(0, 26);
  const vis = el => {
    const s = getComputedStyle(el);
    return s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.05;
  };
  // 把 getBBox（元素自身用户坐标）换算到 SVG 根的 viewBox 坐标系，才能跟 viewBox 比。
  // 注意不能直接用 getCTM()——那是到视口的矩阵，含 viewBox 缩放；渲染宽恰好等于
  // viewBox 宽时看不出问题，一改画布就静默失准。
  const rootBox = el => {
    const b = el.getBBox();
    const sm = svg.getScreenCTM(), em = el.getScreenCTM();
    const m = (sm && em) ? sm.inverse().multiply(em) : null;
    if (!m) return b;
    const pt = (x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; return p.matrixTransform(m); };
    const c = [pt(b.x, b.y), pt(b.x + b.width, b.y), pt(b.x, b.y + b.height), pt(b.x + b.width, b.y + b.height)];
    const xs = c.map(p => p.x), ys = c.map(p => p.y);
    return {x: Math.min(...xs), y: Math.min(...ys),
            width: Math.max(...xs) - Math.min(...xs), height: Math.max(...ys) - Math.min(...ys)};
  };

  for (const t of texts) {
    if (!vis(t)) continue;                    // 自己就不可见，不参与判定
    let b; try { b = rootBox(t); } catch (e) { continue; }
    if (!b.width) continue;

    // 2. 出界
    if (b.x < vb.x - 1 || b.y < vb.y - 1 ||
        b.x + b.width > vb.x + vb.width + 1 || b.y + b.height > vb.y + vb.height + 1) {
      out.outside.push({t: label(t), x: Math.round(b.x), w: Math.round(b.width),
                        right: Math.round(b.x + b.width), vbw: vb.width});
    }

    // 3. 溢框：只跟「真的把这段文字装在里面」的那个 rect 比
    //    （取同 <g> 内包住文字中心的 rect；一组里有多个 chip 时也能各归各）
    const g = t.parentElement;
    if (g && g.tagName.toLowerCase() === 'g') {
      const cx = b.x + b.width / 2, cy = b.y + b.height / 2;
      for (const r of g.querySelectorAll('rect')) {
        const rb = rootBox(r);
        if (cx >= rb.x && cx <= rb.x + rb.width && cy >= rb.y && cy <= rb.y + rb.height) {
          if (b.x + b.width > rb.x + rb.width + 2 || b.x < rb.x - 2) {
            out.overflow.push({t: label(t), textRight: Math.round(b.x + b.width),
                               boxRight: Math.round(rb.x + rb.width)});
          }
          break;
        }
      }
    }

    // 1. 遮挡：沿基线取样，看命中的是不是自己
    const ctm = t.getScreenCTM();
    if (!ctm) continue;
    let lb; try { lb = t.getBBox(); } catch (e) { continue; }
    const pts = [0.15, 0.5, 0.85].map(f => {
      const p = svg.createSVGPoint();
      p.x = lb.x + lb.width * f; p.y = lb.y + lb.height * 0.6;
      return p.matrixTransform(ctm);
    });
    for (const p of pts) {
      const hit = document.elementFromPoint(p.x, p.y);
      if (!hit || hit === t || t.contains(hit) || hit.contains(t)) continue;
      // 只有「后绘制」且「真的看得见」的元素才会盖住它
      if (idx(hit) > idx(t) && vis(hit)) {
        out.occluded.push({t: label(t), by: hit.tagName + (hit.getAttribute('class') ? '.' + hit.getAttribute('class') : '')});
        break;
      }
    }
  }

  // 5. 颜色/字号被 class 压掉：SVG 表现属性优先级低于任何 CSS 规则，
  //    写了 fill="#xxx" 却被 .cls{fill:...} 覆盖时，强调会静默消失
  for (const el of svg.querySelectorAll('[fill],[stroke],[font-size],[font-weight]')) {
    for (const prop of ['fill','stroke','font-size','font-weight']) {
      const attr = el.getAttribute(prop);
      if (!attr || attr === 'none' || !el.getAttribute('class')) continue;
      const used = getComputedStyle(el)[prop];
      const probe = document.createElement('span');
      probe.style.setProperty(prop === 'fill' || prop === 'stroke' ? 'color' : prop, attr);
      document.body.appendChild(probe);
      const want = getComputedStyle(probe)[prop === 'fill' || prop === 'stroke' ? 'color' : prop];
      probe.remove();
      if (want && used && want !== used) {
        out.overridden.push({t: (el.textContent||'').trim().slice(0,20) || el.tagName,
                             cls: el.getAttribute('class'), prop, attr, used});
      }
    }
  }

  // 4. 短箭头
  for (const p of svg.querySelectorAll('path')) {
    const st = getComputedStyle(p);
    if (!st.markerEnd || st.markerEnd === 'none') continue;
    let len; try { len = p.getTotalLength(); } catch (e) { continue; }
    if (len < 20) out.shortArrow.push({d: (p.getAttribute('d') || '').slice(0, 40), len: Math.round(len)});
  }
  return out;
}"""

bad = 0
with sync_playwright() as pw:
    try:
        b = pw.chromium.launch(channel="chrome")
    except Exception:
        b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 1200})
    for f in files:
        pg.goto(f.resolve().as_uri(), wait_until="networkidle")
        try:
            pg.evaluate("async () => { await document.fonts.ready; }")
        except Exception:
            pass
        pg.wait_for_timeout(400)
        r = pg.evaluate(JS)
        n = sum(len(v) for v in r.values())
        if not n:
            print(f"✓ {f.name}")
            continue
        bad += 1
        print(f"✗ {f.name}")
        for k, zh in (("occluded", "被遮挡"), ("outside", "出界"),
                      ("overflow", "溢出所属框"), ("shortArrow", "箭头过短"), ("overridden", "颜色/字号被 class 压掉")):
            for it in r[k]:
                print(f"    [{zh}] {json.dumps(it, ensure_ascii=False)}")
    b.close()

print(f"\n{len(files)} 张，{bad} 张有问题")
sys.exit(1 if bad else 0)
