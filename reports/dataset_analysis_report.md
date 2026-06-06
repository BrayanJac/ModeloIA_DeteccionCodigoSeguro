# Reporte de Análisis del Dataset

## Estadísticas Generales

- **Total de registros**: 4656
- **Registros nulos**: 0
- **Registros vacíos**: 0
- **Registros duplicados**: 2

## Presencia de Campos Requeridos

- **lang**: 4656 (100.00%)
- **vulnerability**: 4656 (100.00%)
- **chosen**: 4656 (100.00%)
- **rejected**: 4656 (100.00%)

## Distribución de Lenguajes (Top 10)

- **c++**: 424 (9.11%)
- **python**: 424 (9.11%)
- **java**: 424 (9.11%)
- **javascript**: 424 (9.11%)
- **c#**: 423 (9.09%)
- **php**: 423 (9.09%)
- **ruby**: 423 (9.09%)
- **swift**: 423 (9.09%)
- **go**: 423 (9.09%)
- **kotlin**: 423 (9.09%)

## Distribución de Vulnerabilidades (Top 10)

- **Cross-Site Scripting (XSS) vulnerabilities in JavaScript can allow attackers to inject malicious scripts into web pages viewed by other users.**: 12 (0.26%)
- **Buffer overflow vulnerability in C++ can occur when a programmer writes more data into a buffer than it can handle.**: 9 (0.19%)
- **Improper handling of user input can lead to SQL Injection vulnerabilities.**: 9 (0.19%)
- **Insecure deserialization of objects can lead to remote code execution.**: 9 (0.19%)
- **The use of uninitialized variables in Fortran can lead to unexpected results or crashes.**: 7 (0.15%)
- **Kotlin's null safety feature can lead to NullPointerException if not properly handled.**: 7 (0.15%)
- **Insecure use of eval() function can lead to code injection attacks.**: 6 (0.13%)
- **Improper validation and sanitization of user input can lead to SQL Injection vulnerabilities.**: 6 (0.13%)
- **The use of unsanitized user input in SQL queries can lead to SQL injection attacks.**: 5 (0.11%)
- **The use of `strcpy` function without checking the size of the source string can lead to buffer overflow.**: 5 (0.11%)

## Métricas de Código

- **Longitud promedio (chosen)**: 534.11 caracteres
- **Longitud promedio (rejected)**: 387.27 caracteres
- **Tokens promedio (chosen)**: 131.59
- **Tokens promedio (rejected)**: 96.66

## Calidad de Datos

- **Registros con caracteres no imprimibles (chosen)**: 236
- **Registros con caracteres no imprimibles (rejected)**: 62
- **Registros con caracteres extraños (chosen)**: 233
- **Registros con caracteres extraños (rejected)**: 62

## Balance de Clases

- **Muestras seguras (chosen)**: 4656
- **Muestras vulnerables (rejected)**: 4656
- **Ratio vulnerable/seguro**: 1.00

## Conclusión

El dataset contiene 4656 registros con un balance perfecto entre código seguro y vulnerable.
