# ⚖️ Nómina Auditor Forense

**Extractor y auditor de nóminas españolas con arquitectura híbrida determinista + IA**

![Version](https://img.shields.io/badge/version-2.5-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-PWA-blueviolet)
![Offline](https://img.shields.io/badge/offline-ready-4ade80)
![Architecture](https://img.shields.io/badge/architecture-deterministic%20first-c9a227)

### 👉 [Abrir la app](https://asesorian.github.io/nomina-auditor/)

---

## 🎯 ¿Qué es?

**Nómina Auditor Forense** es una aplicación web (PWA) para guardar, revisar y auditar tus nóminas españolas. Haces una foto o subes el PDF, la IA lee los datos, **tú los revisas** y a partir de ahí todo lo calcula código determinista. La IA nunca decide una cifra.

✅ Lee fotos y PDFs de nóminas con IA (Gemini) y te deja revisar cada dato antes de guardarlo  
✅ Todos los cálculos y comprobaciones los hace código determinista: la IA nunca calcula cifras  
✅ **Mensual, paga extra y atrasos** guardados por separado: varias nóminas en el mismo mes sin pisarse  
✅ **% de retención de IRPF** siempre visible: leído, deducido de la propia nómina o calculado, y corregible a mano  
✅ Informe mensual e informe anual en texto listo para tu abogado, con avisos de cambios y de meses que faltan  
✅ Aviso antes de sobrescribir una nómina, con comparación de importes  
✅ Backup automático, exportación e importación (JSON o ZIP)  
✅ Instalable en el móvil, **funciona sin conexión** y se actualiza sola  
✅ Tus datos se quedan en tu dispositivo (solo la foto/PDF viaja a Gemini para leerla)

---

## 🆕 Novedades (v2.3 – v2.5)

| | Qué hace | Dónde |
|---|---|---|
| 💰 **Pagas extra y atrasos** | La paga extra de julio ya no machaca la nómina mensual de julio: cada una tiene su sitio. La app detecta sola el tipo y tú lo confirmas | [Ver sección](#-pagas-extra-atrasos-y-varias-nóminas-en-el-mismo-mes) |
| 🔁 **Cambiar el tipo de una nómina guardada** | Si una extra se guardó como mensual (o al revés), se recoloca sin volver a procesarla | Panel → Ver → *Tipo de nómina* |
| 📈 **% de IRPF sin huecos** | Si la nómina no trae el % en las bases, se saca de la línea de IRPF o se calcula. Se puede corregir a mano | [Ver sección](#-porcentaje-de-retención-de-irpf) |
| ⚠️ **Aviso de duplicados mejorado** | Compara importes y te deja guardar aparte en vez de solo sobrescribir | Al guardar |
| 📴 **Modo sin conexión** | La app se abre sin internet para consultar, corregir y exportar | [Ver sección](#-uso-sin-conexión-y-actualizaciones) |
| 🗓️ **Informe anual más útil** | Marca las extras, avisa de meses sin nómina mensual y no da falsas alarmas por las extras | Anual |

Tus nóminas y backups de versiones anteriores siguen funcionando tal cual: no hay que migrar nada.

---

## 🔧 Cómo se usa (paso a paso)

### 1️⃣ Configura tu API key de Gemini (una sola vez)
Es gratis. Ver [Configuración API Key](#-configuración-api-key-de-gemini-gratis). Para pasarla al móvil sin teclear, usa el botón **📱 Enviar al móvil**.

### 2️⃣ Sube la nómina
- Pestaña **Subir** → arrastra o selecciona la foto o el PDF
- Pulsa **Procesar con Gemini IA**. En unos segundos verás los datos extraídos
- Necesita conexión a internet (la lectura la hace Gemini)

### 3️⃣ Revisa los datos (fase 1, obligatoria)
- Arriba aparece el **Tipo de nómina**: 📄 *Mensual*, 💰 *Paga extra* o 📎 *Atrasos*, con el motivo por el que se ha detectado. Si no es correcto, tócalo para cambiarlo
- Toca cualquier valor subrayado para corregirlo. Los números se pueden escribir con coma (`20,42`)
- Revisa sobre todo importes, % IRPF y bases de cotización. Si el % de IRPF no venía en las bases, la app lo rellena y te avisa en naranja para que lo compruebes con el papel

### 4️⃣ Guarda
- Pulsa **✓ Confirmar y Guardar**
- Si ya tienes una nómina en ese mismo sitio (mismo mes y tipo), aparece un aviso con los importes de las dos y estas opciones:

| Opción | Qué hace |
|---|---|
| 💰 Es una paga extra → guardarla aparte | La guarda como paga extra de ese mes. **No borra nada** |
| 📎 Son atrasos → guardarlos aparte | La guarda como atrasos de ese mes. **No borra nada** |
| ➕ Es otra paga extra distinta | Si ya había una extra ese mes, guarda una segunda |
| ♻ Sustituir la guardada | Reemplaza la anterior (se pierde) |
| Cancelar | No guarda nada. Si los importes coinciden, la app te avisa de que probablemente ya la tenías |

- Si el backup automático está activado, se descarga una copia de seguridad

### 5️⃣ Consulta
- **Panel:** totales del año (bruto, neto, IRPF, Seguridad Social) y lista de nóminas. Las extras y atrasos muestran su nombre en negrita bajo el mes
- **Ver** (en cada nómina): informe completo, listo para copiar y enviar a tu abogado
- **Anual:** tabla de todo el año, totales y observaciones automáticas

### 6️⃣ Corrige algo ya guardado (desde Ver)
- **Tipo de nómina:** cambia entre Mensual, Paga extra y Atrasos sin volver a procesarla
- **% Retención IRPF → ✏ Corregir %:** escribe el porcentaje correcto. Si lo dejas vacío, la app lo vuelve a calcular sola
- Para eliminar una nómina: botón 🗑 en el Panel

### 7️⃣ Haz copias de seguridad
Pestaña **Datos**. Ver [Copias de seguridad y varios dispositivos](#-copias-de-seguridad-y-varios-dispositivos).

---

## 💰 Pagas extra, atrasos y varias nóminas en el mismo mes

Un mismo mes puede tener varias nóminas: la mensual, una paga extra, unos atrasos… Cada una se guarda en su propio sitio y ninguna pisa a otra.

**Tipos de nómina**
- 📄 **Mensual:** la nómina normal del mes, aunque incluya la prorrata de pagas extras o la paga extra como una línea más
- 💰 **Paga extra:** nómina de paga extraordinaria emitida aparte (verano, Navidad, beneficios…). Puede haber más de una en el mismo mes
- 📎 **Atrasos:** nómina solo de atrasos o diferencias de convenio

**Cómo detecta el tipo (con reglas, no con la IA)**
- Si los conceptos de paga extra (*Paga extra*, *Gratificación extraordinaria*, *Extra verano/Navidad/beneficios*…) suman **el 60 % o más del bruto**, es una paga extra
- Igual para atrasos (*Atrasos*, *Diferencias de convenio*, *Regularización salarial*…)
- La **prorrata de pagas extras** de una mensual no la convierte en extra, y las **horas extraordinarias** tampoco
- Lo que Gemini lee en la cabecera del documento solo cuenta como pista cuando los conceptos no son concluyentes
- Siempre lo confirmas tú en la verificación, antes de guardar

**En los informes**
- Las extras y atrasos **suman en los totales** del año
- Las comprobaciones de estabilidad (variación del % IRPF, de la base de cotización o de la categoría) se hacen **solo con las nóminas mensuales**. Una paga extra suele llevar la base de cotización a 0 porque va prorrateada, y daría una falsa alarma
- El informe anual avisa de los **meses sin nómina mensual** entre enero y el último mes con datos

---

## 📈 Porcentaje de retención de IRPF

El % de IRPF aparece en el Panel, en el informe de cada nómina y en el informe anual. Se obtiene siempre con este orden, por código:

1. El % que figura en las **bases** de la nómina (o el que hayas corregido a mano)
2. El % impreso en la propia **línea de IRPF** (ej. *TRIBUTACIÓN IRPF 20,42*)
3. **Calculado:** importe retenido ÷ base IRPF
4. **Aproximado:** importe retenido ÷ bruto, si la nómina no trae base IRPF

Los valores calculados o aproximados llevan un asterisco (`20,42 %*`). En el informe de cada nómina se indica de dónde sale el valor. Si no hay forma de obtenerlo, aparece `N/L` y puedes escribirlo a mano con **Ver → ✏ Corregir %**.

---

## 📴 Uso sin conexión y actualizaciones

**Activarlo:** abre la app una vez con conexión, ciérrala y vuelve a abrirla. En **Datos → Modo sin conexión** debe poner **Activo**.

**Sin conexión puedes:** ver el Panel, los informes y el Anual, cambiar el tipo de una nómina, corregir el % IRPF y exportar backups. Aparece un aviso naranja de "Sin conexión".

**Sin conexión no puedes:** procesar una nómina nueva, porque la lectura la hace Gemini. La app te avisa; cuando vuelvas a tener conexión, pulsa otra vez *Procesar*.

**Actualizaciones:** cuando se publica una versión nueva, te llega sola la próxima vez que abras la app con conexión. No hay que reinstalar nada. **Las actualizaciones solo cambian el código de la app: tus nóminas y tu API key no se tocan.**

**Si ves una versión antigua:** **Datos → 🔄 Forzar actualización de la app**. Tampoco borra nóminas ni API key.

> En el ordenador, si abres `index.html` como archivo local, el modo sin conexión no aplica ni hace falta: el archivo ya está en tu disco. Para actualizarlo, descarga de nuevo `index.html` o haz `git pull` si clonaste el repo.

---

## 💾 Copias de seguridad y varios dispositivos

- **Backup automático:** cada vez que guardas o cambias una nómina se descarga un archivo `nominas-backup-FECHA.json` en *Descargas*. Se puede desactivar en *Datos*
- **Exportar:** *Datos → Exportar todo*
- **Importar:** *Datos → Restaurar*. Acepta el `.json` o el `.zip` directamente, sin descomprimir

**Móvil y ordenador no se sincronizan solos.** Cada dispositivo guarda sus propias nóminas. Para tener lo mismo en los dos: exporta en uno e importa en el otro.

> ⚠️ **Al importar,** las nóminas del backup se añaden y, si ya tienes una en el mismo sitio (mismo mes y tipo), **se sustituye por la del backup**. Usa siempre el backup más reciente para no perder correcciones posteriores.

> ⚠️ **Si borras los datos de navegación** de la web de la app, se borran también tus nóminas. La app se recupera sola con conexión, pero las nóminas solo desde un backup. Mantén activado el backup automático.

---

## 📱 Instalación

### En el móvil (recomendado)

**Android:**
1. Abre [la app](https://asesorian.github.io/nomina-auditor/) en **Chrome**
2. Toca el menú (⋮) → **"Instalar app"** (o "Añadir a pantalla de inicio")
3. Aparece en la pantalla de inicio como una app más, con icono ⚖️

**iPhone (iOS):**
1. Abre [la app](https://asesorian.github.io/nomina-auditor/) en **Safari**
2. Toca compartir → **"Agregar a Pantalla de Inicio"**

Después, ábrela una segunda vez con conexión para dejar activo el [modo sin conexión](#-uso-sin-conexión-y-actualizaciones).

### En el ordenador

Abre [la app](https://asesorian.github.io/nomina-auditor/) en el navegador (se puede instalar igual que en el móvil) o descarga `index.html` y ábrelo directamente. Es un archivo autónomo, sin servidor ni instalación.

---

## 🔑 Configuración API Key de Gemini (Gratis)

1. Ve a [Google AI Studio](https://aistudio.google.com/apikey)
2. Crea una API Key. **Importante: selecciona un proyecto nuevo de Google Cloud**, no el proyecto por defecto (en cuentas europeas el proyecto por defecto suele tener `limit: 0` en la capa gratuita)
3. Si no tienes proyecto nuevo: crea uno en [Google Cloud Console](https://console.cloud.google.com) → habilita "Generative Language API" → genera la key con ese proyecto
4. Pega la key en la barra superior de la app → aparece `✓ Configurada` en verde

La key se guarda en el almacenamiento local del navegador. Solo se usa para llamar directamente a Gemini.

### 📱 Pasar la key al móvil (sin teclear)

Teclear una API Key en el móvil es propenso a errores: el teclado autocorrige, cambia mayúsculas o sustituye letras parecidas (`l`, `I`, `1`).

1. En el **ordenador**, donde ya funciona, pulsa el botón amarillo **📱 Enviar al móvil**
2. Aparece un **código QR**
3. En el **móvil**, abre la cámara y apunta al QR
4. La app se abre con la key ya guardada

> La key va dentro del enlace del QR, en la parte tras `#`, que el navegador **nunca envía a ningún servidor**. Al abrirse, la app la guarda y limpia la dirección. Trata el QR como una contraseña: no lo enseñes ni le hagas captura.

**Botón 👁:** muestra u oculta la key para comprobar que está bien escrita.

---

## ❓ Problemas frecuentes

**Subí una paga extra y machacó la nómina mensual (versiones anteriores a 2.3)**
1. Panel → la nómina de ese mes → **Ver** → en *Tipo de nómina* toca **Paga extra**. Pasa a su propio sitio
2. Vuelve a subir la nómina mensual, o importa un backup anterior al error, que la recupera sin tocar la extra

**El % de IRPF sale `N/L` o con `*`**
- `*`: no venía en las bases y se ha calculado. Compruébalo con el papel
- `N/L`: no se ha podido obtener. En ambos casos: **Ver → ✏ Corregir %**

**Veo una versión antigua de la app**
- Cierra y vuelve a abrir la app con conexión. Si sigue igual: **Datos → 🔄 Forzar actualización**

**No me deja procesar una nómina**
- Si aparece "Sin conexión": hace falta internet para que Gemini la lea

**"limit: 0" o "quota exceeded"**
- El proyecto de Google Cloud de tu key tiene la capa gratuita bloqueada (típico en Europa)
- Solución: crea un proyecto **nuevo** en [Google Cloud Console](https://console.cloud.google.com), habilita "Generative Language API" y genera una key nueva con ese proyecto desde [AI Studio](https://aistudio.google.com/apikey)

**"Unable to process input image" en todos los modelos**
- El archivo tiene extensión de imagen pero por dentro es un PDF: la app lo detecta correctamente desde v2.2
- O la imagen está corrupta: prueba con otra foto

**"El modelo X ya no está disponible"**
- Google retira modelos de Gemini cada cierto tiempo
- La app usa la cadena `gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.5-pro` (activos en mayo de 2026)
- Si alguno falla, el error muestra cuál y por qué. Se cambia en el array `GEMINI_MODELS` del código

**La foto no se extrae bien**
- Foto bien enfocada, con la nómina ocupando casi toda la imagen
- Resolución mínima recomendada: 1024 px
- Si un campo falla siempre, corrígelo a mano en la verificación

**No me sale el botón de instalar en el móvil**
- Usa Chrome (Android) o Safari (iOS) y espera a que la página cargue del todo

---

## 🔬 Arquitectura: decisión determinista + IA acotada

Este repo aplica la filosofía **"código científico, IA divulgadora"** a un caso real:

> **El código hace el trabajo del científico: calcula con rigor, verifica con datos, aplica reglas auditables. El LLM hace el trabajo del divulgador: comunica en lenguaje accesible lo que el código ha determinado. Cada uno en lo que es genuinamente bueno.**

### Pipeline técnico real

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 0 — Detección de formato (magic bytes)                 │
│ %PDF → se envía como application/pdf a Gemini               │
│ Imagen → se convierte a JPEG vía Canvas (cualquier formato) │
│ Redimensiona automáticamente si >2500px                     │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 1 — Extracción OCR (Gemini con fallback en cadena)     │
│ gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.5-pro   │
│ Cualquier error en un modelo cae al siguiente               │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 1b — Normalización y clasificación (código)            │
│ Mes normalizado ("JULIO", "7" → Julio)                      │
│ Tipo de nómina por reglas (≥60% del bruto en conceptos)     │
│ % IRPF: bases → línea de IRPF → importe ÷ base              │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2 — Verificación humana (obligatoria)                  │
│ El usuario corrige cualquier campo y confirma el tipo       │
│ Si el sitio mes+tipo ya existe: aviso con comparación y     │
│ opción de guardar aparte en vez de sobrescribir             │
│ Hasta que confirma, no se guarda ni se calcula nada         │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 3 — Cálculos (100% código determinista)                │
│ calcTotals() suma brutos, netos, IRPF, bases                │
│ findIRPFDeduction() / irpfRateOf() retención y su %         │
│ calcSSTotal() suma contingencias + desempleo + formación    │
│ CERO LLM en esta fase. Matemática pura en JavaScript.       │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 4 — Detección de anomalías (código determinista)       │
│ Solo sobre nóminas mensuales:                               │
│ - Variación en % IRPF entre meses                           │
│ - Cambios en Base de Cotización                             │
│ - Cambios de Categoría o tipo de Contrato                   │
│ - Meses sin nómina mensual                                  │
│ Output: booleanos y listados. No "interpretación" de IA.    │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 5 — Informe final (plantilla de texto, sin LLM)        │
│ Tabla resumen anual con extras y atrasos etiquetados        │
│ Observaciones ("⚠ VARIACIÓN" / "✓ Sin cambios")             │
│ Formato exportable para abogados                            │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué esta arquitectura?

En dominios donde las cifras y las normas importan (nóminas, banca, legal, sanidad), **una alucinación = problema real**. Un LLM que "calcula mal" un IRPF o "interpreta" una variación puede generar un informe inútil o engañoso que llegue a un abogado.

La decisión arquitectónica aquí es clara:
- **Donde el LLM aporta valor único (OCR de imagen irregular)** → lo usamos
- **Donde el código determinista es más seguro (cálculos, reglas, clasificación, comparaciones)** → código puro
- **Validación humana como puente entre ambos** → el humano corrige lo que el OCR alucinó antes de que llegue al código

Esto no es "anti-IA". Es IA aplicada donde aporta valor genuino y código aplicado donde la matemática no debe fallar.

### Cómo se guarda cada nómina

Cada nómina tiene un identificador según mes y tipo, de modo que nunca se pisan y quedan ordenadas juntas:

| Nómina | Identificador |
|---|---|
| Mensual de julio 2026 | `2026-07` (formato de siempre, compatible con backups antiguos) |
| Paga extra de julio 2026 | `2026-07-extra` |
| Segunda paga extra de julio | `2026-07-extra-2` |
| Atrasos pagados en julio | `2026-07-atrasos` |

Las nóminas guardadas antes de la v2.3, sin tipo, se consideran mensuales.

---

## 📊 Datos extraídos

```
ADMINISTRATIVOS
├─ Empresa (nombre, CIF, CCC)
├─ Trabajador (nombre, NAF, DNI)
└─ Empleo (categoría, antigüedad, tipo de contrato)

PERÍODO Y TIPO
├─ Mes / Año
├─ Fechas de inicio y fin
├─ Días trabajados
└─ Tipo de nómina (mensual / paga extra / atrasos) y su nombre

DEVENGOS (Ganancias)
├─ Salario Base
├─ Pluses, incentivos, seguros…
└─ Pagas extra y atrasos

DEDUCCIONES
├─ IRPF (retención)
├─ Cotizaciones SS (contingencias, desempleo, formación)
└─ Otros descuentos

BASES Y TOTALES
├─ Bruto, deducciones, neto
├─ Bases de cotización y prorrata de pagas extras
└─ Base IRPF y % de retención (con su origen)
```

---

## 📍 Ámbito geográfico

⚠️ **Optimizada ÚNICAMENTE para nóminas españolas.**

- ✅ Compatible: cálculos españoles (IRPF, Seguridad Social, bases de cotización, pagas extraordinarias)
- ❌ No compatible: México, Colombia, Argentina u otros países hispanohablantes

---

## 🔒 Privacidad y datos

- Tus nóminas y tu API key se guardan **solo en el navegador de tu dispositivo** (localStorage). No hay servidor ni base de datos propia
- **Única excepción:** la foto o PDF se envía a Google Gemini para leerla
- El modo sin conexión guarda únicamente el **código** de la app, nunca tus datos
- Cada dispositivo guarda sus propios datos; no se sincronizan solos
- Exporta tus datos cuando quieras en JSON

> **Si publicas tu propia copia en GitHub Pages:** todas las webs que publiques bajo `tuusuario.github.io` comparten el mismo almacenamiento del navegador. No publiques ahí código de terceros sin revisarlo, porque podría leer las nóminas y la API key.

---

## 🛠️ Tecnología

- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **IA:** Google Gemini 2.5 (exclusivamente para OCR)
- **Dependencias (vía CDN):** JSZip 3.10 (importar backups en ZIP) y QRCode.js 1.0 (pasar la key al móvil)
- **Almacenamiento:** localStorage del navegador
- **PWA:** instalable, con service worker para uso sin conexión
- **Deploy:** GitHub Pages (HTTPS obligatorio para PWA y modo sin conexión)

**Archivos:**
- `index.html` (~90 KB): toda la aplicación. Sin frameworks, sin build step
- `sw.js` (~4 KB): modo sin conexión. Solo guarda el código de la app

**Cómo funciona el modo sin conexión (`sw.js`):**
- `index.html`: red primero, preguntando siempre al servidor si hay versión nueva (sin usar los 10 min de caché que permite GitHub Pages). Si no ha cambiado, el servidor responde "sin cambios" y apenas gasta datos. Sin red, o si tarda más de 4 s, la copia guardada
- Librerías y fuentes: copia guardada primero (sus URLs llevan versión fija)
- Las llamadas a Gemini (POST) no se interceptan nunca
- Solo actúa en la web publicada (https). Abierta como archivo local (`file://`) no aplica
- Las cachés usan el prefijo `nomina-auditor-` para no tocar las de otras apps del mismo dominio

---

## 📋 Changelog

### v2.5 (Octubre 2026)
- **Modo sin conexión:** la app instalada se abre sin internet (consultar, corregir, reclasificar, exportar). Procesar una nómina nueva sigue necesitando conexión (Gemini)
- Con conexión descarga siempre la última versión publicada (red primero; copia guardada si no hay red o tarda más de 4 s)
- Aviso visible de "Sin conexión" y botón **Forzar actualización** en Datos (no borra nóminas ni API key)
- **API key por QR más privada:** viaja tras `#` en el enlace, que no se envía a ningún servidor (antes iba como `?apikey=` y llegaba a GitHub). Los QR antiguos siguen funcionando
- Las etiquetas de estado de la pantalla Datos vuelven a tener estilo
- **Corregido:** justo después de publicar una versión, el móvil podía seguir mostrando la anterior hasta 10 minutos (caché de GitHub Pages). Ahora la app pregunta siempre al servidor
- El nombre de la paga extra o los atrasos aparece bajo el mes con la misma letra que los datos, en negrita (antes, etiqueta naranja)

### v2.4 (Octubre 2026)
- **% de IRPF sin huecos:** si la nómina no lo trae en las bases, se saca de la propia línea de IRPF ("TRIBUTACIÓN IRPF 20,42") o se calcula como importe retenido ÷ base IRPF. Los calculados se marcan con `*`
- **Corregir el % de IRPF a mano** desde el informe de cualquier nómina guardada (Ver → Corregir %); vacío vuelve al cálculo automático
- El % de IRPF aparece en el informe para el abogado con su origen (leído, deducido, calculado o corregido a mano)
- **Edición con coma:** al corregir un número en la verificación, "20,5" ahora se guarda como 20,5 (antes se quedaba en 20)
- El tipo "Ordinaria" pasa a llamarse **Mensual**, con texto que aclara para qué sirve

### v2.3 (Octubre 2026)
- **Pagas extra y atrasos:** varias nóminas por mes sin pisarse. Tipo de nómina con detección automática por conceptos y confirmación en la verificación
- **Aviso de duplicados rediseñado:** compara importes y ofrece guardar aparte en vez de solo sobrescribir
- **Reclasificar nóminas guardadas** desde su informe (arregla extras guardadas como mensual)
- **Informe anual:** extras etiquetadas, comprobaciones de estabilidad solo sobre mensuales, aviso de meses sin nómina mensual
- **Mes normalizado:** "JULIO", "julio" o "7" se guardan como "Julio"; un mes ilegible bloquea el guardado en lugar de crear un hueco erróneo

### v2.2 (Mayo 2026)
- **Detección de formato por magic bytes:** un PDF con extensión `.jpg` se detecta y procesa correctamente
- **Soporte PDF nativo:** enviado a Gemini como `application/pdf` sin conversión
- **Conversión universal de imágenes:** Canvas normaliza cualquier formato (AVIF, HEIC, WebP, BMP...) a JPEG antes de enviar
- **Redimensionado automático:** imágenes >2500px se reducen para no saturar la API
- **Fallback robusto de modelos:** cualquier error (no solo cuota) cae al siguiente modelo
- **Diagnóstico detallado:** el error final muestra qué pasó en cada modelo individualmente
- **Nuevos modelos:** cadena actualizada a `gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.5-pro` (eliminados `gemini-2.0-flash` y `gemini-1.5-flash`, retirados para cuentas nuevas)
- **Detección de duplicados:** aviso antes de sobrescribir un mes ya guardado
- **Importación de ZIP:** acepta el archivo comprimido directamente sin necesidad de descomprimirlo
- **Pasar la API key al móvil con QR**

### v2.1
- Fallback básico entre modelos Gemini
- Backup automático al guardar

### v2.0
- Arquitectura híbrida determinista + IA
- Verificación humana obligatoria entre OCR y cálculo
- Informes anuales con detección de anomalías

---

## 🧩 Reutilización para otros casos de uso

Este repo se publicó con la intención de servir como **base arquitectónica** para construir otros SaaS en dominios regulados donde las alucinaciones de IA no son aceptables.

**Patrón replicable:**
- **Sustituye Fase 1:** OCR de oferta hipotecaria, contrato de alquiler, póliza de seguro
- **Mantén Fase 2:** verificación humana siempre entre OCR y cálculo
- **Sustituye Fase 3-4:** cálculos y reglas específicos de tu dominio
- **Mantén Fase 5:** plantilla de texto sin LLM para generar el informe final

**Casos de uso donde este patrón aplica bien:**
- Asesor hipotecario (análisis de ofertas y subrogaciones)
- Auditor de facturas de suministros (luz, gas, agua)
- Revisor de contratos laborales
- Análisis de cláusulas en pólizas de seguros
- Validador de declaraciones fiscales básicas

---

## 📄 Licencia

MIT License — libre para usar, modificar y distribuir.

---

## 👤 Autor y contexto

Desarrollado como herramienta forense para auditar nóminas españolas y detectar irregularidades. El código está intencionalmente simple (un solo archivo HTML, más un pequeño `sw.js` para el modo sin conexión) para que sea auditable línea por línea por quien quiera usarlo, adaptarlo o aprender del patrón.

**Úsalo para:**
✓ Verificar que tu empresa te paga correctamente  
✓ Detectar errores en cálculos de IRPF o cotizaciones  
✓ Controlar pagas extra y atrasos  
✓ Generar informes para tu abogado  
✓ Auditar cambios en tus condiciones laborales  

---

## 🤝 Aportes

Si encuentras bugs, quieres proponer mejoras o adaptar el patrón a otro dominio, abre un issue o pull request.

---

## 🚀 Construido en comunidad SaaS Factory

Este proyecto nació en **SaaS Factory**, comunidad de makers y emprendedores españoles e hispanohablantes construyendo SaaS juntos.

La filosofía: **soluciones reales, prácticas y accesibles** para problemas del día a día. En este caso, ayudar a cualquier trabajador a auditar sus nóminas, detectar errores y proteger sus derechos laborales sin depender de gestorías caras ni de software cerrado.

**Únete a la comunidad:** [SaaS Factory](https://www.saasfactory.so/)

---

**Made with ⚖️ for honesty in numbers.**
