# Charter inicial del producto

Estas son las tres ideas consideradas para el producto de P1. Se eligió la primera para continuarla en los siguientes hitos.

| Idea | Usuario y problema actual | Alcance mínimo de la v1 | Fuera de alcance | Éxito medible |
| --- | --- | --- | --- | --- |
| Registro de pagos por Yape | Celia administra un minimarket. Anota los pagos en un cuaderno y luego los compara manualmente con Yape; buscar pagos antiguos y sumar lo recibido le toma tiempo. | Registrar nombre, monto y fecha; cambiar entre pendiente y verificado; buscar por nombre o día; mostrar el total diario. | Conexión con Yape, acceso bancario, lectura de capturas, notificaciones e inventario. | Celia registra 20 pagos, encuentra cualquiera por nombre o día en menos de 30 segundos y ve el total de una fecha sin sumarlo a mano. |
| Organizador de tareas escolares | Ariana anota clases, tareas y evaluaciones en distintos lugares y puede perder de vista las fechas próximas. | Registrar curso, actividad y fecha límite; marcarla como completada; ordenar y filtrar tareas; señalar atrasos. | Cuentas múltiples, notificaciones, calendario externo y chat. | Ariana registra 15 actividades en menos de cinco minutos e identifica las tres fechas más próximas en menos de diez segundos. |
| Control básico de inventario | Celia controla productos de memoria o en papel y puede no detectar a tiempo los que se agotan. | Registrar productos, existencias y mínimo; anotar entradas y salidas; buscar y mostrar poco stock. | Facturación, pagos, códigos de barras, predicción de ventas y proveedores. | Celia registra 30 productos en menos de diez minutos y obtiene la lista correcta de los que están bajo el mínimo. |

## Idea elegida

**Registro de pagos por Yape para el minimarket de Celia.** Tiene una usuaria concreta, resuelve una tarea que hoy se hace en papel y permite una primera versión acotada. Las otras dos ideas quedan como alternativas, sin mezclarse con este producto.

## Tres dificultades técnicas identificadas al comenzar

1. Guardar los pagos para que permanezcan después de cerrar la aplicación.
2. Crear búsquedas, filtros y totales sin producir resultados incorrectos.
3. Crear pruebas automáticas y configurar CI con GitHub Actions.

El prototipo y sus pruebas ya abordan estas dificultades. En la revisión de P1, Ariana debe explicar con sus propias palabras cómo las resolvió y qué queda por mejorar.

**Aprobación de la idea:** pendiente de registrar quién la aprobó y en qué fecha. Este documento recoge la propuesta elegida; no constituye por sí solo una constancia de aprobación.
