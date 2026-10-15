import base64, sys
from playwright.sync_api import sync_playwright
from _comun import APP, PDFJS, PDFJS_VERSION, FX, OUT as S


fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

def b64(path): return base64.b64encode(open(path, "rb").read()).decode()

def serve_pdfjs(route, tamper=False):
    name = route.request.url.rsplit("/", 1)[-1]
    body = open(PDFJS + name, "rb").read()
    if tamper: body += b"\n/* modificado */"
    route.fulfill(body=body, headers={"Access-Control-Allow-Origin": "*", "Content-Type": "application/javascript"})

def new_page(b, pdfjs="ok", offline=False):
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True, accept_downloads=True)
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    ctx.route("**/jszip.min.js", lambda r: r.fulfill(body="", content_type="application/javascript"))
    ctx.route("**/qrcode.min.js", lambda r: r.fulfill(body="", content_type="application/javascript"))
    pending = []
    # (lambda: si se pasa serve_pdfjs directamente, Playwright le da también la petición como 2º argumento)
    if pdfjs == "ok": ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", lambda r: serve_pdfjs(r))
    elif pdfjs == "tamper": ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", lambda r: serve_pdfjs(r, tamper=True))
    elif pdfjs == "404": ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", lambda r: r.fulfill(status=404, body="no"))
    elif pdfjs == "abort": ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", lambda r: r.abort())
    elif pdfjs == "hold": ctx.route(f"**/pdf.js/{PDFJS_VERSION}/*", lambda r: pending.append(r))
    if offline: ctx.add_init_script("Object.defineProperty(Navigator.prototype, 'onLine', { get: () => false });")
    p = ctx.new_page()
    errors = []
    p.on("pageerror", lambda e: errors.append(str(e)))
    p.goto(APP)
    p.evaluate("""async () => { localStorage.clear(); localStorage.setItem('nomina-auditor-autobackup','false');
        await new Promise(r => { const q = indexedDB.deleteDatabase('nomina-auditor-docs'); q.onsuccess = q.onerror = q.onblocked = r; }); }""")
    p.reload(); p.wait_for_timeout(300)
    return ctx, p, errors, pending

def seed_and_open(p, pdf_path, pid="2026-04", month="Abril"):
    p.evaluate("""async ([pid, month, b64]) => {
        payrolls = payrolls.filter(x => x.id !== pid);
        const pr = {id: pid, period:{month, year:'2026'}, totals:{grossTotal:1800, netPay:1500}, earnings:[], deductions:[], bases:{}};
        pr.original = await storeOriginal(b64, 'application/pdf', 'nomina.pdf');
        payrolls.push(pr); sortPayrolls(); saveData(); showReport(pr);
    }""", [pid, month, b64(pdf_path)])
    p.wait_for_timeout(200)
    p.click("#originalBody >> text=👁 Ver")

def nonwhite_pixels(p, idx=0):
    return p.evaluate("""(i) => { const c = document.querySelectorAll('#docViewer canvas.pdf-page')[i];
        const d = c.getContext('2d').getImageData(0, 0, c.width, Math.min(c.height, 400)).data; let n = 0;
        for (let k = 0; k < d.length; k += 4) if (d[k] < 128) n++; return n; }""", idx)

with sync_playwright() as pw:
    b = pw.chromium.launch()

    print("1) Primera vez: indicador visual mientras se prepara el visor")
    ctx, p, errors, pending = new_page(b, pdfjs="hold")
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_timeout(400)
    st = p.inner_text("#pdfStatus") if p.query_selector("#pdfStatus") else ""
    check("Preparando el visor de PDF" in st and p.is_visible("#pdfStatus .spinner"), f"se ve el aviso con animación: '{st.strip()}'")
    p.screenshot(path=S + "60_pdf_cargando.png")
    while pending:
        r = pending.pop(0); serve_pdfjs(r); p.wait_for_timeout(150)
    p.wait_for_function("document.querySelectorAll('#docViewer canvas.pdf-page').length === 2", timeout=15000)
    p.wait_for_timeout(300)
    check(p.query_selector("#pdfStatus") is None, "el aviso desaparece al terminar")
    check(nonwhite_pixels(p) > 500, "la página 1 se ha dibujado (hay texto en el lienzo)")
    check("2 páginas" in p.inner_text(".pdf-more"), "indica 2 páginas y ofrece abrir con otra app o descargar")
    w = p.evaluate("document.querySelector('#docViewer canvas.pdf-page').width")
    check(w >= 900, f"resolución suficiente para ampliar con los dedos ({w}px de ancho)")
    p.screenshot(path=S + "61_pdf_visor.png")
    p.click("#docViewer >> text=✕ Cerrar")

    print("2) Segunda vez: abre directamente (visor ya cargado)")
    p.click("#originalBody >> text=👁 Ver")
    p.wait_for_timeout(50)
    # leído de una vez: el aviso puede desaparecer entre dos llamadas si el PDF se dibuja muy rápido
    st = p.evaluate("document.querySelector('#pdfStatus')?.innerText ?? '(ya renderizado)'")
    check("Preparando" not in st, f"no repite la preparación: '{st.strip()}'")
    p.wait_for_function("document.querySelectorAll('#docViewer canvas.pdf-page').length === 2", timeout=10000)
    p.click("#docViewer >> text=✕ Cerrar")

    print("3) PDF con contraseña: incorrecta y luego correcta")
    asked = []
    def on_dialog(d):
        asked.append(d.message)
        d.accept("0000" if len(asked) == 1 else "12345678Z")
    p.on("dialog", on_dialog)
    seed_and_open(p, FX + "abril_protegida.pdf", "2026-05", "Mayo")
    p.wait_for_function("document.querySelectorAll('#docViewer canvas.pdf-page').length === 2", timeout=15000)
    check(len(asked) == 2 and "protegido con contraseña" in asked[0] and "incorrecta" in asked[1], f"pide la contraseña y avisa si es incorrecta: {asked}")
    check(nonwhite_pixels(p) > 500, "con la contraseña correcta se ve la nómina")
    p.click("#docViewer >> text=✕ Cerrar")
    p.remove_listener("dialog", on_dialog)

    print("4) Contraseña cancelada: no se queda cargando")
    p.on("dialog", lambda d: d.dismiss())
    p.click("#originalBody >> text=👁 Ver")
    p.wait_for_selector("#docViewer .pdf-fallback", timeout=8000)
    fb = p.inner_text("#docViewer .pdf-fallback")
    check("protegido con contraseña y no se ha abierto" in fb, "mensaje claro al cancelar")
    check(p.query_selector("#pdfStatus") is None, "sin animación de carga colgada")
    check("Abrir con el visor del móvil" in fb and "Descargar" in fb, "ofrece abrirlo con el visor del móvil o descargarlo")
    p.screenshot(path=S + "62_pdf_contraseña_cancelada.png")
    with p.expect_download() as dl:
        p.click("#docViewer .pdf-fallback >> text=Descargar")
    check(dl.value.suggested_filename == "2026-05 Mayo.pdf", f"la descarga funciona: {dl.value.suggested_filename}")
    p.click("#docViewer >> text=✕ Cerrar")

    print("5) PDF dañado")
    seed_and_open(p, FX + "dañada.pdf", "2026-06", "Junio")
    p.wait_for_selector("#docViewer .pdf-fallback", timeout=8000)
    check("No se ha podido mostrar este PDF" in p.inner_text("#docViewer .pdf-fallback"), "mensaje de PDF dañado con alternativas")
    p.click("#docViewer >> text=✕ Cerrar")

    print("6) Las fotos siguen abriéndose como antes")
    p.evaluate("""async (b64) => { const pr = {id:'2026-07', period:{month:'Julio',year:'2026'}, totals:{}, earnings:[], deductions:[], bases:{}};
        pr.original = await storeOriginal(b64, 'image/jpeg', 'f.jpg'); payrolls.push(pr); saveData(); showReport(pr); }""", b64(FX + "nomina_julio.jpg"))
    p.wait_for_timeout(200)
    p.click("#originalBody >> text=👁 Ver")
    p.wait_for_selector("#docViewer img")
    check(p.query_selector("#docViewer canvas") is None and p.is_visible("#docViewer img"), "visor de fotos intacto")
    p.click("#docViewer >> text=✕ Cerrar")
    check(not errors, f"sin errores JS: {errors}")
    ctx.close()

    print("7) Cerrar mientras carga no rompe nada")
    ctx, p, errors, pending = new_page(b, pdfjs="hold")
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_timeout(300)
    p.click("#docViewer >> text=✕ Cerrar")
    while pending:
        r = pending.pop(0); serve_pdfjs(r); p.wait_for_timeout(150)
    p.wait_for_timeout(500)
    check(p.query_selector("#docViewer") is None and not errors, f"visor cerrado sin errores: {errors}")
    ctx.close()

    print("8) Si no se puede descargar el visor")
    ctx, p, errors, _ = new_page(b, pdfjs="404")
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_selector("#docViewer .pdf-fallback", timeout=8000)
    fb = p.inner_text("#docViewer .pdf-fallback")
    check("No se ha podido cargar el visor de PDF" in fb and "Abrir con el visor del móvil" in fb, "alternativa: visor del móvil o descargar")
    p.screenshot(path=S + "63_pdf_sin_visor.png")
    check(not errors, f"sin errores JS: {errors}")
    ctx.close()

    print("9) Sin conexión la primera vez")
    ctx, p, errors, _ = new_page(b, pdfjs="abort", offline=True)
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_selector("#docViewer .pdf-fallback", timeout=8000)
    check("Sin conexión" in p.inner_text("#docViewer .pdf-fallback"), "explica que la primera vez necesita conexión")
    ctx.close()

    print("10) Visor manipulado (SRI): no se ejecuta")
    ctx, p, errors, _ = new_page(b, pdfjs="tamper")
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_selector("#docViewer .pdf-fallback", timeout=8000)
    check(p.evaluate("typeof window.pdfjsLib") == "undefined", "el navegador bloquea el archivo que no coincide con la huella")
    check("No se ha podido cargar el visor" in p.inner_text("#docViewer .pdf-fallback"), "y se ofrece la alternativa")
    ctx.close()

    print("11) Un PDF no puede ejecutar código (mitigación de CVE-2024-4367)")
    # PDF.js 3.x es vulnerable si evalúa código de las fuentes del PDF; la mitigación oficial es isEvalSupported: false
    ctx, p, errors, _ = new_page(b)
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_selector("#docViewer .pdf-more", timeout=15000)
    p.click("#docViewer >> text=✕ Cerrar")
    p.evaluate("""() => { const orig = window.pdfjsLib; window.__pdfParams = [];
        const espia = Object.create(orig);   // mismo PDF.js, pero apuntando con qué opciones se abre cada PDF
        Object.defineProperty(espia, 'getDocument', { value: src => {
          window.__pdfParams.push({ isEvalSupported: src.isEvalSupported }); return orig.getDocument(src); } });
        window.pdfjsLib = espia; }""")
    seed_and_open(p, FX + "abril_2paginas.pdf")
    p.wait_for_selector("#docViewer .pdf-more", timeout=15000)
    params = p.evaluate("window.__pdfParams")
    check(len(params) == 1 and params[0]["isEvalSupported"] is False, f"el visor abre los PDF con isEvalSupported: false ({params})")
    check(not errors, f"sin errores JS: {errors}")
    ctx.close()
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
