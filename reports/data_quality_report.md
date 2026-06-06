# Reporte de Limpieza del Dataset

## Resumen

- **Registros originales**: 4656
- **Registros finales**: 4360
- **Registros eliminados**: 296
- **Tasa de retención**: 93.64%

## Detalle de Eliminaciones

- **Registros nulos**: 0
- **Registros vacíos**: 0
- **Registros con campos inválidos**: 0
- **Registros con caracteres no imprimibles**: 294
- **Registros duplicados**: 2
- **Registros con texto limpiado**: 4316

## Acciones de Limpieza Realizadas

1. **Eliminación de registros nulos**: Se removieron registros sin contenido.
2. **Eliminación de registros vacíos**: Se removieron registros sin valores en ningún campo.
3. **Validación de campos**: Se verificó que todos los registros tengan los campos requeridos (lang, vulnerability, chosen, rejected).
4. **Eliminación de caracteres no imprimibles**: Se removieron registros con caracteres de control (excepto 
, , 	).
5. **Limpieza de texto**: Se normalizaron espacios, saltos de línea y tabuladores múltiples.
6. **Eliminación de caracteres extraños**: Se removieron caracteres fuera del rango ASCII (caracteres chinos, símbolos raros, etc.).
7. **Eliminación de duplicados**: Se removieron registros duplicados basados en contenido idéntico.

## Conclusión

El dataset limpio contiene 4360 registros de alta calidad, listos para el entrenamiento del modelo.
Todos los registros tienen los campos requeridos y el texto ha sido normalizado.
