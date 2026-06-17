# Branch protection rules

Estas reglas se configuran en GitHub, no desde archivos del repositorio.
Ruta: `Settings -> Rules -> Rulesets` o `Settings -> Branches -> Branch protection rules`.

## Objetivo

Evitar pushes directos de desarrolladores y permitir que el flujo avance solo mediante Pull Requests:

- `dev` -> rama de desarrollo.
- `test` -> staging/pruebas; solo debe recibir cambios aprobados desde PR `dev -> test`.
- `main` -> produccion; solo debe recibir cambios despues de pruebas exitosas.

## Reglas recomendadas

Crear reglas para `dev`, `test` y `main` si se quiere bloquear todo push directo humano.

Reglas base:

- Activar `Require a pull request before merging`.
- Activar `Require status checks to pass before merging`.
- Activar `Require branches to be up to date before merging`.
- Activar `Restrict deletions`.
- Activar `Block force pushes`.
- Activar `Do not allow bypassing the above settings`, excepto si se usa un `PAT_TOKEN` dedicado para el bot del pipeline.

Checks requeridos para `test`:

- `Analyze Code with ML Model`

Checks requeridos para `main`:

- `Unit Tests`
- `Integration Tests`

Checks requeridos para `dev`:

- Ninguno por ahora. La regla solo obliga Pull Request, bloquea force-push y bloquea eliminacion.

## Notas para el pipeline automatico

El repositorio usa workflows que hacen merge automatico a `test` y `main`.
Para mantener la automatizacion sin permitir pushes humanos directos:

1. Usar un `PAT_TOKEN` de una cuenta/bot de CI con permisos minimos.
2. Permitir bypass solo a ese actor en las reglas de GitHub.
3. No permitir bypass a usuarios del equipo.

Con esto, los desarrolladores trabajan mediante PR y el pipeline es el unico que puede avanzar codigo entre ramas despues de pasar las validaciones.

## Configuracion por API

Un usuario owner/admin puede aplicar las reglas con:

```bash
GH_ADMIN_TOKEN="token_con_admin_repo" python3 scripts/ci_cd/configure_branch_protection.py
```

Verificacion:

```bash
GH_ADMIN_TOKEN="token_con_admin_repo" python3 scripts/ci_cd/configure_branch_protection.py --verify-only
```

Si la API responde `404`, el token usado no tiene permisos administrativos suficientes o no puede administrar reglas de proteccion en este repositorio.
