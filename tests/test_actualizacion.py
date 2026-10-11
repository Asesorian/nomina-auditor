"""Tras publicar una versión nueva, la app abre la nueva a la primera.

GitHub Pages sirve index.html con "Cache-Control: max-age=600". En la primera versión
del modo sin conexión el service worker respetaba esa caché y el móvil seguía viendo la
versión vieja hasta 10 minutos (corregido dentro de la v2.5). Esta prueba lo reproduce
con servidor_pages.py, que sirve con las mismas cabeceras.
"""
import re, sys
from playwright.sync_api import sync_playwright
from _comun import PAGES_URL as URL, PAGES_INDEX as SERVED


def set_label(l):
    h = open(SERVED, encoding="utf-8").read()
    open(SERVED, "w", encoding="utf-8").write(re.sub(r"Forense v[\w.]+", "Forense " + l, h, count=1))


fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)


with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--no-proxy-server"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
    p = ctx.new_page()
    lab = lambda: p.inner_text(".logo-badge").upper()
    set_label("vA")
    p.goto(URL); p.wait_for_function("navigator.serviceWorker.controller !== null", timeout=15000)
    p.goto(URL); p.wait_for_timeout(500)          # visita normal, ya controlada por el service worker
    check("VA" in lab(), f"antes de publicar se ve la versión publicada ({lab()})")
    set_label("vB")                                 # "publicamos" una versión nueva
    p.goto("about:blank"); p.goto(URL); p.wait_for_timeout(800)   # abrir la app de nuevo (navegación normal, no recarga)
    got = lab()
    check("VB" in got, f"al abrir la app tras publicar llega la nueva a la primera ({got})")
    b.close()

print("RESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
