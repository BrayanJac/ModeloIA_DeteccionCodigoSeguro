import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer


# Funciones peligrosas a detectar
DANGEROUS_FUNCTIONS = [
    'eval',
    'exec',
    'os.system',
    'subprocess',
    'Runtime.exec',
    'cursor.execute',
    'execute(',
    'system(',
    'popen(',
    'shell=True',
    'input(',
    'raw_input(',
    'open(',
    'file(',
    'pickle.loads',
    'marshal.loads',
    'yaml.load',
    'json.loads',
    'compile(',
    '__import__',
    'getattr',
    'setattr',
    'delattr',
    'globals(',
    'locals(',
    'vars(',
    'dir(',
]

# Funciones de sanitización a detectar
SANITIZATION_FUNCTIONS = [
    'prepareStatement',
    'bindParam',
    'escape',
    'sanitize',
    'htmlspecialchars',
    'real_escape_string',
    'quote(',
    'parameterized',
    'strip_tags',
    'filter_var',
    'ctype_digit',
    'is_numeric',
    'intval',
    'floatval',
    'strval',
]


def count_lines(code: str) -> int:
    """Cuenta el número de líneas de código."""
    return len(code.split('\n'))


def count_tokens(code: str) -> int:
    """Cuenta el número de tokens (palabras y símbolos)."""
    return len(re.findall(r'\w+|[^\w\s]', code))


def count_function_calls(code: str) -> int:
    """Cuenta el número de llamadas a funciones."""
    return len(re.findall(r'\w+\s*\(', code))


def count_dangerous_functions(code: str) -> Dict[str, int]:
    """Cuenta las ocurrencias de funciones peligrosas."""
    counts = {}
    code_lower = code.lower()
    
    for func in DANGEROUS_FUNCTIONS:
        pattern = re.escape(func.lower())
        counts[f'dangerous_{func.replace(".", "_").replace("(", "")}'] = len(re.findall(pattern, code_lower))
    
    return counts


def count_sanitization_functions(code: str) -> Dict[str, int]:
    """Cuenta las ocurrencias de funciones de sanitización."""
    counts = {}
    code_lower = code.lower()
    
    for func in SANITIZATION_FUNCTIONS:
        pattern = re.escape(func.lower())
        counts[f'sanitize_{func.replace(".", "_").replace("(", "")}'] = len(re.findall(pattern, code_lower))
    
    return counts


def detect_raw_sql(code: str) -> int:
    """Detecta patrones de SQL raw (concatenación de strings en queries)."""
    patterns = [
        r'select\s+.*\s+from\s+.*where\s*=.*["\']',
        r'insert\s+into\s+.*values\s*\(',
        r'update\s+.*set\s+.*=.*["\']',
        r'delete\s+from\s+.*where',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def detect_hardcoded_credentials(code: str) -> int:
    """Detecta patrones de credenciales hardcodeadas."""
    patterns = [
        r'password\s*=\s*["\'][^"\']{4,}["\']',
        r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']',
        r'secret\s*=\s*["\'][^"\']{10,}["\']',
        r'token\s*=\s*["\'][^"\']{10,}["\']',
        r'passwd\s*=\s*["\'][^"\']{4,}["\']',
        r'pwd\s*=\s*["\'][^"\']{4,}["\']',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def detect_xss_patterns(code: str) -> int:
    """Detecta patrones de Cross-Site Scripting (XSS)."""
    patterns = [
        r'innerHTML\s*=',
        r'outerHTML\s*=',
        r'document\.write\s*\(',
        r'document\.writeln\s*\(',
        r'eval\s*\(',
        r'innerHTML\s*\+\s*=',
        r'<script',
        r'onerror\s*=',
        r'onload\s*=',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def detect_path_traversal(code: str) -> int:
    """Detecta patrones de Path Traversal."""
    patterns = [
        r'\.\./',
        r'\.\.\\',
        r'%2e%2e%2f',
        r'%2e%2e%5c',
        r'\.\.%2f',
        r'\.\.%5c',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def detect_command_injection(code: str) -> int:
    """Detecta patrones de Command Injection."""
    patterns = [
        r';\s*(ls|cat|rm|mv|cp|chmod|chown)\s',
        r'\|\s*(ls|cat|rm|mv|cp|chmod|chown)\s',
        r'&&\s*(ls|cat|rm|mv|cp|chmod|chown)\s',
        r'\$\(',
        r'`[^`]*`',
        r'backticks',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def detect_insecure_deserialization(code: str) -> int:
    """Detecta patrones de deserialización insegura."""
    patterns = [
        r'pickle\.loads',
        r'marshal\.loads',
        r'yaml\.load',
        r'yaml\.unsafe_load',
        r'objectmapper\.readvalue',
        r'gson\.fromjson',
        r'json\.parse',
        r'xml\.parse',
    ]
    
    code_lower = code.lower()
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, code_lower))
    
    return count


def extract_code_metrics(code: str) -> Dict[str, Any]:
    """
    Extrae métricas básicas del código.
    
    Args:
        code: Código fuente a analizar.
        
    Returns:
        Diccionario con métricas del código.
    """
    return {
        'line_count': count_lines(code),
        'token_count': count_tokens(code),
        'function_call_count': count_function_calls(code),
        'code_length': len(code),
    }


def extract_security_features(code: str) -> Dict[str, Any]:
    """
    Extrae características relacionadas con seguridad.
    
    Args:
        code: Código fuente a analizar.
        
    Returns:
        Diccionario con características de seguridad.
    """
    dangerous_counts = count_dangerous_functions(code)
    sanitization_counts = count_sanitization_functions(code)
    raw_sql_count = detect_raw_sql(code)
    hardcoded_creds_count = detect_hardcoded_credentials(code)
    xss_count = detect_xss_patterns(code)
    path_traversal_count = detect_path_traversal(code)
    command_injection_count = detect_command_injection(code)
    insecure_deserialization_count = detect_insecure_deserialization(code)
    
    features = {
        **dangerous_counts,
        **sanitization_counts,
        'raw_sql_patterns': raw_sql_count,
        'hardcoded_credentials': hardcoded_creds_count,
        'xss_patterns': xss_count,
        'path_traversal_patterns': path_traversal_count,
        'command_injection_patterns': command_injection_count,
        'insecure_deserialization_patterns': insecure_deserialization_count,
    }
    
    # Calcular ratio de sanitización vs funciones peligrosas
    total_dangerous = sum(dangerous_counts.values())
    total_sanitization = sum(sanitization_counts.values())
    
    if total_dangerous > 0:
        features['sanitization_ratio'] = total_sanitization / total_dangerous
    else:
        features['sanitization_ratio'] = 0.0
    
    return features


def extract_all_features(code: str) -> Dict[str, Any]:
    """
    Extrae todas las características del código.
    
    Args:
        code: Código fuente a analizar.
        
    Returns:
        Diccionario con todas las características.
    """
    code_metrics = extract_code_metrics(code)
    security_features = extract_security_features(code)
    
    return {
        **code_metrics,
        **security_features,
    }


class FeatureExtractor:
    """
    Clase para extracción de características usando TF-IDF y características manuales.
    """
    
    def __init__(self, max_features: int = 5000, ngram_range: tuple = (1, 2)):
        """
        Inicializa el extractor de características.
        
        Args:
            max_features: Número máximo de características TF-IDF.
            ngram_range: Rango de n-grams para TF-IDF.
        """
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            lowercase=True,
            stop_words=None,
        )
        self.fitted = False
    
    def fit(self, code_samples: List[str]):
        """
        Ajusta el vectorizador TF-IDF a las muestras de código.
        
        Args:
            code_samples: Lista de muestras de código.
        """
        self.tfidf_vectorizer.fit(code_samples)
        self.fitted = True
    
    def transform(self, code_samples: List[str]) -> List[Dict[str, Any]]:
        """
        Transforma las muestras de código en características.
        
        Args:
            code_samples: Lista de muestras de código.
            
        Returns:
            Lista de diccionarios con características.
        """
        if not self.fitted:
            raise ValueError("El vectorizador no ha sido ajustado. Llama a fit() primero.")
        
        # Obtener características TF-IDF
        tfidf_features = self.tfidf_vectorizer.transform(code_samples).toarray()
        feature_names = self.tfidf_vectorizer.get_feature_names_out()
        
        # Extraer características manuales
        all_features = []
        for i, code in enumerate(code_samples):
            manual_features = extract_all_features(code)
            
            # Combinar características
            feature_dict = manual_features.copy()
            
            # Agregar características TF-IDF
            for j, feature_name in enumerate(feature_names):
                feature_dict[f'tfidf_{feature_name}'] = tfidf_features[i][j]
            
            all_features.append(feature_dict)
        
        return all_features
    
    def fit_transform(self, code_samples: List[str]) -> List[Dict[str, Any]]:
        """
        Ajusta y transforma las muestras de código.
        
        Args:
            code_samples: Lista de muestras de código.
            
        Returns:
            Lista de diccionarios con características.
        """
        self.fit(code_samples)
        return self.transform(code_samples)
    
    def get_feature_names(self) -> List[str]:
        """
        Obtiene los nombres de las características TF-IDF.
        
        Returns:
            Lista de nombres de características.
        """
        if not self.fitted:
            raise ValueError("El vectorizador no ha sido ajustado.")
        return self.tfidf_vectorizer.get_feature_names_out().tolist()
    
    def save_vectorizer(self, path: str):
        """
        Guarda el vectorizador en disco.
        
        Args:
            path: Ruta donde guardar el vectorizador.
        """
        import joblib
        joblib.dump(self.tfidf_vectorizer, path)
    
    def load_vectorizer(self, path: str):
        """
        Carga el vectorizador desde disco.
        
        Args:
            path: Ruta del vectorizador a cargar.
        """
        import joblib
        self.tfidf_vectorizer = joblib.load(path)
        self.fitted = True
