# 🔧 Documentación técnica

Para quien quiera entender, mantener o adaptar Nómina Auditor. Para **usarla**, basta con el [README](../README.md).

Refleja la **v2.7.3** (octubre de 2026). Los nombres de funciones y constantes son los de `index.html`, para poder buscarlos directamente.

## Índice

1. [Principios](#1-principios)
2. [Archivos y dependencias](#2-archivos-y-dependencias)
3. [Recorrido de una nómina](#3-recorrido-de-una-nómina)
4. [Almacenamiento](#4-almacenamiento)
5. [Modelo de datos de una nómina](#5-modelo-de-datos-de-una-nómina)
6. [Identificadores y tipos de nómina](#6-identificadores-y-tipos-de-nómina)
7. [Clasificación automática del tipo](#7-clasificación-automática-del-tipo)
8. [Porcentaje de retención de IRPF](#8-porcentaje-de-retención-de-irpf)
9. [Duplicados y sustitución](#9-duplicados-y-sustitución)
10. [Documentos originales](#10-documentos-originales)
11. [Copias de seguridad](#11-copias-de-seguridad)
12. [Modo sin conexión (sw.js)](#12-modo-sin-conexión-swjs)
13. [Visor de PDF](#13-visor-de-pdf)
14. [Gemini](#14-gemini)
15. [Seguridad y privacidad](#15-seguridad-y-privacidad)
16. [Pendiente y deuda técnica conocida](#16-pendiente-y-deuda-técnica-conocida)
17. [Publicar una versión](#17-publicar-una-versión)
18. [Actualizar PDF.js y otras librerías](#18-actualizar-pdfjs-y-otras-librerías)
19. [Pruebas automáticas](#19-pruebas-automáticas)
20. [Comprobación de las cuentas y corrección](#20-comprobación-de-las-cuentas-y-corrección) (v2.7.2)

---

## 1. Principios

- **Un archivo, sin build y sin backend.** Toda la app es `index.html` (HTML + CSS + JS vanilla). `sw.js` solo añade el modo sin conexión. GitHub Pages sirve archivos estáticos: no hay ningún servidor propio que reciba datos.
- **"Código científico, IA divulgadora".** Gemini solo **transcribe** la nómina a JSON. La clasificación del tipo, el % de IRPF, los totales y las comprobaciones del informe anual los hace código determinista. Desde la v2.7.2, además, **el código comprueba las cuentas de cada lectura** (ver [§20](#20-comprobación-de-las-cuentas-y-corrección)) y, si no cuadran, pide otra lectura; nunca cambia una cifra por su cuenta. Ninguna cifra sale de la IA sin pasar por la verificación humana.
- **Verificación humana obligatoria.** Nada se guarda hasta que el usuario revisa los datos extraídos y pulsa *Confirmar y Guardar*.
- **Los datos no salen del dispositivo.** Nóminas, API key y documentos originales viven en el navegador. La única salida es la imagen o el PDF que se envía a Gemini en el momento de procesarlo.
- **Compatibilidad hacia atrás.** Ningún cambio obliga a migrar: los registros y backups antiguos siguen valiendo tal cual (ver [ids](#6-identificadores-y-tipos-de-nómina)).

---

## 2. Archivos y dependencias

| Archivo | Qué es |
|---|---|
| `index.html` | La app completa (~165 KB). El *manifest* de la PWA y el icono van incrustados como `data:` URI |
| `sw.js` | Service worker del modo sin conexión (~5 KB) |
| `docs/TECNICO.md` | Este documento |
| `tests/` | Pruebas automáticas con navegador real ([tests/README.md](../tests/README.md)) |

**Dependencias externas** (todas con versión fija en la URL):

| Librería | Versión | Para qué | Cuándo se carga | SRI |
|---|---|---|---|---|
| JSZip | 3.10.1 | Backup completo e importar ZIP | Al abrir la app | **Sí** (desde la v2.7.1) |
| QRCode.js | 1.0.0 | QR para pasar la API key al móvil | Al abrir la app | **Sí** (desde la v2.7.1) |
| PDF.js (Mozilla) | 3.11.174 | Visor de PDF | Solo al abrir un PDF (o en la precarga) | **Sí** |
| Google Fonts | Inter, JetBrains Mono | Tipografía | Al abrir la app | No aplica |
| API de Gemini | `gemini-2.5-flash` → `flash-lite` → `pro` | Lectura (OCR) de la nómina | Solo al procesar | — |

---

## 3. Recorrido de una nómina

```
handleFile(file)          readNominaFile(): PDF tal cual (detectado por su contenido, "%PDF")
                          o imagen → JPEG calidad 0,92, máx. 2500 px por lado
processImage()            readWithChecks(base64, tipo) (exige conexión):
                            callGemini() con la cadena de modelos → prepareExtracted() → checkErrors()
                            si hay errores: callGemini(…, feedbackFor(lectura)) → prepareExtracted()
                            y se queda con la de menor readScore() (nunca toca cifras)
prepareExtracted(d)       normalizeMonth() · importes de texto → número (num) · classifyPayroll()
                          · irpfRateOf() si faltaba el %
renderVerification()      renderChecks() con las celdas sospechosas marcadas · el usuario corrige
                          (editField, addLine, removeLine), ve el documento (viewCurrentDocument),
                          relee (rereadCurrent) y confirma el tipo (setPayType)
confirmAndSave()          valida mes y año → si checkErrors(): confirm() → en modo corrección
                          saveEdited() (ver §20) → payrollId() → si el hueco existe: openDupModal()
                            ├─ saveAsType(tipo)    guardar aparte (freePayrollId)
                            └─ confirmOverwrite()  sustituir
doSave(payroll)           storeOriginal() si la casilla está marcada · gestiona el original
                          de la nómina sustituida · saveData() · autoBackup() · showReport()
                          · warmPdfViewer()
```

`savingPayroll` evita guardar dos veces con un doble toque.

---

## 4. Almacenamiento

### localStorage

| Clave | Contenido |
|---|---|
| `nomina-auditor-data` | Array JSON con todas las nóminas |
| `nomina-auditor-apikey` | API key de Gemini |
| `nomina-auditor-autobackup` | `'false'` desactiva el backup automático (ausente o cualquier otro valor = activado) |
| `nomina-auditor-lastbackup` | Fecha ISO del último backup descargado |

### IndexedDB (documentos originales)

- Base de datos `nomina-auditor-docs` (versión 1), almacén `docs` con claves externas.
- Clave: `doc-<uuid>` (`crypto.randomUUID()`, con alternativa si no existe).
- Registro: `{ data: ArrayBuffer, type: 'image/jpeg' | 'application/pdf', name, size, savedAt }`. `name` es el nombre del archivo que eligió el usuario; el nombre que se muestra y descarga se calcula aparte (ver [§10](#10-documentos-originales)).
- La nómina solo guarda una **referencia**: `original: { key, type, size, name, savedAt }`. Así, reclasificar (que cambia el id) no mueve el documento, e importar un JSON sin documentos no los borra.
- `docKeys` (un `Set` en memoria) se rellena al arrancar con `refreshDocKeys()`. `hasOriginal(p)` = la nómina tiene referencia **y** el documento está en este dispositivo.
- Después de guardar un documento se pide `navigator.storage.persist()`, para que el navegador no lo borre si falta espacio. *Datos* indica si lo ha concedido.

### Origen compartido en GitHub Pages

Todas las webs publicadas bajo `asesorian.github.io` comparten origen y, por tanto, el mismo localStorage, IndexedDB y Cache Storage. Por eso todo lleva el prefijo `nomina-auditor-` y el service worker solo borra cachés con ese prefijo. Consecuencia de seguridad: cualquier otra web publicada bajo el mismo usuario podría leer las nóminas y la API key. No publicar ahí código de terceros sin revisarlo.

Abierta como archivo local (`file://`), la app usa el almacenamiento del navegador para archivos locales, **distinto** del de la web publicada: son dos juegos de datos independientes.

---

## 5. Modelo de datos de una nómina

Ejemplo (datos inventados):

```json
{
  "id": "2026-07-extra",
  "payType": "extra",
  "savedAt": "2026-07-31T18:02:11.000Z",
  "period": { "month": "Julio", "year": "2026", "startDate": "01/07/2026", "endDate": "31/07/2026", "days": 30 },
  "company": { "name": "EMPRESA EJEMPLO SL", "cif": "B00000000", "ccc": "N/L" },
  "worker": { "name": "NOMBRE APELLIDO", "naf": "N/L", "dni": "00000000T" },
  "employment": { "category": "OFICIAL 1ª", "seniority": "01/01/2015", "contractCode": "100", "cotizationGroup": "8" },
  "earnings": [{ "code": "010", "concept": "PAGA EXTRA VERANO", "units": "30,00", "price": 60.00, "amount": 1800.00 }],
  "deductions": [
    { "code": "", "concept": "TRIBUTACIÓN IRPF", "units": "", "amount": 288.00 },
    { "code": "", "concept": "Contingencias comunes", "units": "", "amount": 0 }
  ],
  "totals": { "grossTotal": 1800.00, "totalDeductions": 288.00, "netPay": 1512.00 },
  "bases": { "totalRemuneration": 0, "extraPayProrata": 0, "baseCC": 0, "baseAT": 0, "baseIRPF": 1800.00,
             "irpfPercentage": 16, "irpfSource": "calculado" },
  "original": { "key": "doc-3f2a…", "type": "application/pdf", "size": 183204, "name": "scan_julio.pdf",
                "savedAt": "2026-07-31T18:02:11.000Z" }
}
```

- La estructura de `period` a `bases` es la que se pide a Gemini (`EXTRACTION_PROMPT`). Lo que no se puede leer llega como `"N/L"`.
- `price` (precio por unidad) existe desde la v2.7.2 y es opcional: las lecturas anteriores no lo tienen.
- Los añade la app: `id`, `payType`, `savedAt`, `editedAt` (si se corrigió después de guardarla, v2.7.2), `bases.irpfSource` y `original`.
- Los importes son números. Si Gemini los manda como texto, `prepareExtracted()` los convierte con `num()`; lo ilegible se queda como `"N/L"` y en las sumas cuenta 0 (`amt()`).
- Registros anteriores a la v2.3: sin `payType` → se tratan como mensuales (`payTypeOf()`).

---

## 6. Identificadores y tipos de nómina

```js
PAY_TYPES = { ordinaria: 'Mensual', extra: 'Paga extra', atrasos: 'Atrasos' }
```

| Nómina | `id` |
|---|---|
| Mensual de julio 2026 | `2026-07` (el formato de siempre) |
| Paga extra de julio | `2026-07-extra` |
| Segunda paga extra de julio | `2026-07-extra-2` |
| Atrasos pagados en julio | `2026-07-atrasos` |

- `payrollId(p, n)` construye el id. `freePayrollId(p)` devuelve el primer hueco libre: la mensual solo tiene uno (si está ocupado devuelve `null`); extras y atrasos usan `-2`, `-3`…
- Ordenar por id (`sortPayrolls()`) deja juntas las del mismo mes: `2026-07`, `2026-07-atrasos`, `2026-07-extra`, `2026-07-extra-2`, `2026-08`…
- `payLabelOf(p)` da la etiqueta corta que se ve bajo el mes: `Paga extra`, `Atrasos` o, por el sufijo del id, `Paga extra 2`.
- **Reclasificar** (`reclassifyPayroll(id, tipo)`) mueve la nómina a un id nuevo con `freePayrollId()`. Si el destino es la mensual y ya existe, se niega con un mensaje. Conserva la referencia al original.

---

## 7. Clasificación automática del tipo

`classifyPayroll(d)` decide con reglas comprobables. Lo que diga Gemini (`payType`) es solo una pista.

```js
EXTRA_RE    = /\bpaga\s*extra|\bp\.?\s*extra|\bpagas?\s*extraordinaria|gratificaci[oó]n\s*extra|
               extra\s*(de\s*)?(verano|navidad|junio|julio|diciembre|beneficios|marzo)|
               paga\s*(de\s*)?(verano|navidad|beneficios)/i
PRORRATA_RE = /prorr|p\.\s*p\.|parte\s*proporcional|partes\s*proporcionales/i
ATRASOS_RE  = /atrasos|diferencias?\s*(de\s*)?convenio|regularizaci[oó]n\s*salarial|revisi[oó]n\s*salarial/i
```

1. Se calcula qué parte del bruto (`totals.grossTotal`, o la suma de devengos positivos) suman los conceptos que cumplen cada expresión, **excluyendo los de prorrata**.
2. Extra ≥ 60 % del bruto → **paga extra**. Atrasos ≥ 60 % → **atrasos**.
3. Si no es concluyente, cuenta la pista de Gemini (`payType` = `extra` / `atrasos`).
4. Si hay algo de paga extra pero por debajo del 60 % → **mensual** ("incluye la paga extra como una línea más").
5. Si no, **mensual**.

Las horas extraordinarias no cumplen `EXTRA_RE` a propósito. El motivo de la decisión se muestra en la verificación; si el usuario cambia el tipo, la verificación lo indica como elegido a mano.

`normalizeMonth()` acepta `JULIO`, `julio`, `7`, `07` o `setiembre`. Si el mes o el año (4 cifras) no son válidos, `confirmAndSave()` bloquea el guardado.

---

## 8. Porcentaje de retención de IRPF

`irpfRateOf(p)` devuelve `{ rate, source }` con este orden:

| Orden | Origen (`source`) | Cómo |
|---|---|---|
| 1 | `nomina` / `manual` | `bases.irpfPercentage` válido. `manual` si lo corrigió el usuario |
| 2 | `concepto` | `irpfFromLine()`: primero la columna de unidades; si no, el último número de 1–2 cifras (con hasta 3 decimales) del concepto de la línea de IRPF. `TRIBUTACIÓN IRPF.20,42` → 20,42; `I.R.P.F. 2026` → nada |
| 3 | `calculado` | importe retenido ÷ `baseIRPF` |
| 4 | `aprox` | importe retenido ÷ bruto (si no hay base IRPF) |
| — | `null` | No hay forma: se muestra `N/L` |

- `parsePct()` acepta `20,42`, `20.42` o `20,42 %`, solo valores **entre 0 y 60** (exclusivo), redondeados a 2 decimales.
- La línea de IRPF (`findIRPFLine()`, v2.7.2): la primera deducción que `deductionKind()` clasifica como `irpf` (contiene `irpf`/`irpp`, `tributa…`, `hacienda` o `retenc…` sin ser judicial/embargo/pensión/alimentos). Si ninguna, la deducción sin clasificar cuyo importe es exactamente base IRPF × % (cuando el % viene de la nómina o es manual). Hasta la v2.7.1 tenía que contener `irpf` y una lectura como «I.R.P.P.» contaba 0.
- En `prepareExtracted()`, si Gemini no trajo el %, se rellena con el deducido y su origen, para que el usuario lo vea y lo compruebe en la verificación (aviso naranja).
- Corregir a mano: en la verificación (`editField`) o desde *Ver* (`editIrpf`). Dejarlo vacío borra el valor manual y vuelve al cálculo automático.
- `irpfCell()` añade `*` a los valores `calculado` y `aprox`.
- El informe anual solo compara el % entre nóminas **mensuales** (una paga extra suele tener otra retención).

---

## 9. Duplicados y sustitución

Si el hueco (`id`) ya está ocupado, `openDupModal()` muestra bruto, neto y fecha de las dos. Se consideran **los mismos importes** si bruto y neto difieren menos de 0,01 €.

| Nueva nómina | Opciones |
|---|---|
| Mensual | Guardar aparte como paga extra · como atrasos · Sustituir · Cancelar |
| Extra o atrasos | Guardar aparte como otra del mismo tipo (`-2`, `-3`…) · Sustituir · Cancelar |

Con los mismos importes, el botón destacado es *Cancelar — ya la tengo*.

---

## 10. Documentos originales

**Qué se guarda:** exactamente lo que se envió a Gemini: el PDF tal cual o la foto ya convertida a JPEG (máx. 2500 px). Medido con fotos reales de móvil: originales de 1,7–2,8 MB quedan en 0,6–1,1 MB; los PDF ocupan 0,05–0,3 MB.

**Nombre automático** (`originalFileName(p)`): `AAAA-MM Mes[ - Tipo].ext`, por ejemplo `2026-07 Julio - Paga extra.pdf`. Se calcula al vuelo: si se reclasifica la nómina, el nombre se actualiza solo.

**Ciclo de vida** (ninguna operación deja un documento perdido sin querer):

| Operación | Efecto en IndexedDB |
|---|---|
| Guardar una nómina con la casilla marcada | Documento nuevo |
| Sustituir una nómina **con** documento nuevo | Se borra el de la sustituida |
| Sustituir una nómina **sin** documento nuevo | Se conserva el de la sustituida |
| Reclasificar | Nada: la referencia se mantiene |
| *Adjuntar original* / *Cambiar* | Documento nuevo; se borra el anterior |
| *Quitar* | Se borra el documento (la nómina sigue) |
| Eliminar la nómina | Se borra su documento |
| Importar JSON | Nunca borra un documento disponible (ver [§11](#11-copias-de-seguridad)) |
| Importar ZIP completo | Restaura con su misma clave los documentos de nóminas válidas |
| *Datos → Documentos sin nómina → Borrar* | Borra, con confirmación, los que ninguna nómina referencia (`orphanDocKeys`) |
| *Borrar todo* | Vacía el almacén |

**Ver:** las fotos se muestran en un `<img>` con una URL temporal (`URL.createObjectURL`, revocada al cerrar); los PDF, en el [visor propio](#13-visor-de-pdf).

**Guardar en… (Drive, iCloud…):** Web Share API con archivos. El botón solo aparece si `navigator.canShare({ files })` lo permite. El `File` se prepara al abrir el informe (`originalCache`) porque los navegadores móviles exigen llamar a `navigator.share()` dentro del mismo toque, y esperar a IndexedDB podría hacer perder ese permiso. Si no se puede compartir, descarga.

---

## 11. Copias de seguridad

### JSON (`nominas-backup-AAAA-MM-DD-HHMM.json`)

```json
{ "_meta": { "app": "Nomina Auditor Forense", "version": "2.7.3", "exportedAt": "…", "totalPayrolls": 12 },
  "payrolls": [ … ] }
```

El **backup automático** descarga este JSON al guardar una nómina, reclasificarla o corregir su % de IRPF (si está activado).

### ZIP completo (`nominas-backup-completo-AAAA-MM-DD-HHMM.zip`)

```
├── nominas/            las nóminas (fotos y PDF originales), por año
│   └── 2026/
│       ├── 2026-07 Julio.jpg
│       └── 2026-07 Julio - Paga extra.pdf
├── datos-app.json      el JSON de arriba + _meta.documents + _meta.totalDocuments
└── LEEME.txt           qué contiene y cómo restaurarlo
```

- Nombres en las constantes `ZIP_DOCS_DIR` y `ZIP_DATA_FILE`. **Hasta la v2.7.2** eran `documentos/` y `nominas.json`; se cambiaron porque lo que hay dentro son las nóminas y `nominas/` junto a `nominas.json` se confundía. Importar acepta los dos formatos (`ZIP_DOCS_DIRS_OK`, `ZIP_DATA_FILES_OK`).
- Una versión anterior a la v2.7.3 que importe un ZIP nuevo restaura los datos (encuentra el `.json`) pero **no los originales** (solo aceptaba `documentos/`). No debería pasar: la app se actualiza sola al abrirla con conexión.
- `_meta.documents` enlaza cada clave con su ruta: `{ "doc-3f2a…": "nominas/2026/2026-07 Julio.jpg" }`.
- Nombres repetidos → ` (2)`, ` (3)`… Año que no tenga 4 cifras → `nominas/otros/`.

### Importar (`importBackup`, `processImportedJSON`)

- Detecta ZIP por su contenido (`PK\x03\x04`); si no, lo lee como JSON.
- Acepta `{ payrolls: [...] }` o un array suelto (backups muy antiguos).
- **Validación** (`sanitizeImportedPayroll`, desde la v2.7.1). Un backup puede venir de cualquier sitio, así que solo entra lo que tiene la forma exacta que crea la app:
  - `id` con el patrón `^\d{4}-(0[1-9]|1[0-2])(-(extra|atrasos)(-\d+)?)?$`; `period.year` de 4 cifras (se guarda como texto); `period.month` de la lista (se normaliza: `mayo` → `Mayo`); `payType` válido o ausente.
  - `earnings`/`deductions` que no sean listas se vacían; `original` cuya clave no cumpla `^doc-[\w-]+$` se quita (la nómina entra, sin documento).
  - Lo que no pasa se ignora y el resultado dice cuántos registros eran. Si no pasa ninguno, no se toca nada.
- En un ZIP usa `datos-app.json` o `nominas.json` (estén en la carpeta que estén) o, si no hay, el primer `.json`. Antes de fusionar restaura los documentos de `_meta.documents` con **su misma clave**, pero solo si la clave cumple `^doc-[\w-]+$`, la ruta empieza por `nominas/` o `documentos/` y pertenece a una nómina **válida** del backup (así no quedan huérfanos). El tipo se decide por el **contenido** (`%PDF` → PDF; si no, JPEG), no por la extensión.
- Los mensajes de error se insertan escapados (`esc()`): el de `JSON.parse` incluye un trozo del archivo.
- **Fusión por id:** las nuevas se añaden; si ya existe una con el mismo id, **la del backup la sustituye**.
- **Originales:** si la del backup no trae documento disponible y la del dispositivo sí, se conserva el del dispositivo. Si las dos tienen y son distintos, se queda el del backup y se borra el otro.
- Una nómina cuyo documento está en otro dispositivo muestra *"se guardó en otro dispositivo"* y permite adjuntarlo.

### Borrar todo

Doble confirmación. Vacía las nóminas y los documentos. La API key se conserva.

---

## 12. Modo sin conexión (sw.js)

- Solo se registra en `https:` o `localhost` (`SW_SUPPORTED`), con `updateViaCache: 'none'` para que el propio `sw.js` se revise siempre. En `file://` no aplica y la tarjeta de *Datos* se oculta.
- **install:** guarda `./` (con `cache: 'reload'`) y las librerías de `CDN_ASSETS`; si alguna falla no bloquea. `skipWaiting()`.
- **activate:** borra las cachés con prefijo `nomina-auditor-` que no sean la actual. `clients.claim()`.
- **fetch:**

| Petición | Estrategia |
|---|---|
| No GET (Gemini, cualquier envío) | No se toca: va directa a la red |
| Navegación del mismo origen (la app) | **Red primero** con `cache: 'no-cache'` (revalida con ETag → 304 si no ha cambiado) y se guarda como `./`. Si ya hay copia: la red tiene 4 s; si tarda más o no hay conexión, la copia |
| `cdnjs.cloudflare.com`, Google Fonts | **Copia primero** (las URLs llevan versión fija) |
| Lo demás | Red, sin tocar |

- **Por qué `cache: 'no-cache'`:** GitHub Pages sirve `index.html` con `Cache-Control: max-age=600`. Sin ello, tras publicar, el móvil podía seguir mostrando la versión anterior hasta 10 minutos (corregido en la v2.5; lo comprueba `test_actualizacion.py`).
- **`CACHE_VERSION`** (`nomina-auditor-sw3`): cambiarla **solo** si cambia `sw.js` o la lista de librerías. Publicar cambios de `index.html` no lo necesita. Pasó a `sw3` en la v2.7.1: JSZip y QRCode.js empezaron a cargarse con SRI y la caché `sw2` podía tener copias *opacas* (guardadas sin CORS) que ya no pasarían la comprobación.
- **Copias opacas:** `cacheFirst()` no sirve una copia opaca a una petición en modo `cors` (un `<script>` con `integrity`): la ignora y va a la red.
- **Forzar actualización** (`forceAppUpdate`): `registration.update()`, borra las cachés con el prefijo y recarga. No toca localStorage ni IndexedDB.
- **Precarga del visor de PDF** (`warmPdfViewer`): si el service worker controla la página, hay conexión y existe algún PDF guardado, descarga PDF.js en segundo plano para que funcione sin conexión. Usa `fetch(…, { mode: 'cors', credentials: 'omit' })`: una copia *opaca* no superaría la comprobación SRI al usarla sin conexión.

---

## 13. Visor de PDF

```js
PDFJS_BASE  = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/'
PDFJS_FILES = [['pdf.min.js', 'sha384-…'], ['pdf.worker.min.js', 'sha384-…']]
```

- **Carga perezosa** (`loadPdfJs`): solo al abrir el primer PDF. `loadScriptOnce()` añade cada script con `integrity` y `crossOrigin = 'anonymous'`: si el archivo de la CDN no coincide byte a byte, el navegador no lo ejecuta.
- **Sin Web Worker:** cargar `pdf.worker.min.js` como script normal define `window.pdfjsWorker` y PDF.js trabaja en el hilo principal. Evita las restricciones de crear un Worker desde otro origen y basta para nóminas de 1–3 páginas.
- **`isEvalSupported: false`** en `getDocument()`: es la mitigación oficial de **CVE-2024-4367** (un PDF manipulado podía ejecutar JavaScript; afecta a PDF.js ≤ 4.1.392, corregido en 4.2.67). **No quitar esta opción** mientras se use la 3.x. La prueba 11 de `test_visor_pdf.py` lo comprueba.
- **Resolución:** ancho = ancho del visor − 20 px (entre 280 y 880); escala = ancho ÷ ancho de página × DPR (máx. 2) × 1,5, con un tope de ~12 Mpx por página. Nítido al ampliar con los dedos sin agotar la memoria.
- **Aviso visual** (`role="status"`, `aria-live`): *Preparando el visor de PDF… (solo tarda un poco la primera vez)* → *Abriendo el PDF…* → *Mostrando página i de N…*. Al terminar, pie con nº de páginas y alternativas.
- **Contraseña** (`onPassword`): la pide con `prompt()` y la vuelve a pedir si es incorrecta. Al cancelar se llama a `updatePassword(new Error(…))`: con `task.destroy()` la animación de carga se quedaba colgada.
- **Errores**, según la fase: no se pudo cargar el visor (con o sin conexión), PDF con contraseña no introducida o PDF dañado. Siempre ofrece **Abrir con el visor del móvil** (`window.open` de una URL temporal; si el navegador lo bloquea, descarga) o **Descargar**.
- **Cerrar mientras carga:** `alive()` detiene el pintado y `closeDocViewer()` destruye la tarea.

---

## 14. Gemini

- **Petición:** `POST https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key=…` con la imagen o el PDF en `inlineData` y `EXTRACTION_PROMPT` (más, en la segunda lectura, el texto de `feedbackFor()`: `callGemini(base64, tipo, extra)`). `temperature: 0`, `maxOutputTokens: 8192` (en los modelos 2.5 el razonamiento interno cuenta dentro de ese límite) y `responseMimeType: "application/json"` (desde la v2.7.2).
- **Prompt (v2.7.2):** pide `price` aparte de `amount` (en una nómina real se tomó el precio por día como importe), que cada importe vaya en la fila de su concepto, que el porcentaje de las cotizaciones e IRPF vaya en `units`, copiar los conceptos tal cual y comprobar las sumas antes de responder sin inventar cifras.
- **Segunda lectura** (`readWithChecks`, `feedbackFor`): solo si la primera tiene errores de cuadre. Le dice qué cuentas fallan (sin dar cifras "buenas") y, como referencia de formato, los códigos y conceptos de tus otras nóminas de esa empresa. Detalle en [§20](#20-comprobación-de-las-cuentas-y-corrección).
- **Cadena de modelos** (`GEMINI_MODELS`): `gemini-2.5-flash` → `gemini-2.5-flash-lite` → `gemini-2.5-pro`. Cualquier error pasa al siguiente; si fallan todos, el mensaje lista el motivo de cada uno. Google retira modelos cada cierto tiempo: se cambian en ese array.
- **Lectura de la respuesta** (`parseGeminiJSON`): quita bloques de código y recorta a la primera `{` y la última `}`. Primero prueba `JSON.parse` tal cual; si falla, repara lo típico (comentarios fuera de las cadenas con `stripJsonComments`, comas finales, comas que falten entre líneas, `NaN`/`undefined` → 0) y vuelve a probar. Si tampoco, **error** y se pasa al modelo siguiente. Debe ser un objeto (una lista no vale). **Nunca se evalúa como JavaScript** (hasta la v2.7 había un `new Function` como último recurso).
- La key va en la URL codificada (`encodeURIComponent`).
- **Coste medido** (2026): ≈ 0,9 céntimos por lectura con `gemini-2.5-flash` (incluye el "razonamiento" del modelo); `flash-lite` ≈ 0,07 céntimos, pero solo se usa si falla el primero. Los precios cambian: consultar la [página de precios de Google](https://ai.google.dev/gemini-api/docs/pricing).
- **Términos de uso de datos** ([Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms), última actualización 28-4-2026):
  - **De pago** (proyecto con facturación activa): Google no usa las peticiones ni las respuestas para mejorar sus productos; las guarda un tiempo limitado solo para detectar abusos.
  - **Gratis:** Google puede usarlas para mejorar sus productos y pueden leerlas revisores humanos; pide no enviar información personal. **Excepción:** para usuarios del Espacio Económico Europeo, Suiza y Reino Unido se aplica el mismo trato que en la de pago.
  - Los mismos términos indican que quien ofrezca un cliente de la API a usuarios del EEE, Suiza o Reino Unido solo puede usar la modalidad de pago. A tener en cuenta si se adapta la app para dar servicio a terceros con una key propia.
- **Límite de gasto:** en AI Studio → *Spend* / *Gasto* (*Monthly spend cap*). Google lo describe como experimental y avisa de que el gasto puede superarlo un poco, porque la facturación se actualiza con unos minutos de retraso. Al alcanzarlo, Google rechaza las lecturas y la app lo muestra como *Todos los modelos fallaron*.

---

## 15. Seguridad y privacidad

- **Sin servidor propio:** nada que guarde, registre o filtre datos. Lo único que sale del dispositivo es el documento enviado a Gemini al procesarlo.
- **API key:** en localStorage; solo se envía a Google por HTTPS. Para pasarla al móvil, el QR la lleva tras `#` (`#apikey=…`): el fragmento no se envía a ningún servidor. Se sigue aceptando `?apikey=` por los QR antiguos.
  - `readApiKeyFromUrl()` (con la app ya pintada y en cada `hashchange`): limpia la dirección con `history.replaceState` **siempre**; si no había clave o es la misma, la guarda sin preguntar; si hay **otra distinta**, pide confirmación mostrando principio…final de las dos (`maskKey`). Motivo: un enlace ajeno podría hacer que las nóminas se leyeran con la cuenta de Google de otra persona. Ya no recarga la página.
  - `saveApiKey()` acepta el enlace entero (`extractApiKey`: busca `apikey=` tras `#`, `?` o `&`, o al principio) y deja en la casilla solo la clave. Pensado para iPhone, donde la app instalada no comparte almacenamiento con Safari.
  - Junto a la casilla: *¿No tienes clave? Pídesela a quien te pasó la app, o créala tú (guía)*, con enlace a la sección del README.
- **Service worker:** nunca intercepta peticiones que no sean GET y solo guarda código, nunca datos.
- **PDF.js:** SRI + `isEvalSupported: false` + sin Worker.
- **Texto leído por la IA o importado:** se escapa con `esc()` al insertarlo en la página (verificación, informes, panel, errores).
- **Datos dentro de `onclick`:** siempre con `jsArg(valor)` (cadena JS de `JSON.stringify` escapada para atributo con `escAttr`). **Nunca** `'${dato}'` a mano. Protege también los datos raros que ya estuvieran guardados.
- **Copiar:** los botones copian desde una variable (`_reportText`, `annualText`) con `copyToClipboard()`; el texto nunca va dentro del HTML del botón.
- **Librerías externas:** todas con SRI (`integrity` + `crossorigin="anonymous"`); `tests/ejecutar_todo.py` comprueba las huellas de JSZip y PDF.js contra los archivos locales.
- **Backups:** contienen datos personales (DNI, salario…); `LEEME.txt` lo advierte.
- **Origen compartido** en GitHub Pages: ver [§4](#origen-compartido-en-github-pages).

---

## 16. Pendiente y deuda técnica conocida

Revisión de octubre de 2026. Los puntos 1–5 se encontraron al documentar y están **resueltos en la v2.7.1** (comprobados en `tests/test_seguridad.py`).

| # | Qué era | Estado |
|---|---|---|
| 1 | *📋 Copiar para Abogado* metía el texto del informe dentro del `onclick`: con comillas `"` no copiaba nada y un `${…}` en los datos se ejecutaba | ✅ v2.7.1: `copyText(this)` copia desde `_reportText` |
| 2 | Si la respuesta de Gemini no era JSON válido, `callGemini()` la evaluaba como JavaScript (`new Function`) | ✅ v2.7.1: solo `JSON.parse` (con reparaciones); si no, error y modelo siguiente |
| 3 | Importar no validaba los registros (los `id` y años acababan en `onclick`) y los mensajes de error se insertaban sin escapar | ✅ v2.7.1: validación al importar, `jsArg()` en todos los `onclick` y `esc()` en los errores |
| 4 | JSZip y QRCode.js sin SRI | ✅ v2.7.1: `integrity` + `crossorigin`, `CACHE_VERSION` → `sw3` |
| 5 | Documentos huérfanos en IndexedDB | ✅ v2.7.1: *Datos* los muestra con su tamaño y los borra con confirmación. **No** se borran solos: si las nóminas no se pudieran leer, parecerían huérfanos todos (sin ninguna nómina, el aviso aconseja importar el backup y no ofrece borrar) |

Encontrados al revisar un backup con nóminas reales (15-10-2026), **resueltos en la v2.7.2** (`tests/test_lecturas.py`):

| # | Qué era | Estado |
|---|---|---|
| 8 | `calcSSTotal()` solo sumaba conceptos con «contingencia», «formación» o «desempleo»: con `CONT.COMU` y el MEI la S.S. salía en torno al 20 % de la real | ✅ `deductionKind()`: todas las cotizaciones, escritas como vengan |
| 9 | La línea de IRPF dependía de leer «irpf»: con «I.R.P.P.» el IRPF del mes contaba 0 | ✅ `findIRPFLine()` por texto ampliado y, si no, por la cuenta base × % |
| 10 | Nada comprobaba que las líneas sumaran los totales: dos nóminas con filas corridas se guardaron sin aviso | ✅ `checkPayroll()`, segunda lectura, marcas ⚠ y corrección de guardadas ([§20](#20-comprobación-de-las-cuentas-y-corrección)) |
| 11 | `fmt()` usaba `toLocaleString('es-ES')`, que no pone punto en las cifras de 4 dígitos (2100,10 pero 21.000,00); y `editField` leía «2.100,10» como 2,1 | ✅ `fmt()` agrupa siempre a mano; `num()` lee los formatos españoles |

Pendiente:

| # | Qué | Efecto | Solución prevista |
|---|---|---|---|
| 6 | Las pruebas solo usan Chromium | El menú de compartir, el almacenamiento de iPhone/Safari y pegar el enlace en la app instalada de iPhone no están cubiertos | Añadir WebKit a las pruebas y probar en un iPhone real |
| 7 | La key va en la URL de la petición a Gemini (`?key=`) | Es HTTPS y va a Google, pero las URLs acaban más a menudo en registros que las cabeceras | Enviarla en la cabecera `x-goog-api-key` (comprobar antes con una lectura real) |
| 12 | La segunda lectura y el prompt nuevo solo están probados con respuestas simuladas | No se sabe aún cuántas veces la segunda lectura arregla de verdad una nómina mal leída | Probarlo con las nóminas reales que no cuadraban (releerlas desde *Ver*) |
| 13 | Las comprobaciones no ven un error que siga cuadrando (conceptos cambiados con sus importes bien) | Raro, pero posible | La revisión humana sigue siendo obligatoria. La plantilla de códigos (§20) cubre parte |
| 14 | En el móvil, las tablas de la revisión necesitan desplazarse a los lados para ver la columna de importe | Las celdas marcadas de importe pueden quedar fuera de la vista | Diseño de tabla para pantallas estrechas |

---

## 17. Publicar una versión

1. Hacer los cambios en `index.html` (y en `sw.js` si hace falta).
2. **Subir la versión** en los tres sitios: insignia del logo (`Forense vX.Y`), `version` en `createBackupData()` e insignia del README. Añadir la versión a *Novedades* y al *Changelog*.
3. Cambiar `CACHE_VERSION` en `sw.js` **solo** si ha cambiado `sw.js` o la lista de librerías.
4. Ejecutar las pruebas: `python tests/ejecutar_todo.py`.
5. Commit y push a `main`. GitHub Pages publica en 1–3 minutos.
6. Comprobar: abrir `https://asesorian.github.io/nomina-auditor/?v=<cualquier cosa>` y mirar la versión del logo. En el móvil, cerrar y abrir la app con conexión (o *Datos → Forzar actualización*).
7. Si usas una copia local (acceso directo a `index.html`): `git pull` en esa carpeta. Recuerda que sus datos son independientes de los de la web.

---

## 18. Actualizar PDF.js y otras librerías

1. Elegir versión en [cdnjs](https://cdnjs.com/libraries/pdf.js). **Ojo:** desde la 4.0, PDF.js se distribuye como módulos ES (`.mjs`), que no se pueden cargar con un `<script>` normal como hace `loadScriptOnce()`. Pasar a 4.x o posterior exige adaptar `loadPdfJs()` (manteniendo la comprobación SRI), no solo cambiar la URL. A cambio, desde la 4.2.67 CVE-2024-4367 está corregido de raíz (aun así, mantener `isEvalSupported: false`).
2. Calcular la huella SRI de cada archivo y anteponerle `sha384-` (o copiarla de cdnjs):
   ```bash
   curl -s https://cdnjs.cloudflare.com/ajax/libs/pdf.js/VERSION/pdf.min.js | openssl dgst -sha384 -binary | openssl base64 -A
   ```
3. Actualizar `PDFJS_BASE` y `PDFJS_FILES` en `index.html`.
4. Poner la misma versión de `pdfjs-dist` en `tests/package.json` y ejecutar `cd tests && npm install`.
5. `python tests/ejecutar_todo.py`: antes de empezar comprueba que la versión y las huellas coinciden con los archivos locales y, si no, dice qué falta.

**JSZip o QRCode.js:** cambiar la URL **y la huella `integrity`** en `index.html`, la URL en `CDN_ASSETS` de `sw.js` y subir `CACHE_VERSION`. Para JSZip, también su versión en `tests/package.json` (`ejecutar_todo.py` comprueba que la huella coincide con el archivo local). Huella desde Windows, sin `openssl`:
```powershell
$r=Invoke-WebRequest -UseBasicParsing URL; $m=New-Object IO.MemoryStream; $r.RawContentStream.CopyTo($m); "sha384-" + [Convert]::ToBase64String([Security.Cryptography.SHA384]::Create().ComputeHash($m.ToArray()))
```

---

## 19. Pruebas automáticas

Once baterías (más de 300 comprobaciones) con Chromium en tamaño móvil, sin internet y sin gastar lecturas de Gemini. Cómo prepararlas, qué cubre cada una y cómo funcionan por dentro: [tests/README.md](../tests/README.md).

```bash
python tests/ejecutar_todo.py              # todas (~2 minutos)
python tests/ejecutar_todo.py visor irpf   # solo algunas
```

---

## 20. Comprobación de las cuentas y corrección

Desde la v2.7.2. Gemini se equivoca de formas concretas (en nóminas reales: filas de deducciones corridas con una línea perdida, y el precio por día tomado como importe). Una nómina tiene cuentas que se pueden comprobar con sus propias cifras, así que el código las comprueba siempre.

### Qué es cada línea (`deductionKind`)

Por el texto del concepto normalizado (`compactText`/`spacedText`: sin acentos ni signos), nunca por la IA:

| Tipo | Ejemplos que reconoce |
|---|---|
| `irpf` | `TRIBUTACION I.R.P.F.20,42`, `I.R.P.P.`, `RETENCION IRPF` (no `Retención judicial`, embargos, pensiones o alimentos) |
| `cc` | `CONT.COMU`, `Contingencias comunes`, `CONTING. COMUNES`, `Cotiz. CC` |
| `mei` | `MEI`, `M.E.I.`, `equidad intergeneracional` |
| `fp` | `FORMACION`, `Formación Prof.`, `FP` |
| `desempleo` | `DESEMPLEO`, `Desemp.` |
| `solidaridad` | `Cotización adicional de solidaridad` |
| `ss` | cualquier otra con `cotiz…` o `seg. social` (p. ej. `COTIZACION HORAS EXT`) |
| `especie` | `Dcto. conceptos en especie` |
| `otra` | el resto (embargos, anticipos…) |

S.S. del trabajador (`calcSSTotal`) = suma de `cc`, `mei`, `fp`, `desempleo`, `solidaridad` y `ss`.

### Comprobaciones (`checkPayroll`, `checkSums`)

Devuelven `{ level, key, text, paths }`. `paths` son las celdas afectadas (`deductions.3.amount`, `totals.grossTotal`…) para marcarlas en la revisión (`flagMap` → clases `flag-err` / `flag-warn`). Tolerancia `CHECK_TOL` = 0,02 €.

| Clave | Comprobación | Nivel |
|---|---|---|
| `sumE` | suma de devengos = `grossTotal` | `err` |
| `sumD` | suma de deducciones = `totalDeductions` | `err` |
| `net` | `grossTotal` − `totalDeductions` = `netPay` | `err` |
| `irpfMissing` / `irpf` | hay línea de IRPF y vale base IRPF × % (si el % no es calculado ni aproximado) | `err` / `warn` |
| `ss<i>` | cotización con su % (en `units` o en el concepto) = base × %. Vale con cualquiera de las bases posibles: C.C., A.T. o el importe de horas extra. Sin falsas alarmas en las nóminas reales probadas | `warn` |
| `up-earnings<i>` | devengos: unidades × precio = importe (si hay `price`) | `warn` |
| `bcc` | remuneración + prorrata = base C.C. (solo mensual) | `warn` |
| `tpl-<lado><i>` | **plantilla:** el código lleva un concepto parecido (`conceptSimilarity` ≥ 0,6, sin dígitos) al de tus otras nóminas de la misma empresa (mismo CIF) que cuadran; la más reciente manda (`codeTemplate`). Detecta filas corridas | `warn` |

`checkErrors(p)` = solo los `err`. `readScore(d)` = errores × 100 + avisos (menor es mejor).

### Lectura con comprobación (`readWithChecks`)

1. `callGemini()` → `prepareExtracted()` → `checkErrors()`. Si no hay errores, se usa.
2. Si hay errores: `callGemini(…, feedbackFor(primera))` con la lista de fallos y la plantilla de códigos como referencia, y se queda con la lectura de menor `readScore`. Si la segunda falla (error de red o de Gemini), se queda la primera.
3. `readInfo` guarda cómo fue (`reads`, `chosen`, `okNow`, `retryFailed`; `manual`/`worse` en las relecturas a mano) y `readInfoHtml()` lo explica en la revisión.

Coste: una segunda lectura (~0,9 céntimos) solo cuando hay errores.

### En pantalla

- **Revisión:** `renderChecks()` arriba, con *👁 Ver documento* (`viewCurrentDocument`) y, si hay avisos, *🔁 Releer con Gemini* (`rereadCurrent`: nueva lectura con `feedbackFor`; se queda solo si `readScore` es igual o mejor). `addLine` / `removeLine` para filas que falten o sobren.
- **Guardar:** con errores, `confirm()` que los lista.
- **Ver:** tarjeta *Comprobación de las cuentas* con *✏ Corregir datos* y *🔁 Releer con Gemini* (`editAndReread`, con el original guardado). El texto para el abogado lleva `⚠ AVISO…` arriba si hay errores y la sección *5. AVISOS DE LA COMPROBACIÓN AUTOMÁTICA* al final si hay cualquier aviso.
- **Panel y Anual:** `checkFlag()` pone ⚠ junto al mes; el Panel muestra un aviso con las nóminas que no cuadran y el Anual lo pone como primera observación (y en el texto exportable).

### Corregir una nómina guardada (`editPayroll`, `saveEdited`)

- `editingId` = id de la nómina que se corrige. `editPayroll(id)` copia sus datos (sin `id`, `savedAt`, `editedAt`, `original`) a `extractedData` y abre la revisión con el aviso azul y los botones *Guardar cambios* / *Cancelar*. El tipo se muestra como guardado (`typeDetection.saved`).
- `saveEdited(draft)`: mismo mes y tipo → mismo `id`. Si cambian, `freePayrollId(draft, id)`: si el hueco está ocupado, avisa y no cambia nada (nunca pisa otra nómina). Conserva `savedAt` y `original`, añade `editedAt`.
- `currentDocument()` en modo corrección lee el original de IndexedDB (`getDoc` → `arrayBufferToB64`) para releer sin volver a subirlo.
- Salir de la revisión (`showView` a otra pestaña), *Cancelar* (`cancelEdit`) o elegir un archivo nuevo (`handleFile`) anula el modo corrección sin cambiar nada.

### Números (`num`, `fmt`, `amt`, `round2`)

- `num(v)`: lee `2.100,10`, `2100,10`, `2100.10`, `2.100` (miles), `1,234.56`, con `€` o espacios. Lo que no es número → `NaN`.
- `fmt(n)`: siempre 2 decimales y punto de miles, agrupado a mano (el navegador en español no agrupa las cifras de 4 dígitos). `"N/L"` o no numérico → `N/L`.
- `amt(v)`: para sumar (no numérico → 0). `round2()`: redondeo a céntimos.
