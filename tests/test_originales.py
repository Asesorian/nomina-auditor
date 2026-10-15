import json, sys, zipfile
from playwright.sync_api import sync_playwright
from _comun import APP, JSZIP, FX, OUT as S, CORS


fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

def extracted(month, gross, net, **kw):
    d = {"period": {"month": month, "year": "2026", "days": 30},
         "company": {"name": "EMPRESA TEST SL"}, "worker": {"name": "TRABAJADOR TEST"},
         "employment": {"category": "Oficial", "contractCode": "100"},
         "earnings": [{"concept": "Salario base", "amount": gross}],
         "deductions": [{"concept": "IRPF", "amount": round(gross * 0.15, 2)}],
         "totals": {"grossTotal": gross, "totalDeductions": gross - net, "netPay": net},
         "bases": {"baseCC": gross, "baseIRPF": gross, "irpfPercentage": 15}}
    d.update(kw)
    return d

def new_context(browser):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                              is_mobile=True, has_touch=True, accept_downloads=True)
    ctx.route("**/jszip.min.js", lambda r: r.fulfill(path=JSZIP, content_type="application/javascript", headers=CORS))  # CORS: la app la carga con integrity + crossorigin
    ctx.route("**/qrcode.min.js", lambda r: r.fulfill(body="", content_type="application/javascript"))
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.accept())
    page.goto(APP)
    page.evaluate("""async () => { localStorage.clear(); localStorage.setItem('nomina-auditor-autobackup','false');
        localStorage.setItem('nomina-auditor-apikey','AIzaTEST-FAKE-KEY-123');
        await new Promise(r => { const q = indexedDB.deleteDatabase('nomina-auditor-docs'); q.onsuccess = q.onerror = q.onblocked = r; }); }""")
    page.reload(); page.wait_for_timeout(400)
    return ctx, page, errors

def stub_gemini(page, data):
    page.evaluate("(d) => { window.callGemini = async () => JSON.parse(JSON.stringify(d)); }", data)

def upload_and_save(page, path, data, keep=True):
    stub_gemini(page, data)
    page.evaluate("showView('upload')")
    page.set_input_files("#fileInput", path)
    page.wait_for_selector("#uploadBtns:not(.hidden)", timeout=5000)
    page.click("#processBtn")
    page.wait_for_selector("#verifyPhase:not(.hidden) .keep-original", timeout=5000)
    if not keep:
        page.uncheck(".keep-original input")
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(500)

idb_keys = "() => listDocKeys()"
P = lambda page, pid: page.evaluate("(id) => payrolls.find(p => p.id === id)", pid)

with sync_playwright() as pw:
    b = pw.chromium.launch()

    print("1) Pantalla de subida")
    ctx, page, errors = new_context(b)
    page.evaluate("showView('upload')")
    check(page.get_attribute("#cameraInput", "capture") == "environment", "botón Hacer foto abre la cámara trasera (capture=environment)")
    check(page.is_visible("text=📷 Hacer foto") and page.is_visible("text=📁 Elegir archivo"), "botones Hacer foto / Elegir archivo visibles")
    page.screenshot(path=S + "50_subida.png")

    print("2) Procesar una foto y guardarla con su original")
    stub_gemini(page, extracted("Julio", 1800, 1500))
    page.set_input_files("#fileInput", FX + "nomina_julio.jpg")
    page.wait_for_selector("#uploadBtns:not(.hidden)")
    page.click("#processBtn")
    page.wait_for_selector("#verifyPhase:not(.hidden) .keep-original")
    check(page.is_checked(".keep-original input"), "casilla 'Guardar también el original' marcada por defecto")
    page.locator(".keep-original").scroll_into_view_if_needed()
    page.screenshot(path=S + "51_verificacion_casilla.png")
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(500)
    jul = P(page, "2026-07")
    check(jul and jul.get("original", {}).get("type") == "image/jpeg", f"la nómina guarda la referencia al original: {jul and jul.get('original')}")
    keys = page.evaluate(idb_keys)
    check(jul and jul["original"]["key"] in keys, "el documento está en el almacenamiento del dispositivo")
    body = page.inner_text("#originalBody")
    check("2026-07 Julio.jpg" in body, f"nombre automático: {body.splitlines()[0] if body else ''}")
    page.locator("#originalBody").scroll_into_view_if_needed()
    page.screenshot(path=S + "52_informe_con_original.png")

    print("3) Descargar y ver el original")
    with page.expect_download() as dl:
        page.click("#originalBody >> text=⬇ Descargar")
    d = dl.value
    check(d.suggested_filename == "2026-07 Julio.jpg", f"descarga con nombre ordenado: {d.suggested_filename}")
    d.save_as(S + "dl_julio.jpg")
    check(open(S + "dl_julio.jpg", "rb").read(3) == b"\xff\xd8\xff", "el archivo descargado es un JPEG válido")
    page.click("#originalBody >> text=👁 Ver")
    page.wait_for_selector("#docViewer img")
    page.wait_for_timeout(300)
    w = page.evaluate("document.querySelector('#docViewer img').naturalWidth")
    check(w > 0, f"visor muestra la imagen (ancho {w}px)")
    page.screenshot(path=S + "53_visor.png")
    page.click("#docViewer >> text=✕ Cerrar")
    check(page.query_selector("#docViewer") is None, "el visor se cierra")

    print("4) Panel con indicador 📎")
    page.evaluate("currentYear='2026'; showView('dashboard')")
    row = page.inner_text("#dashTable tbody tr")
    check("📎" in row, "la fila de julio muestra 📎")

    print("5) Reclasificar conserva el original")
    page.evaluate("showReport(payrolls.find(p=>p.id==='2026-07'))")
    page.click("#reportContent button.type-opt:has-text('Paga extra')")
    page.wait_for_timeout(300)
    ex = P(page, "2026-07-extra")
    check(ex and ex.get("original", {}).get("key") == jul["original"]["key"], "misma referencia tras pasar a paga extra")
    check("2026-07 Julio - Paga extra.jpg" in page.inner_text("#originalBody"), "el nombre se actualiza: '2026-07 Julio - Paga extra.jpg'")

    print("6) Adjuntar original a una nómina que no lo tenía (sin procesar)")
    page.evaluate("""() => { payrolls.push({id:'2026-06', period:{month:'Junio', year:'2026'}, totals:{grossTotal:1800, netPay:1500},
        earnings:[], deductions:[], bases:{}}); sortPayrolls(); saveData(); showReport(payrolls.find(p=>p.id==='2026-06')); }""")
    check("Adjuntar original" in page.inner_text("#originalBody"), "muestra 'Adjuntar original' si no lo tiene")
    page.locator("#originalBody").scroll_into_view_if_needed()
    page.screenshot(path=S + "54_informe_sin_original.png")
    calls_before = page.evaluate("window.__geminiCalls || 0")
    page.evaluate("() => { window.callGemini = async () => { window.__geminiCalls = (window.__geminiCalls||0)+1; throw new Error('no debería llamarse'); }; }")
    page.set_input_files("#attachInput", FX + "nomina_junio.pdf")
    page.wait_for_selector("#originalBody >> text=2026-06 Junio.pdf", timeout=5000)
    jun = P(page, "2026-06")
    check(jun["original"]["type"] == "application/pdf", "PDF adjuntado tal cual (application/pdf)")
    check(page.evaluate("window.__geminiCalls || 0") == calls_before, "adjuntar no llama a la IA (no gasta lecturas)")
    old_key = jun["original"]["key"]
    page.set_input_files("#attachInput", FX + "nomina_junio_foto.jpg")
    page.wait_for_selector("#originalBody >> text=2026-06 Junio.jpg", timeout=5000)
    keys = page.evaluate(idb_keys)
    check(old_key not in keys, "al cambiar el original, el anterior se borra del dispositivo")

    print("7) Sustituir una nómina")
    upload_and_save(page, FX + "nomina_julio.jpg", extracted("Julio", 1800, 1510))   # nueva mensual de julio
    first = P(page, "2026-07")
    check(first and first.get("original"), "nueva mensual de julio con su original")
    upload_and_save(page, FX + "nomina_julio.jpg", extracted("Julio", 1800, 1510))   # misma otra vez → aviso
    check(page.is_visible("#dupModal"), "salta el aviso de hueco ocupado")
    page.click("#dupModalBtns >> text=Sustituir")
    page.wait_for_timeout(500)
    second = P(page, "2026-07")
    keys = page.evaluate(idb_keys)
    check(second["original"]["key"] != first["original"]["key"] and first["original"]["key"] not in keys, "al sustituir, el original viejo se borra y queda el nuevo")
    upload_and_save(page, FX + "nomina_julio.jpg", extracted("Julio", 1800, 1510), keep=False)
    page.click("#dupModalBtns >> text=Sustituir")
    page.wait_for_timeout(500)
    third = P(page, "2026-07")
    check(third.get("original", {}).get("key") == second["original"]["key"], "sustituir sin guardar original conserva el que había (nunca se pierde uno sin querer)")

    print("8) Eliminar una nómina borra su original")
    jun_key = P(page, "2026-06")["original"]["key"]
    page.evaluate("deletePayroll('2026-06')")
    page.wait_for_timeout(300)
    check(jun_key not in page.evaluate(idb_keys), "documento de junio borrado junto con la nómina")

    print("9) Backup completo (ZIP)")
    page.evaluate("showView('backup')")
    page.wait_for_timeout(200)
    page.screenshot(path=S + "55_datos.png", full_page=True)
    stats = page.inner_text("#dataStats")
    check("Documentos originales: 2" in stats, f"estado de datos cuenta los documentos")
    with page.expect_download() as dl:
        page.click("#fullBackupBtn")
    z = dl.value
    check(z.suggested_filename.startswith("nominas-backup-completo-") and z.suggested_filename.endswith(".zip"), f"nombre: {z.suggested_filename}")
    z.save_as(S + "backup_completo.zip")
    zf = zipfile.ZipFile(S + "backup_completo.zip")
    names = sorted(zf.namelist())
    print("     contenido:", names)
    check("datos-app.json" in names and "LEEME.txt" in names and "nominas.json" not in names, "incluye datos-app.json y LEEME.txt (v2.7.3)")
    check("nominas/2026/2026-07 Julio.jpg" in names and "nominas/2026/2026-07 Julio - Paga extra.jpg" in names, "nóminas en la carpeta nominas/, por año y con nombre automático")
    check(not any(n.startswith("documentos/") for n in names), "ya no hay carpeta documentos/")
    leeme = zf.read("LEEME.txt").decode("utf-8")
    check("nominas/: tus nóminas" in leeme and "datos-app.json" in leeme, "el LEEME explica la carpeta y el archivo de datos")
    meta = json.loads(zf.read("datos-app.json"))["_meta"]
    check(meta.get("totalDocuments") == 2 and len(meta.get("documents", {})) == 2, "el JSON enlaza cada documento con su nómina")
    check(all(v.startswith("nominas/2026/") for v in meta["documents"].values()), "con las rutas nuevas")
    check(zf.read("nominas/2026/2026-07 Julio.jpg")[:3] == b"\xff\xd8\xff", "los documentos dentro del ZIP están intactos")
    # El mismo backup con el formato de antes de la v2.7.3 (nominas.json + documentos/), para el punto 10b
    old_zip = S + "backup_completo_formato_antiguo.zip"
    data_old = json.loads(zf.read("datos-app.json"))
    data_old["_meta"]["documents"] = {k: v.replace("nominas/", "documentos/", 1) for k, v in data_old["_meta"]["documents"].items()}
    with zipfile.ZipFile(old_zip, "w") as zo:
        zo.writestr("nominas.json", json.dumps(data_old))
        for n in names:
            if n.startswith("nominas/") and not n.endswith("/"):
                zo.writestr(n.replace("nominas/", "documentos/", 1), zf.read(n))
        zo.writestr("LEEME.txt", "formato antiguo")
    snapshot = page.evaluate("JSON.stringify(createBackupData())")
    check(not errors, f"sin errores JS en el dispositivo 1: {errors}")
    ctx.close()

    print("10) Restaurar el backup completo en otro dispositivo (vacío)")
    ctx2, page2, errors2 = new_context(b)
    page2.evaluate("showView('backup')")
    page2.set_input_files("#importFileInput", S + "backup_completo.zip")
    page2.wait_for_selector("#importResult >> text=documentos originales restaurados", timeout=8000)
    res = page2.inner_text("#importResult")
    check("2 documentos originales restaurados" in res, f"resultado: {' '.join(res.split())}")
    check(page2.evaluate("payrolls.length") == 2, "2 nóminas restauradas")
    page2.evaluate("showReport(payrolls.find(p=>p.id==='2026-07-extra'))")
    page2.click("#originalBody >> text=👁 Ver")
    page2.wait_for_selector("#docViewer img")
    page2.wait_for_timeout(300)
    check(page2.evaluate("document.querySelector('#docViewer img').naturalWidth") > 0, "el original restaurado se ve en el nuevo dispositivo")
    page2.click("#docViewer >> text=✕ Cerrar")

    print("10b) Un backup completo antiguo (nominas.json + documentos/) se sigue restaurando")
    ctx4, page4, errors4 = new_context(b)
    page4.evaluate("showView('backup')")
    page4.set_input_files("#importFileInput", old_zip)
    page4.wait_for_selector("#importResult >> text=documentos originales restaurados", timeout=8000)
    check("2 documentos originales restaurados" in page4.inner_text("#importResult") and page4.evaluate("payrolls.length") == 2
          and page4.evaluate("payrolls.every(p => hasOriginal(p))"), "nóminas y originales restaurados desde el formato antiguo")
    check(not errors4, f"sin errores JS: {errors4}")
    ctx4.close()

    print("11) Importar un backup SOLO de datos no borra los originales del dispositivo")
    old_json = json.loads(snapshot)
    for p in old_json["payrolls"]: p.pop("original", None)          # backup antiguo, sin referencias
    page2.evaluate("(t) => processImportedJSON(t, document.getElementById('importResult'))", json.dumps(old_json))
    page2.wait_for_timeout(400)
    check(page2.evaluate("payrolls.every(p => hasOriginal(p))"), "las nóminas conservan su original tras importar un JSON sin referencias")

    print("12) Backup de datos en un dispositivo sin los documentos")
    ctx3, page3, errors3 = new_context(b)
    page3.evaluate("(t) => processImportedJSON(t, document.getElementById('importResult'))", snapshot)
    page3.wait_for_timeout(400)
    page3.evaluate("showReport(payrolls.find(p=>p.id==='2026-07'))")
    check("se guardó en otro dispositivo" in page3.inner_text("#originalBody"), "avisa de que el original está en otro dispositivo y permite adjuntarlo")
    check(not errors3, f"sin errores JS en el dispositivo 3: {errors3}")
    ctx3.close()

    print("13) Borrar todo borra también los documentos")
    page2.evaluate("clearAllData()")
    page2.wait_for_timeout(400)
    check(page2.evaluate(idb_keys) == [] and page2.evaluate("payrolls.length") == 0, "sin nóminas ni documentos")
    check(not errors2, f"sin errores JS en el dispositivo 2: {errors2}")
    ctx2.close()
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
