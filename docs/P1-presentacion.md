# Presentación de P1 (10 minutos)

Este guion sirve para practicar. Explica cada decisión con tus propias palabras durante la exposición.

## Minutos 0–2: problema y objetivo

- Celia administra un minimarket y hoy anota pagos por Yape en un cuaderno.
- Después compara a mano las anotaciones con los movimientos de Yape.
- El objetivo es encontrar pagos por nombre o fecha y conocer un total diario. La app no confirma pagos automáticamente.
- Aclara que el prototipo funcional ya está en el repositorio, aunque P1 evalúa sobre todo el flujo con Git y GitHub.

## Minutos 2–4: repositorio y carpetas

Abre el README y explica este mapa:

| Ruta | Motivo |
| --- | --- |
| `payments/` | Modelo, formularios, páginas y pruebas del registro. |
| `templates/` | Pantallas HTML; la interfaz queda separada de la lógica. |
| `config/` | Configuración y rutas de Django. |
| `payments/migrations/` | Cambios versionados de la estructura de PostgreSQL. |
| `.github/workflows/` | Comprobación automática en cada push y PR. |
| `Dockerfile`, `compose.yaml`, `.env.example` | Instalación reproducible y configuración de ejemplo sin secretos reales. |

## Minutos 4–6: historial y rama

Muestra `git log --oneline --graph --all` y la rama `inicio-producto`. Explica que `main` registra por separado la base del proyecto, los datos, la interfaz, las pruebas y la CI. Los commits de la rama preparan la revisión de P1. Muestra `git show --stat <hash>` para enseñar qué cambió en un commit.

## Minutos 6–8: PR y CI

Abre el PR de `inicio-producto` hacia `main`. Explica qué añade, cómo se comprobó y por qué está listo para revisión. Enseña el comentario de revisión propia: debe señalar una decisión concreta y una mejora futura. Abre la pestaña **Checks** y muestra la ejecución verde de CI. El flujo instala dependencias, comprueba la configuración y las migraciones y ejecuta las pruebas con PostgreSQL.

## Minutos 8–10: decisión y corrección de errores

Decisión: se eligió una sola aplicación Django con PostgreSQL para registrar pagos y mantener los datos fuera del proceso web. Se evitó integrar Yape en la primera versión porque Celia puede verificar manualmente en su historial y no se ha confirmado una API pública para su cuenta.

Si un cambio propio está mal, harías un nuevo commit que lo corrija y volverías a comprobar CI. Si un commit ya compartido debe deshacerse completo, usarías `git revert <hash>` para crear un commit inverso y conservar el historial. Evitarías reescribir la rama compartida. Después explicarías en el PR qué pasó y cómo lo verificaste.
