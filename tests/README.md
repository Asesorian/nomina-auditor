# 🧪 Pruebas automáticas

Nueve baterías (~150 comprobaciones) que abren **la app real** en Chromium con tamaño de móvil (390×844) y la usan como lo haría una persona: suben nóminas, pulsan botones, descargan backups, abren PDFs, cortan la conexión…

- **No gastan lecturas de Gemini ni usan ninguna API key:** las respuestas de la IA se simulan.
- **No dependen de internet:** las librerías de la CDN (JSZip y PDF.js) se sirven en local, en la **misma versión exacta** que carga la app.
- **No usan datos reales:** las nóminas de ejemplo (fotos y PDFs) son sintéticas y se generan solas.

Conviene ejecutarlas **antes de publicar cualquier cambio** en `index.html` o `sw.js`.

---

## Qué comprueba cada batería

| Batería | Archivo | Qué comprueba |
|---|---|---|
| Pagas extra, atrasos y duplicados | `test_pagas_extra.py` | Clasificación automática por conceptos (extra, atrasos, prorrata, horas extra), mes normalizado, extra con la mensual ya guardada, aviso de duplicado con opciones, misma nómina subida dos veces, segunda extra del mes (*Paga extra 2*), reclasificar y recuperar desde un backup antiguo, panel e informe anual con extras, mes ilegible que bloquea el guardado |
| % de IRPF y corrección a mano | `test_irpf.py` | Orden de obtención del % (bases → línea de IRPF → calculado → aproximado), asterisco en los calculados, `N/L`, corrección manual desde *Ver* (valor no válido, vacío = automático), informe anual, edición con coma |
| API key por QR | `test_qr.py` | Enlace nuevo `#apikey=` y antiguo `?apikey=`, la dirección queda limpia, el QR se genera con `#` |
| Documentos originales y backup completo | `test_originales.py` | Botones *Hacer foto* / *Elegir archivo*, casilla marcada por defecto, nombre automático, ver y descargar, 📎 en el panel, reclasificar conserva el original, adjuntar sin llamar a la IA, cambiar/sustituir/eliminar sin dejar documentos huérfanos, ZIP completo y restauración en un dispositivo vacío, importar un JSON no borra originales, *Borrar todo* borra también los documentos |
| Compartir a Drive/iCloud | `test_compartir.py` | En móvil aparece *Guardar en… (Drive, iCloud…)* y abre el menú de compartir con el archivo y su nombre |
| Visor de PDF | `test_visor_pdf.py` | Aviso visual mientras se prepara, dibuja la página, varias páginas, resolución para ampliar, segunda apertura directa, contraseña incorrecta / correcta / cancelada, PDF dañado, fotos intactas, cerrar mientras carga, visor no disponible, sin conexión la primera vez, **visor manipulado bloqueado por SRI**, **los PDF se abren sin permitirles ejecutar código** (`isEvalSupported: false`, mitigación de CVE-2024-4367) |
| Modo sin conexión | `test_sin_conexion.py` | Service worker y copia guardada, abrir sin red, aviso visible, nóminas intactas, procesar avisa de que necesita internet, versión nueva a la primera al volver la red, *Forzar actualización*, las peticiones a Gemini nunca pasan por la copia, en `file://` no aplica |
| Visor de PDF sin conexión | `test_pdf_sin_conexion.py` | Con conexión el visor se precarga en segundo plano sin ejecutarse; sin red el PDF se abre dentro de la app |
| Versión nueva a la primera | `test_actualizacion.py` | Con las cabeceras de caché de GitHub Pages (`max-age=600` + `ETag`), tras publicar se ve la versión nueva al abrir la app |

---

## Preparación (una sola vez)

Hace falta **Python 3.9+** y **Node.js 18+**.

```bash
pip install playwright pillow reportlab pypdf
python -m playwright install chromium
cd tests && npm install && cd ..
```

`npm install` solo descarga `jszip 3.10.1` y `pdfjs-dist 3.11.174` en `tests/node_modules/` (el `.npmrc` evita compilar paquetes opcionales que no hacen falta).

## Ejecutar

Desde la raíz del repositorio:

```bash
python tests/ejecutar_todo.py              # todas (~1 minuto)
python tests/ejecutar_todo.py visor irpf   # solo las que contengan esas palabras
```

Muestra una línea `OK` / `FAIL` por comprobación y un resumen final. Termina con código 0 si todo va bien.

- **Capturas, descargas y copias servidas** → `tests/output/`
- **Nóminas de ejemplo** → `tests/fixtures/` (las crea `generar_fixtures.py` la primera vez: dos fotos, un PDF de una página, uno de dos páginas, el mismo **protegido con la contraseña `12345678Z`** y uno dañado)

Ninguna de las dos carpetas se sube a git.

Las baterías que no necesitan servidor también se pueden lanzar sueltas (`python tests/test_irpf.py`), siempre que ya existan los ejemplos (`python tests/generar_fixtures.py`). Las de modo sin conexión y actualización necesitan el servidor que arranca `ejecutar_todo.py`.

---

## Cómo funcionan por dentro

- **Dos formas de abrir la app.** La mayoría abre `index.html` directamente (`file://`, como el acceso directo del PC). Las que prueban el service worker sirven una copia limpia de `index.html` + `sw.js` por `http://localhost`, porque los service workers no funcionan en `file://`:
  - puerto **8765**: `python -m http.server`
  - puerto **8766**: `servidor_pages.py`, que imita las cabeceras de caché de GitHub Pages

  Ambos escuchan solo en `127.0.0.1` y se cierran al terminar.
- **Gemini simulada.** Las pruebas sustituyen `callGemini` por una función que devuelve datos de ejemplo, o rellenan directamente los datos extraídos. Nunca sale una petición a Google.
- **Librerías de la CDN interceptadas.** Las peticiones a `cdnjs.cloudflare.com` se responden con los archivos de `tests/node_modules/`. Como PDF.js se carga con **SRI**, el navegador comprueba que el archivo local sea idéntico byte a byte al publicado: si no lo es, se niega a ejecutarlo (exactamente lo que comprueba la prueba 10 del visor).
- **Service worker y rutas de Playwright.** `ejecutar_todo.py` activa `PW_EXPERIMENTAL_SERVICE_WORKER_NETWORK_EVENTS=1` para que también las peticiones que hace el service worker pasen por esas rutas. Sin ella, el visor de PDF sin conexión fallaría solo en las pruebas (no en la app).
- **Sin números de versión fijos.** La versión de la app (`Forense v…`), la de PDF.js y sus huellas SRI se leen del propio `index.html` (`_comun.py`).
- **Comprobación previa.** Antes de empezar, `ejecutar_todo.py` verifica que las librerías de `node_modules` sean las mismas versiones que carga la app y que las huellas SRI de PDF.js coincidan. Si no, dice exactamente qué cambiar.

## Archivos

| Archivo | Para qué |
|---|---|
| `ejecutar_todo.py` | Lanza todas las baterías, arranca y cierra los servidores, resume el resultado |
| `_comun.py` | Rutas relativas al repositorio y datos leídos de `index.html` (funciona en Windows, Mac y Linux) |
| `generar_fixtures.py` | Crea las nóminas de ejemplo sintéticas |
| `servidor_pages.py` | Servidor local con `Cache-Control: max-age=600` + `ETag`, como GitHub Pages |
| `package.json` / `.npmrc` | Versiones exactas de JSZip y PDF.js para servirlas en local |
| `test_*.py` | Las nueve baterías |

## Si cambias de versión de PDF.js o JSZip

Ver [docs/TECNICO.md → Actualizar PDF.js y otras librerías](../docs/TECNICO.md#18-actualizar-pdfjs-y-otras-librerías). En resumen: nueva URL y nuevas huellas SRI en `index.html`, misma versión en `tests/package.json`, `npm install` y volver a ejecutar las pruebas.
