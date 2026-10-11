import sys
from playwright.sync_api import sync_playwright
from _comun import APP, OUT


def nom(mid, month, irpf_concept, irpf_amount, pct=0, base_irpf=2500.0, units="", gross=2500.0):
    return {
        "id": mid, "period": {"month": month, "year": "2026"},
        "earnings": [{"concept": "Salario base", "amount": gross}],
        "deductions": [{"concept": irpf_concept, "units": units, "amount": irpf_amount},
                       {"concept": "Contingencias comunes", "amount": 125.4}],
        "totals": {"grossTotal": gross, "totalDeductions": irpf_amount + 125.4, "netPay": gross - irpf_amount - 125.4},
        "bases": {"baseCC": 2500.0, "baseIRPF": base_irpf, "irpfPercentage": pct},
    }

ABR = nom("2026-04", "Abril", "TRIBUTACIÓN IRPF", 406.0, pct=16.24)          # % leído de la nómina
MAY = nom("2026-05", "Mayo", "TRIBUTACIÓN IRPF.16,24", 406.0, pct="N/L")     # % solo en el concepto
JUN = nom("2026-06", "Junio", "TRIBUTACION I.R.P.F.", 406.0, pct=0)          # sin %: se calcula
JUL = nom("2026-07", "Julio", "RETENCION IRPF", 406.0, pct=0, base_irpf=0)   # sin base: aproximado
AGO = nom("2026-08", "Agosto", "IRPF", 0, pct=0)                              # imposible: N/L

fails = []
def check(cond, msg):
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond: fails.append(msg)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    page = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    answers = []
    def on_dialog(d):
        if d.type == "prompt" and answers: d.accept(answers.pop(0))
        else: d.accept()
    page.on("dialog", on_dialog)

    page.goto(APP)
    page.evaluate("""(recs) => { localStorage.clear();
        localStorage.setItem('nomina-auditor-data', JSON.stringify(recs));
        localStorage.setItem('nomina-auditor-autobackup', 'false'); }""", [ABR, MAY, JUN, JUL, AGO])
    page.reload(); page.wait_for_timeout(300)

    print("1) Deducción del % IRPF")
    rate = lambda i: page.evaluate(f"irpfRateOf(payrolls.find(p=>p.id==='{i}'))")
    r = rate("2026-04"); check(r == {"rate": 16.24, "source": "nomina"}, f"abril leído: {r}")
    r = rate("2026-05"); check(r == {"rate": 16.24, "source": "concepto"}, f"mayo del concepto 'IRPF.16,24': {r}")
    r = rate("2026-06"); check(r == {"rate": 16.24, "source": "calculado"}, f"junio calculado 406,00/2500,00: {r}")
    r = rate("2026-07"); check(r["source"] == "aprox" and r["rate"] == 16.24, f"julio aproximado sobre bruto: {r}")
    r = rate("2026-08"); check(r == {"rate": None, "source": None}, f"agosto sin datos: {r}")
    for concept, units, exp in [("IRPF 15%", "", 15), ("I.R.P.F. 2026", "", None), ("TRIBUTACION IRPF", "18,5", 18.5), ("RET. IRPF 7,00 %", "", 7)]:
        got = page.evaluate("([c,u]) => irpfFromLine({concept:c, units:u})", [concept, units])
        check(got == exp, f"irpfFromLine({concept!r}, units={units!r}) = {got}")

    print("2) Panel")
    page.evaluate("currentYear='2026'; renderDashboard()")
    page.wait_for_timeout(200)
    t = page.inner_text("#dashTable")
    check("16,24 %" in t and "N/L%" not in t, "mayo ya no sale N/L% en el panel")
    check("16,24 %*" in t, "los calculados llevan *")
    check("Corregir %" in t, "leyenda con cómo corregirlo")
    page.screenshot(path=OUT + "10_panel_irpf.png", full_page=True)

    print("3) Corregir a mano desde Ver")
    page.evaluate("showReport(payrolls.find(p=>p.id==='2026-08'))"); page.wait_for_timeout(200)
    check("no aparece en la nómina" in page.inner_text("#reportContent"), "agosto avisa de que falta")
    answers.append("19,5")
    page.click("text=✏ Corregir %"); page.wait_for_timeout(200)
    st = page.evaluate("payrolls.find(p=>p.id==='2026-08').bases")
    check(st["irpfPercentage"] == 19.5 and st["irpfSource"] == "manual", f"guardado 19,5 manual: {st}")
    check("corregido a mano" in page.inner_text("#reportContent"), "el informe indica 'corregido a mano'")
    check("% RETENCIÓN IRPF: 19,5 %" in page.inner_text("#reportContent"), "aparece en el texto para el abogado")
    page.screenshot(path=OUT + "11_informe_irpf.png")
    answers.append("abc")
    page.click("text=✏ Corregir %"); page.wait_for_timeout(200)
    check(page.evaluate("payrolls.find(p=>p.id==='2026-08').bases.irpfPercentage") == 19.5, "un valor no válido no cambia nada")
    answers.append("")
    page.click("text=✏ Corregir %"); page.wait_for_timeout(200)
    st = page.evaluate("payrolls.find(p=>p.id==='2026-08').bases")
    check(st["irpfPercentage"] == 0 and "irpfSource" not in st, f"vacío vuelve a automático: {st}")

    print("4) Anual")
    page.evaluate("showView('annual')"); page.wait_for_timeout(200)
    ann = page.inner_text("#annualContent")
    check("Variación en el % de IRPF" in ann, "agosto (N/L) sí cuenta como variación")
    check("% de IRPF calculado" in ann, "nota de los calculados")

    print("5) Subida nueva sin % en las bases")
    d = {k: v for k, v in MAY.items() if k != "id"}; d["period"] = {"month": "Septiembre", "year": "2026"}
    page.evaluate("(d) => { showView('upload'); extractedData = JSON.parse(JSON.stringify(d)); prepareExtracted(extractedData); renderVerification(); }", d)
    v = page.inner_text("#verifyPhase")
    check("16,24" in v and "no venía en las bases" in v, "la verificación lo rellena y avisa")
    page.screenshot(path=OUT + "12_verificacion_irpf.png", full_page=True)
    # editar a mano con coma (antes "20,5" se guardaba como 20)
    page.locator("#verifyPhase tr", has=page.locator("td.dim", has_text="% IRPF")).locator("span.editable").click()
    page.fill(".edit-input", "20,5"); page.keyboard.press("Enter"); page.wait_for_timeout(100)
    b2 = page.evaluate("extractedData.bases")
    check(b2["irpfPercentage"] == 20.5 and b2["irpfSource"] == "manual", f"editar con coma guarda 20,5: {b2['irpfPercentage']} {b2.get('irpfSource')}")

    print("6) Texto del botón de tipo")
    page.evaluate("showReport(payrolls.find(p=>p.id==='2026-05'))"); page.wait_for_timeout(200)
    rc = page.inner_text("#reportContent")
    check("Mensual" in rc and "paga extra o unos atrasos" in rc, "el tipo dice Mensual y explica qué es")

    check(not errors, f"sin errores JS: {errors}")
    b.close()

print("\nRESULTADO:", "TODO OK" if not fails else f"{len(fails)} FALLOS")
sys.exit(1 if fails else 0)
