# 🗡️ Almacén de Dotes PF2e

> Visualizador y buscador de Dotes para **Pathfinder 2e** con soporte bilingüe (Español / Inglés), filtros avanzados y diccionario de rasgos interactivo.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/GuilleGearts/pf2e-feat-visualizer)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

---

## 📖 Descripción

**Almacén de Dotes PF2e** es una aplicación web estática que permite explorar y filtrar el catálogo completo de Dotes (Feats) del juego de rol **Pathfinder Segunda Edición**. Diseñada para jugadores y directores de juego que buscan consultar rápidamente las habilidades de sus personajes, la herramienta fue construida con tecnologías web simples y eficientes, sin necesidad de ningún backend.

Los datos son extraídos y procesados desde los archivos del sistema **Foundry VTT (pf2e)** mediante un conjunto de scripts Python, y la interfaz consume el JSON resultante directamente desde el navegador.

---

## ✨ Características

- 🔍 **Búsqueda en tiempo real** por nombre y descripción de la dote
- 🌍 **Soporte bilingüe** (Español / Inglés) con interfaz completamente localizada
- 🎨 **3 Temas visuales:** Clásico PF2e (Rojo pergamino), Modo Oscuro y Modo Claro
- 🏷️ **Filtro avanzado de Rasgos (Tri-State):**
  - ✅ Estado **Incluido** (AND): La dote debe tener el rasgo
  - ❌ Estado **Excluido**: Descarta dotes con el rasgo seleccionado
  - ⚪ Estado **Neutro**: Sin efecto
- 🔢 **Filtro de Nivel** con selección múltiple (1–20)
- 📂 **Filtro por Categoría** (General, Clase, Ancestría, etc.)
- 📚 **Diccionario de Rasgos interactivo:** Hacé clic en cualquier etiqueta de rasgo para ver su descripción oficial en un modal elegante
- 💎 **Metadatos en cada carta:** Rareza (Común, Poco Común, Rara, Única) y Publicación de origen
- 💾 **Carga infinita** (Infinite Scroll) para una navegación fluida
- 🔤 **Terminología oficial Devir** para los términos en español

---

## 📸 Capturas

| Tema PF2e | Modo Oscuro |
|---|---|
| *(screenshot)* | *(screenshot)* |

---

## 🗂️ Estructura del Proyecto

```
PF2E-V2/
│
├── web/                        # Aplicación web (deployable)
│   ├── index.html              # Estructura de la SPA
│   ├── style.css               # Estilos + sistema de temas
│   ├── app.js                  # Lógica de filtros, modal e i18n
│   ├── feats_data.json         # Base de datos de Dotes (generada)
│   └── traits_data.json        # Diccionario de Rasgos (generado)
│
└── scripts/                    # Herramientas de procesamiento de datos
    ├── parser.py               # Extrae dotes de Foundry VTT → JSON
    ├── export_to_excel.py      # Exporta dotes a .xlsx para traducción
    ├── import_from_excel.py    # Reimporta traducciones desde .xlsx
    ├── build_traits.py         # Genera el diccionario de rasgos
    ├── translate_trait_names.py # Auto-traduce nombres de rasgos (Google)
    └── fix_trait_names.py      # Aplica correcciones manuales (Devir)
```

---

## 🚀 Uso Local

No requiere instalación ni servidor. Simplemente:

```bash
# Clona el repositorio
git clone https://github.com/GuilleGearts/pf2e-feat-visualizer.git
cd pf2e-feat-visualizer

# Servir la carpeta web con cualquier servidor HTTP
# Opción 1: Python
python -m http.server 8080 --directory web

# Opción 2: Node.js (npx)
npx serve web

# Opción 3: VS Code Live Server
# Abrí web/index.html con la extensión Live Server
```

Luego abrí `http://localhost:8080` en tu navegador.

---

## 🛠️ Workflow de Datos

### Requisitos
```bash
pip install pandas openpyxl
```

### 1. Generar la base de datos de Dotes
Requiere tener los archivos del sistema `pf2e` de Foundry VTT en una carpeta `GitVTT/pf2e-14-dev/`.
```bash
cd scripts
python parser.py
```

### 2. Traducir Dotes al Español (Excel)
```bash
python export_to_excel.py      # Genera web/traduccion_dotes.xlsx
# → Editá el Excel: completá Name (ES) y Description (ES)
python import_from_excel.py    # Reimporta las traducciones al JSON
```

### 3. Generar y traducir el Diccionario de Rasgos
```bash
python build_traits.py         # Extrae rasgos de Foundry
python translate_trait_names.py # Auto-traduce nombres
python fix_trait_names.py      # Aplica correcciones Devir
```

---

## 🌐 Despliegue en Vercel

1. Subí el repositorio a GitHub
2. Conectá tu cuenta en [vercel.com](https://vercel.com)
3. Al importar el proyecto, configurá el **Root Directory** como `web/`
4. Hacé clic en **Deploy**

Cada `push` a `main` actualizará la web automáticamente.

---

## ⚖️ Aviso Legal

Este proyecto utiliza marcas registradas y/o derechos de autor de **Paizo Inc.**, bajo la [Política de Uso Comunitario de Paizo](http://paizo.com/communityuse).

> *Pathfinder, el logo de Pathfinder y Golarion son marcas registradas de Paizo Inc. Los contenidos de Pathfinder son propiedad de Paizo Inc. y se utilizan con permiso.*

Esta aplicación **no está publicada, respaldada ni específicamente aprobada por Paizo Inc.** y no cobra por el acceso a este contenido.

---

## ☕ Apoyar el Proyecto

Si te fue útil, podés invitarme un cafecito:

[![Cafecito](https://img.shields.io/badge/☕%20Cafecito-guillegearts-orange?style=for-the-badge)](https://cafecito.app/guillegearts)

---

## 👤 Autor

**GuilleGearts**
- 🐙 GitHub: [@GuilleGearts](https://github.com/GuilleGearts)
- ☕ Cafecito: [cafecito.app/guillegearts](https://cafecito.app/guillegearts)
