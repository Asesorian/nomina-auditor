import sys, re
from pathlib import Path
from playwright.sync_api import sync_playwright
from _comun import APP, VERSION, OUT as S, SITE_URL as URL, SITE_INDEX as SERVED


fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

def set_label(label):
    html = open(SERVED, encoding="utf-8").read()
    html = re.sub(r"Forense v[\d.]+", f"Forense {label}", html, count=1)
    open(SERVED, "w", encoding="utf-8").write(html)

REC = {"id": "2026-05", "period": {"month": "Mayo", "year": "2026"},
       "earnings": [{"concept": "Salario base", "amount": 2500.0}],
       "deductions": [{"concept": "TRIBUTACIÓN IRPF.16,24", "amount": 406.0}],
       "totals": {"grossTotal": 2500.0, "totalDeductions": 406.0, "netPay": 2094.0},
       "bases": {"baseIRPF": 2500.0}}

with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--no-proxy-server"])
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.accept())
    label = lambda: page.inner_text(".logo-badge").replace("FORENSE V", "Forense v")

    print("1) Primera visita con conexión: se instala el modo sin conexión")
    page.goto(URL)
    page.evaluate("""(r) => { localStorage.setItem('nomina-auditor-data', JSON.stringify([r]));
                              localStorage.setItem('nomina-auditor-autobackup', 'false'); }""", REC)
    page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=15000)
    check(True, "service worker activo y controlando la página")
    keys = page.evaluate("caches.keys()")
    check(any(k.startswith("nomina-auditor-") for k in keys), f"copia guardada: {keys}")
    page.evaluate("showView('backup')")
    check(page.inner_text("#offlineStatus") == "Activo", "Datos → Modo sin conexión: Activo")
    page.screenshot(path=S + "20_datos_offline_card.png")

    print("2) Sin conexión")
    ctx.set_offline(True)
    page.reload(); page.wait_for_timeout(500)
    check(label() == "Forense " + VERSION, f"la app abre sin red ({label()})")
    check(page.is_visible("#offlineBanner"), "se ve el aviso de sin conexión")
    page.evaluate("currentYear='2026'; renderDashboard()")
    check("Mayo 2026" in page.inner_text("#dashTable"), "tus nóminas siguen ahí")
    page.screenshot(path=S + "21_sin_conexion.png")
    page.evaluate("showView('upload'); imageBase64 = 'x'; processImage()")
    page.wait_for_timeout(200)
    check("Sin conexión" in page.inner_text("#uploadError"), "procesar nómina nueva avisa de que necesita internet")

    print("3) Vuelve la conexión y hay versión nueva publicada: llega a la primera")
    ctx.set_offline(False)
    set_label("v9.9")
    page.reload(); page.wait_for_timeout(500)
    check(label() == "Forense v9.9", f"con red carga la nueva a la primera ({label()})")
    check(page.is_hidden("#offlineBanner"), "el aviso desaparece con conexión")
    ctx.set_offline(True)
    page.reload(); page.wait_for_timeout(500)
    check(label() == "Forense v9.9", f"y sin red ya abre la nueva guardada ({label()})")
    ctx.set_offline(False)

    print("4) Forzar actualización")
    set_label(VERSION)
    page.evaluate("showView('backup')")
    page.click("text=Forzar actualización de la app")
    page.wait_for_load_state("load"); page.wait_for_timeout(800)
    check(label() == "Forense " + VERSION, f"recarga la última ({label()})")
    check(page.evaluate("JSON.parse(localStorage.getItem('nomina-auditor-data')).length") == 1, "las nóminas no se borran")
    page.wait_for_function("caches.keys().then(k => k.some(x => x.startsWith('nomina-auditor-')))", timeout=10000)
    check(True, "la copia sin conexión se vuelve a crear")

    print("5) Gemini nunca pasa por la copia")
    sw = (Path(SERVED).parent / "sw.js").read_text(encoding="utf-8")
    check("if (req.method !== 'GET') return;" in sw, "las peticiones POST (Gemini) van directas a la red")

    check(not errors, f"sin errores JS: {errors}")
    ctx.close()

    print("6) Abierta como archivo local (acceso directo del PC)")
    p2 = b.new_page()
    errs2 = []
    p2.on("pageerror", lambda e: errs2.append(str(e)))
    p2.goto(APP); p2.wait_for_timeout(300)
    p2.evaluate("showView('backup')")
    check(p2.is_hidden("#offlineCard"), "en file:// no aparece la tarjeta (no aplica)")
    check(not errs2, f"sin errores JS en file://: {errs2}")
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
