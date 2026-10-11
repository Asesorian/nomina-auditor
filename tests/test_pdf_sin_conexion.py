import base64, sys
from playwright.sync_api import sync_playwright
from _comun import PDFJS, PDFJS_VERSION, FX, OUT as S, SITE_URL as URL
ok = True
def check(c, m):
    global ok
    print(("  OK   " if c else "  FAIL ") + m); ok &= bool(c)
def serve(route):
    name = route.request.url.rsplit("/", 1)[-1]
    route.fulfill(body=open(PDFJS + name, "rb").read(), headers={"Access-Control-Allow-Origin": "*", "Content-Type": "application/javascript"})
with sync_playwright() as pw:
    b = pw.chromium.launch(args=["--no-proxy-server"])
    ctx = b.new_context(viewport={"width":390,"height":844}, is_mobile=True)
    ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", serve)
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    ctx.route("https://cdnjs.cloudflare.com/ajax/libs/jszip/**", lambda r: r.fulfill(body="", content_type="application/javascript", headers={"Access-Control-Allow-Origin":"*"}))
    ctx.route("https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/**", lambda r: r.fulfill(body="", content_type="application/javascript", headers={"Access-Control-Allow-Origin":"*"}))
    p = ctx.new_page(); errs = []; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(URL); p.wait_for_function("navigator.serviceWorker.controller !== null", timeout=15000)
    pdf = base64.b64encode(open(FX + "abril_2paginas.pdf", "rb").read()).decode()
    p.evaluate("""async (b64) => { const pr = {id:'2026-04', period:{month:'Abril',year:'2026'}, totals:{}, earnings:[], deductions:[], bases:{}};
        pr.original = await storeOriginal(b64, 'application/pdf', 'n.pdf'); payrolls.push(pr); saveData(); warmPdfViewer(); }""", pdf)
    p.wait_for_function("""caches.keys().then(ks => Promise.all(ks.map(k => caches.open(k).then(c => c.keys())))).then(all => {
        const urls = all.flat().map(r => r.url); return urls.some(u => u.endsWith('pdf.min.js')) && urls.some(u => u.endsWith('pdf.worker.min.js')); })""", timeout=20000)
    check(True, "con conexión, el visor queda guardado en segundo plano (sin abrir ningún PDF)")
    check(p.evaluate("typeof window.pdfjsLib") == "undefined", "la precarga no ejecuta nada ni ralentiza la app")
    ctx.set_offline(True)
    p.reload(); p.wait_for_timeout(800)
    check(p.is_visible("#offlineBanner"), "ahora sin conexión (aviso visible)")
    p.evaluate("showReport(payrolls.find(x => x.id === '2026-04'))"); p.wait_for_timeout(200)
    p.click("#originalBody >> text=👁 Ver")
    p.wait_for_function("document.querySelectorAll('#docViewer canvas.pdf-page').length === 2", timeout=15000)
    check(True, "sin conexión el PDF se abre dentro de la app (2 páginas)")
    check(not errs, f"sin errores JS: {errs}")
    b.close()
print("RESULTADO:", "TODO OK" if ok else "FALLOS"); sys.exit(0 if ok else 1)
