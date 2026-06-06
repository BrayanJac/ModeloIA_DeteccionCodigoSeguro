"""
Módulo para cargar y preprocesar el dataset.
"""

import json
from typing import List, Dict, Any, Tuple
import random


def load_clean_dataset(file_path: str) -> List[Dict[str, Any]]:
    """
    Carga el dataset limpio en formato JSONL.
    
    Args:
        file_path: Ruta al archivo JSONL del dataset limpio.
        
    Returns:
        Lista de registros del dataset.
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def prepare_training_data(data: List[Dict[str, Any]]) -> Tuple[List[str], List[int]]:
    """
    Prepara los datos para entrenamiento.
    
    Cada registro del dataset tiene:
    - chosen: código seguro (label = 0)
    - rejected: código vulnerable (label = 1)
    
    Args:
        data: Lista de registros del dataset.
        
    Returns:
        Tuple con (lista de código, lista de labels).
    """
    code_samples = []
    labels = []
    
    for record in data:
        chosen = record.get('chosen', '')
        rejected = record.get('rejected', '')
        
        # Código seguro
        if chosen:
            code_samples.append(chosen)
            labels.append(0) 
        
        # Código vulnerable
        if rejected:
            code_samples.append(rejected)
            labels.append(1)  
    
    return code_samples, labels


def shuffle_data(code_samples: List[str], labels: List[int], random_seed: int = 42) -> Tuple[List[str], List[int]]:
    """
    Mezcla los datos de manera reproducible.
    
    Args:
        code_samples: Lista de muestras de código.
        labels: Lista de labels.
        random_seed: Semilla aleatoria para reproducibilidad.
        
    Returns:
        Tuple con (code_samples mezclados, labels mezclados).
    """
    combined = list(zip(code_samples, labels))
    random.seed(random_seed)
    random.shuffle(combined)
    code_samples_shuffled, labels_shuffled = zip(*combined)
    return list(code_samples_shuffled), list(labels_shuffled)


def split_train_test(code_samples: List[str], labels: List[int], test_size: float = 0.2, random_seed: int = 42) -> Tuple[List[str], List[str], List[int], List[int]]:
    """
    Divide los datos en conjuntos de entrenamiento y prueba.
    
    Args:
        code_samples: Lista de muestras de código.
        labels: Lista de labels.
        test_size: Proporción de datos para prueba (0.0 a 1.0).
        random_seed: Semilla aleatoria para reproducibilidad.
        
    Returns:
        Tuple con (X_train, X_test, y_train, y_test).
    """
    combined = list(zip(code_samples, labels))
    random.seed(random_seed)
    random.shuffle(combined)
    
    split_idx = int(len(combined) * (1 - test_size))
    train_data = combined[:split_idx]
    test_data = combined[split_idx:]
    
    X_train, y_train = zip(*train_data)
    X_test, y_test = zip(*test_data)
    
    return list(X_train), list(X_test), list(y_train), list(y_test)
