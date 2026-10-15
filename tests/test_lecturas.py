"""Lecturas que no cuadran (v2.7.2): comprobaciones, segunda lectura, corrección de nóminas guardadas.
Desde la v2.7.5: la clave va en la cabecera y la revisión se ve entera en pantallas estrechas.

Todo con datos inventados. Los errores de lectura que se simulan son los que se vieron de verdad:
  - filas de deducciones corridas (cada importe en la fila de al lado, falta el MEI y el IRPF leído como «I.R.P.P.»)
  - el precio por día tomado como importe en los devengos
"""
import base64
import json
import sys
from playwright.sync_api import sync_playwright
from _comun import APP, FX, OUT as S, CORS, JSZIP


def r2(x):
    return round(x + (1e-9 if x >= 0 else -1e-9), 2)


def nomina(month, salario=1800.00, plus=200.00, incentivos=0.0, irpf_pct=15.0, horas_extra=0.0):
    """Nómina coherente: todas las cuentas cuadran, como en el papel."""
    earnings = [{"code": "1", "concept": "Salario Base", "units": "30,00", "price": r2(salario / 30), "amount": salario},
                {"code": "45", "concept": "Plus Productividad", "units": "30,00", "amount": plus}]
    if incentivos:
        earnings.append({"code": "394", "concept": "Incentivos", "units": "", "amount": incentivos})
    if horas_extra:
        earnings.append({"code": "80", "concept": "Horas Extras", "units": "", "amount": horas_extra})
    gross = r2(sum(e["amount"] for e in earnings))
    prorrata = 300.00
    base_cc = r2(gross - horas_extra + prorrata)
    base_at = r2(base_cc + horas_extra)
    ded = [{"code": "789", "concept": "Dcto.Conceptos en Especie", "units": "", "amount": 0.74},
           {"code": "995", "concept": "COTIZACION CONT.COMU", "units": "4,70", "amount": r2(base_cc * 0.047)},
           {"code": "994", "concept": "COTIZACION MEI", "units": "0,15", "amount": r2(base_cc * 0.0015)},
           {"code": "996", "concept": "COTIZACION FORMACION", "units": "0,10", "amount": r2(base_at * 0.001)},
           {"code": "997", "concept": "COTIZACION DESEMPLEO", "units": "1,55", "amount": r2(base_at * 0.0155)}]
    if horas_extra:
        ded.append({"code": "998", "concept": "COTIZACION HORAS EXT 4,70", "units": "", "amount": r2(horas_extra * 0.047)})
    ded.append({"code": "999", "concept": "TRIBUTACION I.R.P.F.", "units": f"{irpf_pct:.2f}".replace(".", ","), "amount": r2(gross * irpf_pct / 100)})
    tot = r2(sum(d["amount"] for d in ded))
    return {"period": {"month": month, "year": "2026", "days": 30},
            "company": {"name": "EMPRESA PRUEBA SL", "cif": "B00000000"}, "worker": {"name": "TRABAJADOR PRUEBA"},
            "employment": {"category": "Oficial", "contractCode": "100"},
            "earnings": earnings, "deductions": ded,
            "totals": {"grossTotal": gross, "totalDeductions": tot, "netPay": r2(gross - tot)},
            "bases": {"totalRemuneration": r2(gross - horas_extra), "extraPayProrata": prorrata, "baseCC": base_cc,
                      "baseAT": base_at, "baseIRPF": gross, "irpfPercentage": irpf_pct}}


def filas_corridas(d):
    """Como septiembre: falta el MEI, cada importe sube a la fila de arriba desde formación y el IRPF se lee «I.R.P.P.»"""
    x = json.loads(json.dumps(d))
    ded = x["deductions"]
    amounts = [l["amount"] for l in ded]
    mei = next(i for i, l in enumerate(ded) if "MEI" in l["concept"])
    del ded[mei]
    del amounts[mei + 1]                     # el importe de formación se pierde…
    for i, l in enumerate(ded):              # …y desde el MEI cada fila coge el importe de la siguiente
        l["amount"] = amounts[i] if i < mei else amounts[i + 1] if i + 1 < len(amounts) else amounts[-1]
    ded[-1]["amount"] = amounts[-2]          # el IRPF se queda con el de desempleo
    ded[-1]["concept"] = "TRIBUTACION I.R.P.P."
    ded[0]["code"], ded[1]["code"] = "995", "994"   # y los códigos de arriba también corridos
    return x


def precio_como_importe(d):
    """Como agosto: en los devengos se toma el precio por día como importe"""
    x = json.loads(json.dumps(d))
    x["earnings"][0]["amount"] = x["earnings"][0]["price"]
    return x


ENE, FEB, MAR = nomina("Enero"), nomina("Febrero", incentivos=150.25), nomina("Marzo", horas_extra=107.28)
ABR = nomina("Abril", salario=2100.10, plus=282.03, incentivos=1114.80, irpf_pct=20.19)
ABR_MAL = filas_corridas(ABR)
MAY = nomina("Mayo", salario=2100.10, plus=282.03, incentivos=980.00, irpf_pct=20.19)
MAY_MAL = precio_como_importe(MAY)

fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()

def new_page(browser, dialogs):
    ctx = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    ctx.route("**/jszip.min.js", lambda r: r.fulfill(path=JSZIP, content_type="application/javascript", headers=CORS))
    ctx.route("**/qrcode.min.js", lambda r: r.fulfill(body="", content_type="application/javascript"))
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    def on_dialog(d):
        dialogs.append((d.type, d.message))
        ans = answers.pop(0) if answers else True
        if ans is False: d.dismiss()
        elif isinstance(ans, str): d.accept(ans)
        else: d.accept()
    page.on("dialog", on_dialog)
    page.goto(APP)
    page.evaluate("""async () => { localStorage.clear(); localStorage.setItem('nomina-auditor-autobackup','false');
        localStorage.setItem('nomina-auditor-apikey','AIzaTEST-FAKE-KEY-123');
        await new Promise(r => { const q = indexedDB.deleteDatabase('nomina-auditor-docs'); q.onsuccess = q.onerror = q.onblocked = r; }); }""")
    page.reload(); page.wait_for_timeout(300)
    return ctx, page, errors

answers = []   # respuestas a los diálogos, en orden: True = aceptar, False = cancelar, "texto" = escribir

def seed(page, recs):
    page.evaluate("(r) => { localStorage.setItem('nomina-auditor-data', JSON.stringify(r)); }", recs)
    page.reload(); page.wait_for_timeout(300)

def stub_reads(page, reads):
    """callGemini simulada: devuelve las lecturas en orden y apunta con qué se la llamó"""
    page.evaluate("""(reads) => { window._reads = reads.slice(); window._calls = [];
        window.callGemini = async (b64, type, extra) => { window._calls.push({len: (b64||'').length, b64head: (b64||'').slice(0, 40), type, extra: extra || ''});
            const r = window._reads.shift(); if (!r) throw new Error('sin más lecturas'); return JSON.parse(JSON.stringify(r)); }; }""", reads)

def upload(page, path, reads):
    stub_reads(page, reads)
    page.evaluate("showView('upload')")
    page.set_input_files("#fileInput", path)
    page.wait_for_selector("#uploadBtns:not(.hidden)", timeout=5000)
    page.click("#processBtn")
    page.wait_for_selector("#verifyPhase:not(.hidden) #checksCard", timeout=5000)
    page.wait_for_timeout(150)

P = lambda page, pid: page.evaluate("(id) => payrolls.find(p => p.id === id)", pid)


with sync_playwright() as pw:
    b = pw.chromium.launch()
    dialogs = []
    ctx, page, errors = new_page(b, dialogs)

    print("1) Números: formato con punto de miles y lectura como los escribe una persona")
    for v, exp in [(2100.1, "2.100,10"), (21000, "21.000,00"), (999.5, "999,50"), (-1234.5, "-1.234,50"), (0, "0,00"),
                   (1234567.891, "1.234.567,89"), ("N/L", "N/L"), (None, "N/L"), ("abc", "N/L"), (0.005, "0,01")]:
        got = page.evaluate("v => fmt(v)", v)
        check(got == exp, f"fmt({v!r}) = {got!r}")
    for s_, exp in [("2.100,10", 2100.1), ("2100,10", 2100.1), ("2100.10", 2100.1), ("2.100", 2100), ("20,5", 20.5),
                    ("1.234.567,89", 1234567.89), ("1,234.56", 1234.56), ("  2 100,10 €", 2100.1), ("-12,5", -12.5)]:
        got = page.evaluate("s => num(s)", s_)
        check(abs(got - exp) < 1e-9, f"num({s_!r}) = {got}")
    check(page.evaluate("Number.isNaN(num('N/L')) && Number.isNaN(num('')) && amt('N/L') === 0"), "N/L y vacío no son números y suman 0")

    print("2) Qué es cada línea de deducción (lo decide el código, no la IA)")
    kinds = {"COTIZACION CONT.COMU 4,70": "cc", "Contingencias comunes": "cc", "CONTING. COMUNES": "cc", "Cotiz. CC 4,70%": "cc",
             "COTIZACION MEI 0,15": "mei", "M.E.I.": "mei", "COTIZACION FORMACION 0,10": "fp", "Formación Prof.": "fp",
             "COTIZACION DESEMPLEO 1,55": "desempleo", "Cotización adicional solidaridad": "solidaridad", "COTIZACION HORAS EXT 4,70": "ss",
             "TRIBUTACION I.R.P.F.20,42": "irpf", "TRIBUTACION I.R.P.P.20,19": "irpf", "RETENCION IRPF": "irpf",
             "Retención judicial": "otra", "Embargo de salario": "otra", "Anticipo": "otra", "Dcto.Conceptos en Especie": "especie"}
    for c, exp in kinds.items():
        got = page.evaluate("c => deductionKind({concept: c})", c)
        check(got == exp, f"«{c}» → {got}")

    print("3) S.S. e IRPF con los textos reales de las nóminas")
    ss = page.evaluate("d => calcSSTotal(d)", ENE)
    exp = r2(sum(l["amount"] for l in ENE["deductions"] if "COTIZACION" in l["concept"]))
    check(abs(ss - exp) < 0.005, f"S.S. = CONT.COMU + MEI + formación + desempleo = {ss} (antes de la v2.7.2 solo contaba formación y desempleo)")
    ss = page.evaluate("d => calcSSTotal(d)", MAR)
    exp = r2(sum(l["amount"] for l in MAR["deductions"] if "COTIZACION" in l["concept"]))
    check(abs(ss - exp) < 0.005, f"incluye la cotización de horas extra: {ss}")
    irpf = page.evaluate("d => findIRPFDeduction(d)", {**ENE, "deductions": [{**l, "concept": "TRIBUTACION I.R.P.P."} if l["code"] == "999" else l for l in ENE["deductions"]]})
    check(irpf == ENE["deductions"][-1]["amount"], f"IRPF leído como «I.R.P.P.» se encuentra igual: {irpf}")
    raro = {**ENE, "deductions": [{**l, "concept": "Dto. 999 XX"} if l["code"] == "999" else l for l in ENE["deductions"]]}
    irpf = page.evaluate("d => findIRPFDeduction(d)", raro)
    check(irpf == ENE["deductions"][-1]["amount"], f"con el concepto ilegible, se encuentra por la cuenta base × %: {irpf}")
    na = {**ENE, "deductions": ENE["deductions"] + [{"concept": "COTIZACION OTRA", "amount": "N/L"}]}
    check(page.evaluate("d => typeof calcSSTotal(d) === 'number' && calcSSTotal(d) > 0", na), "un importe «N/L» no rompe la suma")

    print("4) Comprobaciones")
    seed(page, [{**ENE, "id": "2026-01"}, {**FEB, "id": "2026-02"}, {**MAR, "id": "2026-03"}])
    for name, d in [("enero", ENE), ("febrero", FEB), ("marzo (horas extra)", MAR), ("abril", ABR), ("mayo", MAY)]:
        c = page.evaluate("d => checkPayroll(d)", d)
        check(c == [], f"{name} correcta: sin avisos {[x['text'] for x in c]}")
    c = page.evaluate("d => checkPayroll(d)", ABR_MAL)
    keys = [x["key"] for x in c]
    check("sumD" in keys and next(x for x in c if x["key"] == "sumD")["level"] == "err", "filas corridas: las deducciones no suman el total (error)")
    check("irpf" in keys, "filas corridas: el IRPF no es base × %")
    check(any(k.startswith("ss") for k in keys), "filas corridas: alguna cotización no es base × %")
    check(any(k.startswith("tpl-") for k in keys), "filas corridas: el código no lleva el concepto de tus otras nóminas")
    check(all(x["paths"] for x in c), "cada aviso dice qué celdas marcar")
    c = page.evaluate("d => checkPayroll(d)", MAY_MAL)
    keys = [x["key"] for x in c]
    check("sumE" in keys, "precio tomado como importe: los devengos no suman el bruto (error)")
    check(any(k.startswith("up-") for k in keys), "precio tomado como importe: unidades × precio ≠ importe")
    neto = json.loads(json.dumps(ENE)); neto["totals"]["netPay"] = 100
    check([x["key"] for x in page.evaluate("d => checkPayroll(d)", neto)] == ["net"], "líquido que no es bruto − deducciones")
    extra = {"period": {"month": "Julio", "year": "2026"}, "payType": "extra",
             "earnings": [{"code": "1", "concept": "Salario Base", "amount": 2100.10}],
             "deductions": [{"code": "999", "concept": "TRIBUTACION I.R.P.F.", "amount": 428.63}],
             "totals": {"grossTotal": 2100.10, "totalDeductions": 428.63, "netPay": 1671.47},
             "bases": {"baseCC": "N/L", "baseIRPF": 2100.10, "irpfPercentage": 20.41}}
    check(page.evaluate("d => checkPayroll(d)", extra) == [], "paga extra sin cotizaciones y con bases N/L: sin avisos")

    print("5) Subida con la primera lectura mala: segunda lectura automática que sí cuadra")
    upload(page, FX + "nomina_julio.jpg", [ABR_MAL, ABR])
    calls = page.evaluate("window._calls")
    check(len(calls) == 2, f"Gemini se ha llamado 2 veces: {len(calls)}")
    check(calls[0]["extra"] == "", "la primera lectura va sin instrucciones extra")
    ex = calls[1]["extra"]
    check("SEGUNDA lectura" in ex and "Las deducciones suman" in ex, "la segunda dice qué cuentas no cuadran")
    check("995 COTIZACION CONT.COMU" in ex, "y da como referencia los códigos de tus otras nóminas")
    check(page.evaluate("readScore(extractedData) === 0"), "se queda con la lectura que cuadra")
    v = page.inner_text("#verifyPhase")
    check("la segunda sí cuadra" in v and "Las cuentas cuadran" in v, "lo explica en la revisión")
    page.screenshot(path=S + "80_segunda_lectura_ok.png", full_page=True)
    page.evaluate("clearUpload()")

    print("6) Las dos lecturas malas: se muestra la menos mala, con las celdas marcadas")
    upload(page, FX + "nomina_julio.jpg", [ABR_MAL, ABR_MAL])
    check(page.evaluate("window._calls.length") == 2, "dos lecturas")
    v = page.inner_text("#verifyPhase")
    check("ninguna lectura cuadra" in v and "no cuadran" in v, "avisa de que no cuadra")
    check(page.locator("#verifyPhase .flag-err").count() >= 3, f"celdas marcadas en rojo: {page.locator('#verifyPhase .flag-err').count()}")
    check(page.is_visible("#rereadBtn") and page.is_visible("text=👁 Ver documento"), "botones Releer y Ver documento")
    page.screenshot(path=S + "81_no_cuadra.png", full_page=True)
    page.click("text=👁 Ver documento"); page.wait_for_timeout(200)
    check(page.is_visible("#docViewer img"), "se ve la foto mientras se revisa")
    page.click("#docViewer >> text=✕ Cerrar")

    print("7) Releer a mano desde la revisión")
    stub_reads(page, [ABR])
    page.click("#rereadBtn"); page.wait_for_timeout(300)
    check("Las deducciones suman" in page.evaluate("window._calls[0].extra"), "la nueva lectura lleva los fallos")
    check(page.evaluate("readScore(extractedData) === 0") and "ahora las cuentas cuadran" in page.inner_text("#verifyPhase"), "y se queda con ella porque cuadra")
    stub_reads(page, [ABR_MAL])
    page.click("text=Descartar")
    upload(page, FX + "nomina_julio.jpg", [MAY_MAL, MAY_MAL])
    before = page.evaluate("JSON.stringify(extractedData)")
    stub_reads(page, [ABR_MAL])   # cuadra aún peor (otro mes, más errores): no se cambia
    page.evaluate("extractedData.deductions[0].amount = 0.74"); page.click("#rereadBtn"); page.wait_for_timeout(300)
    check(page.evaluate("JSON.stringify(extractedData)") == before and "cuadraba peor" in page.inner_text("#verifyPhase"), "si la nueva cuadra peor, se queda la que había")

    print("8) Corregir a mano: importes con punto de miles, añadir y quitar líneas")
    page.evaluate("clearUpload()")
    upload(page, FX + "nomina_julio.jpg", [MAY_MAL, MAY_MAL])
    page.locator("#verifyPhase span.editable[onclick*=\"'earnings.0.amount'\"]").click()
    page.fill(".edit-input", "2.100,10"); page.keyboard.press("Enter"); page.wait_for_timeout(150)
    check(page.evaluate("extractedData.earnings[0].amount") == 2100.1, "«2.100,10» se guarda como 2100,10 (antes se guardaba 2,1)")
    check("2.100,10" in page.inner_text("#verifyPhase"), "y se ve con punto de miles")
    check(page.evaluate("checkErrors(extractedData).length") == 0 and "Las cuentas cuadran" in page.inner_text("#checksCard"), "corregida la celda, todo cuadra")
    n = page.evaluate("extractedData.deductions.length")
    page.locator("#verifyPhase .link-btn", has_text="Añadir línea").nth(1).click(); page.wait_for_timeout(100)
    check(page.evaluate("extractedData.deductions.length") == n + 1, "añadir una línea de deducción")
    check("no cuadran" not in page.inner_text("#checksCard"), "una línea vacía (0 €) no descuadra")
    answers.append(str(n + 1))
    page.locator("#verifyPhase .link-btn", has_text="Quitar una línea").nth(1).click(); page.wait_for_timeout(100)
    check(page.evaluate("extractedData.deductions.length") == n, "quitar esa línea por su número")
    answers.append("99")
    page.locator("#verifyPhase .link-btn", has_text="Quitar una línea").nth(1).click(); page.wait_for_timeout(100)
    check(page.evaluate("extractedData.deductions.length") == n, "un número que no existe no quita nada")

    print("9) Guardar una que no cuadra: hay que confirmarlo, y queda marcada")
    page.evaluate("clearUpload()")
    page.evaluate("payrolls = []; saveData(); refreshDocKeys()")
    seed(page, [{**ENE, "id": "2026-01"}, {**FEB, "id": "2026-02"}, {**MAR, "id": "2026-03"}])
    upload(page, FX + "nomina_julio.jpg", [ABR_MAL, ABR_MAL])
    dialogs.clear(); answers.append(False)
    page.click("text=✓ Confirmar y Guardar"); page.wait_for_timeout(300)
    check(dialogs and dialogs[0][0] == "confirm" and "no cuadran" in dialogs[0][1], "pide confirmación explicando qué no cuadra")
    check(P(page, "2026-04") is None and page.is_visible("#verifyPhase"), "si cancelas, no se guarda y sigues en la revisión")
    answers.append(True)
    page.click("text=✓ Confirmar y Guardar"); page.wait_for_timeout(500)
    check(P(page, "2026-04") is not None, "si aceptas, se guarda")
    rc = page.inner_text("#reportContent")
    check("Las cuentas no cuadran" in rc and "✏ Corregir datos" in rc and "🔁 Releer con Gemini" in rc, "Ver: avisa y ofrece corregir o releer")
    txt = page.evaluate("document.getElementById('reportContent')._reportText")
    check(txt.startswith("⚠ AVISO: LAS CUENTAS DE ESTA NÓMINA NO CUADRAN") and "5. AVISOS DE LA COMPROBACIÓN" in txt, "la copia para el abogado lo avisa arriba y lo detalla al final")
    page.screenshot(path=S + "82_ver_no_cuadra.png", full_page=True)
    page.evaluate("currentYear='2026'; showView('dashboard')"); page.wait_for_timeout(200)
    dt = page.inner_text("#dashTable")
    check("1 nómina no cuadra: Abril 2026" in dt and page.locator("#dashTable .chk-flag").count() == 1, "Panel: aviso y ⚠ solo en abril")
    page.screenshot(path=S + "83_panel_no_cuadra.png", full_page=True)
    page.evaluate("showView('annual')"); page.wait_for_timeout(200)
    an = page.inner_text("#annualContent")
    check("LAS CUENTAS NO CUADRAN en: Abril 2026" in an and page.locator("#annualContent .chk-flag").count() == 1, "Anual: aviso en observaciones y ⚠ en la fila")

    print("10) ✏ Corregir una nómina guardada (con su original)")
    page.evaluate("currentYear='2026'; showReport(payrolls.find(p => p.id === '2026-04'))"); page.wait_for_timeout(200)
    before = P(page, "2026-04")
    check(before.get("original", {}).get("key"), "la guardada tiene su documento original")
    page.click("#reportContent >> text=✏ Corregir datos"); page.wait_for_timeout(200)
    v = page.inner_text("#verifyPhase")
    check("Estás corrigiendo la nómina guardada de Abril 2026" in v and "Guardar cambios" in v, "abre la revisión en modo corrección")
    check(not page.is_visible(".keep-original"), "sin casilla de guardar original (ya lo tiene)")
    page.screenshot(path=S + "84_corregir.png", full_page=True)
    page.evaluate("showView('dashboard')"); page.wait_for_timeout(100)
    check(page.evaluate("editingId") is None and P(page, "2026-04") == before, "salir sin guardar no cambia nada")

    print("11) 🔁 Releer desde Ver con el documento guardado")
    stub_reads(page, [ABR])
    page.evaluate("showReport(payrolls.find(p => p.id === '2026-04'))"); page.wait_for_timeout(200)
    page.click("#reportContent >> text=🔁 Releer con Gemini"); page.wait_for_timeout(500)
    c0 = page.evaluate("window._calls[0]")
    stored = page.evaluate("async (k) => { const r = await getDoc(k); const b = arrayBufferToB64(r.data); return {head: b.slice(0, 40), len: b.length}; }", before["original"]["key"])
    check(c0["b64head"] == stored["head"] and c0["len"] == stored["len"], "relee el documento guardado, sin volver a subirlo")
    check(c0["type"] == "image/jpeg" and "SEGUNDA lectura" in c0["extra"], "como foto y diciendo qué fallaba")
    check(page.evaluate("editingId") == "2026-04" and "ahora las cuentas cuadran" in page.inner_text("#verifyPhase"), "queda en la revisión con la lectura buena")
    check(page.evaluate("typeDetection && typeDetection.saved === true") and "Guardada como" in page.inner_text("#verifyPhase"), "respeta el tipo con el que estaba guardada")
    page.click("text=✓ Guardar cambios"); page.wait_for_timeout(400)
    after = P(page, "2026-04")
    check(after["original"]["key"] == before["original"]["key"], "conserva su documento original")
    check(after["savedAt"] == before["savedAt"] and after.get("editedAt"), "conserva la fecha de guardado y apunta la corrección")
    check(page.evaluate("checkErrors(payrolls.find(p => p.id === '2026-04')).length") == 0, "ya cuadra")
    check([p["id"] for p in page.evaluate("payrolls")] == ["2026-01", "2026-02", "2026-03", "2026-04"], "no se duplica")
    check("Las cuentas cuadran" in page.inner_text("#reportContent"), "Ver: ✓ las cuentas cuadran")

    print("12) Corregir el mes: solo a un hueco libre")
    page.click("#reportContent >> text=✏ Corregir datos"); page.wait_for_timeout(200)
    page.locator("#verifyPhase tr", has=page.locator("td.dim", has_text="Mes")).locator("span.editable").click()
    page.fill(".edit-input", "Marzo"); page.keyboard.press("Enter"); page.wait_for_timeout(100)
    dialogs.clear(); answers.append(True)
    page.click("text=✓ Guardar cambios"); page.wait_for_timeout(300)
    check(dialogs and "Ya tienes guardada la nómina mensual de Marzo" in dialogs[-1][1], "a un mes ocupado: avisa")
    check([p["id"] for p in page.evaluate("payrolls")] == ["2026-01", "2026-02", "2026-03", "2026-04"] and P(page, "2026-03")["period"]["month"] == "Marzo"
          and P(page, "2026-03")["totals"] == MAR["totals"], "y no pisa nada")
    page.locator("#verifyPhase tr", has=page.locator("td.dim", has_text="Mes")).locator("span.editable").click()
    page.fill(".edit-input", "Junio"); page.keyboard.press("Enter"); page.wait_for_timeout(100)
    page.click("text=✓ Guardar cambios"); page.wait_for_timeout(300)
    ids = [p["id"] for p in page.evaluate("payrolls")]
    check(ids == ["2026-01", "2026-02", "2026-03", "2026-06"], f"a un mes libre: se mueve {ids}")
    check(P(page, "2026-06")["original"]["key"] == before["original"]["key"], "con su documento original")
    check(page.evaluate("listDocKeys()") == [before["original"]["key"]], "sin documentos huérfanos")
    page.click("#reportContent >> text=✏ Corregir datos"); page.wait_for_timeout(200)
    page.click("#verifyPhase >> text=Cancelar"); page.wait_for_timeout(200)
    check(page.evaluate("editingId") is None and page.is_visible("#view-report") and "Junio" in page.inner_text("#reportContent"), "Cancelar vuelve a Ver sin cambios")

    print("13) Una subida nueva después de corregir no hereda el modo corrección")
    upload(page, FX + "nomina_junio_foto.jpg", [MAY])
    check(page.evaluate("editingId") is None and "Confirmar y Guardar" in page.inner_text("#verifyPhase"), "revisión normal")
    page.click("text=✓ Confirmar y Guardar"); page.wait_for_timeout(400)
    check(P(page, "2026-05") is not None and len(page.evaluate("listDocKeys()")) == 2, "se guarda como nueva con su documento")

    print("14) Lo que se envía a Gemini (sin salir a internet)")
    sent, req = [], []
    def gemini(route):
        sent.append(json.loads(route.request.post_data))
        req.append({"url": route.request.url, "headers": route.request.headers})
        route.fulfill(status=200, content_type="application/json",
                      body=json.dumps({"candidates": [{"content": {"parts": [{"text": json.dumps(ABR)}]}}]}))
    page.route("https://generativelanguage.googleapis.com/**", gemini)
    page.reload(); page.wait_for_timeout(300)
    r = page.evaluate("async () => { const d = await callGemini('QUJD', 'image/jpeg', 'INSTRUCCIONES EXTRA'); return d.period.month; }")
    check(r == "Abril" and len(sent) == 1, "callGemini con instrucciones extra funciona")
    body = sent[0]
    prompt = body["contents"][0]["parts"][1]["text"]
    gc = body["generationConfig"]
    check(prompt.endswith("INSTRUCCIONES EXTRA") and '"price"' in prompt and "NUNCA pongas el precio" in prompt, "prompt con precio aparte y las instrucciones al final")
    clave = page.evaluate("getApiKey()")
    check(clave and req[0]["headers"].get("x-goog-api-key") == clave, "la clave va en la cabecera x-goog-api-key")
    check("key=" not in req[0]["url"] and clave not in req[0]["url"], f"y no en la dirección: {req[0]['url']}")
    check(gc.get("responseMimeType") == "application/json" and gc.get("temperature") == 0 and gc.get("maxOutputTokens", 0) >= 8192, f"respuesta JSON forzada: {gc}")

    print("15) Pantalla estrecha (360 px): el importe y sus marcas siempre a la vista, sin desplazarse a los lados")
    page.unroute("https://generativelanguage.googleapis.com/**")
    page.set_viewport_size({"width": 360, "height": 780}); page.wait_for_timeout(150)
    upload(page, FX + "nomina_julio.jpg", [ABR_MAL, ABR_MAL])
    m = page.evaluate("""() => {
        const W = document.documentElement.clientWidth;
        const out = s => [...document.querySelectorAll(s)].filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > W + 0.5 || r.left < -0.5); }).length;
        const cards = [...document.querySelectorAll('#verifyPhase .card')].filter(c => c.scrollWidth > c.clientWidth + 1).length;
        return { W, page: document.documentElement.scrollWidth, amounts: document.querySelectorAll('#verifyPhase table.lines td.c-amount').length,
                 outAmounts: out('#verifyPhase table.lines td.c-amount span'), outFlags: out('#verifyPhase .flag-err, #verifyPhase .flag-warn'),
                 flags: document.querySelectorAll('#verifyPhase .flag-err').length, cards,
                 head: getComputedStyle(document.querySelector('#verifyPhase table.lines thead')).display };
    }""")
    check(m["amounts"] > 5 and m["outAmounts"] == 0, f"todos los importes dentro de la pantalla: {m}")
    check(m["flags"] >= 3 and m["outFlags"] == 0, "las celdas marcadas en rojo también")
    check(m["cards"] == 0 and m["page"] <= m["W"], "ninguna tabla se desplaza a los lados")
    check(m["head"] == "none", "en estrecho cada línea va en dos filas (sin cabecera de columnas)")
    page.screenshot(path=S + "86_revision_360px.png", full_page=True)
    page.locator("#verifyPhase span.editable[onclick*=\"'deductions.1.units'\"]").click()
    check(page.locator(".edit-input").count() == 1, "las unidades siguen siendo editables")
    page.keyboard.press("Escape")
    page.set_viewport_size({"width": 390, "height": 844})

    check(not errors, f"sin errores JS: {errors}")
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
