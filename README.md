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
│       └── analyze_pr.py                    # Análisis de PR (CI/CD)
│
├── reports/
│   ├── dataset_analysis_report.md           # Reporte de análisis
│   ├── data_quality_report.md               # Reporte de calidad
│   ├── evaluation_report.md                 # Reporte de evaluación
│   ├── confusion_matrix.png                 # Matriz de confusión
│   └── roc_curve.png                        # Curva ROC
│
├── tests/
│   ├── seguro.php                           # Ejemplo de código seguro
│   └── vulnerable.php                       # Ejemplo de código vulnerable
│
├── .github/
│   └── workflows/
│       └── security-scan.yml                # Workflow de GitHub Actions
│
├── requirements.txt                         # Dependencias Python
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
git clone <repository-url>
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

Esto genera:
- `models/security_classifier.joblib` - Modelo entrenado
- `models/vectorizer.joblib` - Vectorizador TF-IDF
- `models/feature_names.joblib` - Nombres de características

### Evaluación del Modelo

```bash
python scripts/evaluation/evaluate.py
```

Esto genera:
- `reports/evaluation_report.md` - Reporte de evaluación
- `reports/confusion_matrix.png` - Matriz de confusión visual
- `reports/roc_curve.png` - Curva ROC

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

El workflow de GitHub Actions se activa automáticamente cuando se crea un Pull Request de `dev` hacia `test`.

### Flujo del Pipeline

1. **Trigger**: Pull Request hacia `test`
2. **Checkout**: Obtener código del repositorio
3. **Setup**: Configurar Python y dependencias
4. **Get Changed Files**: Identificar archivos modificados
5. **Security Scan**: Analizar cada archivo modificado con el modelo
6. **Decision**:
   - Si probabilidad de vulnerabilidad > umbral (0.7):
     - ❌ Fallar workflow
     - 🔒 Bloquear merge
     - 💬 Crear comentario en el PR con detalles
   - Si código es seguro:
     - ✅ Permitir continuar el pipeline

### Configuración

El workflow está configurado en `.github/workflows/security-scan.yml`.

Para modificar el umbral de detección, edita el parámetro `--threshold` en el workflow.

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

**Parámetros del Modelo:**
- **n_estimators**: 100 árboles en el bosque
- **random_state**: 42 (para reproducibilidad)
- **n_jobs**: -1 (usa todos los núcleos disponibles)
- **class_weight**: 'balanced' (ajusta pesos para clases desbalanceadas)

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

## 🤝 Contribución

Para contribuir:

1. Fork el repositorio
2. Crear una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request hacia `test`

**Nota**: El workflow de seguridad analizará automáticamente tu código antes de permitir el merge.

## 📚 Referencias

- Fuente de la base de datos: https://huggingface.co/datasets/CyberNative/Code_Vulnerability_Security_DPO
- scikit-learn: https://scikit-learn.org/
- GitHub Actions: https://github.com/features/actions
- OWASP Top 10: https://owasp.org/www-project-top-ten/

## 👨‍💻 Autor

Proyecto desarrollado por el Grupo 4

---

