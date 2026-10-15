# Registro de pagos del minimarket Celia

Aplicación web para anotar pagos por Yape y compararlos manualmente con el historial de Yape. No se conecta a Yape ni solicita sus credenciales.

## Problema y usuario

Celia administra un minimarket. Hoy apunta en un cuaderno el nombre del cliente, el monto y la fecha de cada pago por Yape. Más tarde busca esa anotación y la compara manualmente con los movimientos de Yape. Encontrar pagos antiguos y sumar lo recibido en un día le toma tiempo y puede causar confusiones.

El objetivo es que Celia pueda registrar 20 pagos, encontrar cualquiera por nombre o fecha en menos de 30 segundos y consultar el total diario sin sumarlo a mano. La verificación sigue siendo manual en Yape.

## Funciones de la primera versión

- Registrar cliente, monto en soles y fecha del pago.
- Corregir un registro y cambiar su estado entre pendiente y verificado.
- Buscar por nombre y filtrar por fecha.
- Ver por separado los montos verificados y pendientes de una fecha.
- Proteger el registro mediante el inicio de sesión de Django. No hay registro público ni cuentas para distintos negocios.

Un pago *verificado* significa que Celia encontró el movimiento correspondiente en Yape. El total verificado es la suma de estos pagos; el total pendiente se muestra aparte. Los pagos registrados en esta app no son una confirmación emitida por Yape.

## Arquitectura

Navegador del celular o computadora → Django (páginas HTML) → PostgreSQL. Los pagos y las sesiones se guardan en PostgreSQL. El proceso web puede reiniciarse sin perderlos. No hay caché ni cola de trabajos en esta versión.

## Ejecutar en desarrollo con Docker

Requiere Docker y Docker Compose.

1. Copia el archivo de ejemplo: `cp .env.example .env`.
2. Cambia `DJANGO_SECRET_KEY` y `POSTGRES_PASSWORD` en `.env`; actualiza también la contraseña dentro de `DATABASE_URL` para que coincida. Los valores del ejemplo son solo locales.
3. Ejecuta `docker compose up -d db`.
4. Aplica las migraciones con `docker compose run --rm web python manage.py migrate`.
5. Crea la cuenta de Celia con `docker compose run --rm web python manage.py createsuperuser`. Elige un usuario y una contraseña fuerte; esta cuenta también puede entrar a `/admin/`.
6. Inicia la web: `docker compose up -d --build web`.
7. Abre `http://localhost:8000/` e ingresa con la cuenta creada.

Para revisar los eventos: `docker compose logs -f web`. Para detener los procesos: `docker compose down`. **No uses `docker compose down -v` si quieres conservar los pagos**, porque elimina el volumen de PostgreSQL.

## Pruebas y mantenimiento

Con los servicios de Docker disponibles:

```sh
docker compose run --rm web python manage.py check
docker compose run --rm web python manage.py makemigrations --check --dry-run
docker compose run --rm web python manage.py test
```

Cuando cambie el modelo de datos, crea la migración en desarrollo con `python manage.py makemigrations` y guárdala en Git. Antes de iniciar una versión nueva, ejecuta `python manage.py migrate` como tarea puntual con la configuración del despliegue. El flujo de GitHub Actions ejecuta comprobaciones y pruebas con PostgreSQL.

## Preparar un despliegue

La imagen Docker construye el código, instala las dependencias y prepara los archivos estáticos. Al ejecutar la imagen, proporciona `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL` y `PORT`; usa `DJANGO_DEBUG=false`. La aplicación exige HTTPS cuando `DEBUG` está desactivado. Configura `DJANGO_CSRF_TRUSTED_ORIGINS` con el origen público completo, por ejemplo `https://pagos.ejemplo.com`. Si está detrás de un proxy que reemplaza el encabezado `X-Forwarded-Proto`, configura `DJANGO_TRUST_PROXY=true`. PostgreSQL debe ser un servicio persistente externo al contenedor web y tener copias de seguridad. Ejecuta las migraciones como proceso puntual antes de iniciar la versión nueva. El servidor Gunicorn escucha en `PORT` y escribe logs en la salida estándar.

Todavía no se ha elegido proveedor de alojamiento ni se ha realizado un despliegue público. Antes de publicar, hay que definir dominio, HTTPS, copias de seguridad, presupuesto y política de acceso. No cargues datos reales hasta tenerlos resueltos.

## Twelve-Factor App

| Factor | Estado en este proyecto |
| --- | --- |
| I. Código base | Código preparado para Git y varios despliegues desde el mismo repositorio. |
| II. Dependencias | Versiones declaradas en `requirements.txt` e instaladas en un entorno aislado. |
| III. Configuración | Valores de despliegue en variables de entorno; `.env` excluido de Git. |
| IV. Servicios externos | PostgreSQL conectado mediante `DATABASE_URL`. |
| V. Construir, desplegar, ejecutar | Docker construye una imagen; configuración y migraciones se aplican por separado. |
| VI. Procesos | El proceso web no guarda pagos en memoria ni en su disco. |
| VII. Puertos | Gunicorn escucha en `PORT`. |
| VIII. Concurrencia | Gunicorn usa dos trabajadores; pueden añadirse instancias web con la misma base. |
| IX. Desechabilidad | Inicio sin tareas largas; Gunicorn permite apagado gradual de peticiones. |
| X. Paridad | Desarrollo y CI usan PostgreSQL; producción debe usarlo también. |
| XI. Logs | Eventos de la app y accesos web salen por consola. |
| XII. Administración | Migraciones, pruebas y creación de la cuenta se ejecutan como procesos puntuales. |

Pendiente para operar en producción: elegir alojamiento y configurar HTTPS, copias de seguridad y monitoreo. Una futura importación de reportes de Yape requeriría primero obtener un archivo de ejemplo y verificar su formato.
