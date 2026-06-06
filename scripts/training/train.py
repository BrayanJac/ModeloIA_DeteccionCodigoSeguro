#!/usr/bin/env python3
"""
Script de entrenamiento del clasificador de seguridad.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from preprocessing.data_loader import load_clean_dataset, prepare_training_data, split_train_test
from feature_engineering.feature_extractor import FeatureExtractor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import numpy as np


def train_model(X_train, y_train, n_estimators: int = 100, random_state: int = 42):
    """
    Entrena el clasificador RandomForest.
    
    Args:
        X_train: Características de entrenamiento.
        y_train: Labels de entrenamiento.
        n_estimators: Número de árboles en el bosque.
        random_state: Semilla aleatoria.
        
    Returns:
        Modelo entrenado.
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """
    Evalúa el modelo y retorna métricas.
    
    Args:
        model: Modelo entrenado.
        X_test: Características de prueba.
        y_test: Labels de prueba.
        
    Returns:
        Diccionario con métricas.
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred, average='binary'),
        'recall': recall_score(y_test, y_pred, average='binary'),
        'f1': f1_score(y_test, y_pred, average='binary'),
    }
    
    return metrics, y_pred


def cross_validation(model, X, y, cv: int = 5):
    """
    Realiza validación cruzada.
    
    Args:
        model: Modelo a evaluar.
        X: Características.
        y: Labels.
        cv: Número de folds.
        
    Returns:
        Diccionario con métricas de validación cruzada.
    """
    cv_strategy = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    
    cv_accuracy = cross_val_score(model, X, y, cv=cv_strategy, scoring='accuracy', n_jobs=-1)
    cv_precision = cross_val_score(model, X, y, cv=cv_strategy, scoring='precision', n_jobs=-1)
    cv_recall = cross_val_score(model, X, y, cv=cv_strategy, scoring='recall', n_jobs=-1)
    cv_f1 = cross_val_score(model, X, y, cv=cv_strategy, scoring='f1', n_jobs=-1)
    
    cv_metrics = {
        'accuracy_mean': cv_accuracy.mean(),
        'accuracy_std': cv_accuracy.std(),
        'precision_mean': cv_precision.mean(),
        'precision_std': cv_precision.std(),
        'recall_mean': cv_recall.mean(),
        'recall_std': cv_recall.std(),
        'f1_mean': cv_f1.mean(),
        'f1_std': cv_f1.std(),
    }
    
    return cv_metrics


def convert_features_to_matrix(features_list):
    """
    Convierte una lista de diccionarios de características a una matriz numpy.
    
    Args:
        features_list: Lista de diccionarios de características.
        
    Returns:
        Matriz numpy y lista de nombres de características.
    """
    if not features_list:
        return np.array([]), []
    
    # Obtener todos los nombres de características
    all_feature_names = set()
    for features in features_list:
        all_feature_names.update(features.keys())
    all_feature_names = sorted(all_feature_names)
    
    # Crear matriz
    n_samples = len(features_list)
    n_features = len(all_feature_names)
    X = np.zeros((n_samples, n_features))
    
    for i, features in enumerate(features_list):
        for j, feature_name in enumerate(all_feature_names):
            X[i, j] = features.get(feature_name, 0)
    
    return X, all_feature_names


def main():
    print("=" * 60)
    print("ENTRENAMIENTO DEL CLASIFICADOR DE SEGURIDAD")
    print("=" * 60)
    
    # Cargar dataset limpio
    print("\n1. Cargando dataset limpio...")
    dataset_path = 'datasets/secure_programming_dpo_clean.json'
    data = load_clean_dataset(dataset_path)
    print(f"   Registros cargados: {len(data)}")
    
    # Preparar datos de entrenamiento
    print("\n2. Preparando datos de entrenamiento...")
    code_samples, labels = prepare_training_data(data)
    print(f"   Muestras de código: {len(code_samples)}")
    print(f"   Labels: {len(labels)}")
    print("   Distribución de clases:")
    print(f"     - Seguros (0): {labels.count(0)}")
    print(f"     - Vulnerables (1): {labels.count(1)}")
    
    # Dividir en train/test
    print("\n3. Dividiendo datos en train/test...")
    X_train_raw, X_test_raw, y_train, y_test = split_train_test(code_samples, labels, test_size=0.2, random_seed=42)
    print(f"   Train: {len(X_train_raw)} muestras")
    print(f"   Test: {len(X_test_raw)} muestras")
    
    # Extraer características
    print("\n4. Extrayendo características...")
    feature_extractor = FeatureExtractor(max_features=3000, ngram_range=(1, 2))
    
    print("   Ajustando vectorizador TF-IDF...")
    feature_extractor.fit(X_train_raw)
    
    print("   Extrayendo características de entrenamiento...")
    X_train_features = feature_extractor.transform(X_train_raw)
    X_train, feature_names = convert_features_to_matrix(X_train_features)
    print(f"   Dimensiones de entrenamiento: {X_train.shape}")
    
    print("   Extrayendo características de prueba...")
    X_test_features = feature_extractor.transform(X_test_raw)
    X_test, _ = convert_features_to_matrix(X_test_features)
    print(f"   Dimensiones de prueba: {X_test.shape}")
    
    # Entrenar modelo
    print("\n5. Entrenando modelo RandomForest...")
    model = train_model(X_train, y_train, n_estimators=100, random_state=42)
    print("   Modelo entrenado exitosamente")
    
    # Evaluar modelo
    print("\n6. Evaluando modelo en conjunto de prueba...")
    test_metrics, y_pred = evaluate_model(model, X_test, y_test)
    print("   Métricas en conjunto de prueba:")
    print(f"     - Accuracy:  {test_metrics['accuracy']:.4f}")
    print(f"     - Precision: {test_metrics['precision']:.4f}")
    print(f"     - Recall:    {test_metrics['recall']:.4f}")
    print(f"     - F1-Score:  {test_metrics['f1']:.4f}")
    
    # Validación cruzada
    print("\n7. Realizando validación cruzada (5-fold)...")
    cv_metrics = cross_validation(model, X_train, y_train, cv=5)
    print("   Métricas de validación cruzada:")
    print(f"     - Accuracy:  {cv_metrics['accuracy_mean']:.4f} ± {cv_metrics['accuracy_std']:.4f}")
    print(f"     - Precision: {cv_metrics['precision_mean']:.4f} ± {cv_metrics['precision_std']:.4f}")
    print(f"     - Recall:    {cv_metrics['recall_mean']:.4f} ± {cv_metrics['recall_std']:.4f}")
    print(f"     - F1-Score:  {cv_metrics['f1_mean']:.4f} ± {cv_metrics['f1_std']:.4f}")
    
    # Guardar modelo y vectorizador
    print("\n8. Guardando modelo y vectorizador...")
    os.makedirs('models', exist_ok=True)
    
    model_path = 'models/security_classifier.joblib'
    joblib.dump(model, model_path)
    print(f"   Modelo guardado en: {model_path}")
    
    vectorizer_path = 'models/vectorizer.joblib'
    feature_extractor.save_vectorizer(vectorizer_path)
    print(f"   Vectorizador guardado en: {vectorizer_path}")
    
    # Guardar nombres de características
    feature_names_path = 'models/feature_names.joblib'
    joblib.dump(feature_names, feature_names_path)
    print(f"   Nombres de características guardados en: {feature_names_path}")
    
    # Reporte de clasificación detallado
    print("\n9. Reporte de clasificación detallado:")
    print(classification_report(y_test, y_pred, target_names=['Seguro', 'Vulnerable']))
    
    # Importancia de características
    print("\n10. Características más importantes (top 20):")
    feature_importance = model.feature_importances_
    importance_indices = np.argsort(feature_importance)[::-1][:20]
    
    for i, idx in enumerate(importance_indices):
        print(f"     {i+1}. {feature_names[idx]}: {feature_importance[idx]:.4f}")
    
    print("\n" + "=" * 60)
    print("ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 60)


if __name__ == '__main__':
    main()
