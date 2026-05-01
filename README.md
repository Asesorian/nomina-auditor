# ⚖️ Nómina Auditor Forense

**Extractor y auditor de nóminas españolas con arquitectura híbrida determinista + IA**

![Version](https://img.shields.io/badge/version-2.2-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-PWA-blueviolet)
![Architecture](https://img.shields.io/badge/architecture-deterministic%20first-c9a227)

---

## 🎯 ¿Qué es?

**Nómina Auditor Forense** es una aplicación web (PWA) que te permite auditar tus nóminas españolas con una arquitectura diseñada para **minimizar alucinaciones de IA en los cálculos críticos**.

✅ Extracción OCR automática de fotos y PDFs de nóminas (Gemini 2.5 Flash)  
✅ Detección automática de formato: imagen (JPG, PNG, AVIF, HEIC...) o PDF  
✅ Conversión automática de cualquier imagen a JPEG antes de enviar a Gemini  
✅ Fallback automático entre modelos Gemini si alguno falla  
✅ Verificación humana campo por campo (validador determinista)  
✅ Cálculos totales 100% código determinista (nunca un LLM calcula cifras)  
✅ Detección de anomalías con reglas auditables (no con LLM "interpretando")  
✅ Informes mensuales y anuales en texto plano exportable  
✅ Detección de nóminas duplicadas con aviso antes de sobreescribir  
✅ Importación de backups en JSON o ZIP directamente, sin descomprimir  
✅ PWA instalable en móvil y escritorio  
✅ 100% local: datos nunca salen de tu dispositivo (excepto la foto/PDF a Gemini para OCR)

---

## 🔬 Arquitectura: decisión determinista + IA acotada

Este repo aplica la filosofía **"código científico, IA divulgadora"** a un caso real:

> **El código hace el trabajo del científico: calcula con rigor, verifica con datos, aplica reglas auditables. El LLM hace el trabajo del divulgador: comunica en lenguaje accesible lo que el código ha determinado. Cada uno en lo que es genuinamente bueno.**

### Pipeline técnico real

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 0 — Detección de formato (magic bytes)                 │
│ Lee los primeros bytes del archivo                          │
│ %PDF → envía como application/pdf a Gemini                  │
│ Imagen → convierte a JPEG via Canvas (cualquier formato)    │
│ Redimensiona automáticamente si >2500px                     │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 1 — Extracción OCR (Gemini con fallback en cadena)     │
│ Intenta: gemini-2.5-flash → gemini-2.5-flash-lite →         │
│          gemini-2.5-pro                                     │
│ Cualquier error en un modelo cae al siguiente               │
│ Si todos fallan: muestra error detallado de cada modelo     │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2 — Verificación humana (validador determinista)       │
│ El usuario edita inline cualquier campo mal extraído        │
│ Detección de duplicados: si el mes/año ya existe,           │
│ muestra modal de confirmación antes de sobreescribir        │
│ Hasta que confirma, no se calcula nada                      │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 3 — Cálculos (100% código determinista)                │
│ calcTotals() suma brutos, netos, IRPF, bases de cotización  │
│ findIRPFDeduction() extrae retención con filtro léxico      │
│ calcSSTotal() suma contingencias + desempleo + formación    │
│ CERO LLM en esta fase. Matemática pura en JavaScript.       │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 4 — Detección de anomalías (código determinista)       │
│ Comparaciones mes a mes con reglas auditables:              │
│ - Variación en % IRPF entre meses                           │
│ - Cambios en Base de Cotización                             │
│ - Cambios de Categoría o tipo de Contrato                   │
│ Output: booleanos y listados. No "interpretación" de IA.    │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 5 — Informe final (template plano, sin LLM)            │
│ Tabla resumen anual generada con template de strings        │
│ Observaciones booleanas ("⚠ VARIACIÓN" / "✓ Sin cambios")   │
│ Formato exportable para abogados                            │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué esta arquitectura?

En dominios donde las cifras y las normas importan (nóminas, banca, legal, sanidad), **una alucinación = problema real**. Un LLM que "calcula mal" un IRPF o "interpreta" una variación puede generar un informe inútil o engañoso que llegue a un abogado.

La decisión arquitectónica aquí es clara:
- **Donde el LLM aporta valor único (OCR de imagen irregular)** → lo usamos
- **Donde el código determinista es más seguro (cálculos, reglas, comparaciones)** → código puro
- **Validación humana como puente entre ambos** → el humano corrige lo que el OCR alucinó antes de que llegue al código

Esto no es "anti-IA". Es IA aplicada donde aporta valor genuino y código aplicado donde la matemática no debe fallar.

---

## 🚀 Funcionalidades

### Ingesta inteligente de archivos
- Arrastra cualquier archivo o haz clic para seleccionar
- **Detección automática por magic bytes** (no por extensión): da igual que un PDF venga con extensión `.jpg`, se detecta correctamente
- **PDFs:** enviados nativamente a Gemini como `application/pdf`
- **Imágenes** (JPG, PNG, AVIF, HEIC, WebP, BMP...): convertidas a JPEG via Canvas antes de enviar, con redimensionado automático si superan 2500px
- **Previsualización:** imagen renderizada o icono 📄 para PDFs

### Extracción con fallback robusto
- Cadena de modelos: `gemini-2.5-flash` → `gemini-2.5-flash-lite` → `gemini-2.5-pro`
- Cualquier error (cuota, imagen no soportada, timeout) cae automáticamente al siguiente modelo
- Si todos fallan, el error muestra qué pasó exactamente en **cada modelo** para diagnosticar fácilmente

### Verificación humana (crítica)
- Click en cualquier valor para editarlo inline
- Validación visual de datos administrativos (empresa, trabajador, fechas)
- Revisión línea por línea de devengos y deducciones
- **Esta fase es intencionalmente obligatoria**: hasta que no confirmas, no se calcula nada

### Detección de duplicados
- Al confirmar una nómina, comprueba si ya existe una del mismo mes/año
- Si existe: modal de confirmación con nombre del período antes de sobreescribir
- Protege datos verificados y editados manualmente contra sobrescrituras accidentales

### Backup y sincronización entre dispositivos
- Backup automático en JSON al guardar cada nómina
- Exportación manual completa
- **Importación directa desde ZIP o JSON** — no hace falta descomprimir el ZIP
- Merge inteligente al importar: nuevas nóminas se añaden, las existentes se actualizan
- Flujo recomendado ordenador ↔ móvil: exportar en un dispositivo, importar en el otro

### Informes auditables
- **Informe mensual:** resumen completo de nómina verificada
- **Informe anual:** tabla comparativa de todos los meses del año
- Detección automática de anomalías con umbrales transparentes

---

## 📱 Instalación

### Como PWA en móvil

**Android:**
1. Abre la URL de GitHub Pages en **Chrome**
2. Toca menú (⋮) → **"Instalar app"** (o "Añadir a pantalla de inicio")
3. Aparece en pantalla de inicio como app nativa, con icono ⚖️

**iPhone (iOS):**
1. Abre la URL en **Safari**
2. Toca compartir → **"Agregar a Pantalla de Inicio"**

### En desktop

Abre `index.html` directamente en cualquier navegador moderno. Es un archivo único autónomo, sin servidor, sin build step.

---

## 🔧 Configuración API Key de Gemini (Gratis)

1. Ve a [Google AI Studio](https://aistudio.google.com/apikey)
2. Crea una API Key — **importante: selecciona un proyecto nuevo de Google Cloud**, no el proyecto por defecto (en cuentas europeas el proyecto por defecto suele tener `limit: 0` en la capa gratuita)
3. Si no tienes proyecto nuevo: crea uno en [Google Cloud Console](https://console.cloud.google.com) → habilita "Generative Language API" → genera la key con ese proyecto
4. Pega la key en la barra superior de la app

La key se guarda en `localStorage` del navegador, nunca sale del dispositivo.

---

## 🔧 Uso

### 1️⃣ Subir nómina
- Drag & drop o click en "Subir" → selecciona foto o PDF
- La app detecta el formato automáticamente
- Gemini extrae los datos en 2-5 segundos

### 2️⃣ Verificar (crítico)
- **Revisa cada campo.** Los LLMs pueden confundir dígitos similares (6 vs 8, comas vs puntos)
- Click en cualquier valor para corregirlo inline
- Presta atención especial a: importes principales, % IRPF, bases de cotización

### 3️⃣ Guardar
- Pulsa "Confirmar y Guardar"
- Si el mes ya existe, aparece un aviso para confirmar antes de sobreescribir
- Se descarga un backup JSON automáticamente

### 4️⃣ Ver informes
- **Panel:** vista general de nóminas cargadas
- **Anual:** tabla comparativa + detección de anomalías

---

## 📊 Datos extraídos

```
ADMINISTRATIVOS
├─ Empresa (nombre, CIF, CCC)
├─ Trabajador (nombre, NAF, DNI)
└─ Empleo (categoría, antigüedad, tipo de contrato)

PERÍODO
├─ Mes / Año
├─ Fechas de inicio y fin
└─ Días trabajados

DEVENGOS (Ganancias)
├─ Salario Base
├─ Plus productividad, festivos, ropa, etc.
├─ Incentivos
└─ Seguros

DEDUCCIONES
├─ IRPF (retención)
├─ Cotizaciones SS (contingencias, desempleo, formación)
└─ Otros descuentos

BASES Y TOTALES
├─ Bruto
├─ Deducciones
├─ Neto
└─ Bases de cotización
```

---

## 📍 Ámbito geográfico

⚠️ **Optimizada ÚNICAMENTE para nóminas españolas.**

- ✅ Compatible: cálculos españoles (IRPF, Seguridad Social, bases de cotización)
- ❌ No compatible: México, Colombia, Argentina, u otros países hispanohablantes

---

## 💾 Privacidad y datos

🔒 **100% privado**

- Todos los datos se almacenan **localmente en tu dispositivo** (localStorage)
- Única excepción: la foto o PDF se envía a Gemini para OCR (Google no guarda datos de API según su política)
- Puedes usar offline una vez cargadas las nóminas
- Exporta tus datos en cualquier momento en JSON

---

## 🛠️ Tecnología

- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **IA:** Google Gemini 2.5 (exclusivamente para OCR)
- **Dependencia:** JSZip 3.10 (vía CDN, solo para importar backups en ZIP)
- **Storage:** localStorage del navegador
- **PWA:** Progressive Web App instalable
- **Deploy:** GitHub Pages (HTTPS obligatorio para PWA)

**Arquitectura de archivo único:** toda la aplicación en `index.html` (~64 KB). Sin frameworks, sin build step.

---

## 🐛 Troubleshooting

**"limit: 0" o "quota exceeded"**
- El proyecto de Google Cloud vinculado a tu key tiene la capa gratuita bloqueada (típico en Europa)
- Solución: crea un proyecto **nuevo** en [Google Cloud Console](https://console.cloud.google.com), habilita "Generative Language API", genera una key nueva con ese proyecto desde [AI Studio](https://aistudio.google.com/apikey)

**"Unable to process input image" en todos los modelos**
- El archivo tiene extensión de imagen pero por dentro es un PDF — la app lo detectará correctamente desde v2.2
- O la imagen está corrupta: prueba con otra foto

**"El modelo X ya no está disponible para nuevos usuarios"**
- Gemini retira modelos periódicamente para cuentas nuevas
- La app usa la cadena `gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.5-pro`, todos activos en mayo 2025
- Si alguno falla, el error muestra cuál y por qué; actualiza el array `GEMINI_MODELS` en el código si es necesario

**La foto no se extrae bien**
- Foto bien enfocada, nómina ocupando mayoría de imagen
- Resolución mínima recomendada: 1024px
- Si el OCR falla sistemáticamente en un campo, edítalo manualmente en Fase 2

**No me sale el botón de instalar en móvil**
- Abre en Chrome (Android) o Safari (iOS)
- La URL debe ser HTTPS
- Espera a que la página cargue completamente

---

## 📋 Changelog

### v2.2 (Mayo 2025)
- **Detección de formato por magic bytes:** un PDF con extensión `.jpg` se detecta y procesa correctamente
- **Soporte PDF nativo:** enviado a Gemini como `application/pdf` sin conversión
- **Conversión universal de imágenes:** Canvas normaliza cualquier formato (AVIF, HEIC, WebP, BMP...) a JPEG antes de enviar
- **Redimensionado automático:** imágenes >2500px se reducen para no saturar la API
- **Fallback robusto de modelos:** cualquier error (no solo cuota) cae al siguiente modelo
- **Diagnóstico detallado:** el error final muestra qué pasó en cada modelo individualmente
- **Nuevos modelos:** cadena actualizada a `gemini-2.5-flash → gemini-2.5-flash-lite → gemini-2.5-pro` (eliminado `gemini-2.0-flash` y `gemini-1.5-flash`, retirados para cuentas nuevas)
- **Detección de duplicados:** modal de confirmación antes de sobreescribir un mes ya guardado
- **Importación de ZIP:** acepta el archivo comprimido directamente sin necesidad de descomprimirlo

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
- **Mantén Fase 5:** template plano sin LLM para generar el informe final

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

Desarrollado como herramienta forense para auditar nóminas españolas y detectar irregularidades. El código está intencionalmente simple (un solo archivo HTML) para que sea auditable línea por línea por quien quiera usarlo, adaptarlo o aprender del patrón.

**Úsalo para:**
✓ Verificar que tu empresa te paga correctamente  
✓ Detectar errores en cálculos de IRPF o cotizaciones  
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
