import json, sys
from playwright.sync_api import sync_playwright
from _comun import APP, OUT


def nomina(month, year, earnings, gross, net, base_cc=1900, irpf=12.0, prorrata=0, **extra):
    d = {
        "period": {"month": month, "year": year, "days": 30},
        "company": {"name": "EMPRESA TEST SL"}, "worker": {"name": "TRABAJADOR PRUEBA"},
        "employment": {"category": "Oficial", "contractCode": "100"},
        "earnings": [{"code": "", "concept": c, "units": "", "amount": a} for c, a in earnings],
        # Deducciones coherentes con los totales (desde la v2.7.2 la app comprueba que las cuentas cuadren)
        "deductions": [{"concept": "IRPF", "amount": round(gross * irpf / 100, 2)},
                       {"concept": "Contingencias comunes", "amount": round(gross - net - round(gross * irpf / 100, 2), 2)}],
        "totals": {"grossTotal": gross, "totalDeductions": gross - net, "netPay": net},
        "bases": {"totalRemuneration": base_cc - prorrata, "extraPayProrata": prorrata, "baseCC": base_cc,
                  "baseAT": base_cc, "baseIRPF": gross, "irpfPercentage": irpf},
    }
    d.update(extra)
    return d

ORD_JUN = {**nomina("Junio", "2026", [("Salario base", 1700), ("Plus transporte", 100)], 1800, 1500), "id": "2026-06"}
ORD_JUL = {**nomina("Julio", "2026", [("Salario base", 1700), ("Plus transporte", 100)], 1800, 1510), "id": "2026-07"}
EXTRA_JUL = nomina("Julio", "2026", [("PAGA EXTRA VERANO", 1700)], 1700, 1496, base_cc=0, payType="extra", payLabel="Paga Extra Verano")

fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("dialog", lambda d: d.accept())

    def seed(records):
        page.goto(APP)
        page.evaluate("""(recs) => { localStorage.clear();
            localStorage.setItem('nomina-auditor-data', JSON.stringify(recs));
            localStorage.setItem('nomina-auditor-autobackup', 'false'); }""", records)
        page.reload()
        page.wait_for_timeout(300)

    def ids():
        return page.evaluate("payrolls.map(p => p.id)")

    def process(d):
        page.evaluate("""(d) => { showView('upload'); extractedData = JSON.parse(JSON.stringify(d));
            prepareExtracted(extractedData); renderVerification(); }""", d)

    print("\n1) Clasificación automática")
    cases = [
        ("mensual normal", nomina("Marzo", "2026", [("Salario base", 1700), ("Plus", 100)], 1800, 1500), "ordinaria"),
        ("mensual con prorrata pagas extras", nomina("Marzo", "2026", [("Salario base", 1500), ("Prorrata pagas extras", 300)], 1800, 1500, prorrata=300), "ordinaria"),
        ("mensual que incluye la extra como línea", nomina("Junio", "2026", [("Salario base", 1700), ("Paga extra junio", 1700)], 3400, 2800), "ordinaria"),
        ("extra sola (concepto)", nomina("Julio", "2026", [("P. EXTRA VERANO", 1700)], 1700, 1496), "extra"),
        ("extra por pista de Gemini", nomina("Julio", "2026", [("Salario base", 1500), ("Antigüedad", 200)], 1700, 1496, payType="extra"), "extra"),
        ("gratificación extraordinaria Navidad", nomina("Diciembre", "2026", [("Gratificación extraordinaria Navidad", 1700)], 1700, 1496), "extra"),
        ("horas extraordinarias NO es extra", nomina("Mayo", "2026", [("Salario base", 1000), ("Horas extraordinarias", 900)], 1900, 1600), "ordinaria"),
        ("atrasos de convenio", nomina("Abril", "2026", [("Atrasos convenio 2025", 640)], 640, 560), "atrasos"),
    ]
    page.goto(APP)
    for name, d, exp in cases:
        got = page.evaluate("(d) => classifyPayroll(d).type", d)
        check(got == exp, f"{name}: {got} (esperado {exp})")
    for raw, exp in [("JULIO", "Julio"), ("julio", "Julio"), ("7", "Julio"), ("Setiembre", "Septiembre"), ("Jul", None)]:
        got = page.evaluate("(m) => normalizeMonth(m)", raw)
        check(got == exp, f"normalizeMonth({raw!r}) = {got}")

    print("\n2) Subir la extra de julio con la mensual de julio ya guardada (backup antiguo sin tipo)")
    seed([ORD_JUN, ORD_JUL])
    process(EXTRA_JUL)
    page.screenshot(path=OUT + "01_verificacion_extra.png", full_page=False)
    check("Paga extra" in page.inner_text("#verifyPhase"), "la verificación muestra el selector con Paga extra")
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(200)
    check(page.is_hidden("#dupModal"), "no salta el aviso: va directa a su hueco")
    check(ids() == ["2026-06", "2026-07", "2026-07-extra"], f"ids = {ids()}")
    jul = page.evaluate("payrolls.find(p => p.id === '2026-07').totals.netPay")
    check(jul == 1510, "la mensual de julio sigue intacta (neto 1510)")

    print("\n3) Detección fallida → el usuario guarda como ordinaria → aviso con opciones")
    seed([ORD_JUN, ORD_JUL])
    process(EXTRA_JUL)
    page.click("button.type-opt:has-text('Mensual')")
    check("Elegido por ti" in page.inner_text("#verifyPhase"), "marca la elección manual")
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(200)
    check(page.is_visible("#dupModal"), "salta el aviso de hueco ocupado")
    page.screenshot(path=OUT + "02_aviso_duplicado.png")
    body = page.inner_text("#dupModal")
    check("distintos" in body and "1.510,00" in body and "1.496,00" in body, "compara importes guardada vs nueva (con punto de miles)")
    page.click("#dupModalBtns button:has-text('Es una paga extra')")
    page.wait_for_timeout(200)
    check(ids() == ["2026-06", "2026-07", "2026-07-extra"], f"guardada aparte: {ids()}")

    print("\n4) Misma nómina subida dos veces")
    seed([ORD_JUN, ORD_JUL])
    d = {k: v for k, v in ORD_JUL.items() if k != "id"}
    process(d)
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(200)
    check("mismos importes" in page.inner_text("#dupModal"), "detecta que es la misma")
    page.screenshot(path=OUT + "03_aviso_misma.png")
    page.click("text=Cancelar — ya la tengo")
    check(ids() == ["2026-06", "2026-07"], "cancelar no toca nada")

    print("\n5) Segunda paga extra en el mismo mes")
    seed([ORD_JUN, ORD_JUL, {**EXTRA_JUL, "id": "2026-07-extra"}])
    process(nomina("Julio", "2026", [("PAGA BENEFICIOS", 900)], 900, 790, payType="extra", payLabel="Paga de beneficios"))
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(200)
    page.click("#dupModalBtns button:has-text('distinta')")
    page.wait_for_timeout(200)
    check(ids() == ["2026-06", "2026-07", "2026-07-extra", "2026-07-extra-2"], f"ids = {ids()}")
    page.evaluate("currentYear='2026'; showView('dashboard')")
    dt = page.inner_text("#dashTable")
    check("Paga extra 2" in dt and dt.count("Paga extra") == 2, "la segunda se ve como 'Paga extra 2'")
    page.locator("#dashTable").screenshot(path=OUT + "40_panel_dos_extras.png")

    print("\n6) Caso de versiones anteriores a la 2.3: la extra machacó la mensual de julio → reclasificar y recuperar")
    broken = {**EXTRA_JUL, "id": "2026-07"}
    broken.pop("payType"); broken.pop("payLabel")
    seed([ORD_JUN, broken])
    page.evaluate("showReport(payrolls.find(p => p.id === '2026-07'))")
    page.wait_for_timeout(200)
    page.screenshot(path=OUT + "04_informe_cambiar_tipo.png")
    page.click("#reportContent button.type-opt:has-text('Paga extra')")
    page.wait_for_timeout(200)
    check(ids() == ["2026-06", "2026-07-extra"], f"reclasificada: {ids()}")
    check(page.inner_text("#reportContent .type-badge") == "Paga extra", "el título del informe dice solo 'Paga extra'")
    # importar un backup antiguo (formato v2.1) que tenía la mensual de julio
    old_backup = json.dumps({"_meta": {"app": "Nomina Auditor Forense", "version": "2.1", "exportedAt": "2026-07-01T10:00:00Z"},
                             "payrolls": [ORD_JUN, ORD_JUL]})
    page.evaluate("(t) => { showView('backup'); processImportedJSON(t, document.getElementById('importResult')); }", old_backup)
    page.wait_for_timeout(200)
    check(ids() == ["2026-06", "2026-07", "2026-07-extra"], f"backup antiguo recupera la mensual sin tocar la extra: {ids()}")
    page.evaluate("renderBackupView()")
    page.screenshot(path=OUT + "05_backup.png", full_page=True)

    print("\n7) Panel y anual")
    page.evaluate("currentYear='2026'; showView('dashboard')")
    page.wait_for_timeout(200)
    page.screenshot(path=OUT + "06_panel.png", full_page=True)
    sub = page.inner_text("#dashSubtitle")
    check("2 mensuales + 1 extra" in sub, f"subtítulo: {sub}")
    page.evaluate("showView('annual')")
    page.wait_for_timeout(200)
    page.screenshot(path=OUT + "07_anual.png", full_page=True)
    ann = page.inner_text("#annualContent")
    check("Sin nómina mensual registrada: Enero, Febrero, Marzo, Abril, Mayo" in ann, "avisa de meses sin mensual")
    check("Base de Cotización estable" in ann, "la extra (base 0) no da falsa alarma de base de cotización")
    check("Julio (Paga extra)" in ann, "lista la extra en observaciones")
    tot = page.evaluate("calcTotals(payrolls).neto")
    check(abs(tot - (1500 + 1510 + 1496)) < 0.01, f"totales incluyen la extra: {tot}")

    print("\n8) Mes ilegible no se guarda en un hueco basura")
    seed([ORD_JUN])
    bad = nomina("N/L", "2026", [("Salario base", 1700)], 1700, 1400)
    process(bad)
    page.click("text=✓ Confirmar y Guardar")
    page.wait_for_timeout(200)
    check(ids() == ["2026-06"], "bloquea el guardado hasta corregir el mes")

    check(not errors, f"sin errores JS: {errors}")
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
