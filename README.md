# ⚖️ Nómina Auditor Forense

**Extractor y auditor de nóminas españolas con arquitectura híbrida determinista + IA**

![Version](https://img.shields.io/badge/version-2.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-PWA-blueviolet)
![Architecture](https://img.shields.io/badge/architecture-deterministic%20first-c9a227)

---

## 🎯 ¿Qué es?

**Nómina Auditor Forense** es una aplicación web (PWA) que te permite auditar tus nóminas españolas con una arquitectura diseñada para **minimizar alucinaciones de IA en los cálculos críticos**.

✅ Extracción OCR automática de fotos de nóminas (Gemini 2.5 Flash)  
✅ Verificación humana campo por campo (validador determinista)  
✅ Cálculos totales 100% código determinista (nunca un LLM calcula cifras)  
✅ Detección de anomalías con reglas auditables (no con LLM "interpretando")  
✅ Informes mensuales y anuales en texto plano exportable  
✅ PWA instalable en móvil  
✅ 100% local: datos nunca salen de tu dispositivo (excepto la foto a Gemini para OCR)

---

## 🔬 Arquitectura: decisión determinista + IA acotada

Este repo aplica la filosofía **"código científico, IA divulgadora"** a un caso real:

> **El código hace el trabajo del científico: calcula con rigor, verifica con datos, aplica reglas auditables. El LLM hace el trabajo del divulgador: comunica en lenguaje accesible lo que el código ha determinado. Cada uno en lo que es genuinamente bueno.**

### Pipeline técnico real

```
┌─────────────────────────────────────────────────────────────┐
│ FASE 1 — Extracción OCR (Gemini 2.5 Flash)                  │
│ El LLM convierte foto → JSON estructurado                   │
│ Riesgo: puede alucinar cifras o confundir conceptos         │
│ Mitigación: SIEMPRE pasa por Fase 2 de verificación humana  │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2 — Verificación humana (validador determinista)       │
│ El usuario edita inline cualquier campo mal extraído        │
│ Hasta que confirma, no se calcula nada                      │
│ Este paso es el que impide que alucinaciones lleguen al     │
│ cálculo final                                               │
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

### Extracción inteligente
- Arrastra una foto de nómina o pégala
- Gemini 2.5 Flash extrae campos automáticamente en 2-5 segundos
- Fallback automático a otros modelos Gemini si hay problemas de cuota

### Verificación humana (crítica)
- Click en cualquier valor para editarlo inline
- Validación visual de datos administrativos (empresa, trabajador, fechas)
- Revisión línea por línea de devengos y deducciones
- **Esta fase es intencionalmente obligatoria**: hasta que no confirmas, no se calcula nada

### Informes auditables
- **Informe mensual:** resumen completo de nómina verificada
- **Informe anual:** tabla comparativa de todos los meses del año
- Detección automática de anomalías con umbrales transparentes:
  - Variaciones en % IRPF (listado mes a mes)
  - Cambios en Base de Cotización
  - Cambios de Categoría o tipo de Contrato

### Datos y respaldo
- Backup automático descargable en formato JSON
- Exportación JSON completa para auditoría legal
- Importación de backups anteriores
- Storage: localStorage del navegador (nunca servidor)

---

## 📱 Instalación

### Como PWA en móvil

**Android:**
1. Abre la URL de GitHub Pages en **Chrome**
2. Toca menú (⋮) → **"Instalar app"**
3. Aparece en pantalla de inicio como app nativa

**iPhone (iOS):**
1. Abre la URL en **Safari**
2. Toca compartir → **"Agregar a Pantalla de Inicio"**

### En desktop

Simplemente abre `index.html` en navegador moderno. Es un solo archivo autónomo.

---

## 🔧 Uso

### 1️⃣ Configurar API Key de Gemini (Gratis)
- Ve a [Google AI Studio](https://aistudio.google.com/apikey)
- Obtén tu API Key gratuita
- Pégala en la barra superior de la app
- Si falla con "limit: 0", crea un proyecto nuevo en [Google Cloud Console](https://console.cloud.google.com)

### 2️⃣ Subir nómina
- Drag & drop o click en "Subir" → selecciona foto
- Gemini extrae los datos en 2-5 segundos
- Aparece la Fase 2 con datos pre-rellenados

### 3️⃣ Verificar (crítico)
- **Revisa cada campo.** Los LLMs pueden confundir similares (6 vs 8, -vs comas)
- Click en cualquier valor para corregirlo inline
- Presta atención especial a: importes principales, % IRPF, bases de cotización
- Guarda cuando todo esté verificado

### 4️⃣ Ver informes
- **Panel:** vista general de nóminas cargadas
- **Anual:** tabla comparativa + detección de anomalías
- **Copiar informe:** descarga o copia al portapapeles para abogado

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
- ❌ No compatible: México, Colombia, Argentina, u otros países
- ❌ Los sistemas fiscales de otros países son diferentes y la app no los manejará correctamente

---

## 💾 Privacidad y datos

🔒 **100% privado**

- Todos los datos se almacenan **localmente en tu dispositivo** (localStorage)
- Única excepción: la foto se envía a Gemini para OCR (Google no guarda datos según su política de API)
- Puedes usar offline una vez cargadas las nóminas
- Exporta tus datos en cualquier momento en JSON

---

## 🛠️ Tecnología

- **Frontend:** HTML5 + CSS3 + JavaScript vanilla (cero dependencias)
- **IA:** Google Gemini 2.5 Flash (exclusivamente para OCR)
- **Storage:** localStorage del navegador
- **PWA:** Progressive Web App instalable
- **Deploy:** GitHub Pages (HTTPS obligatorio para PWA)

**Arquitectura de archivo único:** toda la aplicación en `index.html` (~58 KB). Sin frameworks, sin build step, sin dependencias externas que mantener.

---

## 🐛 Troubleshooting

**"Error de cuota agotada"**
- Crea un proyecto NUEVO en [Google Cloud Console](https://console.cloud.google.com)
- Habilita "Generative Language API"
- Genera una API Key con ese proyecto

**"La foto no se extrae bien"**
- Foto bien enfocada, nómina ocupando mayoría de imagen
- Resolución mínima recomendada: 1024px
- Si el OCR falla sistemáticamente en un campo, edítalo manualmente en Fase 2 — esa es la razón de que Fase 2 exista

**"No me sale el botón de instalar en móvil"**
- Abre en Chrome (Android) o Safari (iOS), no en otros navegadores
- URL debe ser HTTPS
- Espera unos segundos a que cargue completamente

---

## 🧩 Reutilización para otros casos de uso

Este repo se publicó con la intención de servir como **base arquitectónica** para construir otros SaaS en dominios regulados donde las alucinaciones de IA no son aceptables.

**Patrón replicable:**
- **Sustituye Fase 1:** en vez de OCR de nómina, OCR de oferta hipotecaria, contrato de alquiler, póliza de seguro
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
