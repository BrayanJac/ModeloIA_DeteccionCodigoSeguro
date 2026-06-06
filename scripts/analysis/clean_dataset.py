#!/usr/bin/env python3
"""
Script para limpieza del dataset de programación segura.
FASE 0: Limpieza del dataset original.
"""

import json
import re
from typing import Dict, List, Any, Tuple


def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """Carga el dataset JSONL."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return data


def has_non_printable(text: str) -> bool:
    """Verifica si el texto tiene caracteres no imprimibles."""
    return any(ord(char) < 32 or ord(char) > 126 for char in text if char not in '\n\r\t')


def has_strange_chars(text: str) -> bool:
    """Verifica si el texto tiene caracteres fuera del rango ASCII básico."""
    return any(ord(char) > 127 for char in text)


def clean_text(text: str) -> str:
    """Limpia el texto eliminando caracteres no imprimibles y extraños."""
    # Eliminar caracteres no imprimibles excepto \n, \r, \t
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    # Eliminar caracteres fuera del rango ASCII (caracteres extraños como chino, etc.)
    text = ''.join(char for char in text if ord(char) <= 127)
    # Normalizar espacios múltiples
    text = re.sub(r' +', ' ', text)
    # Normalizar saltos de línea múltiples
    text = re.sub(r'\n+', '\n', text)
    # Normalizar tabuladores múltiples
    text = re.sub(r'\t+', '\t', text)
    # Eliminar espacios al inicio y final de líneas
    text = '\n'.join(line.strip() for line in text.split('\n'))
    return text.strip()


def validate_record(record: Dict[str, Any]) -> bool:
    """Valida que el registro tenga todos los campos requeridos."""
    required_fields = ['lang', 'vulnerability', 'chosen', 'rejected']
    return all(field in record and record[field] for field in required_fields)


def clean_dataset(data: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """Limpia el dataset y retorna el dataset limpio y estadísticas."""
    
    original_count = len(data)
    cleaned_data = []
    
    # Estadísticas de limpieza
    stats = {
        'removed_null': 0,
        'removed_empty': 0,
        'removed_invalid_fields': 0,
        'removed_non_printable': 0,
        'cleaned_text': 0,
        'removed_duplicates': 0
    }
    
    # Eliminar registros nulos o vacíos
    data = [record for record in data if record]
    stats['removed_null'] = original_count - len(data)
    
    data = [record for record in data if any(record.values())]
    stats['removed_empty'] = original_count - len(data) - stats['removed_null']
    
    # Eliminar registros con campos inválidos
    valid_data = []
    for record in data:
        if validate_record(record):
            valid_data.append(record)
        else:
            stats['removed_invalid_fields'] += 1
    data = valid_data
    
    # Limpiar texto y eliminar registros con caracteres no imprimibles
    cleaned_data = []
    for record in data:
        chosen = str(record.get('chosen', ''))
        rejected = str(record.get('rejected', ''))
        
        # Verificar caracteres no imprimibles
        if has_non_printable(chosen) or has_non_printable(rejected):
            stats['removed_non_printable'] += 1
            continue
        
        # Limpiar texto
        original_chosen = chosen
        original_rejected = rejected
        
        chosen_clean = clean_text(chosen)
        rejected_clean = clean_text(rejected)
        
        if chosen != chosen_clean or rejected != rejected_clean:
            stats['cleaned_text'] += 1
        
        # Verificar que después de la limpieza no esté vacío
        if not chosen_clean or not rejected_clean:
            stats['removed_empty'] += 1
            continue
        
        record['chosen'] = chosen_clean
        record['rejected'] = rejected_clean
        cleaned_data.append(record)
    
    # Eliminar duplicados
    seen = set()
    unique_data = []
    for record in cleaned_data:
        record_str = json.dumps(record, sort_keys=True)
        if record_str not in seen:
            seen.add(record_str)
            unique_data.append(record)
        else:
            stats['removed_duplicates'] += 1
    
    stats['final_count'] = len(unique_data)
    
    return unique_data, stats


def save_dataset(data: List[Dict[str, Any]], output_path: str):
    """Guarda el dataset limpio en formato JSONL."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in data:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    print(f"Dataset limpio guardado en: {output_path}")


def generate_cleaning_report(stats: Dict[str, int], original_count: int, output_path: str):
    """Genera un reporte de limpieza en formato markdown."""
    
    report = f"""# Reporte de Limpieza del Dataset

## Resumen

- **Registros originales**: {original_count}
- **Registros finales**: {stats['final_count']}
- **Registros eliminados**: {original_count - stats['final_count']}
- **Tasa de retención**: {(stats['final_count'] / original_count * 100):.2f}%

## Detalle de Eliminaciones

- **Registros nulos**: {stats['removed_null']}
- **Registros vacíos**: {stats['removed_empty']}
- **Registros con campos inválidos**: {stats['removed_invalid_fields']}
- **Registros con caracteres no imprimibles**: {stats['removed_non_printable']}
- **Registros duplicados**: {stats['removed_duplicates']}
- **Registros con texto limpiado**: {stats['cleaned_text']}

## Acciones de Limpieza Realizadas

1. **Eliminación de registros nulos**: Se removieron registros sin contenido.
2. **Eliminación de registros vacíos**: Se removieron registros sin valores en ningún campo.
3. **Validación de campos**: Se verificó que todos los registros tengan los campos requeridos (lang, vulnerability, chosen, rejected).
4. **Eliminación de caracteres no imprimibles**: Se removieron registros con caracteres de control (excepto \n, \r, \t).
5. **Limpieza de texto**: Se normalizaron espacios, saltos de línea y tabuladores múltiples.
6. **Eliminación de caracteres extraños**: Se removieron caracteres fuera del rango ASCII (caracteres chinos, símbolos raros, etc.).
7. **Eliminación de duplicados**: Se removieron registros duplicados basados en contenido idéntico.

## Conclusión

El dataset limpio contiene {stats['final_count']} registros de alta calidad, listos para el entrenamiento del modelo.
Todos los registros tienen los campos requeridos y el texto ha sido normalizado.
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Reporte de limpieza generado en: {output_path}")


def main():
    input_path = 'datasets/secure_programming_dpo.json'
    output_path = 'datasets/secure_programming_dpo_clean.json'
    report_path = 'reports/data_quality_report.md'
    
    print("Cargando dataset original...")
    data = load_dataset(input_path)
    original_count = len(data)
    print(f"Registros originales: {original_count}")
    
    print("\nLimpiando dataset...")
    cleaned_data, stats = clean_dataset(data)
    
    print("\n=== ESTADÍSTICAS DE LIMPIEZA ===")
    print(f"Registros originales: {original_count}")
    print(f"Registros finales: {stats['final_count']}")
    print(f"Registros eliminados: {original_count - stats['final_count']}")
    print(f"Tasa de retención: {(stats['final_count'] / original_count * 100):.2f}%")
    print("\nDetalle:")
    print(f"  Registros nulos: {stats['removed_null']}")
    print(f"  Registros vacíos: {stats['removed_empty']}")
    print(f"  Campos inválidos: {stats['removed_invalid_fields']}")
    print(f"  Caracteres no imprimibles: {stats['removed_non_printable']}")
    print(f"  Duplicados: {stats['removed_duplicates']}")
    print(f"  Texto limpiado: {stats['cleaned_text']}")
    
    print("\nGuardando dataset limpio...")
    save_dataset(cleaned_data, output_path)
    
    print("\nGenerando reporte de limpieza...")
    generate_cleaning_report(stats, original_count, report_path)
    
    print("\nLimpieza completada.")


if __name__ == '__main__':
    main()
