import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from feature_engineering.feature_extractor import FeatureExtractor
import joblib
import numpy as np
import argparse
from typing import List, Dict, Any
import json


def convert_features_to_matrix(features_list, feature_names):
    """Convierte una lista de diccionarios de características a una matriz numpy."""
    if not features_list:
        return np.array([])
    
    n_samples = len(features_list)
    n_features = len(feature_names)
    X = np.zeros((n_samples, n_features))
    
    for i, features in enumerate(features_list):
        for j, feature_name in enumerate(feature_names):
            X[i, j] = features.get(feature_name, 0)
    
    return X


def predict_code(code: str, model, feature_extractor, feature_names, threshold: float = 0.75) -> Dict[str, Any]:
    """Predice si el código es seguro o vulnerable."""
    code_features = feature_extractor.transform([code])
    X = convert_features_to_matrix(code_features, feature_names)
    
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    
    is_vulnerable = probability[1] >= threshold
    
    return {
        'prediction': int(prediction),
        'is_vulnerable': is_vulnerable,
        'probability_secure': float(probability[0]),
        'probability_vulnerable': float(probability[1]),
        'confidence': float(max(probability)),
    }


def analyze_file(file_path: str, model, feature_extractor, feature_names, threshold: float) -> Dict[str, Any]:
    """Analiza un archivo de código."""
    if not os.path.exists(file_path):
        return {
            'file': file_path,
            'error': 'File not found',
            'analyzed': False
        }
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if not code.strip():
            return {
                'file': file_path,
                'error': 'Empty file',
                'analyzed': False
            }
        
        result = predict_code(code, model, feature_extractor, feature_names, threshold)
        result['file'] = file_path
        result['analyzed'] = True
        
        return result
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e),
            'analyzed': False
        }


def main():
    parser = argparse.ArgumentParser(description='Analiza archivos modificados en un PR')
    parser.add_argument('--files', type=str, required=True, help='Archivos modificados (separados por espacio)')
    parser.add_argument('--pr-number', type=str, required=True, help='Número del PR')
    parser.add_argument('--repo-owner', type=str, required=True, help='Propietario del repo')
    parser.add_argument('--repo-name', type=str, required=True, help='Nombre del repo')
    parser.add_argument('--threshold', type=float, default=0.75, help='Umbral de vulnerabilidad')
    parser.add_argument('--output-json', type=str, default='reports/analysis_result.json', help='Archivo JSON de salida')
    
    args = parser.parse_args()
    
    # Cargar modelo
    model_path = 'models/security_classifier.joblib'
    vectorizer_path = 'models/vectorizer.joblib'
    feature_names_path = 'models/feature_names.joblib'
    
    if not os.path.exists(model_path):
        print(f"ERROR: Modelo no encontrado en {model_path}")
        sys.exit(1)
    
    print("Cargando modelo y vectorizador...")
    model = joblib.load(model_path)
    feature_extractor = FeatureExtractor()
    feature_extractor.load_vectorizer(vectorizer_path)
    feature_names = joblib.load(feature_names_path)
    print("Modelo cargado exitosamente")
    
    # Obtener archivos modificados
    files_list = args.files.split()
    print(f"\nAnalizando {len(files_list)} archivos modificados...")
    
    # Analizar cada archivo
    results = []
    vulnerable_files = []
    
    for file_path in files_list:
        print(f"  Analizando: {file_path}")
        result = analyze_file(file_path, model, feature_extractor, feature_names, args.threshold)
        results.append(result)
        
        if result['analyzed'] and result['is_vulnerable']:
            vulnerable_files.append(result)
    
    # Generar reporte
    os.makedirs('reports', exist_ok=True)
    
    # Guardar resultado JSON
    analysis_result = {
        'pr_number': args.pr_number,
        'repo': f"{args.repo_owner}/{args.repo_name}",
        'total_files': len(results),
        'vulnerable_files': len(vulnerable_files),
        'is_safe': len(vulnerable_files) == 0,
        'results': results
    }
    
    with open(args.output_json, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, indent=2)
    
    comment_lines = [
        "## 🔒 Análisis de Seguridad del Pull Request",
        "",
        f"**PR #{args.pr_number}** - {args.repo_owner}/{args.repo_name}",
        "",
        f"**Archivos analizados:** {len(results)}",
        f"**Archivos vulnerables:** {len(vulnerable_files)}",
        "",
    ]
    
    if vulnerable_files:
        comment_lines.extend([
            "### ⚠️ ALERTA: Se detectó código vulnerable",
            "",
            "Los siguientes archivos fueron clasificados como vulnerables:",
            "",
        ])
        
        for vf in vulnerable_files:
            comment_lines.extend([
                f"#### 📁 `{vf['file']}`",
                f"- **Probabilidad de vulnerabilidad:** {vf['probability_vulnerable']:.2%}",
                f"- **Probabilidad de seguridad:** {vf['probability_secure']:.2%}",
                f"- **Confianza:** {vf['confidence']:.2%}",
                "",
            ])
        
        comment_lines.extend([
            "### 📋 Recomendaciones",
            "",
            "- Revisa los archivos marcados como vulnerables",
            "- Considera usar funciones de sanitización apropiadas",
            "- Valida y sanitiza todas las entradas de usuario",
            "- Usa consultas preparadas para bases de datos",
            "- Evita el uso de funciones peligrosas como `eval()` o `exec()`",
            "",
            "❌ **El PR no puede ser mergeado hasta que se corrijan las vulnerabilidades.**",
        ])
        
        # Guardar comentario
        comment = "\n".join(comment_lines)
        with open('reports/pr_comment.md', 'w', encoding='utf-8') as f:
            f.write(comment)
        
        print("\n❌ Se detectaron vulnerabilidades. El workflow fallará.")
        sys.exit(1)
    else:
        comment_lines.extend([
            "### ✅ Resultado: No se detectaron vulnerabilidades",
            "",
            "Todos los archivos analizados pasaron el análisis de seguridad.",
            "",
            "El código parece seguir buenas prácticas de seguridad.",
            "",
            "✅ **El PR puede ser mergeado.**",
        ])
        
        # Guardar comentario
        comment = "\n".join(comment_lines)
        with open('reports/pr_comment.md', 'w', encoding='utf-8') as f:
            f.write(comment)
        
        print("\n✅ No se detectaron vulnerabilidades. El workflow continuará.")
        sys.exit(0)


if __name__ == '__main__':
    main()
