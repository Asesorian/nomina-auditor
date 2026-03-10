# ⚖️ Nómina Auditor Forense

**Extractor inteligente de nóminas con IA** | Audita, verifica y genera informes de nóminas españolas.

![Version](https://img.shields.io/badge/version-2.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Web%20%26%20Mobile-blueviolet)

---

## 🎯 ¿Qué es?

**Nómina Auditor Forense** es una aplicación web que te permite:

✅ **Extraer datos automáticamente** de fotos de nóminas usando IA (Gemini Flash)  
✅ **Verificar y corregir** los datos extraídos manualmente  
✅ **Calcular totales** (bruto, neto, IRPF, cotizaciones SS)  
✅ **Generar informes mensuales y anuales** con análisis forense  
✅ **Exportar datos** en JSON para auditoría legal  
✅ **Funciona offline** — tus datos nunca salen de tu dispositivo  
✅ **Instalar como app** en móvil (Android/iOS)

---

## 🚀 Características

### Fase 1: Extracción de Datos
- Sube una foto de tu nómina
- Gemini 2.5 Flash extrae automáticamente todos los datos
- Fallback automático a otros modelos si hay problemas de cuota

### Fase 2: Verificación y Corrección
- Edita inline cualquier valor que no sea correcto
- Valida campos administrativos (empresa, trabajador, fechas)
- Revisa devengos y deducciones línea por línea

### Fase 3: Informes Profesionales
- **Informe Mensual**: Resumen completo de la nómina
- **Informe Anual**: Tabla comparativa de todos los meses
- Detección automática de anomalías:
  - Variaciones en % IRPF
  - Cambios en Base de Cotización
  - Cambios de Categoría o Contrato

### Datos y Respaldo
- **Backup automático** descargable en Descargas
- **Exportación JSON** completa para auditoría
- **Importación** de backups anteriores
- Toda la información se guarda localmente en tu navegador

---

## 📱 Instalación en Móvil

### Android
1. Abre esta URL en **Chrome**: `https://tuusuario.github.io/nomina-auditor/`
2. Toca el menú (⋮) → **"Instalar app"**
3. Aparecerá en tu pantalla de inicio como app nativa

### iPhone (iOS)
1. Abre en **Safari**: `https://tuusuario.github.io/nomina-auditor/`
2. Toca el botón compartir → **"Agregar a Pantalla de Inicio"**
3. Nombrala y listo

---

## 🔧 Cómo Usar

### 1️⃣ Configurar API Key (Gratis)
- Ve a [Google AI Studio](https://aistudio.google.com/apikey)
- Obtén tu API Key gratuita
- Pégala en la barra superior de la app
- ✓ Si te falla con "limit: 0", crea un proyecto nuevo en [Google Cloud Console](https://console.cloud.google.com)

### 2️⃣ Subir Nómina
- Click en "Subir" o arrastra una foto de tu nómina
- La app extrae automáticamente los datos
- Espera 2-5 segundos (depende del modelo IA)

### 3️⃣ Verificar
- Haz clic en cualquier valor para corregirlo
- Revisa especialmente los importes y porcentajes
- Click en "Guardar" cuando esté todo correcto

### 4️⃣ Ver Informes
- **Panel**: Vista general de nóminas cargadas
- **Anual**: Tabla con todos los meses comparados
- **Copiar**: Descarga informes para tu abogado

---

## 📊 Datos Extraídos

La app captura automáticamente:

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

## 💾 Privacidad y Datos

🔒 **100% Privado**
- Todos los datos se almacenan **localmente en tu móvil/PC**
- No se envía información a servidores (excepto a Gemini para la extracción, que no guarda datos)
- Puedes usar offline una vez cargadas las nóminas
- Exporta tus datos en cualquier momento

---

## 🛠️ Tecnología

- **Frontend**: HTML5 + CSS3 + JavaScript vanilla (sin dependencias)
- **IA**: Google Gemini 2.5 Flash (OCR forense)
- **Storage**: localStorage del navegador
- **PWA**: Progressive Web App (funciona offline)
- **Responsive**: Optimizada para móvil y desktop

---

## 📄 Requisitos

- Navegador moderno con JavaScript habilitado
- Conexión a Internet (solo para extracción con IA)
- API Key gratuita de Google (Gemini)
- Fotos nítidas de tus nóminas (resolución mínima 1024px)

---

## 🐛 Troubleshooting

**"Error de cuota agotada"**
- Crea un proyecto NUEVO en [Google Cloud Console](https://console.cloud.google.com)
- Habilita "Generative Language API"
- Genera una API Key con ese proyecto

**"La foto no se extrae bien"**
- Asegúrate de que la foto está bien enfocada
- La nómina debe ocupar la mayoría de la imagen
- Prueba con otra foto más clara

**"No me sale el botón de instalar en móvil"**
- Abre en Chrome (no en Safari ni Firefox)
- La URL debe ser HTTPS (GitHub Pages lo es)
- Espera unos segundos a que cargue completamente

---

## 📋 Licencia

MIT License — Libre para usar, modificar y distribuir

---

## 👤 Autor

Desarrollado como herramienta forense para auditar nóminas españolas y detectar irregularidades.

**Úsalo para:**
✓ Verificar que tu empresa te paga correctamente  
✓ Detectar errores en cálculos de IRPF o cotizaciones  
✓ Generar informes para tu abogado  
✓ Auditar cambios en tus condiciones laborales  

---

## 🤝 Aportes

Si encuentras bugs o tienes mejoras, abre un issue o pull request.

---

**Made with ⚖️ for justice**
