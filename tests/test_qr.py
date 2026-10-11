from playwright.sync_api import sync_playwright
from _comun import APP_FILE, APP
ok = True
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for suffix, name in [("#apikey=AIzaTEST_frag-123", "QR nuevo (#)"), ("?apikey=AIzaTEST_query-456", "QR antiguo (?)")]:
        p = b.new_page()
        p.goto(APP)
        p.evaluate("localStorage.clear()")
        p.goto(APP + suffix)
        p.wait_for_timeout(800)
        key = p.evaluate("localStorage.getItem('nomina-auditor-apikey')")
        url = p.url
        exp = suffix.split("=")[1]
        good = key == exp and "apikey" not in url
        ok &= good
        print(("OK  " if good else "FAIL"), name, "| key guardada:", key, "| dirección final limpia:", "apikey" not in url)
    p = b.new_page(); p.goto(APP)
    p.evaluate("localStorage.setItem('nomina-auditor-apikey','AIzaXYZ')")
    src = open(APP_FILE, encoding="utf-8").read()
    good = "nomina-auditor/#apikey=" in src and "nomina-auditor/?apikey=" not in src
    ok &= good
    print(("OK  " if good else "FAIL"), "el QR se genera con #apikey=")
    b.close()
print("RESULTADO:", "TODO OK" if ok else "FALLOS")
