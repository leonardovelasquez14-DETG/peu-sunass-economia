# 🏛️ BANCO DE PREGUNTAS Y SIMULADOR DE ADMISIÓN PEU SUNASS 2026
## Especialidad: Economía | 900 Preguntas con Solucionario Detallado y Motor Inteligente de Dependencias

**Por BackBone Academy** · Instagram: [@backbone.academy](https://www.instagram.com/backbone.academy) · TikTok: [@backbone.academy](https://www.tiktok.com/@backbone.academy)

> [!TIP]
> **🌐 USA EL SIMULADOR WEB DIRECTAMENTE (sin instalar nada, desde celular o PC):**  
> 👉 **[https://leonardovelasquez14-detg.github.io/peu-sunass-economia/](https://leonardovelasquez14-detg.github.io/peu-sunass-economia/)**  
> *(Nota: en la versión web el progreso se guarda solo localmente en tu navegador y no se sincroniza entre dispositivos; ver detalles en la [Guía de Uso](#-guía-de-uso-del-simulador-interactivo)).*

---

### 📌 Tabla de Contenidos
1. [Descripción General](#-descripción-general)
2. [Estructura del Banco de Preguntas](#-estructura-del-banco-de-preguntas)
3. [Arquitectura de Archivos y Documentos](#-arquitectura-de-archivos-y-documentos)
4. [Motor de Dependencias y Preguntas Encadenadas](#-motor-de-dependencias-y-preguntas-encadenadas)
5. [Sistema de Preguntas Saltadas y Cuaderno de Estudio](#-sistema-de-preguntas-saltadas-y-cuaderno-de-estudio)
6. [Guía de Uso del Simulador Interactivo](#-guía-de-uso-del-simulador-interactivo)
7. [Metodología de Estudio Recomendada](#-metodología-de-estudio-recomendada)

---

### 📖 Descripción General

Este repositorio constituye la plataforma integral de preparación para el **Curso de Extensión Universitaria (PEU) de la Superintendencia Nacional de Servicios de Saneamiento (SUNASS)** en la especialidad de **Economía**. 

Contiene **900 preguntas originales y rigurosas** elaboradas con base en el temario oficial publicado por SUNASS (`8699730-temario-peu.pdf`), abarcando desde fundamentos micro y macroeconómicos hasta regulación tarifaria, subsidios cruzados y economía de empresas prestadoras de saneamiento (EPS).

Cada pregunta cuenta con:
- Enunciado formal con notación matemática rigurosa en LaTeX.
- Cuatro alternativas estructuradas \([A, B, C, D]\) con distractores plausibles.
- Solucionario completo paso a paso: desarrollo algebraico, cálculo de derivadas/integrales y justificación económica/normativa.
- Claves balanceadas uniformemente en cada módulo (\(\approx 25\%\) para cada letra: A, B, C, D).

---

### 📚 Estructura del Banco de Preguntas

El banco está distribuido en los **10 módulos oficiales** del examen (90 preguntas por módulo):

| Módulo | Nombre del Módulo | Preguntas | Banco PDF | Teoría (Beamer) |
| :---: | :--- | :---: | :--- | :--- |
| **01** | Teoría del Consumidor | 90 | `01/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_I.pdf` | `teoria/M01_Teoria_Consumidor.pdf` |
| **02** | Teoría del Productor | 90 | `02/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_II.pdf` | `teoria/M02_Teoria_Productor.pdf` |
| **03** | Competencia Perfecta | 90 | `03/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_III.pdf` | `teoria/M03_Competencia_Perfecta.pdf` |
| **04** | Equilibrio General y Bienestar | 90 | `04/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_IV.pdf` | `teoria/M04_Equilibrio_General_Bienestar.pdf` |
| **05** | Monopolio, Discriminación y Regulación | 90 | `05/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_V.pdf` | `teoria/M05_Monopolio_Regulacion.pdf` |
| **06** | Mercados de Factores | 90 | `06/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_VI.pdf` | `teoria/M06_Mercados_Factores.pdf` |
| **07** | Competencia Imperfecta | 90 | `07/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_VII.pdf` | `teoria/M07_Competencia_Imperfecta.pdf` |
| **08** | Otras Fallas de Mercado | 90 | `08/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_VIII.pdf` | `teoria/M08_Fallas_Mercado.pdf` |
| **09** | Econometría | 90 | `09/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_IX.pdf` | `teoria/M09_Econometria.pdf` |
| **10** | Finanzas Corporativas y Proyectos | 90 | `10/Banco_Preguntas_PEU_SUNASS_Economia_Modulo_X.pdf` | `teoria/M10_Finanzas.pdf` |

#### Distribución interna de cada módulo (90 preguntas):
- **Bloque A (Preguntas 1 a 30):** Fundamentos conceptuales, deducción teórica e intuición económica (30%).
- **Bloque B (Preguntas 31 a 65):** Modelos analíticos, optimización matemática, cálculo marginal y financiero (39%).
- **Bloque C (Preguntas 66 a 90):** Aplicación práctica a la regulación económica, saneamiento en el Perú, metodologías SUNASS y casuística de EPS (31%).

---

### 📁 Arquitectura de Archivos y Documentos

```text
BANCO DE PREGUNTAS SUNASS/
├── 01/ ... 10/                             # Carpetas por módulo temático (900 preguntas)
│   ├── [mX_]bloque_{a,b,c}.tex             # Enunciados de las preguntas por bloque en LaTeX
│   ├── [mX_]claves.tex                     # Tabla de claves de respuestas
│   ├── [mX_]solucionario.tex               # Solucionarios desarrollados
│   ├── banco_peu_sunass[_modulo_X].tex     # Documento principal compilable
│   └── Banco_Preguntas_..._Modulo_[X].pdf  # Versión PDF lista para estudio/impresión
├── teoria/                                 # Guías teóricas Beamer 16:9 (10 módulos, 96 págs.)
│   ├── sunass_estilo.sty                   # Plantilla gráfica BackBone Academy + PEU SUNASS
│   ├── backbone_logo*.png                  # Logotipos de BackBone Academy
│   ├── M01_... hasta M10_...tex            # Fuente LaTeX + TikZ/pgfplots
│   └── M01_... hasta M10_...pdf            # Diapositivas teóricas compiladas por módulo
├── 8699730-temario-peu.pdf                 # Temario oficial de SUNASS
├── banco_preguntas_consolidado.json        # Base de datos central (900 preguntas con metadata)
├── cuaderno_errores.json                   # Registro persistente de falladas y saltadas [S]
├── historial_simulacros.json               # Historial cronológico de notas y tiempos
├── simulador.py                            # Motor de ejecución del simulador CLI en Python
├── iniciar_simulador.bat                   # Acceso rápido en Windows (doble clic)
├── iniciar_simulador.sh                    # Acceso rápido en Linux/macOS (./iniciar_simulador.sh)
├── index.html                              # Simulador web estático (GitHub Pages)
└── README.md                               # Este manual y documentación integral
```

---

### 🔗 Motor de Dependencias y Preguntas Encadenadas

#### El Problema Común en los Simulacros Convencionales:
En los exámenes de economía y regulación cuantitativa (como SUNASS y BCRP), abundan los ejercicios en cadena donde una pregunta solicita calcular el precio de equilibrio de monopolio, la siguiente pide la pérdida irrecuperable de eficiencia con los datos calculados, y la siguiente solicita evaluar la tarifa eficiente bajo regulación por tasa de retorno. 

En simulacros aleatorios comunes, estas preguntas suelen aparecer desordenadas (ej. la parte 3 antes de la parte 1) o aisladas sin los datos del problema base, volviéndolas imposibles de responder.

#### La Solución Implementada en la v2.0:
1. **Detección y Etiquetado:** Se identificaron y auditaron las **48 preguntas dependientes** del banco, asignándoles claves:
   - `cluster_id`: Identificador único que agrupa a toda la familia de preguntas.
   - `parent_id`: ID de la pregunta raíz que introdujo los datos del problema.
   - `depends_on`: ID de la pregunta inmediata de la cual depende.
   - `context_premise`: Copia literal íntegra del problema o funciones de costos/demanda iniciales.
2. **Muestreo por Clusters Atómicos (`sample_clustered`):**
   - Cuando el simulador selecciona preguntas aleatorias, **nunca rompe un cluster**.
   - Toda la cadena se selecciona en bloque y se presenta al postulante en estricto orden cronológico (1, 2, 3...).
3. **Caja Visual de Contexto:**
   - Si la pregunta depende de un problema previo, la terminal renderiza automáticamente un recuadro destacado con la premisa:
   ```text
   ┌─ 📌 PREMISA / CONTEXTO VINCULADO (M03-Q48) ────────────────────────────┐
   │  Considere el mercado de agua potable en bloque donde la demanda es   │
   │  P = 120 - 2Q y el costo marginal de producción es CMg = 20 + Q.      │
   └────────────────────────────────────────────────────────────────────────┘
   ```
4. **Modo Secuencial Oficial por Módulo:**
   - En el menú por módulo, el usuario puede seleccionar el orden 1 al 90 o por bloques (A, B, C) para estudiar el temario tal cual fue diseñado de forma pedagógica.

---

### 📓 Sistema de Preguntas Saltadas y Cuaderno de Estudio

Para optimizar el tiempo de cara a la fecha de examen:
- **Saltar con tecla `[S]`:** Si una pregunta es muy extensa o el usuario duda de la respuesta, puede presionar `S`. El simulador no la cuenta como adivinanza; le revela la solución para aprender de inmediato y **la registra automáticamente en `cuaderno_errores.json`** bajo la etiqueta `error_type: "saltada"`.
- **Preguntas Falladas:** Aquellas donde se marque una alternativa errónea se guardan como `error_type: "fallada"`.
- **Filtros en el Cuaderno de Estudio (Opción 3 del Menú Principal):**
  1. Repasar **TODAS** las pendientes (falladas + saltadas).
  2. Repasar **únicamente las FALLADAS** (para atacar errores conceptuales).
  3. Repasar **únicamente las SALTADAS** (para practicar cálculo y agilidad).
  4. Muestra rápida aleatoria (15 preguntas).
- **Descarte Progresivo (Mastery Tracking):**
  - Al repasar en el Cuaderno de Estudio, cada pregunta que el usuario responda correctamente **se retira automáticamente de la lista de pendientes**.
  - El objetivo es reducir el cuaderno a **0 preguntas pendientes** antes del examen.

---

### 🚀 Guía de Uso del Simulador Interactivo

#### Opción A — Versión Web (sin instalar nada)
Puedes usar el simulador directamente desde el navegador (celular o PC) entrando al sitio publicado en **GitHub Pages**:
- 🌐 **Simulador Web:** https://leonardovelasquez14-detg.github.io/peu-sunass-economia/

> **⚠️ Importante sobre el guardado en la versión Web:**  
> La versión web funciona de forma estática (sin servidor ni cuentas de usuario). Tu cuaderno de errores e historial de simulacros se guardan únicamente en la memoria local del navegador (`localStorage`) del dispositivo actual y **no se sincronizan en la nube ni entre dispositivos**. Si limpias los datos del navegador o entras desde otro equipo/navegador, tu progreso no aparecerá allí (puedes respaldarlo manualmente usando el botón **Exportar / Importar progreso (.json)** dentro de *Estadísticas*).

#### Opción B — Versión Local en PC (progreso persistente en archivos JSON)
Si prefieres guardar tu progreso en archivos locales (`cuaderno_errores.json` e `historial_simulacros.json`):
1. Descarga el repositorio desde GitHub (**Code → Download ZIP**) y descomprime la carpeta (o clónalo con `git`).
2. **En Windows:** haz **doble clic en `iniciar_simulador.bat`** (requiere Python 3 instalado).
3. **En Linux / macOS:** abre una terminal en la carpeta y ejecuta:
```bash
./iniciar_simulador.sh
```
O directamente con Python en cualquier sistema:
```bash
python3 simulador.py
```

#### 2. Menú Principal
```text
  1. 🎯 Simulacro General Tipo Examen SUNASS (Aleatorio Clustered)
  2. 📚 Estudio Dirigido por Módulo Temático (Secuencial o Bloques A/B/C)
  3. 📓 Cuaderno de Estudio (Repaso Activo de Errores y Saltadas)
  4. 📊 Radiografía de Rendimiento y Estadísticas
  5. 🚪 Salir
```

#### 3. Atajos durante la resolución:
- `A`, `B`, `C`, `D`: Seleccionar alternativa.
- `S`: **Saltar la pregunta** (guarda en el cuaderno para estudio posterior y muestra la solución si está en modo Tutor).
- `Q`: Pausar o salir de la sesión actual guardando las estadísticas acumuladas hasta ese momento.

#### 4. Modalidades de Retroalimentación:
- **Modo Tutor:** Tras cada pregunta muestra la justificación, procedimiento algebraico completo y lecciones clave.
- **Modo Examen:** Experiencia 100% silenciosa y cronometrada. El puntaje, desglose por módulo y solucionario se revelan al finalizar.

---

### 🎯 Metodología de Estudio Recomendada (Rumbo al PEU)

1. **Fase 1: Módulos Nucleares de SUNASS (Mayor Ponderación)**
   - Priorizar **Módulo 05** (Monopolio y Regulación), **Módulo 02** (Teoría del Productor: escala y subaditividad), **Módulo 07** (Competencia Imperfecta) y **Módulo 08** (Otras Fallas de Mercado).
   - Resolver el **Bloque C** de cada módulo en modo secuencial para dominar el marco regulatorio de saneamiento y la terminología técnica de SUNASS.
2. **Fase 2: Agilidad Cuantitativa (Bloques B)**
   - Entrenar los Bloques B de los 10 módulos (problemas de optimización de Lagrange, equilibrios de Cournot/Stackelberg, MCO, contraste de hipótesis, WACC y VAN).
3. **Fase 3: Simulacros Cronometrados**
   - Ejecutar el **Simulacro Completo Oficial de 90 preguntas** con cronómetro (150 minutos = 1 min 40 s por pregunta).
   - Revisar al final del día el **Cuaderno de Estudio** para pulir las preguntas falladas y saltadas.

---
*Edición preparada por **BackBone Academy** ([@backbone.academy](https://www.instagram.com/backbone.academy) en Instagram y [@backbone.academy](https://www.tiktok.com/@backbone.academy) en TikTok) para el postulante de Economía - PEU SUNASS 2026.*
