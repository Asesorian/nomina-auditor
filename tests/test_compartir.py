from playwright.sync_api import sync_playwright
from _comun import APP, OUT as S
ok = True
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    # Simula el menú de compartir de un móvil
    ctx.add_init_script("""
      window.__shared = [];
      navigator.canShare = (d) => !!(d && d.files && d.files.length);
      navigator.share = async (d) => { window.__shared.push({ name: d.files[0].name, type: d.files[0].type, size: d.files[0].size, title: d.title }); };
    """)
    ctx.route("https://fonts.googleapis.com/**", lambda r: r.fulfill(body="", content_type="text/css"))
    ctx.route("**/*.min.js", lambda r: r.fulfill(body="", content_type="application/javascript"))
    p = ctx.new_page(); errs=[]; p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(APP)
    p.evaluate("async () => { localStorage.clear(); localStorage.setItem('nomina-auditor-autobackup','false'); await new Promise(r => { const q = indexedDB.deleteDatabase('nomina-auditor-docs'); q.onsuccess = q.onerror = q.onblocked = r; }); }")
    p.reload(); p.wait_for_timeout(300)
    p.evaluate("""async () => {
      payrolls.push({id:'2026-07-extra', payType:'extra', period:{month:'Julio',year:'2026'}, totals:{grossTotal:1700, netPay:1496}, earnings:[], deductions:[], bases:{}});
      saveData();
      const b64 = btoa('%PDF-1.4 prueba');
      payrolls[0].original = await storeOriginal(b64, 'application/pdf', 'scan.pdf'); saveData();
      showReport(payrolls[0]);
    }""")
    p.wait_for_timeout(400)
    vis = p.is_visible("#originalBody >> text=Guardar en…")
    print(("OK  " if vis else "FAIL"), "en móvil aparece el botón 'Guardar en… (Drive, iCloud…)'"); ok &= vis
    p.locator("#originalBody").scroll_into_view_if_needed()
    p.screenshot(path=S+"56_compartir.png")
    p.click("#originalBody >> text=Guardar en…"); p.wait_for_timeout(300)
    sh = p.evaluate("window.__shared")
    good = len(sh)==1 and sh[0]["name"]=="2026-07 Julio - Paga extra.pdf" and sh[0]["type"]=="application/pdf"
    print(("OK  " if good else "FAIL"), "abre el menú de compartir con el archivo:", sh); ok &= good
    print(("OK  " if not errs else "FAIL"), "sin errores JS", errs); ok &= not errs
    b.close()
print("RESULTADO:", "TODO OK" if ok else "FALLOS")
