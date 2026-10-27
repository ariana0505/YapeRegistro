# Registro de pagos del minimarket Celia

Aplicación web para anotar pagos por Yape y compararlos manualmente con el historial de Yape. No se conecta a Yape ni solicita sus credenciales.

## Problema y usuario

Celia administra un minimarket. Hoy apunta en un cuaderno el nombre del cliente, el monto y la fecha de cada pago por Yape. Más tarde busca esa anotación y la compara manualmente con los movimientos de Yape. Encontrar pagos antiguos y sumar lo recibido en un día le toma tiempo y puede causar confusiones.

El objetivo es que Celia pueda registrar 20 pagos, encontrar cualquiera por nombre o fecha en menos de 30 segundos y consultar el total diario sin sumarlo a mano. La verificación sigue siendo manual en Yape.

La idea aprobada y su alcance están en el [charter del producto](docs/P1-charter.md). Para P1, revisa la rama `inicio-producto`, el PR con revisión propia y la CI en verde.

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

### Ver la interfaz sin cuenta

Para abrir una vista local con pagos de ejemplo, sin crear usuario ni instalar PostgreSQL:

```sh
git clone https://github.com/ariana0505/YapeRegistro.git
cd YapeRegistro
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DJANGO_DEMO_MODE=true python manage.py runserver
```

Abre `http://localhost:8000/`. Puedes probar los filtros; los pagos de ejemplo no se guardan. Para detener el servidor, pulsa `Ctrl+C`. Este comando inicia el servidor solo en tu computadora y no permite registrar ni modificar pagos. Si Django avisa de migraciones pendientes, puedes ignorar ese aviso en la vista previa.

### Usar la aplicación con datos reales

Requiere Python 3.14 y PostgreSQL en ejecución. En una sesión de `psql` con una cuenta administradora, crea una cuenta y una base para la aplicación:

```sql
CREATE ROLE yaperegistro LOGIN CREATEDB PASSWORD 'local-development-only-change-me';
CREATE DATABASE yaperegistro OWNER yaperegistro;
```

`CREATEDB` permite que el ejecutor de pruebas cree una base temporal. La contraseña del ejemplo es solo para desarrollo local; si la cambias, cambia también `DATABASE_URL` en `.env`.

```sh
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Abre `.env` y reemplaza `DJANGO_SECRET_KEY` por un valor propio. Luego carga la configuración y arranca la aplicación:

```sh
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
