#!/usr/bin/env python3
"""
Script para análisis completo del dataset de programación segura.
FASE 0: Auditoría del dataset original.
"""

import json
from collections import Counter
from typing import Dict, List, Any
import re


def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """Carga el dataset JSONL."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def analyze_dataset(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analiza el dataset y genera estadísticas."""
    
    total_records = len(data)
    
    # Verificar registros nulos o vacíos
    null_records = sum(1 for record in data if not record)
    empty_records = sum(1 for record in data if record and not any(record.values()))
    
    # Verificar campos requeridos
    required_fields = ['lang', 'vulnerability', 'chosen', 'rejected']
    field_presence = {field: sum(1 for record in data if field in record) for field in required_fields}
    
    # Distribución de lenguajes
    languages = Counter(record.get('lang', 'unknown') for record in data)
    
    # Distribución de vulnerabilidades
    vulnerabilities = Counter(record.get('vulnerability', 'unknown') for record in data)
    
    # Longitud promedio del código
    avg_chosen_length = sum(len(str(record.get('chosen', ''))) for record in data) / total_records if total_records > 0 else 0
    avg_rejected_length = sum(len(str(record.get('rejected', ''))) for record in data) / total_records if total_records > 0 else 0
    
    # Balance de clases (cada registro tiene chosen y rejected)
    total_secure = total_records  # chosen es seguro
    total_vulnerable = total_records  # rejected es vulnerable
    
    # Verificar duplicados
    seen = set()
    duplicates = 0
    for record in data:
        record_str = json.dumps(record, sort_keys=True)
        if record_str in seen:
            duplicates += 1
        seen.add(record_str)
    
    # Verificar caracteres no imprimibles
    def has_non_printable(text: str) -> bool:
        return any(ord(char) < 32 or ord(char) > 126 for char in text if char not in '\n\r\t')
    
    non_printable_chosen = sum(1 for record in data if has_non_printable(str(record.get('chosen', ''))))
    non_printable_rejected = sum(1 for record in data if has_non_printable(str(record.get('rejected', ''))))
    
    # Detectar caracteres extraños (ej. caracteres chinos, símbolos raros)
    def has_strange_chars(text: str) -> bool:
        # Caracteres fuera del rango ASCII imprimible básico
        return any(ord(char) > 127 for char in text)
    
    strange_chars_chosen = sum(1 for record in data if has_strange_chars(str(record.get('chosen', ''))))
    strange_chars_rejected = sum(1 for record in data if has_strange_chars(str(record.get('rejected', ''))))
    
    # Análisis de tokens
    def count_tokens(text: str) -> int:
        # Contador simple de tokens (palabras y símbolos)
        return len(re.findall(r'\w+|[^\w\s]', text))
    
    avg_tokens_chosen = sum(count_tokens(str(record.get('chosen', ''))) for record in data) / total_records if total_records > 0 else 0
    avg_tokens_rejected = sum(count_tokens(str(record.get('rejected', ''))) for record in data) / total_records if total_records > 0 else 0
    
    return {
        'total_records': total_records,
        'null_records': null_records,
        'empty_records': empty_records,
        'duplicates': duplicates,
        'field_presence': field_presence,
        'languages': dict(languages.most_common(10)),
        'vulnerabilities': dict(vulnerabilities.most_common(10)),
        'avg_chosen_length': avg_chosen_length,
        'avg_rejected_length': avg_rejected_length,
        'total_secure_samples': total_secure,
        'total_vulnerable_samples': total_vulnerable,
        'non_printable_chosen': non_printable_chosen,
        'non_printable_rejected': non_printable_rejected,
        'strange_chars_chosen': strange_chars_chosen,
        'strange_chars_rejected': strange_chars_rejected,
        'avg_tokens_chosen': avg_tokens_chosen,
        'avg_tokens_rejected': avg_tokens_rejected,
        'class_balance': {
            'secure': total_secure,
            'vulnerable': total_vulnerable,
            'ratio': total_vulnerable / total_secure if total_secure > 0 else 0
        }
    }


def generate_report(stats: Dict[str, Any], output_path: str):
    """Genera un reporte markdown con las estadísticas."""
    
    report = f"""# Reporte de Análisis del Dataset

## Estadísticas Generales

- **Total de registros**: {stats['total_records']}
- **Registros nulos**: {stats['null_records']}
- **Registros vacíos**: {stats['empty_records']}
- **Registros duplicados**: {stats['duplicates']}

## Presencia de Campos Requeridos

"""
    for field, count in stats['field_presence'].items():
        percentage = (count / stats['total_records']) * 100
        report += f"- **{field}**: {count} ({percentage:.2f}%)\n"
    
    report += """
## Distribución de Lenguajes (Top 10)

"""
    for lang, count in stats['languages'].items():
        percentage = (count / stats['total_records']) * 100
        report += f"- **{lang}**: {count} ({percentage:.2f}%)\n"
    
    report += """
## Distribución de Vulnerabilidades (Top 10)

"""
    for vuln, count in stats['vulnerabilities'].items():
        percentage = (count / stats['total_records']) * 100
        report += f"- **{vuln}**: {count} ({percentage:.2f}%)\n"
    
    report += f"""
## Métricas de Código

- **Longitud promedio (chosen)**: {stats['avg_chosen_length']:.2f} caracteres
- **Longitud promedio (rejected)**: {stats['avg_rejected_length']:.2f} caracteres
- **Tokens promedio (chosen)**: {stats['avg_tokens_chosen']:.2f}
- **Tokens promedio (rejected)**: {stats['avg_tokens_rejected']:.2f}

## Calidad de Datos

- **Registros con caracteres no imprimibles (chosen)**: {stats['non_printable_chosen']}
- **Registros con caracteres no imprimibles (rejected)**: {stats['non_printable_rejected']}
- **Registros con caracteres extraños (chosen)**: {stats['strange_chars_chosen']}
- **Registros con caracteres extraños (rejected)**: {stats['strange_chars_rejected']}

## Balance de Clases

- **Muestras seguras (chosen)**: {stats['total_secure_samples']}
- **Muestras vulnerables (rejected)**: {stats['total_vulnerable_samples']}
- **Ratio vulnerable/seguro**: {stats['class_balance']['ratio']:.2f}

## Conclusión

El dataset contiene {stats['total_records']} registros con un balance perfecto entre código seguro y vulnerable.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Reporte generado en: {output_path}")


def main():
    dataset_path = 'datasets/secure_programming_dpo.json'
    report_path = 'reports/dataset_analysis_report.md'
    
    print("Cargando dataset...")
    data = load_dataset(dataset_path)
    
    print("Analizando dataset...")
    stats = analyze_dataset(data)
    
    print("\n=== ESTADÍSTICAS DEL DATASET ===")
    print(f"Total de registros: {stats['total_records']}")
    print(f"Registros nulos: {stats['null_records']}")
    print(f"Registros vacíos: {stats['empty_records']}")
    print(f"Registros duplicados: {stats['duplicates']}")
    print("\nPresencia de campos:")
    for field, count in stats['field_presence'].items():
        print(f"  {field}: {count}/{stats['total_records']}")
    print("\nLenguajes (top 10):")
    for lang, count in stats['languages'].items():
        print(f"  {lang}: {count}")
    print("\nVulnerabilidades (top 10):")
    for vuln, count in stats['vulnerabilities'].items():
        print(f"  {vuln}: {count}")
    print("\nLongitud promedio:")
    print(f"  chosen: {stats['avg_chosen_length']:.2f} caracteres")
    print(f"  rejected: {stats['avg_rejected_length']:.2f} caracteres")
    print("\nCalidad de datos:")
    print(f"  Caracteres no imprimibles (chosen): {stats['non_printable_chosen']}")
    print(f"  Caracteres no imprimibles (rejected): {stats['non_printable_rejected']}")
    print(f"  Caracteres extraños (chosen): {stats['strange_chars_chosen']}")
    print(f"  Caracteres extraños (rejected): {stats['strange_chars_rejected']}")
    print("\nBalance de clases:")
    print(f"  Seguras: {stats['total_secure_samples']}")
    print(f"  Vulnerables: {stats['total_vulnerable_samples']}")
    print(f"  Ratio: {stats['class_balance']['ratio']:.2f}")
    
    print("\nGenerando reporte...")
    generate_report(stats, report_path)
    
    print("\nAnálisis completado.")


if __name__ == '__main__':
    main()
