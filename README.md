# Documentación del Proyecto: API de Clientes, Facturas y Transacciones con FastAPI

## Cómo iniciar el servidor

Cuando el proyecto inicia correctamente aparecerá el siguiente mensaje:

```
Server started: http://127.0.0.1:8000
Documentación Swagger: http://127.0.0.1:8000/docs
```

La documentación interactiva de la API se encuentra en:

```
http://127.0.0.1:8000/docs
```

---

# Cómo guardar cambios en Git

Cada vez que realices cambios en el proyecto es recomendable verificar el estado del repositorio y crear un nuevo commit.

1. Verificar los archivos modificados.

```bash
git status
```

2. Agregar los cambios.

```bash
git add .
```

3. Crear el commit.

```bash
git commit -m "Descripción de los cambios"
```

---

# Cómo ejecutar el proyecto

Primero se debe activar el entorno virtual.

En Windows:

```bash
.\.mi_env\Scripts\Activate
```

Después se inicia el servidor de FastAPI.

```bash
fastapi dev app/main.py
```

---

# Nota importante

Para visualizar fácilmente la base de datos SQLite es recomendable instalar la extensión **SQLite Viewer** en Visual Studio Code.

Si no se dispone de la extensión, también es posible consultar la base de datos desde la terminal utilizando SQLite.

```bash
sqlite3 bd_clientes.sqlite3
```

Ver las tablas.

```sql
.tables
```

Consultar los clientes.

```sql
SELECT * FROM cliente;
```

---

# 1. Descripción general

Este proyecto consiste en una API REST desarrollada con FastAPI para administrar clientes, facturas y transacciones.

Su objetivo es permitir realizar todas las operaciones básicas (crear, consultar, actualizar y eliminar información) sobre estas tres entidades.

La relación entre ellas funciona de la siguiente manera:

* Un cliente puede tener muchas facturas.
* Cada factura pertenece únicamente a un cliente.
* Una factura puede tener muchas transacciones.
* Cada transacción pertenece únicamente a una factura.

De esta forma la información queda organizada y relacionada correctamente dentro de la base de datos.

---

# 2. Primera etapa: trabajando únicamente con memoria

Al principio del proyecto no se utilizaba ninguna base de datos.

Toda la información se guardaba en listas de Python dentro del archivo **listas.py**.

Por ejemplo, existían listas como:

* lista_clientes
* lista_facturas
* lista_transacciones

Mientras el servidor permanecía encendido todo funcionaba normalmente.

Sin embargo, al detener FastAPI o reiniciar el computador, toda la información desaparecía porque únicamente estaba almacenada en la memoria RAM.

Además, para buscar, modificar o eliminar un elemento era necesario recorrer manualmente las listas utilizando ciclos **for** y en algunos casos **enumerate()**.

Aunque este método fue útil para aprender la lógica del proyecto, tenía varias desventajas:

* Los datos no eran permanentes.
* No existía integridad entre clientes, facturas y transacciones.
* El código se hacía más largo y repetitivo.
* No era una solución adecuada para una aplicación real.

---

# 3. Segunda etapa: migración a SQLModel

Después de tener funcionando la API se decidió migrar toda la información hacia una base de datos utilizando SQLModel.

SQLModel combina las ventajas de SQLAlchemy para trabajar con bases de datos y Pydantic para validar la información que recibe FastAPI.

Con este cambio el proyecto mejoró considerablemente.

Ahora los datos quedan almacenados permanentemente dentro de SQLite y no se pierden cuando el servidor se reinicia.

También comenzó a utilizarse una sesión de base de datos para cada petición mediante la dependencia **sesion_dependencia**, permitiendo abrir y cerrar conexiones automáticamente.

Otra ventaja importante es que SQLModel facilita el manejo de las relaciones entre las tablas utilizando llaves foráneas y relaciones entre modelos.

---

# 4. Organización del proyecto

Para mantener el código organizado se dividió en diferentes carpetas.

```
app/
├── conexion_bd.py
├── listas.py
├── modelos/
│   ├── clientes.py
│   ├── facturas.py
│   └── transacciones.py
└── enrutadores/
    ├── clientes.py
    ├── facturas.py
    └── transacciones.py
```

Cada archivo tiene una responsabilidad específica.

**conexion_bd.py**

Contiene la configuración de la base de datos y la creación de las sesiones.

**listas.py**

Contiene las listas utilizadas durante la primera versión del proyecto. Actualmente prácticamente ya no se utilizan.

**modelos**

Aquí se encuentran las clases que representan las tablas de la base de datos.

**enrutadores**

Contienen todas las rutas o endpoints que utiliza la API.

---

# 5. Modelos de la base de datos

## Cliente

El modelo Cliente representa la información básica de cada cliente.

Cada cliente puede tener muchas facturas.

Entre sus principales campos están:

* id
* nombre
* email

Además tiene una relación con la tabla Factura para poder acceder fácilmente a todas las facturas que pertenecen al cliente.

---

## Factura

La factura representa una compra realizada por un cliente.

Cada factura pertenece a un solo cliente.

Sus principales campos son:

* id
* cliente_id
* vr_total

También posee una relación con las transacciones, ya que una factura puede contener muchos productos o movimientos.

---

## Transacción

La transacción representa cada producto o movimiento registrado dentro de una factura.

Sus principales campos son:

* id
* cantidad
* vr_unitario
* descripcion
* factura_id

Cada transacción pertenece únicamente a una factura.

---

# 6. Funcionamiento de los endpoints

Con la migración hacia SQLModel todos los endpoints comenzaron a trabajar directamente con la base de datos.

Por ejemplo, en el módulo de clientes:

**GET**

Consulta todos los clientes almacenados.

**POST**

Crea un nuevo cliente después de validar la información recibida.

**PATCH**

Actualiza únicamente los campos enviados por el usuario.

**DELETE**

Elimina un cliente existente.

En el módulo de facturas también se realizan validaciones importantes.

Antes de crear una factura el sistema verifica que el cliente realmente exista.

De igual forma, las respuestas pueden incluir información relacionada, como los datos del cliente o las transacciones asociadas.

---

# 7. Problemas encontrados durante el desarrollo

## Error de SQLAlchemy

Uno de los errores más difíciles ocurrió cuando SQLAlchemy mostraba el mensaje:

```
InvalidRequestError: One or more mappers failed to initialize
```

Después de revisar el código se descubrió que el problema estaba en el modelo **Transaccion**.

La relación con **Factura** estaba definida incorrectamente utilizando una lista, cuando en realidad cada transacción solamente pertenece a una factura.

Al cambiar la relación para que apuntara correctamente a **"Factura"**, el ORM pudo crear todas las relaciones sin inconvenientes.

---

## Mezclar listas con base de datos

Otro problema apareció cuando algunas rutas ya utilizaban SQLModel mientras que otras seguían trabajando con las listas de Python.

Como resultado, algunos registros se guardaban correctamente en SQLite, pero las rutas de editar o eliminar seguían buscando la información dentro de las listas antiguas.

Esto provocaba inconsistencias porque la información de la base de datos y la memoria ya no coincidían.

La solución fue actualizar todos los endpoints para que utilizaran únicamente la sesión de base de datos.

Desde ese momento todas las operaciones CRUD comenzaron a trabajar directamente sobre SQLite, manteniendo la información sincronizada y evitando errores.

---

# Conclusión

Durante el desarrollo del proyecto se pasó de una API sencilla basada únicamente en listas de Python a una aplicación mucho más completa utilizando SQLModel y SQLite.

Este cambio permitió almacenar la información de forma permanente, mejorar la organización del código, aprovechar las relaciones entre tablas y simplificar las operaciones CRUD.

Además, el uso de FastAPI junto con SQLModel facilitó la creación de una API más cercana a un entorno de desarrollo profesional, donde los datos permanecen seguros y todas las entidades se encuentran correctamente relacionadas.
