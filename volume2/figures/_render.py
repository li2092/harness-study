#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML -> PNG (3x DPI) via Playwright. 用法: python _render.py <in.html> <out.png> [selector]"""
import sys, pathlib
from playwright.sync_api import sync_playwright

html, png = sys.argv[1], sys.argv[2]
sel = sys.argv[3] if len(sys.argv) > 3 else ".canvas"
url = pathlib.Path(html).resolve().as_uri()

def _launch(p):
    for ch in ("msedge", "chrome"):
        try:
            return p.chromium.launch(channel=ch)
        except Exception:
            continue
    return p.chromium.launch()

with sync_playwright() as p:
    b = _launch(p)
    pg = b.new_page(device_scale_factor=3)
    try:
        pg.goto(url, wait_until="networkidle", timeout=20000)
    except Exception:
        pg.goto(url)
    try:
        pg.evaluate("async () => { await document.fonts.ready; }")
    except Exception:
        pass
    pg.wait_for_timeout(600)
    el = pg.query_selector(sel)
    el.screenshot(path=png)
    b.close()
print("OK ->", png)
