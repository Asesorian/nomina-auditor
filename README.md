# ⚖️ Nómina Auditor Forense

**Extractor y auditor de nóminas españolas con arquitectura híbrida determinista + IA**

![Version](https://img.shields.io/badge/version-2.15.0-blue)
![License](https://img.shields.io/badge/license-PolyForm_Noncommercial_1.0.0-orange)
![Platform](https://img.shields.io/badge/platform-PWA-blueviolet)
![Offline](https://img.shields.io/badge/offline-ready-4ade80)
![Architecture](https://img.shields.io/badge/architecture-deterministic%20first-c9a227)

### 👉 [Abrir la app](https://asesorian.github.io/nomina-auditor/)

---

## 🎯 ¿Qué es?

**Nómina Auditor Forense** es una aplicación web (PWA) para guardar, revisar y auditar tus nóminas españolas. Haces una foto o subes el PDF, la IA lee los datos, **tú los revisas** y a partir de ahí todo lo calcula código determinista. La IA nunca decide una cifra.

✅ Haz la foto desde la propia app (o elige el PDF): la IA (Gemini) lee los datos y tú revisas cada uno antes de guardarlo  
✅ **Sube un año entero de una vez:** elige todas las nóminas, se leen solas y las revisas una a una  
✅ **Guarda el documento original** de cada nómina con nombre automático, solo en tu dispositivo, y cópialo a Drive o iCloud con un toque  
✅ Todos los cálculos y comprobaciones los hace código determinista: la IA nunca calcula cifras  
✅ **La app comprueba las cuentas** de cada nómina (sumas, líquido, IRPF y cotizaciones) y, si la lectura no cuadra, la repite y te marca qué revisar  
✅ **Mensual, paga extra y atrasos** guardados por separado: varias nóminas en el mismo mes sin pisarse  
✅ **% de retención de IRPF** siempre visible: leído, deducido de la propia nómina o calculado, y corregible a mano  
✅ Informe mensual e informe anual en texto listo para tu abogado, con avisos de cambios y de meses que faltan  
✅ Aviso antes de sobrescribir una nómina, con comparación de importes  
✅ **Backup completo** (ZIP con tus nóminas y sus datos) para restaurarlo todo en otro dispositivo, y **aviso** cuando tienes cambios sin copia  
✅ Instalable en el móvil, **funciona sin conexión** y se actualiza sola  
✅ Tus datos y documentos se quedan en tu dispositivo: ningún servidor guarda copia (solo la foto/PDF viaja a Gemini en el momento de leerla)

---

## 🆕 Novedades (v2.3 – v2.15.0)

| | Qué hace | Dónde |
|---|---|---|
| 🎯 **Bonus (v2.15.0)** | Un tipo de nómina nuevo, **Bonus** (objetivos, participación en beneficios…), aparte de la paga extra: no tapa una paga extra que falte. Si la app no sabe qué tipo es una nómina, **te lo pregunta** y lo **recuerda** para las siguientes de esa empresa con el mismo texto en el periodo. El mes sin leer sale en rojo | Revisión, *Ver*, Anual |
| 🧭 **Avisos más claros cuando no cuadra (v2.14.2)** | Si una suma no cuadra, la app da una **pista** de dónde mirar: la línea que vale justo la diferencia, o la que tiene el importe a 0 y esa cifra en otra columna. Primero sale la suma (la causa) y después lo demás. Los códigos de relleno («N/L», «-») ya no dan avisos falsos de «filas corridas» | Revisión, *Ver* |
| 📎 **Un solo botón para subir y nóminas de dos páginas (v2.14.1)** | **📎 Subir nómina (foto o PDF)**: en el móvil abre el menú del sistema (*Cámara*, o *Fotos y vídeos → Archivos* para un PDF). Si tus nóminas ocupan **dos páginas**, la app lo pregunta la primera vez que unes dos y, desde entonces, junta las páginas de dos en dos (una lectura por nómina; se cambia en *Datos*). Una línea con unidades y precio pero **sin importe** (una previsión de la empresa) sale en gris como *línea informativa* si las sumas cuadran sin ella. El código QR para pasar la clave al móvil está ahora en *Datos* (solo en el ordenador) | Subir · Bandeja · Datos |
| 📑 **Un PDF con varias nóminas (v2.14.0)** | Si te mandan **varios meses en un solo PDF** (habitual cuando lo envía una gestoría), súbelo tal cual: la app **lo separa sola**, una página por nómina, y cada una entra en la bandeja con su propio original. Si el PDF trae **los dos ejemplares** de cada nómina (trabajador y empresa), se queda con uno. Si una página no tiene líquido (una nómina de dos páginas), te ofrece **🔗 Unirla** con la de al lado | Subir · Bandeja |
| 📄 **PDF digital (v2.12.0)** | Si subes la nómina en el **PDF que genera el programa de nóminas** (no un escaneo), la app saca sus números del propio PDF, **sin IA**, y comprueba que **cada cifra que ha leído Gemini está en el documento**. Pilla una cifra mal leída aunque las sumas cuadren. No tienes que hacer nada: sale el sello «📄 PDF digital: N de N cifras comprobadas» | En la revisión y en *Ver* |
| 📖 **Glosario (v2.11.0)** | En cada nómina, **«¿Qué es cada concepto?»**: toca una línea (salario base, prorrata, contingencias comunes, MEI, desempleo, IRPF…) y te explica qué es. En las cotizaciones, además, el **tipo oficial de ese año** (del BOE) frente al % de tu nómina. Y una página con el glosario completo y la tabla de tipos por año. Sin IA: textos fijos, revisados con las fuentes oficiales | Ver · Panel |
| 🏛️ **¿Está completo el año? y Comparar con Hacienda (v2.10.0–v2.10.1)** | El Anual te dice si **falta alguna nómina** (también las del final del año y las pagas extra que tuviste el año anterior) y, en los años cerrados, te pregunta si cobraste algún bonus, atrasos o finiquito en una **nómina aparte**. Y si escribes las tres cifras de tus **datos fiscales** (o del certificado de retenciones de tu empresa), las compara con tus nóminas: si coinciden, si difieren en céntimos o, si Hacienda tiene más, **cómo sería la nómina que te falta** para buscarla en el banco. Sin IA y sin entrar en Hacienda: tú escribes las cifras y se guardan solo en tu dispositivo (y en el backup) | Anual |
| 📊 **Precios por concepto (v2.9.0–v2.9.1)** | La app compara el **precio por unidad** de cada concepto (salario base por día, plus por hora…) con el de tu nómina mensual anterior y te dice si **sube, baja o cambia mucho**, en qué mes y desde cuándo. Los conceptos sin precio (incentivos, comisiones…) muestran su importe mes a mes. Sin IA: lo calcula la app con tus nóminas guardadas | Anual y Ver |
| ≈ **Redondeos de la empresa (v2.8.13)** | Si el IRPF, una cotización o la base de cotización difieren de la cuenta (base × %) en **10 céntimos o menos** y las sumas de la nómina cuadran, la app lo muestra en gris como *redondeo de la empresa*, no como aviso: la cifra está bien leída y la diferencia es del cálculo de la empresa. Si alguna suma no cuadra, sigue siendo un aviso. Desde la v2.12.3 dice **hacia qué lado**: si te han descontado esos céntimos de más o de menos y, si hay varias deducciones con céntimos de diferencia, **cuánto suman en total** | Revisión, Ver nómina, bandeja y texto para el abogado |
| 🌐 **Glosario en tu idioma (v2.13.0)** | Las explicaciones del glosario, en **Español, Català o English**, sea cual sea el idioma de tu nómina. Los conceptos se ven tal como vienen en el papel; en inglés, cada término lleva su nombre en español. Se elige en la propia tarjeta y se recuerda. Es el primer paso para tener toda la app en varios idiomas | Ver · Glosario |
| 📤 **Backup en iCloud o Drive desde el iPhone (v2.12.5)** | En iPhone y iPad, **🗂️ Guardar backup completo…** abre el menú de compartir: eliges *Guardar en Archivos* → **iCloud Drive**, o la app de **Drive**. Si el menú no se abre o lo cierras, el backup queda preparado con un botón **Guardar en…** y otro para descargarlo | Panel · Datos |
| 🗂️ **Guardar el backup en Drive (v2.8.10)** | En Chrome (Android y ordenador), **🗂️ Guardar backup completo…** abre el «Guardar como» del móvil o del ordenador: eliges Drive (o una carpeta) y la app comprueba que el archivo ha quedado entero. Drive lo sube después: la app te dice cuánto debe pesar para que lo compruebes en Drive (v2.8.11). Sin iniciar sesión en Google ni dar permisos a la app. En iPhone y en otros navegadores se descarga, como antes, y el aviso explica cómo llevarlo a Drive desde Descargas | Panel · Datos |
| 💳 **Saldo de Gemini agotado (v2.8.9)** | Google cobra ahora Gemini por **prepago**: compras crédito y cada lectura lo va gastando. Si se acaba, la app lo dice tal cual («Se ha acabado el saldo de Gemini de esta clave») y explica qué hacer, en vez de un error genérico. En la bandeja, la lectura se para sin marcar nada como error y sigue con *Reanudar* cuando hay saldo | Subir · Bandeja |
| ⇄ **Línea en el lado equivocado (v2.8.8)** | A veces Gemini pone una línea de deducciones en los devengos (o al revés), y además igual en las dos lecturas. Si a un lado le sobra justo lo que le falta al otro, la app te dice qué línea pasar para que cuadren las dos sumas, con un botón **⇄ Pasar a deducciones**. Es una sugerencia: mira el papel antes. Y debajo de cada tabla, **⇄ Pasar una línea…** para hacerlo a mano. Además, una cifra que ya has corregido o mirado deja de marcarse con **≠**, y la lista de diferencias avisa de que la otra lectura **cuadraba peor**: úsala solo si lo confirma el papel | Subir · Bandeja |
| ≠ **Las dos lecturas no coinciden (v2.8.7)** | Si Gemini ha leído la nómina dos veces, la app marca con **≠** las cifras en las que las dos lecturas no dicen lo mismo y enseña las dos (*ahora 58,40 € · la segunda lectura: 58,46 €*). Miras el papel y, si la buena es la otra, la usas con un toque; si a la lectura que ves le falta una línea que la otra sí tiene, la añades con otro. La app no elige por ti. Y el aviso de *unidades × precio* muestra el precio con todos sus decimales (7,125, no 7,13) | Subir · Bandeja |
| 🧮 **Totales mal leídos (v2.8.6)** | Si una suma no cuadra, la ventana al guardar pide comparar también el **total bruto**, el **total a deducir** y el **líquido** con el papel: a veces Gemini lee bien todas las líneas y mal un total. Antes solo hablaba de líneas y empujaba a guardar la nómina «con aviso» como si el error fuera de la empresa | Subir · Bandeja |
| 🔎 **Lecturas «cuadradas» a la fuerza (v2.8.5)** | Gemini ya no intenta que las sumas cuadren: copia lo que pone el papel, y es la app la que comprueba. Si un importe no coincide con *unidades × precio*, es un **error** (antes, un aviso): así se detecta una lectura que cambió un importe junto con el bruto y el neto para que todo sumara. Si el resultado es el importe de otra línea, se queda en aviso de *precios corridos de fila* | Subir · Bandeja |
| ⚖️ **Cuando las cuentas no cuadran (v2.8.4)** | Al guardar, una ventana con dos botones claros: **✏ Volver a corregir** (te lleva a la línea en rojo) o **⚠ Guardar con aviso**. Si has comprobado que coincide con el papel, el descuadre es de la propia nómina: se guarda marcada con ⚠. Y los precios con tres decimales (7,125 €/día) ya no salen como miles | Subir · Bandeja |
| 🏷️ **Atrasos y pagas extra mejor detectados (v2.8.2)** | La app mira también el **campo PERIODO** de la cabecera («ATRASOS», «PAGA EXTRA…»), los **días del periodo** (una mensual no pasa de 31) y el **nombre del archivo** («…Junio Atrasos.pdf»). En la bandeja, dos mensuales del mismo mes con importes distintos ya no salen como *Repetida* sino como **Revisa el tipo** | Subir · Bandeja |
| 🔑 **Barra de la clave más limpia (v2.8.1)** | Con la clave puesta, la barra se queda en una línea (*🔑 Gemini API Key ✓ Configurada · Cambiar*); sin clave, o si falla, se despliega sola. En el móvil, la etiqueta va encima de la casilla y ya no se sale de la pantalla | Barra superior |
| 📥 **Varias nóminas a la vez (v2.8)** | Elige todas las de un año (fotos o PDF): van a una **bandeja**, Gemini las lee de dos en dos y tú las **revisas y confirmas una a una**, ordenadas por fecha, con *‹ ›* para moverte y la barra fija **✓ Confirmar y siguiente**. Puedes empezar a revisar en cuanto está la primera. La bandeja sigue ahí aunque cierres la app, avisa de las repetidas y, si se corta internet o la clave llega a su límite, se para sin perder nada y sigue con *Reanudar* | [Ver sección](#-varias-nóminas-a-la-vez-la-bandeja) |
| 📱 **Revisión cómoda en el móvil (v2.7.5)** | En pantallas estrechas cada línea de la nómina ocupa dos filas: código, concepto e **importe siempre a la vista** (con sus marcas rojas), y debajo unidades y precio. Ya no hay que desplazar las tablas a los lados | Subir · Corregir datos |
| 💾 **Aviso de copia pendiente (v2.7.4)** | Cuando cambias algo y no tienes copia, el Panel te avisa con un botón para descargar el backup completo. El backup automático (un archivo en Descargas cada vez que guardabas) pasa a venir **desactivado** | Panel · Datos |
| 🗂️ **Backup completo más claro (v2.7.3)** | Dentro del ZIP, tus nóminas van en la carpeta `nominas/` y los datos en `datos-app.json` | Datos |
| 🧮 **La app comprueba las cuentas (v2.7.2)** | Cada nómina se comprueba sola: devengos = bruto, deducciones = total a deducir, bruto − deducciones = líquido, IRPF y cotizaciones = base × %. Si la lectura de Gemini no cuadra, **la vuelve a leer** diciéndole qué falla y se queda con la que cuadra; si sigue sin cuadrar, marca en rojo los valores sospechosos. Las que no cuadran salen con ⚠ en el Panel y el Informe anual | [Ver sección](#-comprobación-de-las-cuentas) |
| ✏ **Corregir una nómina guardada (v2.7.2)** | *Ver → ✏ Corregir datos* abre la misma revisión que al subirla. Y *🔁 Releer con Gemini* vuelve a leer el documento que ya tienes guardado, sin subirlo otra vez | Panel → Ver |
| 🔢 **S.S. bien sumada y cifras con punto de miles (v2.7.2)** | La Seguridad Social suma todas las cotizaciones aunque vengan abreviadas (`CONT.COMU`, `MEI`…). Las cifras salen como `2.100,10` y puedes escribirlas así al corregir | Panel · Anual · Ver |
| 🔒 **Más segura (v2.7.1)** | Si te pasan la app con un enlace, puedes pegar el enlace entero en la casilla de la clave (útil en iPhone). Si un enlace trae una clave distinta de la tuya, la app pregunta antes de cambiarla. Los backups se comprueban antes de importarlos y *Datos* avisa si hay documentos sin nómina ocupando espacio | Barra de la clave · Datos |
| 📎 **Documento original de cada nómina** | Haz la foto desde la app y queda guardada junto a la nómina, con nombre automático (`2026-07 Julio - Paga extra.pdf`). Desde *Ver* la abres, la copias a Drive/iCloud o la descargas. A las nóminas antiguas puedes adjuntarles el original sin volver a procesarlas | [Ver sección](#-documentos-originales) |
| 📄 **Visor de PDF propio** | Los PDF se ven dentro de la app, aunque el móvil no tenga lector de PDF, y también sin conexión. Si el PDF tiene contraseña, la pide | *Ver → 👁 Ver* |
| 🗂️ **Backup completo** | Un ZIP con tus datos y todos los originales ordenados por año, que se restaura en otro dispositivo | Datos |
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
- **Si alguien te ha pasado la app**, te dará la clave o un enlace que la lleva: ábrelo, o pega el enlace entero en la casilla de la clave
- **Si quieres usar la tuya:** ver [API key de Gemini](#-api-key-de-gemini-gratis-o-de-pago). Hay capa gratuita y, con la facturación activada, cuesta alrededor de 1 céntimo por nómina
- Para pasarla al móvil sin teclear, en el ordenador: **Datos → 📱 Mostrar el código QR**
- Una vez puesta, la barra se pliega en una línea con **✓ Configurada**. Para verla o cambiarla, toca **Cambiar**

### 2️⃣ Sube la nómina
- Pestaña **Subir** → **📎 Subir nómina (foto o PDF)**. En el móvil se abre un menú: *Cámara* para hacer la foto, o *Fotos y vídeos → Archivos* para elegir un PDF. En el ordenador también puedes arrastrarla
- ¿Tienes varias (por ejemplo, un año entero)? Elígelas todas de golpe: van a la [bandeja](#-varias-nóminas-a-la-vez-la-bandeja)
- Pulsa **Procesar con Gemini IA**. En unos segundos verás los datos extraídos
- Necesita conexión a internet (la lectura la hace Gemini)
- Consejo: el PDF que te da la empresa, o la nómina escaneada con el móvil, se leen mejor que una foto ([cómo](#-problemas-frecuentes))

### 3️⃣ Revisa los datos (fase 1, obligatoria)
- Arriba aparece el **Tipo de nómina**: 📄 *Mensual*, 💰 *Paga extra* o 📎 *Atrasos*, con el motivo por el que se ha detectado. Si no es correcto, tócalo para cambiarlo
- Arriba del todo, **Comprobación de las cuentas**: ✓ en verde si todo cuadra; si no, la lista de lo que falla y los valores sospechosos marcados en rojo (o en ámbar si solo conviene mirarlos). Ver [Comprobación de las cuentas](#-comprobación-de-las-cuentas)
- **👁 Ver documento** abre la foto o el PDF para compararlo mientras revisas. **🔁 Releer con Gemini** lo vuelve a leer indicando qué no cuadra
- Toca cualquier valor subrayado para corregirlo. Los números se pueden escribir como en el papel: `2.100,10`, `2100,10` o `20,42`
- Si a la lectura le falta una fila o le sobra una, usa **＋ Añadir línea** o **－ Quitar una línea…** debajo de cada tabla
- Revisa sobre todo importes, % IRPF y bases de cotización. Si el % de IRPF no venía en las bases, la app lo rellena y te avisa en naranja para que lo compruebes con el papel

### 4️⃣ Guarda
- Deja marcada la casilla **📎 Guardar también el documento original** (viene marcada) si quieres conservar la foto o el PDF junto a la nómina
- Pulsa **✓ Confirmar y Guardar**
- Si las cuentas no cuadran, la app te lo dice y te pregunta si la guardas igualmente. Si aceptas, queda marcada con ⚠ hasta que la corrijas
- Si ya tienes una nómina en ese mismo sitio (mismo mes y tipo), aparece un aviso con los importes de las dos y estas opciones:

| Opción | Qué hace |
|---|---|
| 💰 Es una paga extra → guardarla aparte | La guarda como paga extra de ese mes. **No borra nada** |
| 📎 Son atrasos → guardarlos aparte | La guarda como atrasos de ese mes. **No borra nada** |
| ➕ Es otra paga extra distinta | Si ya había una extra ese mes, guarda una segunda |
| ♻ Sustituir la guardada | Reemplaza la anterior (se pierde) |
| Cancelar | No guarda nada. Si los importes coinciden, la app te avisa de que probablemente ya la tenías |

- Si has activado el backup automático (viene desactivado), se descarga una copia de los datos. Si no, el Panel te avisará de que tienes cambios sin copia

### 5️⃣ Consulta
- **Panel:** totales del año (bruto, neto, IRPF, Seguridad Social) y lista de nóminas. Bajo el mes aparece en negrita **Paga extra** o **Atrasos** (y **Paga extra 2** si hay otra el mismo mes). El 📎 indica que tiene guardado el documento original y el ⚠ que sus cuentas no cuadran (encima de la lista se dice cuáles)
- **Ver** (en cada nómina): informe completo, listo para copiar y enviar a tu abogado. En las mensuales, **Precios por unidad** dice si algún precio ha cambiado respecto a tus nóminas anteriores
- **Anual:** tabla de todo el año, totales, **precios por concepto** y observaciones automáticas

### 6️⃣ Corrige algo ya guardado (desde Ver)
- **✏ Corregir datos:** abre la revisión con los datos guardados. Cambia lo que haga falta y pulsa **✓ Guardar cambios** (se guarda en su sitio, con su documento original). **Cancelar** o salir de la pantalla no cambia nada
- **🔁 Releer con Gemini** (si las cuentas no cuadran y tienes el original guardado): vuelve a leer ese documento sin subirlo otra vez (~1 céntimo) y te deja la nueva lectura en la revisión para que la confirmes
- **Tipo de nómina:** cambia entre Mensual, Paga extra y Atrasos sin volver a procesarla
- **% Retención IRPF → ✏ Corregir %:** escribe el porcentaje correcto. Si lo dejas vacío, la app lo vuelve a calcular sola
- **📎 Documento original:** verlo, guardarlo en Drive/iCloud, descargarlo, cambiarlo o quitarlo. Si la nómina no lo tiene, **📎 Adjuntar original** (no la vuelve a procesar ni gasta lecturas)
- Para eliminar una nómina: botón 🗑 en el Panel (borra también su documento original)

### 7️⃣ Haz copias de seguridad
- Cuando tengas cambios sin copia, el **Panel te avisa**. Pulsa **🗂️ Guardar backup completo…** y elige Drive (o una carpeta fuera del móvil). En iPhone y iPad, el mismo botón abre el menú de compartir: elige *Guardar en Archivos* → **iCloud Drive**, o **Drive** (v2.12.5). En algunos navegadores el botón dice **Descargar backup completo**: el ZIP va a Descargas y desde ahí lo llevas a Drive (el aviso te dice cómo). **Ahora no** oculta el aviso hasta el siguiente cambio
- También desde la pestaña **Datos**. Ver [Copias de seguridad y varios dispositivos](#-copias-de-seguridad-y-varios-dispositivos)

---

## 📥 Varias nóminas a la vez (la bandeja)

Para empezar con un año entero (o cuando tienes varias pendientes) no hace falta subirlas de una en una.

1. **Subir → 📎 Subir nómina (foto o PDF)** y selecciona todas (fotos o PDF; en el ordenador también puedes arrastrarlas). Van a la **bandeja** y se guardan en tu dispositivo. Un **PDF con varias nóminas** también vale: la app lo separa sola, una página por nómina (desde la v2.14.0).
2. La app te dice cuántas lecturas de Gemini hará (menos de 1 céntimo cada una con una clave de pago) y pulsas **▶ Leer las N**. Las lee de dos en dos, con las mismas comprobaciones que una sola: si una no cuadra, la vuelve a leer.
3. **Puedes empezar a revisar en cuanto está la primera.** Se revisan **ordenadas por fecha**, con la pantalla de revisión de siempre. Arriba, *‹ ›* para moverte y *← Volver a la bandeja*; abajo, una barra fija con **Descartar** y **✓ Confirmar y siguiente**.
4. Al terminar, la app te dice cuántas has guardado y te lleva al informe anual del año.

Cada nómina se confirma por separado: **no hay «aceptar todas»**. La revisión es lo que hace fiable la app, porque hay errores de lectura que las cuentas no detectan.

En la bandeja, cada nómina lleva una etiqueta:

| Etiqueta | Qué significa |
|---|---|
| ✅ **Cuadra** | Las cuentas cuadran. Revísala igualmente con el papel |
| **Con avisos** / **No cuadra** | Hay algo que mirar o algo mal leído: los valores sospechosos salen marcados en la revisión |
| **Repetida** | La misma nómina dos veces: mismo mes, mismo tipo y mismos importes (por ejemplo, el PDF y una foto). Confirma una y descarta la otra |
| **Revisa el tipo** | Dos nóminas «mensuales» del mismo mes con importes distintos: casi seguro una es de atrasos o una paga extra. Al abrirla, elige su tipo |
| **Ya guardada** / **Mes ocupado** | Ya tenías esa nómina (o otra en ese mes). Al confirmar, la app te pregunta qué hacer, como siempre |
| **Sin líquido** | Una página de un PDF separado que no tiene líquido a percibir: casi seguro es la primera de una nómina de dos páginas. Pulsa **🔗 Unir con la página…** y se leen juntas (una lectura más) |
| **Error** | Esa lectura ha fallado: *🔁 Reintentar*. Si era una página de un PDF separado, también puedes unirla con la de al lado |

**Un PDF con varias nóminas (v2.14.0).** Cada página se guarda como un PDF propio («nombre (pág. 2).pdf»), que será el original de su nómina, y se lee aparte: un PDF de 4 nóminas son 4 lecturas. Si trae los dos ejemplares de cada nómina, la app se queda con la primera página cuando las dos lecturas dan **exactamente** el mismo mes, tipo, bruto, deducciones y líquido; si no coinciden, se quedan las dos (salen como *Revisa el tipo*) para que elijas tú con el papel. Si no hay conexión y la app aún no tiene guardado el separador, el PDF se lee entero, como antes. **Nóminas de dos páginas (v2.14.1):** si en *Datos → Nóminas en PDF* eliges «dos páginas» (o dices que sí cuando la app lo pregunta al unir), el PDF se separa de dos en dos; si un par no es una nómina (trae dos distintas o no tiene líquido), se vuelve a separar solo.

**Si algo se interrumpe no se pierde nada:**
- **Sin conexión:** la lectura se para y sigue sola cuando vuelve internet.
- **La clave falla, llega a su límite de gasto o se le acaba el saldo:** se para y lo explica. Cuando lo arregles, pulsa *Reanudar*.
- **Cierras la app:** la bandeja y las correcciones que hayas hecho siguen ahí. Al volver no gasta lecturas por su cuenta: pulsa *Reanudar*.
- **Mientras lee,** el móvil no apaga la pantalla (en Android y en iPhone recientes).

El Panel te avisa si tienes nóminas en la bandeja, y el botón *Subir* muestra cuántas son. Hasta que no las confirmas no están guardadas: no salen en el Panel ni en los backups.

---

## 📎 Documentos originales

La foto o el PDF de cada nómina se guarda **junto a ella, en el propio dispositivo**. Ningún servidor guarda copia.

- **Desde que haces la foto:** al procesar una nómina, la app la guarda con ella (casilla *Guardar también el documento original*, marcada por defecto). Las fotos se guardan como JPEG optimizado (máx. 2500 px) y los PDF tal cual.
- **Nombre automático y ordenado:** `2026-07 Julio.jpg`, `2026-07 Julio - Paga extra.pdf`, `2026-12 Diciembre - Atrasos.pdf`. Si cambias el tipo de la nómina, el nombre se actualiza solo.
- **Desde Ver:**
  - 👁 **Ver** el original dentro de la app, fotos y PDF. Los PDF se muestran con el visor propio de la app, así que **no hace falta tener un lector de PDF en el móvil**. Si el PDF tiene contraseña (muchas empresas usan el DNI), la app la pide. Si algo fallara, ofrece abrirlo con el visor del móvil o descargarlo
  - 📤 **Guardar en…**: abre el menú de compartir del móvil para guardarlo en **Google Drive, iCloud**, enviarlo por correo o WhatsApp… (aparece en móviles que lo permiten)
  - ⬇ **Descargar**, 🔄 **Cambiar** o 🗑 **Quitar**
- **Nóminas que ya tenías:** *Ver → 📎 Adjuntar original*. Eliges la foto o el PDF (también desde Drive) y queda guardado **sin volver a procesarlo con la IA**.
- **Panel:** el 📎 junto al mes indica que el original está guardado, y abajo se avisa de cuántas nóminas no lo tienen.

**Dónde se guardan:** en el almacenamiento interno del navegador (IndexedDB) del dispositivo donde los guardaste. Si usas el móvil y el ordenador, cada uno tiene los suyos: para pasarlos de uno a otro usa el **backup completo**.

**Cuánto ocupan:** cada foto, entre 0,6 y 1,1 MB (de los 2–3 MB que saca la cámara, la app guarda un JPEG optimizado de 2500 px como máximo); cada PDF, entre 0,05 y 0,3 MB. Un año completo, con extras, son unos **10–17 MB**. Lo que más acaba ocupando son los **backups completos que se acumulan en Descargas**: cuando subas uno a Drive, borra del móvil los antiguos. Las fotos hechas con *📷 Hacer foto* normalmente no se guardan además en la galería.

> ⚠️ Si pierdes el móvil o borras los datos de navegación de la app, los originales que solo estaban ahí se pierden. Guarda una copia en Drive (*Guardar en…*) o descarga de vez en cuando el **backup completo**.

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

## 🧮 Comprobación de las cuentas

Gemini **solo lee** la nómina, y a veces se equivoca: se salta una fila, pone un importe en la fila de al lado o toma el precio por día como importe. Una nómina se puede comprobar con sus propias cifras, así que la app lo hace siempre, con código y sin IA:

| Comprobación | Si falla |
|---|---|
| Suma de devengos = total bruto | ✗ error |
| Suma de deducciones = total a deducir | ✗ error |
| Bruto − deducciones = líquido | ✗ error |
| IRPF = base IRPF × % | ⚠ aviso (≈ redondeo si son 10 céntimos o menos y las sumas cuadran) |
| Cada cotización = su base × su % (contingencias comunes y MEI sobre la base C.C.; formación y desempleo sobre la A.T.; horas extra sobre su importe) | ⚠ aviso (≈ redondeo si son 10 céntimos o menos y las sumas cuadran) |
| Unidades × precio = importe, en los devengos. Desde la v2.10.2, con el margen que dan los decimales impresos (con 30 días y un precio de 3 decimales, unos céntimos): una cifra del precio mal leída ya no pasa | ✗ error (⚠ aviso si el resultado es el importe de otra línea: precios corridos de fila) |
| Remuneración + prorrata = base C.C. (solo mensual) | ⚠ aviso (≈ redondeo si son 10 céntimos o menos y las sumas cuadran) |
| Cada código lleva el mismo concepto que en tus otras nóminas de esa empresa (si no, probablemente las filas están corridas) | ⚠ aviso |
| Si las dos sumas fallan y a un lado le sobra lo que le falta al otro, qué línea pasar de lado para que cuadren | ⚠ aviso con botón ⇄ (sugerencia) |
| El CIF o NIF de la empresa tiene un formato válido y su dígito o letra de control cuadra (v2.9.1) | ⚠ aviso (no es error: no marca ⚠ en el Panel) |
| Con un PDF digital, cada cifra leída (importes, totales, bases, unidades y precio) está en el texto del PDF (v2.12.0). Si falta un importe, un total o una base, se lee otra vez | ⚠ aviso (no marca ⚠ en el Panel) |
| Cada código va en el mismo lado (devengos o deducciones) que en tus otras nóminas de esa empresa (v2.10.2). Si dos líneas del mismo importe se leen cambiadas de lado, las sumas cuadran igual: esto es lo único que lo ve | ⚠ aviso (no marca ⚠ en el Panel) |

**Qué hace con eso:**
- **Al subir:** si la primera lectura tiene errores, la app la manda **una vez más** a Gemini diciéndole exactamente qué no cuadra, y se queda con la lectura que cuadre mejor. Solo pasa cuando hay errores, y cuesta lo mismo que una lectura (~1 céntimo)
- **En la revisión:** lista lo que falla y marca los valores sospechosos. **La app nunca cambia una cifra por su cuenta**: eliges tú entre releer o corregir a mano mirando el documento
- **Al guardar:** si hay errores, pregunta antes
- **Después:** las nóminas que no cuadran salen con ⚠ en el Panel y en el Informe anual (con un aviso de que sus totales pueden estar mal), y la copia para el abogado lo advierte arriba y lo detalla al final. Se arreglan con **Ver → ✏ Corregir datos** o **🔁 Releer con Gemini**

**Redondeos de la empresa (v2.8.13):** muchas empresas calculan el IRPF o las cotizaciones de forma que el resultado se queda a unos céntimos de base × %. Si la diferencia es de **10 céntimos o menos** y las tres sumas de la nómina cuadran, la cifra está bien leída: la app lo muestra en gris con **≈** («redondeo de la empresa») y no lo cuenta como aviso. Si alguna suma no cuadra, o falta un total para comprobarlo, sigue saliendo como ⚠ aviso, porque podría ser un error de lectura. Desde la v2.12.3 dice hacia qué lado va la diferencia («te han descontado 3 céntimos más de lo que sale de la cuenta», o «menos»; en la base C.C., «mayor» o «menor») y, si varias deducciones tienen céntimos de diferencia, el total: a menudo se compensan entre ellas. Solo lo documenta: con el % impreso redondeado, la app no puede saber cuál de las dos cifras es la exacta. Las cotizaciones van a la Seguridad Social y el IRPF a Hacienda, a tu nombre.

**PDF digital (v2.12.0):** el PDF que sale del programa de nóminas lleva el texto dentro. La app lo saca en tu dispositivo, sin IA, y busca en él cada cifra que ha leído Gemini. Así se ve una cifra mal leída o inventada **aunque las sumas cuadren**. Con un escaneo o una foto no hay texto (o el que hay es de un OCR, con sus propios errores) y no se comprueba nada, como antes. A Gemini se le sigue mandando el PDF entero: Google ya le pasa ese texto al modelo sin cobrarlo, y con el PDF ve en qué columna va cada cifra.

**Lo que no puede detectar:** un error de lectura que siga cuadrando (por ejemplo, dos conceptos con el nombre cambiado pero con sus importes bien). Con un PDF digital, tampoco una cifra que sí está en el documento pero en otra línea o en el otro lado. Por eso la revisión humana sigue siendo obligatoria.

---

## 📊 Precios por concepto

Casi todos los conceptos de una nómina son **unidades × precio**: 30 días × el salario base por día, 20 horas × el plus por hora… El importe cambia cada mes con los días o las horas, pero el **precio por unidad** solo cambia cuando cambia lo que te pagan (una subida del convenio, un cambio de categoría o de jornada… o un error). La app lo vigila sola, sin IA, con tus nóminas guardadas:

- **Anual → Precios por concepto:** el precio de cada concepto y sus cambios en el año: **▲** sube, **▼** baja (en ámbar) y **⚠ cambio grande** (más del 25 %: compruébalo con el papel; puede ser un error de lectura o un cambio de jornada o de contrato). Cada cambio dice en qué mes y desde qué nómina, y si entre medias te faltan nóminas por subir. Los cambios van también a las *Observaciones para Abogado* y al texto que se copia
- **Ver → Precios por unidad** (en cada nómina mensual): si algún precio ha cambiado respecto a tus nóminas anteriores. Si hay cambios, la copia para el abogado los incluye
- **Conceptos sin precio** (incentivos, comisiones, un seguro…): solo se ve su importe de cada mes, sin avisos, porque cambian por naturaleza

Cómo lo hace:
- Compara solo nóminas **mensuales** de la **misma empresa**: las pagas extra y los atrasos no cuentan (los atrasos llevan diferencias, no precios), ni las nóminas con ⚠ (sus cifras no son fiables hasta que las corrijas)
- Reconoce cada concepto por su **código**, aunque el nombre venga escrito de otra forma en cada nómina; si una nómina no tiene códigos, por el nombre
- Usa el precio de la nómina si **unidades × precio = importe**; si no cuadra (por ejemplo, con los precios corridos de fila) o no viene, lo calcula como **importe ÷ unidades** y lo marca con *. Ese precio calculado solo vale si **está impreso en algún sitio de esa nómina** (con las filas corridas, en otra línea); si no, ese mes el concepto queda sin precio (v2.9.1): con las filas corridas, las unidades también pueden ser de otra línea
- La **misma empresa** es la del mismo CIF **o el mismo CCC** (v2.9.1): una nómina con el CIF mal leído no se separa como si fuera de otra empresa, y el Anual te dice cuál es para que lo corrijas
- Cuenta como cambio una diferencia del **0,5 % o más**: los redondeos de la empresa no llegan
- **Solo informa:** no cambia ninguna nómina ni el ⚠ del Panel

Ejemplo (datos inventados): *«Salario base» (010): el precio por unidad sube un 3,00 % (de 40,00 € a 41,20 €) en Marzo 2026, respecto a Diciembre 2025. Entre medias faltan 2 nóminas mensuales.*

---

## 🏛️ ¿Está completo el año? y Comparar con Hacienda

**¿Está completo el año?** (Anual, v2.10.0). Un informe anual solo vale si están todas las nóminas. La tarjeta te avisa de:
- **Meses sin nómina mensual:** de enero a diciembre en los años cerrados; en el año en curso, hasta el mes anterior al de hoy (no te pide la que todavía no has cobrado). Si cambiaste de empresa, también los huecos de cada una dentro de su tramo
- **Pagas extra que faltan:** si el año anterior la misma empresa te pagó una extra (por ejemplo, la de diciembre) y este año no está, ni aparte ni como línea de la mensual (con un mes de margen). Si tus mensuales llevan la prorrata de pagas, no se espera ninguna aparte
- **Nóminas aparte:** en los años cerrados te pregunta si cobraste algún bonus, atrasos o finiquito en una nómina aparte (y te dice cuáles tienes ya). La app no puede saber que existe una nómina que nunca ha visto, y esas suelen ser las que no se guardan. Si comparas con Hacienda, la respuesta sale sola: si coincide, no falta ninguna; si Hacienda tiene más, parece que falta una

Son avisos: no ponen ⚠ en el Panel ni cambian ninguna nómina.

**Comparar con Hacienda** (Anual, v2.10.0). Tu empresa declara a Hacienda lo que te ha pagado. Para comprobar que coincide con tus nóminas:
1. Busca las cifras en la app o la web de la Agencia Tributaria → **Renta (año) → Datos fiscales → Rendimientos del trabajo** (salen en primavera del año siguiente), o en el **certificado de retenciones** que da la empresa (suele llegar en enero o febrero)
2. En el Anual, pulsa **🏛️ Comparar con Hacienda** y escribe, por pagador, el **íntegro** (retribuciones dinerarias), las **retenciones** y los **gastos deducibles** (Seguridad Social). Si Hacienda tiene un pagador que la app no tiene, añádelo con **+ Otro pagador**
3. La app compara con el bruto, el IRPF y la Seguridad Social de tus nóminas de ese año mientras escribes, y enseña la diferencia exacta:
   - ✓ **Coincide**, o ≈ **coincide salvo unos céntimos** (hasta 1 €: redondeos o un céntimo mal leído)
   - **Parece que falta una nómina** (Hacienda tiene más): te dibuja cómo sería (bruto, Seguridad Social, IRPF y líquido aproximados) para que la busques en el banco y se la pidas a la empresa
   - **Tus nóminas suman más:** las causas posibles (la nómina de diciembre cobrada en enero, atrasos de otro año, una cifra mal leída, una nómina repetida)
   - **Un pagador sin nóminas en la app:** ¿un trabajo que no has subido?

Las cifras se guardan en tu dispositivo y van en el backup. La app **no entra en Hacienda** (ni con Cl@ve ni con ningún servidor): solo compara lo que escribes. Es orientativo: documenta, no aconseja sobre tu declaración.

---

## 📴 Uso sin conexión y actualizaciones

**Activarlo:** abre la app una vez con conexión, ciérrala y vuelve a abrirla. En **Datos → Modo sin conexión** debe poner **Activo**.

**Sin conexión puedes:** ver el Panel, los informes y el Anual, ver (también los PDF) y adjuntar documentos originales, cambiar el tipo de una nómina, corregir el % IRPF y exportar backups. Aparece un aviso naranja de "Sin conexión".

**Sin conexión no puedes:** procesar una nómina nueva, porque la lectura la hace Gemini. La app te avisa; cuando vuelvas a tener conexión, pulsa otra vez *Procesar*.

**Actualizaciones:** cuando se publica una versión nueva, te llega sola la próxima vez que abras la app con conexión. No hay que reinstalar nada. **Las actualizaciones solo cambian el código de la app: tus nóminas y tu API key no se tocan.**

**Si ves una versión antigua:** **Datos → 🔄 Forzar actualización de la app**. Tampoco borra nóminas ni API key.

> En el ordenador, si abres `index.html` como archivo local, el modo sin conexión no aplica ni hace falta: el archivo ya está en tu disco. Para actualizarlo, descarga de nuevo `index.html` o haz `git pull` si clonaste el repo.

---

## 💾 Copias de seguridad y varios dispositivos

| Copia | Qué contiene | Para qué |
|---|---|---|
| **Backup automático** (`nominas-backup-FECHA.json`) | Solo los datos. **Viene desactivado** (desde la v2.7.4); si lo activas en *Datos*, se descarga cada vez que guardas o corriges una nómina | Para quien prefiera una copia ligera en cada cambio |
| **Exportar datos** (*Datos → Exportar datos*) | Lo mismo, cuando tú quieras | Pasar los datos a otro dispositivo |
| **Backup completo** (*Datos → Guardar backup completo…* o *Descargar backup completo*) | ZIP con la carpeta `nominas/AÑO/` (tus nóminas: las fotos y PDF originales) y `datos-app.json` (los datos leídos) | Guardarlo en Drive y **restaurarlo todo** (datos y documentos) en otro dispositivo |

- **Restaurar:** *Datos → Importar backup*. Acepta el `.json` o el `.zip` directamente, sin descomprimir. Con el backup completo se restauran también los documentos originales. Los backups completos de antes de la v2.7.3 (con `nominas.json` y la carpeta `documentos/`) se siguen importando igual.
- **Importar nunca borra un original que ya tengas en el dispositivo:** si el backup no trae el documento de una nómina, se conserva el que ya había.
- **Guardarlo en Drive** (v2.8.10):
  - **Chrome en Android o en el ordenador:** *Guardar backup completo…* abre el «Guardar como» del sistema. Elige **Drive** (o una carpeta) y pulsa *Guardar*. La app comprueba que el archivo tiene el tamaño correcto; si no, lo quita y lo descarga. Si cancelas, no se hace nada y el aviso sigue.
    - **Comprueba en Drive que el archivo pesa lo que dice la app** (por ejemplo, 12,5 MB). Drive lo sube en segundo plano y la subida puede fallar: en una prueba quedó en Drive con **0 bytes** mientras la app decía *guardado*. Si pesa 0 o Drive avisa de que no ha podido subirlo, vuelve a guardarlo (y borra el vacío). No hace falta iniciar sesión en Google en la app: el archivo lo guarda el propio móvil u ordenador.
  - **iPhone y iPad (v2.12.5):** se abre el menú de compartir: *Guardar en Archivos* → iCloud Drive, o la app de Drive.
  - **Otros navegadores:** se descarga en *Descargas*. Para llevarlo a Drive: app de archivos (*Archivos*, *Files* o *Mis archivos*) → *Descargas* → mantén pulsado el archivo → *Compartir* → *Drive*. En iPhone, si se ha descargado, también puedes *Mover* a iCloud Drive.

**Aviso de copia pendiente:** cada vez que cambias algo (guardar, corregir, adjuntar un original…), la app lo apunta. Si no has hecho un backup completo después, el **Panel te avisa** con un botón para hacerlo. Solo cuenta el backup completo: el de solo datos no lleva tus nóminas. En *Datos* ves la fecha del último backup completo.

**Móvil y ordenador no se sincronizan solos.** Cada dispositivo guarda sus propias nóminas y documentos. Para tener lo mismo en los dos: backup completo en uno e importarlo en el otro.

> ⚠️ **Al importar,** las nóminas del backup se añaden y, si ya tienes una en el mismo sitio (mismo mes y tipo), **se sustituye por la del backup**. Usa siempre el backup más reciente para no perder correcciones posteriores.

> ⚠️ **Si borras los datos de navegación** de la web de la app, se borran también tus nóminas y sus documentos. La app se recupera sola con conexión, pero las nóminas y los originales solo desde un backup. Haz el backup completo cuando el Panel te avise y guárdalo fuera del móvil (por ejemplo, en Drive).

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
3. Abre la app **desde el icono** y pega la clave en su casilla (o el enlace entero que te pasaron). En iPhone, la app instalada guarda sus datos aparte de Safari: la clave que abriste en Safari no le llega

Después, ábrela una segunda vez con conexión para dejar activo el [modo sin conexión](#-uso-sin-conexión-y-actualizaciones).

### En el ordenador

Abre [la app](https://asesorian.github.io/nomina-auditor/) en el navegador (se puede instalar igual que en el móvil) o descarga `index.html` y ábrelo directamente. Es un archivo autónomo, sin servidor ni instalación.

---

## 🔑 API key de Gemini: gratis o de pago

La app usa **tu propia** API key de Gemini (Google). No hay intermediarios: la key y la nómina van directamente de tu navegador a Google.

### Conseguir la key

1. Ve a [Google AI Studio](https://aistudio.google.com/apikey)
2. Crea una API Key. **Importante: selecciona un proyecto nuevo de Google Cloud**, no el proyecto por defecto (en cuentas europeas el proyecto por defecto suele tener `limit: 0` en la capa gratuita)
3. Si no tienes proyecto nuevo: crea uno en [Google Cloud Console](https://console.cloud.google.com) → habilita "Generative Language API" → genera la key con ese proyecto
4. Pega la key en la barra superior de la app → aparece `✓ Configurada` en verde

Las claves que da Google desde 2026 empiezan por `AQ.`; las de antes, por `AIza`. La app acepta las dos.

La key se guarda en el almacenamiento local del navegador. Solo se usa para llamar directamente a Gemini.

### ¿Gratis o de pago? Lo que cambia con tus nóminas

Una nómina lleva tu DNI, tu sueldo y los datos de tu empresa, así que importa qué hace Google con ella. Según los [términos de la API de Gemini](https://ai.google.dev/gemini-api/terms) (actualizados el 28-4-2026):

| | Capa gratuita | Con facturación activada |
|---|---|---|
| ¿Puede Google usar tus nóminas para mejorar sus productos? | Sí, y pueden leerlas revisores humanos. **Excepción:** en el Espacio Económico Europeo (España incluida), Suiza y Reino Unido se aplica el mismo trato que en la de pago | No. Solo las guarda un tiempo limitado para detectar abusos |
| Coste | 0 € | Alrededor de **0,3 céntimos por nómina** procesada (medido en octubre de 2026 con `gemini-3.5-flash-lite`; con `gemini-2.5-flash` era ≈ 0,9) |
| Límites de uso | Bajos y cambiantes; en algunas cuentas europeas, `limit: 0` | Holgados para uso personal |

**Qué elegir:**
- **Fuera del EEE, Suiza y Reino Unido:** activa la facturación para tus nóminas.
- **En España:** las dos tratan tus datos igual. La de pago evita los límites de la gratuita (incluido el `limit: 0`) por unos céntimos al año.
- En ambos casos, si activas la facturación, pon un **límite de gasto mensual** bajo (por ejemplo, 1 €): un año de nóminas, con algún reintento, se queda en unos 15–20 céntimos.
- **Prepago:** las cuentas nuevas de Google pagan Gemini **por adelantado** (a las que ya existían, Google les asigna un plan o les pide pasarse): compras crédito (el mínimo ronda los 5 €; AI Studio lo indica) y cada lectura lo va gastando. El crédito caduca a los 12 meses. Si se acaba, **se paran todas las claves de esa cuenta de facturación** hasta que añadas más (la app lo avisa: *Se ha acabado el saldo de Gemini*). La recarga automática es opcional. Si tienes varios proyectos en la misma cuenta, comparten ese crédito: el límite de gasto de cada uno sigue sirviendo para que uno no se lo gaste todo.

**Dónde se mira y se cambia** (en [AI Studio](https://aistudio.google.com)):
- *Claves de API*: junto a cada key aparece el nivel de su proyecto. Si pone algo como *Nivel 1 · Prepago* o *Nivel 1 · Pospago*, la facturación está activada.
- *Facturación*: el crédito que te queda (prepago) y dónde añadir más.
- *Gasto*: lo gastado en el mes y el límite de gasto mensual. Si se alcanza el límite, Gemini deja de leer nóminas (la app mostrará *Todos los modelos fallaron*) hasta que lo subas o empiece el mes siguiente.

### 📱 Pasar la key al móvil (sin teclear)

Teclear una API Key en el móvil es propenso a errores: el teclado autocorrige, cambia mayúsculas o sustituye letras parecidas (`l`, `I`, `1`).

1. En el **ordenador**, donde ya funciona, ve a **Datos** y pulsa **📱 Mostrar el código QR** (la tarjeta solo sale en el ordenador)
2. Aparece un **código QR**
3. En el **móvil**, abre la cámara y apunta al QR
4. La app se abre con la key ya guardada

> La key va dentro del enlace del QR, en la parte tras `#`, que el navegador **nunca envía a ningún servidor**. Al abrirse, la app la guarda y limpia la dirección. Trata el QR como una contraseña: no lo enseñes ni le hagas captura.

**El mismo enlace sirve para pasar la app a otra persona** (por ejemplo, por WhatsApp): al abrirlo, la app queda con esa clave. También se puede **pegar el enlace entero en la casilla** de la clave: la app se queda solo con la clave.

**Si ya tienes una clave y abres un enlace con otra**, la app te pregunta antes de cambiarla y te enseña el principio y el final de las dos. Acepta solo si el enlace viene de alguien de confianza: con esa clave, tus nóminas se leerían con la cuenta de Google de quien la creó.

**Botón 👁:** muestra u oculta la key para comprobar que está bien escrita.

---

## ❓ Problemas frecuentes

**Subí una paga extra y machacó la nómina mensual (versiones anteriores a 2.3)**
1. Panel → la nómina de ese mes → **Ver** → en *Tipo de nómina* toca **Paga extra**. Pasa a su propio sitio
2. Vuelve a subir la nómina mensual, o importa un backup anterior al error, que la recupera sin tocar la extra

**El Panel dice «Tienes cambios sin copia de seguridad»**
- Has guardado o cambiado algo desde tu último backup completo. Pulsa **🗂️ Guardar backup completo…** (o *Descargar*) y guarda el ZIP en Drive. El aviso desaparece
- Si ahora no puedes, **Ahora no** lo oculta hasta el próximo cambio

**Ya no se descarga un archivo cada vez que guardo una nómina**
- Desde la v2.7.4 el backup automático viene desactivado: llenaba Descargas de copias casi iguales con tus datos. En su lugar, el Panel te avisa cuando toca hacer el backup completo. Si lo prefieres como antes: *Datos → Backup automático*

**Una nómina sale con ⚠ o «Las cuentas no cuadran»**
- Gemini leyó mal alguna línea. Ábrela con **Ver**: verás qué falla
- **🔁 Releer con Gemini** la vuelve a leer con el documento guardado indicando el fallo. Si la nueva lectura cuadra, revísala y pulsa **✓ Guardar cambios**
- O **✏ Corregir datos** y corrige a mano los valores marcados en rojo, mirando el documento con **👁 Ver documento**

**Al actualizar a la v2.7.2 ha cambiado el total de S.S. obrero**
- Es lo correcto: hasta la v2.7.1 solo se sumaban las líneas que decían «contingencia», «formación» o «desempleo», y se quedaban fuera las abreviadas (`CONT.COMU`) y el MEI. Ahora entran todas las cotizaciones del trabajador

**El % de IRPF sale `N/L` o con `*`**
- `*`: no venía en las bases y se ha calculado. Compruébalo con el papel
- `N/L`: no se ha podido obtener. En ambos casos: **Ver → ✏ Corregir %**

**Tengo mis nóminas antiguas como fotos en Drive**
- Para cada nómina ya guardada: **Ver → 📎 Adjuntar original** y elige la foto en Drive. No se vuelve a procesar y queda con su nombre ordenado

**En el otro dispositivo no veo el documento original**
- Los originales se guardan en el dispositivo donde los guardaste. Haz el **backup completo** (*Datos*) en ese dispositivo e impórtalo en el otro

**Un PDF no se abre o pide contraseña**
- Si pide contraseña: es la que te dio la empresa (a menudo tu DNI). Si la cancelas, puedes abrirlo con el visor del móvil o descargarlo
- La primera vez que abres un PDF, la app descarga su visor (unos segundos, verás el aviso "Preparando el visor de PDF…"). Después funciona también sin conexión. Si la primera vez estás sin conexión, la app te lo indica y te deja abrirlo con el visor del móvil

**Al importar un backup dice "registros ignorados"**
- Esos registros no tienen la forma de una nómina guardada por la app (mes, año o identificador no válidos) y se descartan para no dañar tus datos. El resto se importa con normalidad
- Si eran nóminas tuyas, vuelve a procesarlas o revisa de dónde salió ese archivo

**En Datos aparecen "documentos sin nómina"**
- Son originales que no pertenecen a ninguna nómina (por ejemplo, de una importación que se cortó). Ocupan espacio: puedes borrarlos con el botón de al lado
- Si aparecen todos y **no ves ninguna nómina**, no borres nada: importa tu último backup y volverán a su sitio

**Veo una versión antigua de la app**
- Cierra y vuelve a abrir la app con conexión. Si sigue igual: **Datos → 🔄 Forzar actualización**

**No me deja procesar una nómina**
- Si aparece "Sin conexión": hace falta internet para que Gemini la lea

**"Se ha acabado el saldo de Gemini de esta clave (error 402)"**
- La cuenta de Google de esa clave es de prepago y no le queda crédito. Ningún modelo leerá hasta que se recargue: la app ya no lo intenta con los demás
- Si la clave es tuya: en [AI Studio](https://aistudio.google.com), en la facturación, añade crédito. Si te la dio otra persona, avísale
- Lo que tienes guardado en la app no se pierde; en la bandeja, pulsa *Reanudar* cuando haya saldo

**"Todos los modelos fallaron"**
- Debajo aparece el motivo de cada modelo. Los más habituales:
  - `API key not valid`: la key está mal copiada o se ha borrado. Vuelve a pegarla (o pásala con el QR)
  - `limit: 0` o `quota exceeded`: ver el punto siguiente
  - Has llegado al **límite de gasto** que pusiste: súbelo en AI Studio → *Gasto* o espera al mes siguiente
  - Un modelo "no disponible": Google lo ha retirado (ver más abajo)

**Un PDF que pide contraseña no se procesa**
- Gemini no puede leer un PDF que pide contraseña para abrirse: su contenido está cifrado
- Ábrelo con la contraseña en el móvil o el ordenador, haz una captura de cada página y procesa la captura
- Después, si quieres guardar el PDF como original en lugar de la captura: *Ver → 📎 Documento original → 🔄 Cambiar*. La app lo mostrará pidiéndote la contraseña

**En el ordenador veo nóminas distintas en la web y en el archivo local**
- La web publicada y el `index.html` abierto como archivo guardan los datos por separado: para el navegador son dos sitios distintos
- Usa siempre la misma o pasa los datos de una a otra con el **backup completo**

**"limit: 0" o "quota exceeded"**
- El proyecto de Google Cloud de tu key tiene la capa gratuita bloqueada (típico en Europa)
- Solución: crea un proyecto **nuevo** en [Google Cloud Console](https://console.cloud.google.com), habilita "Generative Language API" y genera una key nueva con ese proyecto desde [AI Studio](https://aistudio.google.com/apikey)

**"Unable to process input image" en todos los modelos**
- El archivo tiene extensión de imagen pero por dentro es un PDF: la app lo detecta correctamente desde v2.2
- O la imagen está corrupta: prueba con otra foto

**"El modelo X ya no está disponible"**
- Google retira modelos de Gemini cada cierto tiempo
- La app usa la cadena `gemini-3.5-flash-lite → gemini-2.5-flash → gemini-3.8-flash` (desde la v2.12.2, octubre de 2026). Google ya no da los modelos 2.5 a las claves nuevas, salvo (de momento) `gemini-2.5-flash`; si un modelo no está, la app lee con el siguiente sin que hagas nada
- Si alguno falla, el error muestra cuál y por qué. Se cambia en el array `GEMINI_MODELS` del código

**La foto no se extrae bien**
- Si la empresa te da la nómina en PDF, sube ese PDF
- Si solo la tienes en papel, mejor **escanearla** que fotografiarla: el escáner del móvil recorta la hoja, la endereza y mejora el contraste (Android: *Google Drive → + → Escanear*; iPhone: *Notas → Escanear documentos*). Puedes subir el PDF que crea
- Si es una foto: bien enfocada, de frente, sin sombras y con la nómina ocupando casi toda la imagen
- Si un campo falla siempre, corrígelo a mano en la verificación. La comprobación de las cuentas te dirá si queda algo mal

**No me sale el botón de instalar en el móvil**
- Usa Chrome (Android) o Safari (iOS) y espera a que la página cargue del todo

---

## ⚠️ Limitaciones conocidas

- **Procesar necesita internet** y una API key de Gemini. Sin conexión se puede consultar y corregir, pero no leer nóminas nuevas
- **La IA puede leer mal un dato:** la app comprueba las cuentas y avisa de casi todos los errores, pero no de los que siguen cuadrando. Por eso la verificación es obligatoria: revisa siempre importes, bases y % de IRPF antes de guardar
- **Solo nóminas españolas**
- **No hay sincronización** entre dispositivos, ni entre navegadores del mismo dispositivo: todo se pasa con el backup completo
- **Si se borran los datos del navegador**, se pierden las nóminas y los originales que no estén en un backup
- **PDF que piden contraseña:** se ven y se guardan como original, pero Gemini no puede leerlos ([qué hacer](#-problemas-frecuentes))
- **No es asesoramiento laboral ni fiscal:** los informes resumen lo que dicen tus nóminas para que lo revise un profesional

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
│ gemini-3.5-flash-lite → gemini-2.5-flash → gemini-3.8-flash │
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
│ FASE 1c — Comprobación de las cuentas (código, v2.7.2)      │
│ Sumas, líquido, IRPF y cotizaciones = base × %,             │
│ uds × precio, códigos frente a tus otras nóminas            │
│ Si no cuadra: 2ª lectura de Gemini diciéndole qué falla     │
│ y se queda con la que cuadra mejor (nunca toca cifras)      │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 2 — Verificación humana (obligatoria)                  │
│ El usuario corrige cualquier campo y confirma el tipo       │
│ Ve qué no cuadra y los valores sospechosos marcados         │
│ Si el sitio mes+tipo ya existe: aviso con comparación y     │
│ opción de guardar aparte en vez de sobrescribir             │
│ Hasta que confirma, no se guarda ni se calcula nada         │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│ FASE 3 — Cálculos (100% código determinista)                │
│ calcTotals() suma brutos, netos, IRPF, bases                │
│ findIRPFDeduction() / irpfRateOf() retención y su %         │
│ calcSSTotal() suma todas las cotizaciones del trabajador    │
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
│ Aviso si alguna nómina no cuadra                            │
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
└─ Tipo de nómina (mensual / paga extra / atrasos)

DEVENGOS (Ganancias)
├─ Salario Base
├─ Pluses, incentivos, seguros…
├─ Pagas extra y atrasos
└─ De cada línea: código, concepto, unidades, precio e importe

DEDUCCIONES
├─ IRPF (retención)
├─ Cotizaciones SS (contingencias comunes, MEI, formación, desempleo, horas extra…)
└─ Otros descuentos (conceptos en especie, embargos, anticipos…)

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
- Los **documentos originales** (fotos y PDF) también se guardan solo en tu dispositivo (IndexedDB). Ningún servidor guarda copia; solo salen de él si tú los compartes o descargas
- **Única excepción:** al procesar una nómina, la foto o PDF se envía a Google Gemini para leerla. Qué puede hacer Google con ella depende de si usas la capa gratuita o la de pago, y de dónde estés: ver [API key de Gemini](#-api-key-de-gemini-gratis-o-de-pago)
- El modo sin conexión guarda únicamente el **código** de la app, nunca tus datos
- Cada dispositivo guarda sus propios datos; no se sincronizan solos
- Exporta tus datos cuando quieras en JSON

> **Si publicas tu propia copia en GitHub Pages:** todas las webs que publiques bajo `tuusuario.github.io` comparten el mismo almacenamiento del navegador. No publiques ahí código de terceros sin revisarlo, porque podría leer las nóminas y la API key.

---

## 🛠️ Tecnología

- **Frontend:** HTML5 + CSS3 + JavaScript vanilla
- **IA:** Google Gemini 2.5 (exclusivamente para OCR)
- **Dependencias (vía CDN, todas verificadas con SRI):** JSZip 3.10 (backups completos en ZIP), QRCode.js 1.0 (pasar la key al móvil) y PDF.js 3.11.174 de Mozilla (visor de PDF: se carga solo al abrir un PDF, sin Worker y con `isEvalSupported: false`, que impide que un PDF manipulado ejecute código: CVE-2024-4367). Si el archivo de la CDN no coincide byte a byte con el esperado, el navegador no lo ejecuta
- **Almacenamiento:** localStorage del navegador (datos) e IndexedDB (documentos originales, que pueden ocupar varios MB)
- **PWA:** instalable, con service worker para uso sin conexión
- **Deploy:** GitHub Pages (HTTPS obligatorio para PWA y modo sin conexión)

**Archivos:**
- `index.html` (~170 KB): toda la aplicación. Sin frameworks, sin build step
- `sw.js` (~5 KB): modo sin conexión. Solo guarda el código de la app

**Cómo funciona el modo sin conexión (`sw.js`):**
- `index.html`: red primero, preguntando siempre al servidor si hay versión nueva (sin usar los 10 min de caché que permite GitHub Pages). Si no ha cambiado, el servidor responde "sin cambios" y apenas gasta datos. Sin red, o si tarda más de 4 s, la copia guardada
- Librerías y fuentes: copia guardada primero (sus URLs llevan versión fija). El visor de PDF se descarga en segundo plano si hay algún PDF guardado, para que funcione sin conexión
- Las llamadas a Gemini (POST) no se interceptan nunca
- Solo actúa en la web publicada (https). Abierta como archivo local (`file://`) no aplica
- Las cachés usan el prefijo `nomina-auditor-` para no tocar las de otras apps del mismo dominio

---

## 📋 Changelog

### v2.15.0 (Octubre 2026)
- **Tipo de nómina «Bonus»:** bonus, objetivos, incentivo anual o participación en beneficios, en el periodo o en los conceptos. No cuenta como paga extra (un bonus de noviembre ya no tapa que falte la extra de Navidad) ni como atrasos. «Paga de beneficios» sigue siendo paga extra: en muchos convenios es la tercera
- **Si no sabe qué tipo es, pregunta:** una nómina de más de 31 días sin ninguna palabra que diga qué es ya no se guarda como atrasos sin más: la tarjeta del tipo pide que elijas, y no se guarda hasta que lo haces
- **Y lo recuerda:** lo que eliges se aplica a las siguientes nóminas de la misma empresa con el mismo texto en el periodo (sin contar las cifras: «VARIABLE 2025» y «VARIABLE 2026» son lo mismo). Sale de tus nóminas guardadas: no hay nada más que configurar y va en el backup
- **Mes o año sin leer:** salen en rojo en la Zona 1, con un aviso que explica qué poner (en una nómina sin periodo, el mes de la fecha de pago)
- En la ventana de «ya tienes una nómina de ese mes», también «Es un bonus → guardarlo aparte»

### v2.14.2 (Octubre 2026)
- **Pista cuando una suma no cuadra:** si sobra dinero y una línea vale justo la diferencia, la app la nombra («Mira en el papel si se ha leído de más»). Si falta y una línea tiene el importe a 0 con esa cifra en otra columna (unidades, % o precio), dice que seguramente es su importe leído en la columna equivocada. Solo señala dónde mirar: no cambia ninguna cifra, y la pista no se le pasa a Gemini en la segunda lectura
- **Orden de los mensajes:** primero las sumas que no cuadran (la causa), después los errores y al final los avisos
- **Línea que puede ser informativa:** si una línea tiene unidades y precio pero no importe y las sumas aún no cuadran, el mensaje explica que, si en el papel no tiene importe, saldrá en gris en cuanto cuadren las sumas
- **Códigos de relleno:** «N/L», «N/A», «-»… (lo que pone Gemini cuando una línea no tiene código) ya no entran en la plantilla de códigos. Antes, si el IRPF venía sin código, todas las cotizaciones sin código salían como «filas corridas»

### v2.14.1 (Octubre 2026)
- **Un solo botón para subir:** «📎 Subir nómina (foto o PDF)» sustituye a «Hacer foto», «Elegir archivos» y «Elegir PDF». En Android los tres abrían el mismo menú; ahora la ayuda dice dónde está cada cosa (*Cámara*, o *Fotos y vídeos → Archivos* para un PDF). En la bandeja, «📎 Añadir nómina (foto o PDF)»
- **Nóminas de dos páginas:** la primera vez que unes dos páginas, la app pregunta si tus nóminas suelen ocupar dos. Si dices que sí, los PDF siguientes se separan de dos en dos: una lectura por nómina en vez de tres y sin pulsar «Unir». Se cambia en *Datos → Nóminas en PDF*. Si un par resulta ser dos nóminas distintas (o no tiene líquido), la app lo vuelve a separar sola, página a página, y lo dice
- **Líneas informativas:** una línea con unidades y precio pero sin importe (por ejemplo, una previsión de vacaciones que la empresa no paga ese mes) ya no sale como error si las sumas cuadran sin ella: sale en gris con ℹ. Si las sumas no cuadran, sigue siendo error
- **El QR de la clave, en Datos:** «📱 Enviar al móvil» sale de la barra de la clave y pasa a una tarjeta de *Datos*, con su explicación y solo en el ordenador (en el móvil no sirve)

### v2.14.0 (Octubre 2026)
- **Un PDF con varias nóminas se separa solo:** al subir un PDF de varias páginas, cada página entra en la bandeja como una nómina, con su propio original («nombre (pág. 2).pdf»). No hay que separarlo antes con otra app
- **Los dos ejemplares, en uno:** si el PDF trae la copia del trabajador y la de la empresa en páginas distintas, la app se queda con una cuando las dos lecturas coinciden en mes, tipo, bruto, deducciones y líquido. La bandeja dice cuántas copias ha quitado
- **Nóminas de dos páginas:** una página sin líquido sale como *Sin líquido* con el botón **🔗 Unir con la página…**: se juntan en un PDF y se leen juntas
- **En un PDF digital,** las cifras de cada nómina se comprueban con el texto de **su** página, no con el del documento entero
- Funciona sin conexión una vez que la app ha guardado el separador (pdf-lib, que se descarga con la actualización)

### v2.13.1 (Octubre 2026)
- **Pegar la clave sustituye la anterior:** al pegar el enlace o la clave en la casilla, lo que hubiera se borra. Antes se insertaba donde estaba el cursor y, como la casilla va en puntitos, la clave anterior podía quedarse delante sin que se viera (y Google respondía «API key not valid»). También se quitan los caracteres invisibles, los saltos de línea y el punto o las comillas que se cuelan al copiar de un mensaje
- **Intro guarda y lo dice:** al pulsar Intro se cierra el teclado y sale «✓ Clave guardada: AQ.Ab12…wxyz» (el principio y el final), para ver que es la nueva. Si lo pegado no parece una clave (dos claves juntas, un trozo del enlace…), avisa «⚠ Revisa la clave» y la barra se queda abierta
- **Un archivo con varias nóminas:** si un PDF trae varios meses, la app ya no da un error técnico: dice cuántas nóminas hay y cómo separarlas. Si son los dos ejemplares de la misma nómina (trabajador y empresa), lee una sin preguntar
- **Botón «📄 Elegir PDF»:** en Android, «Elegir archivos» abre el selector de fotos y el PDF hay que buscarlo; este botón abre directamente el explorador de archivos

### v2.13.0 (Octubre 2026)
- **Glosario en tu idioma:** español, català o English, elegido en la tarjeta «¿Qué es cada concepto?» o en la página del glosario, y recordado. La nómina puede estar en un idioma y las explicaciones en otro: los conceptos se muestran como vienen en el papel. El resto de la app sigue en español por ahora
- **Glosario, base del IRPF corregida:** decía que no incluye la prorrata de las pagas extra; si las cobras repartidas cada mes, sí pagan IRPF. Lo que no entra es la prorrata que solo se suma para cotizar, cuando las pagas se cobran aparte

### v2.12.5 (Octubre 2026)
- **Backup en iCloud o Drive desde el iPhone:** en iPhone y iPad, *Guardar backup completo…* abre el menú de compartir del sistema y desde ahí lo guardas en *Archivos* → iCloud Drive o en Drive. Antes solo se descargaba. Si el menú no llega a abrirse (con muchas nóminas, preparar el ZIP tarda) o lo cierras sin elegir, el backup queda preparado con su botón *Guardar en…* y otro para *Descargar*. En Android y en el ordenador no cambia nada

### v2.12.4 (Octubre 2026)
- **Nóminas en catalán:** la app reconoce los conceptos en catalán (cotització, formació, desocupació, contingències comunes, sou base, paga de Nadal, endarreriments…). Antes, en una nómina en catalán la formación y el desempleo no se sumaban a la Seguridad Social (el Anual, *Comparar con Hacienda* y el informe salían cortos) ni se comprobaban con base × %, y el glosario no explicaba esas líneas. Si ya tienes guardada alguna nómina en catalán, se corrige sola: no hay que volver a subirla

### v2.12.3 (Octubre 2026)
- **Redondeos con su lado:** el ≈ de un redondeo de la empresa ya dice si te han descontado esos céntimos **de más o de menos** (en la base C.C., si es mayor o menor que remuneración + prorrata). Y si varias deducciones tienen céntimos de diferencia, una línea más con **el total**, que muchas veces es cero porque se compensan. Sigue sin ser un aviso

### v2.12.2 (Octubre 2026)
- **Modelo principal nuevo: `gemini-3.5-flash-lite`.** Probado con 25 nóminas reales frente a `gemini-2.5-flash`: lee igual o mejor (98,9 % de cifras bien frente a 97,8 %; 22 de 24 cuadraban a la primera frente a 19), unas 5 veces más rápido (unos 3,5 s por nómina) y unas 3 veces más barato (≈ 0,3 céntimos por lectura). `gemini-2.5-flash` pasa a ser el recambio y `gemini-3.8-flash` sigue el último

### v2.12.1 (Octubre 2026)
- **Modelos de recambio para claves nuevas:** Google ya no da `gemini-2.5-flash-lite` ni `gemini-2.5-pro` a los usuarios nuevos (responden 404). Con una clave nueva, si `gemini-2.5-flash` fallaba un rato, no quedaba otro modelo. Ahora la cadena es `gemini-2.5-flash → gemini-3.5-flash-lite` (mismo precio) `→ gemini-3.8-flash` (más caro, el último). Con tu clave de siempre no cambia nada: sigue leyendo con `gemini-2.5-flash`

### v2.12.0 (Octubre 2026)
- **PDF digital:** con el PDF que genera el programa de nóminas (no un escaneo), la app saca los números del texto del PDF con el visor que ya tenía (sin IA) y comprueba que cada cifra leída por Gemini está en el documento. Las que no están salen marcadas con un aviso, y si es un importe, un total o una base, Gemini la lee otra vez. Sello en la revisión y en *Ver*. Se guarda solo la lista de números del PDF, para volver a comprobar al corregir a mano. Escaneos y fotos, como antes. Las nóminas ya guardadas no cambian

### v2.11.1 (Octubre 2026)
- **Nombre del backup con el día bueno:** el día salía en hora UTC y la hora en hora local, así que un backup hecho entre medianoche y la 1:00 (las 2:00 en verano) llevaba en el nombre la fecha del día anterior. Ahora los dos van en hora local. Los backups antiguos no cambian: solo su nombre podía estar un día atrás

### v2.11.0 (Octubre 2026)
- **Glosario:** en *Ver*, la tarjeta «¿Qué es cada concepto?» explica cada línea que reconoce (unos 30 conceptos habituales de devengos y deducciones). Los conceptos propios de la empresa salen aparte, sin inventar nada: su regla está en el convenio, el contrato o un acuerdo de empresa
- **Tipo oficial frente al de tu nómina:** en contingencias comunes, MEI, desempleo y formación profesional, el tipo a cargo del trabajador de ese año (2024–2026, comprobado en la orden de cotización del BOE) junto al % impreso. Solo informa: no es una comprobación de las cuentas y no pone ⚠
- **Página del glosario:** todos los conceptos, las bases y los totales, y la tabla de tipos por año con sus fuentes. Se abre desde el Panel y desde *Ver*

### v2.10.2 (Octubre 2026)
- **Unidades × precio, más fino:** el margen ya no es el 0,2 % del importe, sino lo que pueden mover los redondeos según los decimales impresos del precio y de las unidades. En una prueba real, una cifra del precio mal leída (más de un euro de diferencia en el importe) pasaba sin aviso y la subida del precio salía mal en el historial y en las observaciones. Ahora es un error en la revisión, y el historial de precios usa importe ÷ unidades (con *). Con las nóminas guardadas de la prueba, solo esa pasa a salir con ⚠
- **Un concepto en el lado contrario:** si un código va en deducciones y en tus otras nóminas de esa empresa va siempre en devengos (o al revés), la app avisa. Dos líneas del mismo importe cambiadas de lado no descuadran las sumas, así que antes no lo veía nada. Es un aviso: no pone ⚠ en el Panel. Las líneas a 0 € no cuentan

### v2.10.1 (Octubre 2026)
- **Comparar con Hacienda mientras escribes:** el resultado se actualiza al dejar de teclear, sin tener que salir de la casilla (antes, si te quedabas en la última, salía sin la Seguridad Social ni el líquido). Intro cierra la casilla
- **La pregunta de la nómina aparte:** si ya tienes nóminas aparte ese año, las nombra y pregunta si hubo alguna otra. Si comparas con Hacienda y coincide, la pregunta desaparece («no falta ninguna nómina aparte»); si Hacienda tiene más, la tarjeta del año completo avisa de que parece faltar una nómina. Las observaciones y el texto exportable se actualizan al momento

### v2.10.0 (Octubre 2026)
- **¿Está completo el año?** Tarjeta en el Anual (y en las observaciones y el texto exportable). Los años cerrados se miran de enero a diciembre y el año en curso hasta el mes anterior al de hoy: antes solo se miraba hasta el último mes con nómina, y con noviembre y diciembre sin subir decía «completas de enero a octubre». Con dos empresas, los huecos de cada una dentro de su tramo. Avisa de la **paga extra que falta** si el año anterior la misma empresa la pagó (un mes de margen; no si las mensuales llevan la prorrata como devengo). En los años cerrados, pregunta si hubo algún bonus, atrasos o finiquito en una nómina aparte. Son avisos: el Panel y las nóminas guardadas no cambian
- **Comparar con Hacienda:** en el Anual, escribe por pagador el íntegro, las retenciones y los gastos deducibles de tus datos fiscales o del certificado de retenciones de la empresa. La app los compara con el bruto, el IRPF y la Seguridad Social de tus nóminas, con la diferencia exacta: ✓ coincide, ≈ coincide salvo céntimos (hasta 1 €), o no coincide. Si Hacienda tiene más, dibuja **la nómina que parece faltar** (bruto, S.S., IRPF y líquido aproximados); si la app tiene más, da las causas posibles; y avisa de un pagador sin nóminas en la app. Las cifras se guardan en el dispositivo y van en el backup. Sin IA y sin entrar en Hacienda
- **Backup:** la versión que guarda dentro sale ahora del logo (en la v2.9.2 se quedó en 2.9.1)

### v2.9.2 (Octubre 2026)
- **Backup completo en Drive (Android):** Drive a veces se queda en «Subiendo…» y deja el archivo con 0 bytes, aunque la app lo haya escrito entero. El aviso de después de guardar lo explica: si pesa 0 o se queda en «Subiendo…», volver a guardarlo en Drive (aunque el primero siga subiendo), porque el segundo suele subir bien, y después borrar en Drive el que pesa 0. La app no puede saber si Drive ha terminado de subirlo

### v2.9.1 (Octubre 2026)
- **CIF mal leído:** la app comprueba el formato y el dígito o la letra de control del CIF o NIF de la empresa (también NIE y con prefijo ES). Si no es válido, *Ver* y la revisión lo avisan en su casilla, como aviso (no como error: el Panel no cambia). No se le dice a Gemini en la segunda lectura, para que no se invente uno que lo parezca
- **Precios por concepto, misma empresa:** dos nóminas con el mismo CCC son de la misma empresa aunque el CIF no coincida. Antes, una nómina con el CIF mal leído salía en el Anual como otra empresa, con sus precios aparte. Ahora cuenta con las demás y el Anual dice qué nómina tiene otro CIF (también en las observaciones)
- **Precios por concepto, filas corridas:** el precio calculado (importe ÷ unidades) solo vale si coincide con algún precio impreso en esa nómina. Con las filas corridas, un concepto sin unidades ni precio en el papel podía quedarse con los de otra línea, y la división daba un precio que no existía y un «cambio grande» falso. Ahora ese mes queda sin precio. Si la nómina no trae ningún precio leído, se calcula como antes

### v2.9.0 (Octubre 2026)
- **Precios por concepto:** la app compara el precio por unidad de cada devengo con el de la nómina mensual anterior de la misma empresa y avisa si sube, baja o cambia más del 25 % (desde el 0,5 %). Se ve en el Informe Anual (tarjeta *Precios por concepto*, observaciones y texto exportable) y en *Ver* de cada nómina mensual (y en la copia para el abogado si hay cambios). Reconoce cada concepto por su código aunque cambie el nombre, y por el nombre si a una nómina le faltan los códigos. Con precios corridos de fila o sin precio leído, calcula importe ÷ unidades. Fuera: pagas extra, atrasos, deducciones y nóminas con ⚠. Los conceptos sin precio muestran su importe de cada mes, sin avisos. Sin IA y sin cambiar ninguna nómina guardada

### v2.8.13 (Octubre 2026)
- **Redondeos de la empresa:** una diferencia de 10 céntimos o menos entre el IRPF o una cotización y su base × %, o entre remuneración + prorrata y la base C.C., sale en gris con **≈** como redondeo de la empresa, no como aviso. Solo cuando las tres sumas de la nómina se pueden comprobar y cuadran (así la cifra está bien leída); si alguna falla, sigue siendo un aviso. No cuenta para *Con avisos*, no marca celdas, no ofrece *Releer* ni se le dice a Gemini en la segunda lectura. El informe y el texto para el abogado lo siguen mostrando

### v2.8.12 (Octubre 2026)
- **Errores de Gemini clasificados por su código:** en la bandeja, la app decide si un fallo es de la clave (401 o 403), del límite de uso (429) o solo de esa nómina por el código que devuelve Google, no por los números que aparezcan en el texto del error. Antes, un fallo de lectura cuyo texto llevaba un «403» paraba la bandeja como si la clave estuviera mal, y un 401 o 403 de verdad sin las palabras de siempre no se reconocía como problema de la clave
- **Claves nuevas de Google:** el aviso de una clave con espacios o caracteres raros ya no dice que empieza por «AIza…» (las nuevas empiezan por `AQ.`). Probado que las claves nuevas, con sus puntos, se guardan enteras al pegarlas o al abrir el enlace

### v2.8.11 (Octubre 2026)
- **Guardar en Drive desde Android:** tras guardar, el aviso dice cuánto pesa el backup y pide comprobar en Drive que el archivo pesa eso. En una prueba real, el primer intento quedó en Drive con 0 bytes («no se puede subir») y la app dijo *guardado*: el móvil tenía el archivo entero y lo que falló fue la subida de Drive, que la app no puede ver. El segundo intento salió bien

### v2.8.10 (Octubre 2026)
- **Guardar el backup completo en Drive:** donde el navegador lo permite (Chrome en Android desde la versión 132 y en el ordenador), el botón pasa a ser **🗂️ Guardar backup completo…** y abre el «Guardar como» del sistema, donde se puede elegir Drive o una carpeta. Se abre al pulsar, antes de preparar el ZIP; si cancelas, no se hace nada ni cuenta como copia. Después de guardar, la app comprueba que el archivo tiene el tamaño correcto; si no, lo quita y lo descarga en su lugar. Sin iniciar sesión en Google ni servidor
- Donde no se puede elegir (iPhone, Firefox…), se descarga como antes y el aviso explica los pasos para llevarlo a Drive desde Descargas. Chrome no deja usar «Compartir» con un `.zip`, por eso no hay botón de compartir para el backup completo

### v2.8.9 (Octubre 2026)
- **Saldo de Gemini agotado:** desde que la API de Gemini es de prepago, Google responde con el error 402 cuando se acaba el crédito de la cuenta. La app lo reconoce: dice «Se ha acabado el saldo de Gemini de esta clave» y qué hacer (avisar a quien te dio la clave o añadir crédito), sin probar los otros dos modelos (comparten la cuenta y tampoco leerían). En la bandeja, la lectura se para (no marca las nóminas como error ni sigue gastando intentos) y sigue con *Reanudar*
- **Corregido:** en la bandeja, cualquier lectura en la que fallaban los tres modelos se tomaba por un error de la clave (el consejo del final del mensaje nombra «API key not valid»). Un límite de gasto salía como «Gemini no acepta la clave», y una nómina que Gemini no sabía leer paraba toda la bandeja en vez de marcarse como *Error*

### v2.8.8 (Octubre 2026)
- **Línea en el lado equivocado:** si las dos sumas fallan y a los devengos les sobra justo lo que les falta a las deducciones (o al revés), y en el lado que sobra hay una línea de ese importe, aviso «Si pasas … a deducciones, cuadran las dos sumas» con botón **⇄**. Con varias líneas posibles se desempata por el lado en que va ese código en tus otras nóminas, por el tipo de deducción y por los conceptos que empiezan por *Dcto*, *Dto* o *Descuento*; si sigue el empate, un botón por línea. Nunca sugiere pasar el IRPF o una cotización a devengos. No mueve nada sola, no cuenta para elegir lectura y no se le dice a Gemini
- **⇄ Pasar una línea…** debajo de cada tabla de la revisión (como *Quitar una línea…*): la pasa al otro lado con su código, concepto, unidades, precio e importe, en el orden de los códigos
- **≠ que desaparece:** una cifra que corriges o miras (aunque la dejes igual) deja de marcarse como distinta de la otra lectura; las marcas siguen a su línea al quitar, añadir o pasar líneas. Si cada lectura pone la misma línea en un lado, sale una sola diferencia con ⇄ (antes, «falta aquí» y «sobra allí»)
- La lista de diferencias avisa de que la otra lectura **cuadraba peor** (o no cuadraba mejor): usa sus cifras solo si lo confirma el papel. Con una nómina real, «Usar» sin mirar habría empeorado casi todas las cifras

### v2.8.7 (Octubre 2026)
- **Las dos lecturas no coinciden:** cuando Gemini lee la nómina dos veces (segunda lectura automática o *🔁 Releer con Gemini*), la app guarda también la otra lectura y marca con **≠** las cifras en las que no coinciden (importes, precios, totales y bases), con las dos cifras a la vista. Botones *Usar…* y *＋ Añadir esta línea* (cuando a la lectura que se ve le falta una línea que la otra tiene). La app no elige: decide la persona mirando el papel. Si la lectura que se ve ya cuadra, las diferencias quedan plegadas y sin botones
- **Corregido:** el aviso *unidades × precio* redondeaba el precio a dos decimales («30,00 × 7,13 = 213,75 €») y la cuenta parecía mal hecha. Ahora sale el precio entero (7,125)

### v2.8.6 (Octubre 2026)
- **Ventana «Las cuentas no cuadran»:** si falla una suma (devengos, deducciones o líquido), pide comparar también los **totales** con el papel y explica que la app no los recalcula. Con una nómina real, las líneas estaban bien y el bruto y el neto mal leídos, y la ventana solo hablaba de líneas
- Los avisos de las sumas dicen que el total también puede estar mal leído
- **Corregido:** si se cerraba la revisión con un campo abierto en edición, salía un error de JavaScript

### v2.8.5 (Octubre 2026)
- **Prompt:** se quita la instrucción de comprobar que las sumas cuadren antes de responder. Con una nómina real, Gemini cambió +3 € en un importe, el bruto y el neto, y todo cuadraba aunque el papel decía otra cosa. Ahora se le pide copiar cada cifra tal cual, aunque no cuadre
- **Unidades × precio ≠ importe** pasa a ser un **error** (cuenta para la segunda lectura y pide confirmación al guardar). Excepción: si el resultado es el importe de otra línea, es un aviso de *precios corridos de fila* y se marca el precio
- El precio sospechoso se marca en rojo o ámbar en la revisión

### v2.8.4 (Octubre 2026)
- **Corregido:** los precios con tres decimales que manda Gemini («7.125», «0.375») se tomaban como punto de miles (7.125 €) y salían avisos falsos de *unidades × precio*. Lo que manda Gemini usa siempre punto decimal; lo que escribes tú se sigue leyendo como en español. Las unidades con tres decimales se muestran con coma
- **Guardar con las cuentas sin cuadrar:** en vez del aviso del navegador («Aceptar» guardaba y, en la bandeja, pasaba a la siguiente), una ventana con **✏ Volver a corregir** y **⚠ Guardar con aviso (y seguir)**, que explica que, si todo coincide con el papel, el descuadre es de la propia nómina

### v2.8.3 (Octubre 2026)
- **Corregido:** al corregir un valor y tocar directamente *Confirmar* (con el campo aún abierto), el primer toque solo cerraba el campo y había que tocar otra vez. Ahora guarda al primer toque, con el valor corregido. La barra de botones ya no se redibuja al corregir

### v2.8.2 (Octubre 2026)
- **Tipo de nómina:** además de los conceptos, cuentan el texto del campo PERIODO (Gemini lo copia tal cual; si pone «ATRASOS» o «PAGA EXTRA», el código lo clasifica así), los días del periodo (más de 31 → no es mensual) y el nombre del archivo («Atrasos», «Paga extra», «Navidad»…). El motivo se ve en la revisión
- **Bandeja:** *Repetida* solo cuando coinciden también los importes; dos mensuales del mismo mes con importes distintos salen como *Revisa el tipo*, con un aviso en la revisión
- Al actualizar, las nóminas ya leídas de la bandeja se reclasifican con estas reglas (sin volver a leerlas), salvo las que hayas cambiado a mano

### v2.8.1 (Octubre 2026)
- **Barra de la clave:** con la clave puesta se pliega en una línea (*✓ Configurada · Cambiar*); se despliega sola si no hay clave o si Gemini no la acepta, y no se pliega mientras escribes. En pantallas estrechas la etiqueta va encima de la casilla
- **Corregido:** en el móvil, la casilla de la clave se salía por la derecha y la página se desplazaba a los lados (sobre todo con el texto del sistema grande)

### v2.8 (Octubre 2026) · Varias nóminas a la vez
- **Bandeja:** al elegir (o arrastrar) varias fotos o PDF se guardan en el dispositivo y, tras confirmar cuántas lecturas se harán, Gemini las lee **de dos en dos** con las mismas comprobaciones y la misma segunda lectura que una sola. Cada una se **revisa y confirma una a una** (no hay «aceptar todas»), ordenadas por fecha, con *‹ ›*, *← Volver a la bandeja* y una **barra fija** con *Descartar* y *✓ Confirmar y siguiente*
- Se puede **revisar mientras sigue leyendo**. Cada corrección se guarda en la bandeja al momento
- La bandeja **sobrevive a cerrar la app**; al volver no sigue gastando lecturas sola: pide *Reanudar*. El Panel avisa de las que quedan y el botón *Subir* lleva el número
- **Sin conexión, sin clave o con la clave en su límite:** la lectura se para, las nóminas vuelven a la cola y no se pierde nada. Sin conexión sigue sola al volver internet. Una lectura que falla se marca con *Error* y *🔁 Reintentar*
- **Repetidas:** el mismo archivo no entra dos veces; dos documentos del mismo mes se marcan *Repetida*, y si ya tenías esa nómina guardada, *Ya guardada* (al confirmarla, *Descartar esta — ya la tengo*)
- Mientras lee, el móvil **no apaga la pantalla** (donde el navegador lo permite) y la pestaña dice cómo va
- Al confirmar, el documento de la bandeja pasa a ser el original de la nómina (no se copia dos veces). Una sola nómina sigue el camino de siempre
- La barra con los botones de la revisión se queda fija abajo también al subir una sola o al corregir una guardada

### v2.7.5 (Octubre 2026)
- **Revisión en el móvil:** en pantallas estrechas las líneas de devengos y deducciones se muestran en dos filas, con el importe y sus marcas siempre a la vista; los datos administrativos y las bases tampoco se desplazan a los lados
- **Clave de Gemini en la cabecera** `x-goog-api-key` en vez de en la dirección (`?key=`): así no queda en historiales ni registros de direcciones. Si la clave pegada tiene espacios o caracteres raros, la app lo dice claramente

### v2.7.4 (Octubre 2026)
- **Aviso de copia pendiente:** cuando hay cambios sin backup completo, el Panel avisa con un botón para descargarlo (y *Ahora no* para ocultarlo hasta el próximo cambio). En *Datos*, fecha del último backup completo
- **El backup automático viene desactivado:** ya no se descarga un archivo de datos cada vez que guardas. Quien lo quiera, lo activa en *Datos*
- Restaurar un backup en un dispositivo vacío no genera aviso (lo que hay es justo lo del backup)

### v2.7.3 (Octubre 2026)
- **Backup completo más claro:** dentro del ZIP, la carpeta de las fotos y PDF se llama ahora **`nominas/`** (antes `documentos/`) y el archivo de datos **`datos-app.json`** (antes `nominas.json`, que se confundía con la carpeta). Los backups anteriores se siguen importando igual

### v2.7.2 (Octubre 2026) · Lecturas que no cuadran
- **Comprobación de las cuentas** de cada nómina (sumas, líquido, IRPF y cotizaciones = base × %, unidades × precio y códigos frente a tus otras nóminas), en la revisión, en *Ver*, en el Panel y en el Informe anual. [Detalles](#-comprobación-de-las-cuentas)
- **Segunda lectura automática** cuando la primera no cuadra, diciéndole a Gemini qué falla; la app se queda con la que cuadra mejor. Botón **🔁 Releer con Gemini** en la revisión y en *Ver* (con el documento guardado)
- **✏ Corregir datos** de una nómina ya guardada, con **👁 Ver documento** al lado. Se guarda en su sitio y conserva su original; si se cambia el mes o el tipo, solo pasa a un hueco libre
- **＋ Añadir línea / － Quitar una línea** en la revisión
- **Guardar una nómina que no cuadra** pide confirmación, y la copia para el abogado lo advierte
- **S.S. obrero:** suma todas las cotizaciones (antes se quedaban fuera `CONT.COMU` y el MEI, y el total salía muy por debajo)
- **IRPF:** la línea se encuentra aunque Gemini lea «I.R.P.P.» o «TRIBUTACIÓN…», o por la cuenta base × % si el texto es ilegible. Las retenciones judiciales y embargos no se confunden con el IRPF
- **Cifras con punto de miles** en toda la app (`2.100,10`). Al corregir, «2.100,10» se guarda como 2100,10 (antes se guardaba 2,1)
- **Instrucciones a Gemini:** el precio por unidad va aparte del importe, cada importe en su fila y respuesta siempre en JSON
- Nueva batería de pruebas `test_lecturas.py`

### v2.7.1 (Octubre 2026) · Seguridad
- **📋 Copiar para Abogado** ya funciona aunque algún dato lleve comillas (`TALLERES "EL SOL" SL`), y el texto de la nómina nunca puede ejecutarse como código al copiarlo
- La respuesta de Gemini se lee **solo como datos (JSON)**: si no lo es, se descarta y se prueba el modelo siguiente (antes, como último recurso, se ejecutaba)
- **Importar backups:** cada nómina se comprueba (identificador, mes, año y tipo) antes de entrar; lo que no encaja se ignora y se avisa de cuántos registros eran. Del ZIP solo se restauran los documentos de nóminas válidas, y su tipo se decide por el contenido. Los mensajes de error se muestran como texto
- Los datos que van en los botones (identificadores, años) se pasan siempre como texto, también los que ya estuvieran guardados
- **JSZip y QRCode.js con SRI**, como PDF.js. El modo sin conexión renueva su copia (`sw3`) para no reutilizar copias antiguas que ya no pasarían la comprobación
- **Documentos sin nómina:** *Datos* los muestra con su tamaño y deja borrarlos con confirmación. Nunca se borran solos
- **Casilla de la clave:** acepta el enlace entero (`…#apikey=…`), útil en iPhone. Si un enlace trae una clave distinta de la guardada, pregunta antes de cambiarla. Nuevo texto: *¿No tienes clave? Pídesela a quien te pasó la app, o créala tú (guía)*
- Nueva batería de pruebas `test_seguridad.py`

### Repositorio (11 de octubre de 2026)
- **Licencia:** de MIT a **PolyForm Noncommercial 1.0.0** para todo lo publicado a partir de esta fecha. Lo publicado hasta la v2.7 sigue con MIT ([detalles](#-licencia))

### v2.7 (Octubre 2026)
- **Visor de PDF dentro de la app** (PDF.js): ya no hace falta lector de PDF en el móvil; funciona sin conexión tras la primera vez (se precarga en segundo plano si hay PDFs guardados)
- Aviso visual mientras carga ("Preparando el visor de PDF…", "Mostrando página 1 de 2…"), resolución suficiente para ampliar con los dedos
- PDF con contraseña: la pide y avisa si es incorrecta
- Si algo falla (sin conexión la primera vez, PDF dañado, contraseña cancelada…), nunca te deja sin ver la nómina: abrir con el visor del móvil o descargar
- Seguridad: el visor se verifica con SRI (si el archivo de la CDN no coincide exactamente, no se ejecuta) y no evalúa código de los PDF

### v2.6 (Octubre 2026)
- **📷 Hacer foto** desde la app (abre la cámara) además de *Elegir archivo*
- **Documento original guardado con cada nómina**, solo en el dispositivo (IndexedDB), con nombre automático por mes y tipo
- Desde *Ver*: ver, **guardar en Drive/iCloud** (menú de compartir del móvil), descargar, cambiar o quitar el original; **adjuntar el original** a nóminas ya guardadas sin volver a procesarlas
- **Backup completo** en ZIP (datos + documentos por año) y restauración con documentos
- Importar un backup nunca borra un original que ya esté en el dispositivo; eliminar una nómina o sustituirla borra el original que sobra
- Indicador 📎 en el Panel y recuento de documentos en *Datos*
- Se pide al navegador almacenamiento persistente para que no borre los documentos si falta espacio

### v2.5 (Octubre 2026)
- **Modo sin conexión:** la app instalada se abre sin internet (consultar, corregir, reclasificar, exportar). Procesar una nómina nueva sigue necesitando conexión (Gemini)
- Con conexión descarga siempre la última versión publicada (red primero; copia guardada si no hay red o tarda más de 4 s)
- Aviso visible de "Sin conexión" y botón **Forzar actualización** en Datos (no borra nóminas ni API key)
- **API key por QR más privada:** viaja tras `#` en el enlace, que no se envía a ningún servidor (antes iba como `?apikey=` y llegaba a GitHub). Los QR antiguos siguen funcionando
- Las etiquetas de estado de la pantalla Datos vuelven a tener estilo
- **Corregido:** justo después de publicar una versión, el móvil podía seguir mostrando la anterior hasta 10 minutos (caché de GitHub Pages). Ahora la app pregunta siempre al servidor
- Bajo el mes aparece en negrita, con la misma letra que los datos, **Paga extra** o **Atrasos** (antes, etiqueta naranja con el nombre largo, p. ej. "Paga extra de verano"). Si hay dos extras el mismo mes, la segunda se ve como **Paga extra 2**

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

## 📄 Licencia

**[PolyForm Noncommercial 1.0.0](LICENSE)**, desde el 11 de octubre de 2026. En resumen (manda el texto de la licencia):

- ✅ **Uso no comercial, gratis:** llevar y auditar tus propias nóminas, estudiar el código, adaptarlo para ti o usarlo en entidades benéficas, educativas o públicas
- ❌ **Uso comercial, solo con permiso del autor:** venderla, ofrecerla como servicio de pago, integrarla en otro producto o usarla en una actividad profesional (gestoría, despacho, asesoría…) requiere una licencia comercial. Para pedirla, abre un *issue* en este repositorio
- Si compartes una copia, modificada o no, incluye la licencia (o su enlace) y la línea `Required Notice` del archivo [LICENSE](LICENSE)

> Las versiones publicadas hasta la **v2.7** (11-10-2026) se distribuyeron con licencia **MIT**, y quien las obtuvo puede seguir usándolas con esa licencia. Todo lo publicado después está bajo PolyForm Noncommercial.

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

Si encuentras errores o tienes ideas de mejora, abre un *issue*. Si quieres aportar código, coméntalo antes en un issue: para aceptarlo, el autor necesita poder distribuirlo tanto con esta licencia como con licencias comerciales.

---

## 🚀 Construido en comunidad SaaS Factory

Este proyecto nació en **SaaS Factory**, comunidad de makers y emprendedores españoles e hispanohablantes construyendo SaaS juntos.

La filosofía: **soluciones reales, prácticas y accesibles** para problemas del día a día. En este caso, ayudar a cualquier trabajador a auditar sus nóminas, detectar errores y proteger sus derechos laborales sin depender de gestorías caras ni de software cerrado.

**Únete a la comunidad:** [SaaS Factory](https://www.saasfactory.so/)

---

**Made with ⚖️ for honesty in numbers.**
