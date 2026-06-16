# Pipeline CI/CD Seguro con IA para Detección de Vulnerabilidades

**Desarrollo e Implementación de un Pipeline CI/CD Seguro con integración de IA para la Detección Automática de Vulnerabilidades en código fuente mediante un Modelo de Minería de Datos.**

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Pipeline CI/CD](#pipeline-cicd)
- [Métricas del Modelo](#métricas-del-modelo)
- [Características del Modelo](#características-del-modelo)
- [Contribución](#contribución)
- [Referencias](#referencias)

## 📖 Descripción

Este proyecto implementa un pipeline CI/CD seguro que utiliza Machine Learning clásico (scikit-learn) para detectar automáticamente vulnerabilidades en código fuente. El sistema analiza el código modificado en Pull Requests y bloquea el merge si se detecta código potencialmente vulnerable.

### Características Principales

- **Clasificador Binario**: Determina si el código es SEGURO (0) o VULNERABLE (1)
- **Machine Learning Clásico**: Utiliza RandomForestClassifier de scikit-learn
- **Extracción de Características**: Basada en tokens, funciones peligrosas, funciones de sanitización y métricas de código
- **Integración CI/CD**: Workflow de GitHub Actions que analiza PRs automáticamente
- **Dataset Local**: Entrenado con dataset de programación segura (DPO)

## 🏗️ Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Actions                          │
│                  (Security Scan Workflow)                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Pull Request (dev → test)                      │
│         Obtiene diff de archivos modificados                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Análisis de Código Modificado                  │
│         Ejecuta modelo entrenado sobre cada archivo         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Evaluación de Resultados                       │
│    Probabilidad > Umbral → Bloquear merge + Comentar PR     │
│    Probabilidad ≤ Umbral → Permitir merge                   │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

```
project/
│
├── app/                                     # Aplicación principal (Node.js/Express)
│   ├── app.js                              # Configuración Express
│   ├── server.js                           # Servidor principal
│   ├── package.json                        # Dependencias Node.js
│   ├── test/                               # Pruebas unitarias
│   └── .env                                # Variables de entorno
│
├── api/                                     # API endpoints
│   └── index.js                            # Entry point API
│
├── datasets/
│   ├── secure_programming_dpo.json          # Dataset original
│   └── secure_programming_dpo_clean.json    # Dataset limpio
│
├── models/
│   ├── security_classifier.joblib           # Modelo entrenado
│   ├── vectorizer.joblib                    # Vectorizador TF-IDF
│   └── feature_names.joblib                 # Nombres de características
│
├── scripts/
│   ├── preprocessing/
│   │   └── data_loader.py                   # Carga y preparación de datos
│   │
│   ├── feature_engineering/
│   │   └── feature_extractor.py             # Extracción de características
│   │
│   ├── analysis/
│   │   ├── analyze_dataset.py               # Análisis del dataset
│   │   └── clean_dataset.py                 # Limpieza del dataset
│   │
│   ├── training/
│   │   └── train.py                         # Entrenamiento del modelo
│   │
│   ├── evaluation/
│   │   └── evaluate.py                      # Evaluación del modelo
│   │
│   ├── inference/
│   │   └── predict.py                       # Inferencia/predicción
│   │
│   └── ci_cd/
│       ├── analyze_pr.py                    # Análisis de PR (CI/CD)
│       ├── send_telegram.py                 # Notificaciones Telegram
│       ├── comment_pr.py                    # Comentarios en PR
│       └── create_issue.py                  # Creación de issues automáticas
│
├── reports/
│   ├── dataset_analysis_report.md           # Reporte de análisis
│   ├── data_quality_report.md               # Reporte de calidad
│   ├── evaluation_report.md                 # Reporte de evaluación
│   └── confusion_matrix.png                 # Matriz de confusión
│
├── .github/
│   └── workflows/
│       ├── security-review.yml              # Revisión de seguridad con ML
│       ├── tests.yml                        # Ejecución de pruebas
│       └── deploy.yml                       # Despliegue a producción
│
├── requirements.txt                         # Dependencias Python
├── vercel.json                              # Configuración Vercel
├── .gitignore
└── README.md
```

## 🔧 Requisitos

- Python 3.10+
- scikit-learn
- joblib
- numpy
- matplotlib

## 📦 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro.git
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

### FASE 0: Auditoría y Limpieza del Dataset

Antes de entrenar cualquier modelo, es necesario limpiar el dataset:

```bash
# Analizar dataset original
python scripts/analysis/analyze_dataset.py

# Limpiar dataset
python scripts/analysis/clean_dataset.py
```

Esto genera:
- `datasets/secure_programming_dpo_clean.json` - Dataset limpio
- `reports/dataset_analysis_report.md` - Reporte de análisis
- `reports/data_quality_report.md` - Reporte de calidad de datos

### Entrenamiento del Modelo

```bash
python scripts/training/train.py
```

El script de entrenamiento ahora incluye **optimización automática de hiperparámetros** usando GridSearchCV:
- Busca la mejor combinación de hiperparámetros para el RandomForest
- Prioriza el **recall** para mejorar la detección de vulnerabilidades
- Usa validación cruzada de 3-fold para asegurar robustez
- Muestra el progreso de la búsqueda en tiempo real
- Puede tomar varios minutos dependiendo del hardware

Esto genera:
- `models/security_classifier.joblib` - Modelo entrenado con mejores hiperparámetros
- `models/vectorizer.joblib` - Vectorizador TF-IDF
- `models/feature_names.joblib` - Nombres de características

### Evaluación del Modelo

```bash
python scripts/evaluation/evaluate.py
```

Esto genera:
- `reports/evaluation_report.md` - Reporte de evaluación
- `reports/confusion_matrix.png` - Matriz de confusión visual

### Inferencia/Predicción

Predicción sobre código directo:
```bash
python scripts/inference/predict.py --code "tu código aquí"
```

Predicción sobre archivo:
```bash
python scripts/inference/predict.py --file ruta/al/archivo.py
```

Con umbral personalizado:
```bash
python scripts/inference/predict.py --file ruta/al/archivo.py --threshold 0.8
```

### Validación del Modelo

La carpeta `tests/` contiene ejemplos de código para validar el modelo:

```bash
# Probar código seguro
python scripts/inference/predict.py --file tests/seguro.php

# Probar código vulnerable
python scripts/inference/predict.py --file tests/vulnerable.php
```

- **seguro.php**: Ejemplo de código PHP seguro usando prepared statements
- **vulnerable.php**: Ejemplo de código PHP vulnerable con SQL injection directo

## 🔄 Pipeline CI/CD

El pipeline CI/CD se activa automáticamente cuando se crea un Pull Request de `dev` hacia `test`.

### Flujo del Pipeline

#### Etapa 1: Revisión de Seguridad con Modelo de Minería de Datos
- **Trigger**: Pull Request de `dev` → `test`
- **Análisis**: Descarga el diff del PR y procesa el código modificado en la carpeta `app/`
- **Clasificación**: Utiliza un modelo de Machine Learning clásico (scikit-learn) para clasificar el código como SEGURO o VULNERABLE
- **Si VULNERABLE**:
  - ❌ Bloquea el merge del PR
  - 💬 Crea comentario detallado en el PR con probabilidad y tipo de vulnerabilidad
  - 📱 Envía notificación inmediata vía Telegram
  - 🏷️ Aplica etiqueta "fixing-required"
  - 📝 Crea issue automática vinculada
- **Si SEGURO**:
  - ✅ Continúa el pipeline
  - 🔀 Auto-merge del PR a rama `test`

#### Etapa 2: Merge Automático a test + Pruebas
- **Trigger**: Push a rama `test` (después del auto-merge)
- **Pruebas**: Ejecución de pruebas unitarias e integración (Jest)
- **Si fallan**:
  - ❌ Bloquea el merge
  - 📱 Envía notificación Telegram
  - 🏷️ Aplica etiqueta "tests-failed"
- **Si pasan**:
  - ✅ Continúa el pipeline
  - 🔀 Auto-merge a rama `main`

#### Etapa 3: Merge a main y Despliegue en Producción
- **Trigger**: Push a rama `main` (después del auto-merge)
- **Despliegue**: Despliegue automático en Vercel
- **Notificación**: Mensaje final de éxito vía Telegram

### Notificaciones Telegram

El pipeline envía notificaciones automáticas en los siguientes eventos:
- 🔍 Inicio de revisión de seguridad
- 📊 Resultado de la clasificación del modelo (seguro/vulnerable + probabilidad)
- 🔀 Merge a test realizado
- 🧪 Resultado de pruebas
- 🚀 Despliegue en producción exitoso
- ❌ Despliegue en producción fallido
- � Rechazo por vulnerabilidad (con detalle)

### Configuración de Secrets

Para que el pipeline funcione correctamente, configura los siguientes secrets en GitHub:

**Para Telegram:**
- `TELEGRAM_BOT_TOKEN`: Token del bot de Telegram
- `TELEGRAM_CHAT_ID`: ID del chat donde enviar notificaciones

**Para GitHub Actions:**
- `PAT_TOKEN`: Personal Access Token con permisos de repo (para auto-merge)
- `VERCEL_TOKEN`: Token de Vercel para despliegue
- `VERCEL_ORG_ID`: ID de organización en Vercel
- `VERCEL_PROJECT_ID`: ID del proyecto en Vercel

### Workflows

El pipeline consta de 3 workflows principales:

1. **`.github/workflows/security-review.yml`**: Revisión de seguridad con ML
2. **`.github/workflows/tests.yml`**: Ejecución de pruebas
3. **`.github/workflows/deploy.yml`**: Despliegue a producción

Para modificar el umbral de detección, edita el parámetro `--threshold` en `security-review.yml` (actualmente 0.75).

## 📊 Métricas del Modelo

El modelo utiliza las siguientes métricas de evaluación:

- **Accuracy**: Precisión general del modelo
- **Precision**: Proporción de vulnerabilidades detectadas correctamente
- **Recall**: Proporción de vulnerabilidades reales detectadas
- **F1-Score**: Media armónica de precision y recall
- **AUC-ROC**: Área bajo la curva ROC

### Validación Cruzada

El modelo se evalúa con validación cruzada de 5-fold para asegurar su robustez.

## 🤖 Modelo Entrenado

### Archivos del Modelo (.joblib)

La carpeta `models/` contiene 3 archivos esenciales para el funcionamiento del clasificador:

#### 1. security_classifier.joblib
**Contenido**: Modelo RandomForestClassifier entrenado

**Descripción**: Este archivo contiene el modelo de Machine Learning ya entrenado con el dataset de programación segura. Incluye:
- Los 100 árboles de decisión construidos durante el entrenamiento
- La estructura del ensemble learning
- Los parámetros de configuración del modelo
- La información de las características aprendidas

**Uso**: Se carga con `joblib.load()` para realizar predicciones sobre nuevo código. El modelo toma como entrada las características extraídas del código y retorna:
- La clasificación (0 = Seguro, 1 = Vulnerable)
- Las probabilidades de cada clase

**Tamaño**: Variable (dependiendo del dataset y número de características)

#### 2. vectorizer.joblib
**Contenido**: Vectorizador TF-IDF entrenado

**Descripción**: Este archivo contiene el objeto TfidfVectorizer ajustado al dataset de entrenamiento. Incluye:
- El vocabulario de tokens aprendido del dataset
- Los parámetros de vectorización (max_features=3000, ngram_range=(1,2))
- Los IDF (Inverse Document Frequency) calculados
- La configuración de preprocesamiento de texto

**Uso**: Es esencial para transformar nuevo código al mismo espacio de características usado durante el entrenamiento. Sin este vectorizador, las características extraídas del nuevo código no serían compatibles con el modelo.

**Importancia**: Garantiza que las características de entrada tengan el mismo formato y significado que las usadas durante el entrenamiento.

#### 3. feature_names.joblib
**Contenido**: Lista de nombres de características

**Descripción**: Este archivo contiene una lista ordenada con todos los nombres de características utilizadas por el modelo. Incluye:
- Nombres de características TF-IDF (tokens del código)
- Nombres de características manuales (funciones peligrosas, sanitización, métricas)
- El orden exacto de las características en la matriz de entrada

**Uso**: Se utiliza para:
- Mapear las características extraídas a las columnas correctas de la matriz de entrada
- Interpretar la importancia de características (feature importance)
- Debugging y análisis del modelo
- Reconstruir la matriz de características en el orden correcto

**Importancia**: Es crítico para asegurar que las características se alineen correctamente con las expectativas del modelo.

### RandomForestClassifier

El modelo utiliza un **RandomForestClassifier** de scikit-learn, un algoritmo de ensemble learning que construye múltiples árboles de decisión y combina sus predicciones.

**Funcionamiento:**
- Construye 100 árboles de decisión independientes
- Cada árbol se entrena con una muestra aleatoria del dataset (bootstrap)
- Cada árbol considera un subconjunto aleatorio de características en cada división
- La predicción final es el voto mayoritario de todos los árboles

**Ventajas:**
- **Robustez**: Reduce el overfitting comparado con un solo árbol
- **Precisión**: Generalmente logra mejor precisión que modelos individuales
- **Interpretabilidad**: Permite identificar las características más importantes
- **Manejo de datos no lineales**: Capaz de capturar relaciones complejas

**Hiperparámetros del Modelo:**

El modelo utiliza **GridSearchCV** para optimización automática de hiperparámetros:

**Hiperparámetros explorados:**
- **n_estimators**: [50, 100, 200] - Número de árboles en el bosque
- **max_depth**: [10, 20, None] - Profundidad máxima de los árboles
- **min_samples_split**: [2, 5, 10] - Mínimo de muestras para dividir un nodo
- **min_samples_leaf**: [1, 2, 4] - Mínimo de muestras en nodo hoja
- **max_features**: ['sqrt', 'log2'] - Máximo de características a considerar

**Hiperparámetros fijos:**
- **random_state**: 42 (para reproducibilidad)
- **n_jobs**: -1 (usa todos los núcleos disponibles)
- **class_weight**: 'balanced' (ajusta pesos para clases desbalanceadas)
- **cv**: 3-fold cross-validation

**Métrica de optimización:**
- **scoring**: 'recall' (prioriza detección de vulnerabilidades)

**Proceso de Clasificación:**
1. **Entrada**: Código fuente en texto plano
2. **Extracción de características**: TF-IDF + características manuales
3. **Predicción**: Cada árbol vota si el código es seguro (0) o vulnerable (1)
4. **Salida**: Clasificación final basada en mayoría de votos
5. **Probabilidad**: Porcentaje de árboles que votaron por cada clase

**Interpretación de Resultados:**
- **Label 0 (Seguro)**: El código sigue buenas prácticas de seguridad
- **Label 1 (Vulnerable)**: El código contiene patrones potencialmente peligrosos
- **Probabilidad**: Confianza del modelo en la predicción (0.0 a 1.0)

## 🔬 Características del Modelo

### Características TF-IDF

- Análisis de n-grams (1-2)
- Máximo 3000 características
- Vectorización del código fuente

### Características Manuales

#### Funciones Peligrosas Detectadas
- `eval`
- `exec`
- `os.system`
- `subprocess`
- `Runtime.exec`
- `cursor.execute`
- `execute(`
- `system(`
- `popen(`
- `shell=True`

#### Funciones de Sanitización Detectadas
- `prepareStatement`
- `bindParam`
- `escape`
- `sanitize`
- `htmlspecialchars`
- `real_escape_string`
- `quote(`
- `parameterized`

#### Métricas de Código
- Cantidad de líneas
- Cantidad de tokens
- Cantidad de llamadas a funciones
- Longitud del código
- Patrones de SQL raw
- Ratio de sanitización vs funciones peligrosas

### Modelo de Clasificación

- **Algoritmo**: RandomForestClassifier
- **Estimadores**: 100 árboles
- **Balanceo de clases**: `class_weight='balanced'`
- **Semilla aleatoria**: 42 (reproducibilidad)



## 📚 Referencias

- Fuente de la base de datos: https://huggingface.co/datasets/CyberNative/Code_Vulnerability_Security_DPO
- scikit-learn: https://scikit-learn.org/
- GitHub Actions: https://github.com/features/actions
- OWASP Top 10: https://owasp.org/www-project-top-ten/

## 👨‍💻 Autor

Proyecto desarrollado por el Grupo 4

---


## 🧪 Prueba de CI/CD
Validación del pipeline automático.
