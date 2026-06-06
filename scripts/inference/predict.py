#!/usr/bin/env python3
"""
Script de inferencia/predicción del clasificador de seguridad.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feature_engineering.feature_extractor import FeatureExtractor
import joblib
import numpy as np
import argparse


def convert_features_to_matrix(features_list, feature_names):
    """
    Convierte una lista de diccionarios de características a una matriz numpy.
    
    Args:
        features_list: Lista de diccionarios de características.
        feature_names: Lista de nombres de características.
        
    Returns:
        Matriz numpy.
    """
    if not features_list:
        return np.array([])
    
    n_samples = len(features_list)
    n_features = len(feature_names)
    X = np.zeros((n_samples, n_features))
    
    for i, features in enumerate(features_list):
        for j, feature_name in enumerate(feature_names):
            X[i, j] = features.get(feature_name, 0)
    
    return X


def predict_code(code: str, model, feature_extractor, feature_names, threshold: float = 0.7):
    """
    Predice si el código es seguro o vulnerable.
    
    Args:
        code: Código a analizar.
        model: Modelo entrenado.
        feature_extractor: Extractor de características.
        feature_names: Nombres de características.
        threshold: Umbral de probabilidad para clasificar como vulnerable.
        
    Returns:
        Diccionario con predicción y probabilidad.
    """
    # Extraer características
    code_features = feature_extractor.transform([code])
    X = convert_features_to_matrix(code_features, feature_names)
    
    # Realizar predicción
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    # Determinar clase basado en umbral
    is_vulnerable = probability[1] >= threshold
    
    result = {
        'prediction': int(prediction),
        'is_vulnerable': is_vulnerable,
        'probability_secure': float(probability[0]),
        'probability_vulnerable': float(probability[1]),
        'confidence': float(max(probability)),
        'label': 'VULNERABLE' if is_vulnerable else 'SEGURO'
    }
    
    return result


def load_model_and_vectorizer(model_path='models/security_classifier.joblib',
                               vectorizer_path='models/vectorizer.joblib',
                               feature_names_path='models/feature_names.joblib'):
    """
    Carga el modelo, vectorizador y nombres de características.
    
    Args:
        model_path: Ruta del modelo.
        vectorizer_path: Ruta del vectorizador.
        feature_names_path: Ruta de los nombres de características.
        
    Returns:
        Tuple con (modelo, extractor de características, nombres de características).
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}")
    
    model = joblib.load(model_path)
    
    feature_extractor = FeatureExtractor()
    feature_extractor.load_vectorizer(vectorizer_path)
    
    feature_names = joblib.load(feature_names_path)
    
    return model, feature_extractor, feature_names


def main():
    parser = argparse.ArgumentParser(description='Predice si un código es seguro o vulnerable.')
    parser.add_argument('--code', type=str, help='Código a analizar (entre comillas)')
    parser.add_argument('--file', type=str, help='Archivo de código a analizar')
    parser.add_argument('--threshold', type=float, default=0.7, help='Umbral de probabilidad (default: 0.7)')
    parser.add_argument('--model', type=str, default='models/security_classifier.joblib', help='Ruta del modelo')
    parser.add_argument('--vectorizer', type=str, default='models/vectorizer.joblib', help='Ruta del vectorizador')
    
    args = parser.parse_args()
    
    # Obtener código
    if args.code:
        code = args.code
    elif args.file:
        if not os.path.exists(args.file):
            print(f"ERROR: No se encontró el archivo {args.file}")
            return
        with open(args.file, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        print("ERROR: Debes proporcionar --code o --file")
        parser.print_help()
        return
    
    # Cargar modelo
    try:
        print("Cargando modelo y vectorizador...")
        model, feature_extractor, feature_names = load_model_and_vectorizer(
            args.model, args.vectorizer, 'models/feature_names.joblib'
        )
        print("Modelo cargado exitosamente")
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Ejecuta primero: python scripts/train.py")
        return
    
    # Realizar predicción
    print("\nAnalizando código...")
    result = predict_code(code, model, feature_extractor, feature_names, args.threshold)
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADO DE LA PREDICCIÓN")
    print("=" * 60)
    print(f"\nClasificación: {result['label']}")
    print(f"Probabilidad de código SEGURO:     {result['probability_secure']:.4f} ({result['probability_secure']*100:.2f}%)")
    print(f"Probabilidad de código VULNERABLE: {result['probability_vulnerable']:.4f} ({result['probability_vulnerable']*100:.2f}%)")
    print(f"Confianza: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
    print(f"\nUmbral utilizado: {args.threshold}")
    
    if result['is_vulnerable']:
        print("\n⚠️  ALERTA: El código fue clasificado como VULNERABLE")
        print("   Se recomienda revisar el código antes de desplegar.")
    else:
        print("\n✓ El código fue clasificado como SEGURO")
    
    print("=" * 60)
    
    # Código de salida para integración CI/CD
    # 0 = seguro, 1 = vulnerable
    sys.exit(1 if result['is_vulnerable'] else 0)


if __name__ == '__main__':
    main()
