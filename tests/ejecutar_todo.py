#!/usr/bin/env python3
"""Ejecuta todas las pruebas de Nómina Auditor en un navegador real (Chromium, tamaño móvil).

Uso (desde la raíz del repositorio):
    python tests/ejecutar_todo.py            # todas
    python tests/ejecutar_todo.py visor irpf # solo las que contengan esas palabras

Antes, una sola vez:  cd tests && npm install   (ver tests/README.md)
"""
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent
OUT = TESTS / "output"

# (nombre, archivo, necesita: None | "site" | "pages")
SUITES = [
    ("Pagas extra, atrasos y duplicados", "test_pagas_extra.py", None),
    ("% de IRPF y corrección a mano", "test_irpf.py", None),
    ("API key por QR", "test_qr.py", None),
    ("Documentos originales y backup completo", "test_originales.py", None),
    ("Compartir a Drive/iCloud", "test_compartir.py", None),
    ("Visor de PDF", "test_visor_pdf.py", None),
    ("Modo sin conexión", "test_sin_conexion.py", "site"),
    ("Visor de PDF sin conexión", "test_pdf_sin_conexion.py", "site"),
    ("Versión nueva a la primera (caché de GitHub Pages)", "test_actualizacion.py", "pages"),
]


def port_open(port):
    with socket.socket() as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def wait_port(port, timeout=10):
    t = time.time()
    while time.time() - t < timeout:
        if port_open(port):
            return True
        time.sleep(0.2)
    return False


def comprobar_librerias():
    """Las librerías locales deben ser exactamente las que carga la app (misma versión y misma huella SRI)."""
    import base64
    import hashlib
    import json
    import re
    from _comun import APP_FILE, PDFJS, PDFJS_VERSION, PDFJS_SRI

    html = Path(APP_FILE).read_text(encoding="utf-8")
    jszip_app = re.search(r"/jszip/(\d+\.\d+\.\d+)/", html).group(1)
    for paquete, en_app in (("jszip", jszip_app), ("pdfjs-dist", PDFJS_VERSION)):
        instalada = json.loads((TESTS / "node_modules" / paquete / "package.json").read_text(encoding="utf-8"))["version"]
        if instalada != en_app:
            sys.exit(f"La app usa {paquete} {en_app}, pero en tests/node_modules está la {instalada}.\n"
                     f'Pon "{paquete}": "{en_app}" en tests/package.json y ejecuta:  cd tests && npm install')

    if len(PDFJS_SRI) != 2:
        sys.exit("No encuentro las huellas SRI de PDF.js en index.html (constante PDFJS_FILES).")
    for nombre, sri in PDFJS_SRI.items():
        real = "sha384-" + base64.b64encode(hashlib.sha384((Path(PDFJS) / nombre).read_bytes()).digest()).decode()
        if real != sri:
            sys.exit(f"La huella SRI de {nombre} en index.html no coincide con el archivo de PDF.js {PDFJS_VERSION}:\n"
                     f"  index.html: {sri}\n  archivo:    {real}\n"
                     "Si has cambiado de versión, pon la huella nueva en PDFJS_FILES (ver docs/TECNICO.md).")


def fresh_copy(name):
    """Copia limpia de index.html + sw.js en output/<name>/nomina-auditor/ (algunas pruebas la modifican)."""
    base = OUT / name
    shutil.rmtree(base, ignore_errors=True)
    dest = base / "nomina-auditor"
    dest.mkdir(parents=True)
    for f in ("index.html", "sw.js"):
        shutil.copy(ROOT / f, dest / f)
    return base, dest / "index.html"


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    filtros = [a.lower() for a in sys.argv[1:]]
    suites = [s for s in SUITES if not filtros or any(f in (s[0] + s[1]).lower() for f in filtros)]
    if not suites:
        sys.exit("Ninguna batería coincide con: " + " ".join(sys.argv[1:]) + "\nDisponibles: "
                 + ", ".join(s[1] for s in SUITES))

    if not (TESTS / "node_modules" / "jszip").exists() or not (TESTS / "node_modules" / "pdfjs-dist").exists():
        sys.exit("Faltan las librerías locales. Ejecuta antes:  cd tests && npm install")
    comprobar_librerias()
    if not (TESTS / "fixtures" / "abril_protegida.pdf").exists():
        subprocess.run([sys.executable, str(TESTS / "generar_fixtures.py")], check=True)
    OUT.mkdir(exist_ok=True)

    env_base = dict(os.environ)
    # Para que las peticiones del service worker también pasen por las rutas de Playwright
    env_base["PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS"] = "1"
    # Salida de cada batería en UTF-8 (en Windows, por defecto, sería cp1252)
    env_base["PYTHONIOENCODING"] = "utf-8"

    resultados = []
    for nombre, archivo, necesita in suites:
        env = dict(env_base)
        server = None
        try:
            if necesita == "site":
                base, index = fresh_copy("site")
                env["NA_SITE_INDEX"] = str(index)
                if port_open(8765):
                    sys.exit("El puerto 8765 está ocupado: ciérralo y vuelve a intentarlo.")
                server = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "--bind", "127.0.0.1", "--directory", str(base)],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                wait_port(8765)
            elif necesita == "pages":
                base, index = fresh_copy("site_pages")
                env["NA_PAGES_INDEX"] = str(index)
                if port_open(8766):
                    sys.exit("El puerto 8766 está ocupado: ciérralo y vuelve a intentarlo.")
                server = subprocess.Popen([sys.executable, str(TESTS / "servidor_pages.py"), str(base), "8766"],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                wait_port(8766)

            print(f"\n━━━ {nombre} ({archivo})")
            t0 = time.time()
            p = subprocess.run([sys.executable, str(TESTS / archivo)], env=env, cwd=str(TESTS),
                               capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
            salida = p.stdout + p.stderr
            for linea in salida.splitlines():
                if linea.strip().startswith(("OK", "FAIL")) or "RESULTADO" in linea or linea[:3].strip().rstrip(")").isdigit():
                    print("  " + linea.strip())
            ok = p.returncode == 0 and "TODO OK" in salida
            if not ok and "RESULTADO" not in salida:
                print("\n".join("  | " + l for l in salida.strip().splitlines()[-15:]))
            resultados.append((nombre, ok, time.time() - t0))
        finally:
            if server:
                server.terminate()
                server.wait(timeout=10)

    print("\n" + "═" * 64)
    for nombre, ok, dur in resultados:
        print(f"{'✅' if ok else '❌'}  {nombre:52s} {dur:5.1f} s")
    fallos = sum(1 for _, ok, _ in resultados if not ok)
    print("═" * 64)
    print("TODO OK" if not fallos else f"{fallos} batería(s) con fallos")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
