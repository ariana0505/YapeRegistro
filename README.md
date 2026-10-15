# Registro de pagos del minimarket Celia

Aplicación web para anotar pagos por Yape y compararlos manualmente con el historial de Yape. No se conecta a Yape ni solicita sus credenciales.

## Problema y usuario

Celia administra un minimarket. Hoy apunta en un cuaderno el nombre del cliente, el monto y la fecha de cada pago por Yape. Más tarde busca esa anotación y la compara manualmente con los movimientos de Yape. Encontrar pagos antiguos y sumar lo recibido en un día le toma tiempo y puede causar confusiones.

El objetivo es que Celia pueda registrar 20 pagos, encontrar cualquiera por nombre o fecha en menos de 30 segundos y consultar el total diario sin sumarlo a mano. La verificación sigue siendo manual en Yape.

**Estado de P1:** el repositorio ya contiene un prototipo funcional adelantado respecto a la entrega que pide la primera función en P3. En P1 el foco de la revisión es el uso de Git y GitHub, la documentación, el PR y la CI. Las instrucciones para ejecutar lo que existe están abajo.

Para la exposición, consulta el [guion de P1](docs/P1-presentacion.md).

## Funciones de la primera versión

- Registrar cliente, monto en soles y fecha del pago.
- Corregir un registro y cambiar su estado entre pendiente y verificado.
- Buscar por nombre y filtrar por fecha.
- Ver por separado los montos verificados y pendientes de una fecha.
- Proteger el registro mediante el inicio de sesión de Django. No hay registro público ni cuentas para distintos negocios.

Un pago *verificado* significa que Celia encontró el movimiento correspondiente en Yape. El total verificado es la suma de estos pagos; el total pendiente se muestra aparte. Los pagos registrados en esta app no son una confirmación emitida por Yape.

## Arquitectura

Navegador del celular o computadora → Django (páginas HTML) → PostgreSQL. Los pagos y las sesiones se guardan en PostgreSQL. El proceso web puede reiniciarse sin perderlos. No hay caché ni cola de trabajos en esta versión.

## Ejecutar en desarrollo

Requiere Python 3.14 y PostgreSQL en ejecución. En una sesión de `psql` con una cuenta administradora, crea una cuenta y una base para la aplicación:

```sql
CREATE ROLE yaperegistro LOGIN CREATEDB PASSWORD 'local-development-only-change-me';
CREATE DATABASE yaperegistro OWNER yaperegistro;
```

`CREATEDB` permite que el ejecutor de pruebas cree una base temporal. La contraseña del ejemplo es solo para desarrollo local; si la cambias, cambia también `DATABASE_URL` en `.env`. Después de copiar `.env.example`, reemplaza `DJANGO_SECRET_KEY` por un valor propio antes de cargar `.env`.

```sh
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edita DJANGO_SECRET_KEY en .env antes de continuar.
set -a
. ./.env
set +a
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://localhost:8000/` e ingresa con la cuenta creada. Esta cuenta también puede entrar a `/admin/`. Para detener la web, pulsa `Ctrl+C`; los pagos seguirán en PostgreSQL. En otra sesión de terminal, activa `.venv` y carga `.env` otra vez antes de ejecutar comandos de Django. `.env` está excluido de Git.

## Pruebas y mantenimiento

Con PostgreSQL en ejecución y el entorno virtual y `.env` cargados:

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Cuando cambie el modelo de datos, crea la migración en desarrollo con `python manage.py makemigrations` y guárdala en Git. Antes de iniciar una versión nueva, ejecuta `python manage.py migrate` como tarea puntual con la configuración del despliegue. El flujo de GitHub Actions ejecuta comprobaciones y pruebas con PostgreSQL.

## Preparar un despliegue

Para construir una versión, instala las dependencias de `requirements.txt` en un entorno aislado y ejecuta `python manage.py collectstatic --noinput`. En el despliegue, proporciona `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DATABASE_URL` y `PORT`; usa `DJANGO_DEBUG=false`. La aplicación exige HTTPS cuando `DEBUG` está desactivado. Configura `DJANGO_CSRF_TRUSTED_ORIGINS` con el origen público completo, por ejemplo `https://pagos.ejemplo.com`. Si está detrás de un proxy que reemplaza el encabezado `X-Forwarded-Proto`, configura `DJANGO_TRUST_PROXY=true`. PostgreSQL debe ser un servicio persistente separado de los procesos web y tener copias de seguridad. Ejecuta `python manage.py migrate` como proceso puntual antes de iniciar la versión nueva. Inicia la web con `gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 2 --access-logfile - --error-logfile - --graceful-timeout 30`; los logs salen por la salida estándar.

Todavía no se ha elegido proveedor de alojamiento ni se ha realizado un despliegue público. Antes de publicar, hay que definir dominio, HTTPS, copias de seguridad, presupuesto y política de acceso. No cargues datos reales hasta tenerlos resueltos.

## Twelve-Factor App

| Factor | Estado en este proyecto |
| --- | --- |
| I. Código base | Código preparado para Git y varios despliegues desde el mismo repositorio. |
| II. Dependencias | Versiones declaradas en `requirements.txt` e instaladas en un entorno aislado. |
| III. Configuración | Valores de despliegue en variables de entorno; `.env` excluido de Git. |
| IV. Servicios externos | PostgreSQL conectado mediante `DATABASE_URL`. |
| V. Construir, desplegar, ejecutar | Dependencias y archivos estáticos se preparan antes; configuración, migraciones y ejecución se aplican por separado. |
| VI. Procesos | El proceso web no guarda pagos en memoria ni en su disco. |
| VII. Puertos | Gunicorn escucha en `PORT`. |
| VIII. Concurrencia | Gunicorn usa dos trabajadores; pueden añadirse instancias web con la misma base. |
| IX. Desechabilidad | Inicio sin tareas largas; Gunicorn permite apagado gradual de peticiones. |
| X. Paridad | Desarrollo y CI usan PostgreSQL; producción debe usarlo también. |
| XI. Logs | Eventos de la app y accesos web salen por consola. |
| XII. Administración | Migraciones, pruebas y creación de la cuenta se ejecutan como procesos puntuales. |

Pendiente para operar en producción: elegir alojamiento y configurar HTTPS, copias de seguridad y monitoreo. Una futura importación de reportes de Yape requeriría primero obtener un archivo de ejemplo y verificar su formato.
