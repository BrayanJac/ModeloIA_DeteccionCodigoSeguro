import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from preprocessing.data_loader import load_clean_dataset, prepare_training_data, split_train_test
from feature_engineering.feature_extractor import FeatureExtractor
import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
import matplotlib.pyplot as plt


def convert_features_to_matrix(features_list, feature_names=None):
    """
    Convierte una lista de diccionarios de características a una matriz numpy.
    
    Args:
        features_list: Lista de diccionarios de características.
        feature_names: Lista de nombres de características (opcional).
        
    Returns:
        Matriz numpy y lista de nombres de características.
    """
    if not features_list:
        return np.array([]), []
    
    if feature_names is None:
        # Obtener todos los nombres de características
        all_feature_names = set()
        for features in features_list:
            all_feature_names.update(features.keys())
        feature_names = sorted(all_feature_names)
    
    # Crear matriz
    n_samples = len(features_list)
    n_features = len(feature_names)
    X = np.zeros((n_samples, n_features))
    
    for i, features in enumerate(features_list):
        for j, feature_name in enumerate(feature_names):
            X[i, j] = features.get(feature_name, 0)
    
    return X, feature_names


def plot_confusion_matrix(cm, classes, output_path):
    """
    Genera y guarda una matriz de confusión visual.
    
    Args:
        cm: Matriz de confusión.
        classes: Lista de nombres de clases.
        output_path: Ruta donde guardar la imagen.
    """
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Matriz de Confusión')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    fmt = 'd'
    thresh = cm.max() / 2
    for i, j in np.ndindex(cm.shape):
        plt.text(j, i, format(cm[i, j], fmt),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black")
    
    plt.ylabel('Etiqueta Real')
    plt.xlabel('Etiqueta Predicha')
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Matriz de confusión guardada en: {output_path}")


def main():
    print("=" * 60)
    print("EVALUACIÓN DEL CLASIFICADOR DE SEGURIDAD")
    print("=" * 60)
    
    # Cargar modelo y vectorizador
    print("\n1. Cargando modelo y vectorizador...")
    model_path = 'models/security_classifier.joblib'
    vectorizer_path = 'models/vectorizer.joblib'
    feature_names_path = 'models/feature_names.joblib'
    
    if not os.path.exists(model_path):
        print(f"   ERROR: No se encontró el modelo en {model_path}")
        print("   Ejecuta primero: python scripts/train.py")
        return
    
    model = joblib.load(model_path)
    print(f"   Modelo cargado desde: {model_path}")
    
    feature_extractor = FeatureExtractor()
    feature_extractor.load_vectorizer(vectorizer_path)
    print(f"   Vectorizador cargado desde: {vectorizer_path}")
    
    feature_names = joblib.load(feature_names_path)
    print(f"   Nombres de características cargados desde: {feature_names_path}")
    
    # Cargar dataset de prueba
    print("\n2. Cargando dataset limpio...")
    dataset_path = 'datasets/secure_programming_dpo_clean.json'
    data = load_clean_dataset(dataset_path)
    print(f"   Registros cargados: {len(data)}")
    
    # Preparar datos
    print("\n3. Preparando datos de evaluación...")
    code_samples, labels = prepare_training_data(data)
    print(f"   Muestras de código: {len(code_samples)}")
    
    # Dividir en train/test (usando la misma semilla que en entrenamiento)
    X_train_raw, X_test_raw, y_train, y_test = split_train_test(code_samples, labels, test_size=0.2, random_seed=42)
    print(f"   Test: {len(X_test_raw)} muestras")
    
    # Extraer características
    print("\n4. Extrayendo características...")
    X_test_features = feature_extractor.transform(X_test_raw)
    X_test, _ = convert_features_to_matrix(X_test_features, feature_names)
    print(f"   Dimensiones de prueba: {X_test.shape}")
    
    # Realizar predicciones
    print("\n5. Realizando predicciones...")
    y_pred = model.predict(X_test)
    y_scores = model.predict_proba(X_test)[:, 1]  # Probabilidades de clase 1 (vulnerable)
    
    # Calcular métricas
    print("\n6. Calculando métricas...")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='binary')
    recall = recall_score(y_test, y_pred, average='binary')
    f1 = f1_score(y_test, y_pred, average='binary')
    auc_score = roc_auc_score(y_test, y_scores)
    
    print("   Métricas en conjunto de prueba:")
    print(f"     - Accuracy:  {accuracy:.4f}")
    print(f"     - Precision: {precision:.4f}")
    print(f"     - Recall:    {recall:.4f}")
    print(f"     - F1-Score:  {f1:.4f}")
    print(f"     - AUC-ROC:   {auc_score:.4f}")
    
    # Matriz de confusión
    print("\n7. Generando matriz de confusión...")
    cm = confusion_matrix(y_test, y_pred)
    print("   Matriz de confusión:")
    print(f"     {cm[0]}")
    print(f"     {cm[1]}")
    
    os.makedirs('reports', exist_ok=True)
    plot_confusion_matrix(cm, ['Seguro', 'Vulnerable'], 'reports/confusion_matrix.png')
    
    # Reporte de clasificación detallado
    print("\n9. Reporte de clasificación detallado:")
    print(classification_report(y_test, y_pred, target_names=['Seguro', 'Vulnerable']))
    
    # Guardar reporte en archivo
    report_path = 'reports/evaluation_report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Reporte de Evaluación del Modelo\n\n")
        f.write("## Métricas de Rendimiento\n\n")
        f.write(f"- **Accuracy**: {accuracy:.4f}\n")
        f.write(f"- **Precision**: {precision:.4f}\n")
        f.write(f"- **Recall**: {recall:.4f}\n")
        f.write(f"- **F1-Score**: {f1:.4f}\n")
        f.write(f"- **AUC-ROC**: {auc_score:.4f}\n\n")
        f.write("## Matriz de Confusión\n\n")
        f.write("```\n")
        f.write(f"{cm[0]}\n")
        f.write(f"{cm[1]}\n")
        f.write("```\n\n")
        f.write("## Reporte de Clasificación\n\n")
        f.write("```\n")
        f.write(classification_report(y_test, y_pred, target_names=['Seguro', 'Vulnerable']))
        f.write("```\n\n")
    
    print(f"   Reporte guardado en: {report_path}")
    
    # Importancia de características
    print("\n10. Características más importantes (top 20):")
    feature_importance = model.feature_importances_
    importance_indices = np.argsort(feature_importance)[::-1][:20]
    
    for i, idx in enumerate(importance_indices):
        print(f"     {i+1}. {feature_names[idx]}: {feature_importance[idx]:.4f}")
    
    print("\n" + "=" * 60)
    print("EVALUACIÓN COMPLETADA")
    print("=" * 60)


if __name__ == '__main__':
    main()
