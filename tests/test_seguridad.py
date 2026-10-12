"""Seguridad (v2.7.1): datos que no se ejecutan, backups manipulados, librerías con SRI y la API key.

Todo con datos inventados; las respuestas de Gemini se simulan (no se gasta ninguna lectura).
"""
import json, re, zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from _comun import APP, APP_FILE, JSZIP, FX, OUT as S, CORS, ROOT

fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

GUIA = "https://github.com/Asesorian/nomina-auditor#-api-key-de-gemini-gratis-o-de-pago"

# Respuestas a los diálogos (confirm/alert): se van gastando en orden; si no hay, se acepta
dialog_plan = []
dialog_log = []
def on_dialog(d):
    dialog_log.append(d.message)
    (d.accept() if (dialog_plan.pop(0) if dialog_plan else True) else d.dismiss())

def new_context(browser, jszip="ok"):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                              is_mobile=True, has_touch=True, accept_downloads=True)
    if jszip == "ok":
        ctx.route("**/jszip.min.js", lambda r: r.fulfill(path=JSZIP, content_type="application/javascript", headers=CORS))
    else:   # manipulado: mismo archivo con una línea añadida
        body = Path(JSZIP).read_bytes() + b"\nwindow.__jszipManipulado = 1;"
        ctx.route("**/jszip.min.js", lambda r: r.fulfill(body=body, content_type="application/javascript", headers=CORS))
    ctx.route("**/qrcode.min.js", lambda r: r.fulfill(body="", content_type="application/javascript", headers=CORS))
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", on_dialog)
    page.goto(APP)
    page.evaluate("""async () => { localStorage.clear(); localStorage.setItem('nomina-auditor-autobackup','false');
        await new Promise(r => { const q = indexedDB.deleteDatabase('nomina-auditor-docs'); q.onsuccess = q.onerror = q.onblocked = r; }); }""")
    page.reload(); page.wait_for_timeout(400)
    return ctx, page, errors

def rec(pid, month, year="2026", **kw):
    d = {"id": pid, "period": {"month": month, "year": year, "days": 30},
         "company": {"name": "EMPRESA TEST SL"}, "worker": {"name": "TRABAJADOR TEST"},
         "earnings": [{"concept": "Salario base", "amount": 2000}],
         "deductions": [{"concept": "IRPF", "amount": 300}],
         "totals": {"grossTotal": 2000, "totalDeductions": 300, "netPay": 1700},
         "bases": {"baseIRPF": 2000, "irpfPercentage": 15}}
    d.update(kw)
    return d

def set_payrolls(page, lst):
    page.evaluate("(l) => { payrolls = l; sortPayrolls(); saveData(); }", lst)

def ids(page):
    return page.evaluate("payrolls.map(p => p.id)")

def write_json(name, data):
    path = S + name
    Path(path).write_text(data if isinstance(data, str) else json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path

def import_file(page, path):
    page.evaluate("showView('backup'); document.getElementById('importResult').innerHTML = ''")
    page.set_input_files("#importFileInput", path)
    page.wait_for_function("() => { const t = document.getElementById('importResult').innerText; return t && !t.includes('Procesando') && !t.includes('descomprimido'); }", timeout=8000)
    page.wait_for_timeout(200)
    return page.inner_text("#importResult")

GEMINI_STUB = """(texto) => {
  window.__llamadasGemini = 0;
  window.fetch = async (url) => {
    if (String(url).includes('generativelanguage.googleapis.com')) {
      window.__llamadasGemini++;
      return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: texto }] } }] }),
                          { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    throw new TypeError('sin red en la prueba');
  };
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()

    # ───────────────────────────────────────────────────────────────
    print("1) «Copiar para Abogado» con comillas, ${…}, comillas invertidas y barras en los datos")
    ctx, page, errors = new_context(b)
    raro = rec("2026-03", "Marzo",
               company={"name": 'TALLERES "EL SOL" SL'},
               worker={"name": "O'BRIEN `PRUEBA` \\ C:\\nominas"},
               earnings=[{"concept": "Plus ${window.__ejecutado = 1}", "amount": 2000}])
    set_payrolls(page, [raro])
    page.evaluate("""() => { window.__copiado = null;
        Object.defineProperty(navigator, 'clipboard', { configurable: true,
          value: { writeText: async t => { window.__copiado = t; } } }); }""")
    page.evaluate("showReport(payrolls.find(p => p.id === '2026-03'))")
    onclick = page.get_attribute("#reportContent button:has-text('Copiar para Abogado')", "onclick")
    check(onclick == "copyText(this)", f"el botón ya no lleva el texto dentro: onclick=\"{onclick}\"")
    page.click("#reportContent button:has-text('Copiar para Abogado')")
    page.wait_for_timeout(300)
    copiado = page.evaluate("window.__copiado") or ""
    check('TALLERES "EL SOL" SL' in copiado, "con comillas en la empresa, copia el informe")
    check("${window.__ejecutado = 1}" in copiado and "O'BRIEN `PRUEBA` \\ C:\\nominas" in copiado, "copia los datos tal cual, sin alterarlos")
    check(copiado == page.evaluate("document.getElementById('reportContent')._reportText"), "copia exactamente el texto del informe")
    check(page.evaluate("window.__ejecutado") is None, "un ${…} en los datos NO se ejecuta al copiar")
    check(page.locator("#reportContent button:has-text('¡Copiado!')").count() == 1, "el botón confirma «✓ ¡Copiado!»")
    page.screenshot(path=S + "70_copiar_con_comillas.png")
    page.evaluate("currentYear = '2026'; showView('annual')")
    page.click("#copyAnnualBtn")
    page.wait_for_timeout(300)
    check((page.evaluate("window.__copiado") or "").startswith("TABLA RESUMEN ANUAL 2026"), "«Copiar Informe Anual» sigue funcionando")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("2) Respuesta de Gemini que no es JSON: nunca se ejecuta")
    ctx, page, errors = new_context(b)
    page.evaluate("localStorage.setItem('nomina-auditor-apikey', 'AIzaTEST-FAKE-KEY-123')")
    malicioso = '{ "period": { "month": "Julio", "year": "2026" }, "x": (window.__geminiEjecutado = 1) }'
    page.evaluate(GEMINI_STUB, malicioso)
    err = page.evaluate("callGemini('AAAA', 'image/jpeg').then(() => 'SIN ERROR', e => e.message)")
    check(page.evaluate("window.__geminiEjecutado") is None, "el código dentro de la respuesta NO se ejecuta")
    check(err.startswith("Todos los modelos fallaron"), f"se rechaza y se informa: {err.splitlines()[0]}")
    check(page.evaluate("window.__llamadasGemini") == 3, "prueba los 3 modelos antes de rendirse")
    check("consigue una gratis" not in err.lower() and GUIA in err, "el error final enlaza la guía y no dice «consigue una gratis»")
    src = Path(APP_FILE).read_text(encoding="utf-8")
    check("new Function" not in src and not re.search(r"\beval\(", src), "no queda new Function ni eval en la app")

    print("   …y una respuesta desordenada pero válida se sigue leyendo")
    desordenado = ('Aquí tienes:\n```json\n{\n  "period": { "month": "Julio", "year": "2026" } // mes\n'
                   '  "company": { "name": "EMPRESA \\"X\\" SL", "web": "http://ejemplo.test/a//b" },\n'
                   '  "earnings": [ { "concept": "Salario base", "amount": 1800, }, ],\n'
                   '  /* comentario */ "totals": { "grossTotal": 1800, "netPay": NaN }\n}\n```')
    page.evaluate(GEMINI_STUB, desordenado)
    d = page.evaluate("callGemini('AAAA', 'image/jpeg').catch(e => ({ error: e.message }))")
    check(d.get("period", {}).get("month") == "Julio" and d.get("totals", {}).get("netPay") == 0,
          f"repara comas, comentarios y NaN: {str(d)[:90]}")
    check(d.get("company", {}).get("web") == "http://ejemplo.test/a//b" and d.get("company", {}).get("name") == 'EMPRESA "X" SL',
          "no estropea los «//» ni las comillas que hay dentro de los datos")
    check(page.evaluate("window.__llamadasGemini") == 1, "se queda con el primer modelo")
    page.evaluate(GEMINI_STUB, "[1, 2, 3]")
    err = page.evaluate("callGemini('AAAA', 'image/jpeg').then(() => 'SIN ERROR', e => e.message)")
    check(err.startswith("Todos los modelos fallaron"), "un JSON que no es una nómina (una lista) se rechaza")
    page.evaluate("localStorage.removeItem('nomina-auditor-apikey')")
    err = page.evaluate("callGemini('AAAA', 'image/jpeg').then(() => 'SIN ERROR', e => e.message)")
    check("pídele la clave" in err and GUIA in err and "consigue una gratis" not in err.lower(),
          "sin clave: dice que la pida a quien le pasó la app o enlaza la guía")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("3) Backup JSON manipulado")
    ctx, page, errors = new_context(b)
    set_payrolls(page, [rec("2026-01", "Enero")])
    backup = {"_meta": {"app": "Nomina Auditor Forense", "version": "2.7", "exportedAt": "2026-10-01T10:00:00Z"},
              "payrolls": [
                  rec("2026-05", "mayo", year=2026),                                              # válido (mes y año se normalizan)
                  rec("2026-07-extra", "Julio", payType="extra",
                      original={"key": "x'); window.__docEjecutado = 1; ('", "type": "image/jpeg"}),  # válido, sin la referencia rara
                  rec("2026-06'),window.__idEjecutado=1,('", "Junio"),                            # id con código
                  rec("2026-08", "Agosto", year="2026'};window.__anioEjecutado=1;//"),             # año con código
                  rec("2026-09", "<img src=x onerror=window.__mesEjecutado=1>"),                 # mes inventado
                  rec("2026-10", "Octubre", payType="<b>raro</b>"),                               # tipo inventado
                  "no soy una nómina", None, ["lista"],
              ]}
    txt = import_file(page, write_json("backup_manipulado.json", backup))
    check(sorted(ids(page)) == ["2026-01", "2026-05", "2026-07-extra"], f"solo entran las válidas y se conservan las que había: {ids(page)}")
    check("7 registros ignorados" in txt, f"avisa de cuántos se han ignorado: «{' '.join(txt.split())[:120]}»")
    p5 = page.evaluate("payrolls.find(p => p.id === '2026-05')")
    check(p5["period"] == {"month": "Mayo", "year": "2026", "days": 30}, f"mes y año normalizados: {p5['period']}")
    check("original" not in page.evaluate("payrolls.find(p => p.id === '2026-07-extra')"), "la referencia a documento extraña se descarta (la nómina sí entra)")
    page.evaluate("currentYear = '2026'; showView('dashboard')")
    page.click("#dashTable button:has-text('Ver') >> nth=1")
    page.wait_for_timeout(200)
    page.evaluate("showView('annual')")
    vars_ = page.evaluate("[window.__docEjecutado, window.__idEjecutado, window.__anioEjecutado, window.__mesEjecutado]")
    check(vars_ == [None, None, None, None], "nada de lo manipulado se ejecuta (panel, ver, anual)")
    page.screenshot(path=S + "71_backup_manipulado.png")

    print("   …un archivo que no es JSON muestra el error sin interpretarlo como HTML")
    txt = import_file(page, write_json("no_es_json.json", '<img src=x onerror="window.__errorEjecutado=1"> hola'))
    page.wait_for_timeout(300)
    check("Error al importar" in txt, "muestra «Error al importar»")
    check(page.locator("#importResult img").count() == 0 and page.evaluate("window.__errorEjecutado") is None,
          "el mensaje de error se muestra como texto (no crea elementos ni ejecuta nada)")
    txt = import_file(page, write_json("todo_malo.json", {"payrolls": [rec("hola", "Enero"), rec("2026-13", "Enero")]}))
    check("No se ha importado nada" in txt and sorted(ids(page)) == ["2026-01", "2026-05", "2026-07-extra"],
          "si no hay ninguna válida, no se toca nada y se dice")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    print("4) Backup completo (ZIP) manipulado")
    ctx, page, errors = new_context(b)
    jpg = Path(FX + "nomina_julio.jpg").read_bytes()
    pdf = Path(FX + "nomina_junio.pdf").read_bytes()
    data = {"_meta": {"app": "Nomina Auditor Forense", "version": "2.7", "exportedAt": "2026-10-01T10:00:00Z",
                      "documents": {"doc-bueno-1": "documentos/2026/2026-04 Abril.jpg",
                                    "doc-pdf-con-nombre-jpg": "documentos/2026/2026-02 Febrero.jpg",
                                    "doc-de-nomina-rechazada": "documentos/2026/rechazada.jpg",
                                    "doc-sin-nomina": "documentos/2026/suelto.jpg",
                                    "doc-ruta-fuera": "../../fuera.jpg",
                                    "<b>clave</b>": "documentos/2026/clave.jpg"}},
            "payrolls": [rec("2026-04", "Abril", original={"key": "doc-bueno-1", "type": "image/jpeg"}),
                         rec("2026-02", "Febrero", original={"key": "doc-pdf-con-nombre-jpg", "type": "image/jpeg"}),
                         rec("2026-11", "Noviembre", original={"key": "doc-ruta-fuera", "type": "image/jpeg"}),
                         rec("2026-99", "Diciembre", original={"key": "doc-de-nomina-rechazada", "type": "image/jpeg"})]}
    zpath = S + "backup_manipulado.zip"
    with zipfile.ZipFile(zpath, "w") as z:
        z.writestr("nominas.json", json.dumps(data))
        for name in ("2026-04 Abril.jpg", "rechazada.jpg", "suelto.jpg", "clave.jpg"):
            z.writestr("documentos/2026/" + name, jpg)
        z.writestr("documentos/2026/2026-02 Febrero.jpg", pdf)
        z.writestr("fuera.jpg", jpg)
    txt = import_file(page, zpath)
    keys = sorted(page.evaluate("listDocKeys()"))
    check(keys == ["doc-bueno-1", "doc-pdf-con-nombre-jpg"], f"solo se restauran los documentos de nóminas válidas, con clave y ruta válidas: {keys}")
    check(sorted(ids(page)) == ["2026-02", "2026-04", "2026-11"], f"nóminas importadas: {ids(page)}")
    check("1 registro ignorado" in txt, "avisa del registro ignorado")
    tipo = page.evaluate("getDoc('doc-pdf-con-nombre-jpg').then(r => r.type)")
    check(tipo == "application/pdf", "el tipo del documento se decide por su contenido, no por el nombre del archivo")
    page.evaluate("showView('backup')")
    page.wait_for_timeout(500)
    check(page.inner_text("#orphanInfo").strip() == "", "no quedan documentos sin nómina tras importar")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("5) Datos raros que ya estuvieran guardados (importados con una versión anterior)")
    ctx, page, errors = new_context(b)
    viejo = [rec("2026-01'),window.__viejoId=1,('", "Enero"), rec("2026-02", "Febrero", year="2026');window.__viejoAnio=1;('")]
    page.evaluate("(l) => localStorage.setItem('nomina-auditor-data', JSON.stringify(l))", viejo)
    page.reload(); page.wait_for_timeout(400)
    page.evaluate("currentYear = '2026'; renderDashboard()")
    page.click("#dashTable button:has-text('Ver')")
    page.wait_for_timeout(200)
    check("Enero" in page.inner_text("#reportContent"), "«Ver» abre la nómina aunque su identificador sea raro")
    page.evaluate("showView('dashboard')")
    page.click("#yearPills button:has-text('window')")
    page.wait_for_timeout(200)
    page.evaluate("showView('annual')")
    check(page.evaluate("[window.__viejoId, window.__viejoAnio]") == [None, None],
          "los botones llevan los datos como texto: nada se ejecuta al pulsarlos")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("6) Librerías externas con huella SRI")
    html = Path(APP_FILE).read_text(encoding="utf-8")
    for lib in ("jszip.min.js", "qrcode.min.js"):
        check(bool(re.search(lib.replace(".", r"\.") + r'"\s+integrity="sha384-[A-Za-z0-9+/=]{64}"\s+crossorigin="anonymous"', html)),
              f"{lib} se carga con integrity + crossorigin")
    sw = (ROOT / "sw.js").read_text(encoding="utf-8")
    check("'sw2'" not in sw and re.search(r"CACHE_PREFIX \+ 'sw(\d+)'", sw) and int(re.search(r"CACHE_PREFIX \+ 'sw(\d+)'", sw).group(1)) >= 3,
          "CACHE_VERSION subida (borra las copias antiguas, que podían estar guardadas sin CORS)")
    check("hit.type === 'opaque' && req.mode === 'cors'" in sw, "el service worker no sirve copias opacas a un <script> con SRI")
    ctx, page, errors = new_context(b, jszip="ok")
    check(page.evaluate("typeof JSZip") == "function", "JSZip auténtico: se carga")
    ctx.close()
    ctx, page, errors = new_context(b, jszip="manipulado")
    check(page.evaluate("typeof JSZip") == "undefined" and page.evaluate("window.__jszipManipulado") is None,
          "JSZip manipulado: el navegador lo bloquea y no se ejecuta")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("7) API key: pegar el enlace entero, confirmación y textos")
    ctx, page, errors = new_context(b)
    for pegado, esperada, nombre in [
        ("https://asesorian.github.io/nomina-auditor/#apikey=AIzaPEGADA-enlace_123", "AIzaPEGADA-enlace_123", "enlace con #apikey="),
        ("  https://asesorian.github.io/nomina-auditor/?apikey=AIzaPEGADA-query_456  ", "AIzaPEGADA-query_456", "enlace antiguo con ?apikey="),
        ("Toma: https://asesorian.github.io/nomina-auditor/#apikey=AIzaPEGADA%2Dcod_789", "AIzaPEGADA-cod_789", "enlace con texto delante y la clave codificada"),
        ("AIzaSOLO-LA-CLAVE-000", "AIzaSOLO-LA-CLAVE-000", "solo la clave"),
    ]:
        page.fill("#apiKeyInput", pegado)
        guardada = page.evaluate("localStorage.getItem('nomina-auditor-apikey')")
        casilla = page.input_value("#apiKeyInput")
        check(guardada == esperada and casilla == esperada and page.inner_text("#apiStatus") == "✓ Configurada",
              f"{nombre}: guarda «{guardada}» y la casilla muestra solo la clave")
    ayuda = page.inner_text("#apiHelp")
    href = page.get_attribute("#apiHelp a", "href")
    check("Pídesela a quien te pasó la app" in ayuda and href == GUIA, f"texto junto a la casilla: «{ayuda}»")
    check("Obtener gratis" not in page.inner_text(".api-bar") and "limit:0" not in page.inner_text(".api-bar"),
          "ya no dice «Obtener gratis» ni lo de «limit:0»")
    page.screenshot(path=S + "72_casilla_api_key.png")

    def abrir_enlace(clave, respuesta=None):
        dialog_log.clear()
        if respuesta is not None: dialog_plan.append(respuesta)
        page.goto(APP + "#apikey=" + clave)
        page.wait_for_timeout(700)
        dialog_plan.clear()
        return page.evaluate("localStorage.getItem('nomina-auditor-apikey')")

    page.evaluate("localStorage.setItem('nomina-auditor-apikey', 'AIzaMIA-ORIGINAL-1111')")
    k = abrir_enlace("AIzaAJENA-DE-OTRO-9999", respuesta=False)
    msg = dialog_log[0] if dialog_log else ""
    check(len(dialog_log) == 1 and "AIzaMIA-…1111" in msg and "AIzaAJEN…9999" in msg,
          "enlace con otra clave: pregunta antes, mostrando el principio y el final de las dos")
    check(k == "AIzaMIA-ORIGINAL-1111" and "apikey" not in page.url, "si dices que no, se queda la tuya (y la dirección queda limpia)")
    k = abrir_enlace("AIzaAJENA-DE-OTRO-9999", respuesta=True)
    check(k == "AIzaAJENA-DE-OTRO-9999" and page.input_value("#apiKeyInput") == k and page.inner_text("#apiStatus") == "✓ Configurada",
          "si dices que sí, se cambia y se ve al momento")
    k = abrir_enlace("AIzaAJENA-DE-OTRO-9999")
    check(not dialog_log and k == "AIzaAJENA-DE-OTRO-9999", "la misma clave otra vez: no pregunta")
    page.evaluate("localStorage.removeItem('nomina-auditor-apikey')")
    k = abrir_enlace("AIzaPRIMERA-VEZ-2222")
    check(not dialog_log and k == "AIzaPRIMERA-VEZ-2222", "sin clave guardada: la guarda sin preguntar")
    dialog_log.clear()
    page.evaluate("location.hash = 'apikey=AIzaPOR-HASH-3333'")
    page.wait_for_timeout(500)
    check(len(dialog_log) == 1 and page.evaluate("localStorage.getItem('nomina-auditor-apikey')") == "AIzaPOR-HASH-3333",
          "con la app ya abierta, un enlace nuevo también pregunta")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    # ───────────────────────────────────────────────────────────────
    print("8) Documentos sin nómina (huérfanos)")
    ctx, page, errors = new_context(b)
    page.evaluate("""async () => {
        const buf = new Uint8Array(300 * 1024).buffer;
        await putDoc('doc-de-julio', { data: buf, type: 'image/jpeg', name: 'j.jpg', size: buf.byteLength });
        await putDoc('doc-huerfano', { data: buf, type: 'image/jpeg', name: 'h.jpg', size: buf.byteLength });
        payrolls = [{ id: '2026-07', period: { month: 'Julio', year: '2026' }, totals: {}, earnings: [], deductions: [], bases: {},
                      original: { key: 'doc-de-julio', type: 'image/jpeg', size: buf.byteLength } }];
        saveData(); await refreshDocKeys(); }""")
    page.evaluate("showView('backup')")
    page.wait_for_selector("#orphanInfo button", timeout=4000)
    info = page.inner_text("#orphanInfo")
    check("1 documento sin nómina (300 KB)" in info, f"lo indica con su tamaño: «{' '.join(info.split())[:70]}»")
    page.locator("#orphanInfo").scroll_into_view_if_needed()
    page.screenshot(path=S + "73_huerfanos.png")
    dialog_plan.append(False)
    page.click("#orphanInfo button")
    page.wait_for_timeout(300)
    check(sorted(page.evaluate("listDocKeys()")) == ["doc-de-julio", "doc-huerfano"], "si cancelas, no borra nada")
    page.click("#orphanInfo button")
    page.wait_for_timeout(600)
    check(page.evaluate("listDocKeys()") == ["doc-de-julio"], "al confirmar, borra solo el huérfano (el de julio sigue)")
    check(page.inner_text("#orphanInfo").strip() == "", "y el aviso desaparece")
    page.evaluate("async () => { await putDoc('doc-otro', { data: new ArrayBuffer(10), type: 'image/jpeg', size: 10 }); payrolls = []; saveData(); }")
    page.evaluate("showView('backup')")
    page.wait_for_function("document.getElementById('orphanInfo').innerText.length > 0", timeout=4000)
    info = page.inner_text("#orphanInfo")
    check("ninguna nómina" in info and "no borres nada" in info and page.locator("#orphanInfo button").count() == 0,
          "sin ninguna nómina (¿datos perdidos?) no ofrece borrar: aconseja importar el backup")
    check(sorted(page.evaluate("listDocKeys()")) == ["doc-de-julio", "doc-otro"], "nunca se borran solos")
    check(not errors, f"sin errores de JavaScript ({errors[:1]})")
    ctx.close()

    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
for f in fails: print("  -", f)
