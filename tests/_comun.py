"""Rutas y datos comunes de las pruebas.

Todo es relativo al repositorio: las pruebas funcionan en cualquier ordenador
(Linux, Mac o Windows) sin tocar nada.
"""
import os
import re
import sys
from pathlib import Path

# Que los acentos y emojis de los mensajes no rompan la salida en la consola de Windows
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TESTS = Path(__file__).resolve().parent
ROOT = TESTS.parent

APP_FILE = str(ROOT / "index.html")
APP = (ROOT / "index.html").as_uri()                      # la app abierta como archivo local (file://)

OUT = str(TESTS / "output") + os.sep                      # capturas, descargas y copias servidas
FX = str(TESTS / "fixtures") + os.sep                     # archivos de ejemplo (los crea generar_fixtures.py)

# Librerías de la CDN servidas en local (el navegador de pruebas no descarga nada de internet)
JSZIP = str(TESTS / "node_modules" / "jszip" / "dist" / "jszip.min.js")
PDFJS = str(TESTS / "node_modules" / "pdfjs-dist" / "build") + os.sep

# Copia de la app servida por http (para probar el service worker / modo sin conexión)
SITE_URL = "http://localhost:8765/nomina-auditor/"
SITE_INDEX = os.environ.get("NA_SITE_INDEX", str(TESTS / "output" / "site" / "nomina-auditor" / "index.html"))

# Copia servida con las cabeceras de caché de GitHub Pages (max-age=600 + ETag)
PAGES_URL = "http://localhost:8766/nomina-auditor/"
PAGES_INDEX = os.environ.get("NA_PAGES_INDEX", str(TESTS / "output" / "site_pages" / "nomina-auditor" / "index.html"))

# Datos leídos del propio index.html (las pruebas no fijan números de versión)
_HTML = Path(APP_FILE).read_text(encoding="utf-8")
VERSION = re.search(r"Forense (v[\d.]+)", _HTML).group(1)                       # p. ej. "v2.7"
PDFJS_VERSION = re.search(r"/pdf\.js/(\d+\.\d+\.\d+)/", _HTML).group(1)         # p. ej. "3.11.174"
PDFJS_SRI = dict(re.findall(r"\['(pdf(?:\.worker)?\.min\.js)',\s*'(sha384-[A-Za-z0-9+/=]+)'\]", _HTML))

os.makedirs(OUT, exist_ok=True)
