# Evidencias del pipeline CI/CD seguro

Fecha de verificacion: 2026-06-17

## 1. PR vulnerable rechazado automaticamente

- PR de evidencia: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/pull/14
- Workflow: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/actions/runs/27707771204
- Resultado esperado: `Security Review with AI` falla y bloquea el merge.
- Evidencia observada:
  - Archivo analizado: `app/vulnerable-evidence-demo.js`
  - Probabilidad de vulnerabilidad: `90.67%`
  - Etiqueta aplicada: `fixing-required`
  - Comentario automatico en el PR con probabilidad, confianza y recomendaciones.
  - Job `Merge to Test Branch` queda `skipped`.

Capturas recomendadas:

- PR #14 con etiqueta `fixing-required`.
- Comentario automatico del analisis de seguridad.
- Workflow run #27707771204 con `Analyze Code with ML Model` en failure.
- Telegram con evento de inicio de analisis y rechazo por vulnerabilidad.

## 2. PR seguro hasta test/main

- PR de verificacion: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/pull/11
- Security Review exitoso: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/actions/runs/27690373032
- Testing exitoso: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/actions/runs/27690411055

Evidencia observada:

- `Analyze Code with ML Model`: success.
- `Merge to Test Branch`: success.
- `Unit Tests`: success.
- `Integration Tests`: success.
- `Notify Test Result`: success.
- `Merge to Main Branch`: success.

Capturas recomendadas:

- PR #11 cerrado/mergeado.
- Workflow de seguridad exitoso.
- Workflow de pruebas exitoso.
- Telegram con resultado seguro, merge a test, resultado de pruebas y merge a main.

## 3. Modelo y metricas

- Reporte local: `reports/evaluation_report.md`
- Accuracy en test: `0.8268`
- Accuracy en validacion cruzada 5-fold: `0.8273 +/- 0.0143`
- Feature obligatoria agregada: `ast_depth`
- Artefactos actualizados:
  - `models/security_classifier.joblib`
  - `models/vectorizer.joblib`
  - `models/feature_names.joblib`

Capturas recomendadas:

- `reports/evaluation_report.md`.
- README con metricas actuales.
- Validacion local o log de entrenamiento donde aparezca matriz `(6976, 3054)` y `ast_depth`.

## 4. Telegram

Los workflows ya tienen pasos de notificacion para:

- Inicio de revision de seguridad.
- Resultado seguro/vulnerable con probabilidad.
- Rechazo por vulnerabilidad.
- Merge a test.
- Resultado de pruebas.
- Merge a main.
- Despliegue exitoso/fallido.

Evidencia observada en GitHub Actions:

- En PR #14, `Send Telegram notification - Analysis Start`: success.
- En PR #14, `Handle vulnerable code`: ejecutado y finaliza el job con failure esperado.
- En run de testing #27690411055, `Notify Test Result`: success.

Capturas recomendadas:

- Conversacion del bot de Telegram con mensajes del PR #14.
- Mensajes del PR seguro #11 hasta pruebas.
- Mensaje de despliegue fallido si se mantiene la falla de Vercel.

## 5. Branch protection

Archivo guia versionado: `.github/branch-protection.md`

Estado via API al 2026-06-17:

- `test`: no aparece protegido por API (`404`).
- `main`: no aparece protegido por API (`404`).

Pendiente para cumplir completamente:

- Activar branch protection/rulesets en GitHub para `test` y `main`.
- Requerir checks:
  - `Analyze Code with ML Model` para `test`.
  - `Unit Tests` e `Integration Tests` para `main`.
- Bloquear force pushes y eliminacion de ramas.
- Permitir bypass solo al actor/token del pipeline si se mantiene merge automatico.

Capturas recomendadas:

- Settings -> Rules -> Rulesets o Settings -> Branches mostrando reglas activas.
- Checks requeridos visibles en la regla.

## 6. Despliegue Vercel

Deployments observados:

- Production success previo: https://modelo-ia-deteccion-codigo-seguro-lwks9s8zj.vercel.app/
- Deployment status: success en GitHub Deployment `5083595121`.
- Corrida reciente de production deployment: https://github.com/BrayanJac/ModeloIA_DeteccionCodigoSeguro/actions/runs/27690491096
- Estado reciente: failure en paso `Deploy to Vercel`.

Pendiente para cumplir completamente:

- El URL de Vercel respondio `401` por proteccion/autenticacion de Vercel.
- Se debe desactivar Deployment Protection/SSO en Vercel o publicar un deployment accesible sin login.
- Revisar logs de Vercel desde la cuenta propietaria con:

```bash
npx vercel inspect dpl_G1db6RDZmF7CSeXDt6r21QGq3CwA --logs
```

Capturas recomendadas:

- URL de produccion respondiendo publicamente `Backend funcionando`.
- Run de deploy exitoso.
- Configuracion de Vercel sin proteccion de acceso.
