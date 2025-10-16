# 🛒 App Tecnoshop  
Aplicación web **Ecommerce** desarrollada con **Django**, para la venta de productos electrónicos.


# ⚙️ Configuración del entorno

## 1️⃣ Crear e iniciar entorno virtual
```bash
py -m venv venv
```

Activar el entorno virtual, en Windows:
```bash
venv\Scripts\activate
```
En macOS / Linux:
```bash
source venv/bin/activate
```
## 2️⃣ Instalar dependencias
Asegúrate de tener el archivo requirements.txt en el directorio raíz del proyecto.
```bash
pip install -r requirements.txt
```
## 3️⃣ Preparar y migrar la base de datos
Ejecuta las migraciones de Django para crear las tablas necesarias en la base de datos.
```bash
python manage.py makemigrations
python manage.py migrate
```
## 4️⃣ Crear superusuario
Crea una cuenta de administrador para acceder al panel de administración de Django.

```bash
python manage.py createsuperuser
```
Sigue las instrucciones en consola para ingresar usuario, email y contraseña.

## 5️⃣ Iniciar el servidor
Por defecto, el proyecto se ejecuta en el puerto 8000.

```bash
python manage.py runserver
```
Luego, accede a la aplicación en tu navegador en:
👉 http://localhost:8000


## 6️⃣ Subir productos a través del admin
Inicia sesión en el panel de administración de Django:
👉 http://localhost:8000/admin
En la sección Catálogo, selecciona la opción para importar productos.
Carga el archivo data_catalog.csv incluido en el repositorio.
No es necesario subir un slug, ya que estos se generan automáticamente.

## 7️⃣ Prueba de ETL
Para probar el funcionamiento del proceso ETL en Django, ejecuta el siguiente comando:
```bash
python manage.py run_etl
```

Asegúrate de que el archivo CSV se encuentre en la carpeta data.
Este comando se encarga de ordenar y limpiar el contenido del CSV para subirlo automáticamente a la base de datos.

Una vez hecho esto, puedes iniciar el servidor de Django con:
```bash
python manage.py runserver
```

## 🚀 Estructura general de la app
La aplicación se compone de las siguientes apps de Django:

- accounts – Gestión de usuarios y autenticación.
- cart – Manejo del carrito de compras.
- catalog – Gestión de productos y categorías.
- orders – Procesamiento de pedidos.
- pages – Páginas informativas (home, contacto, etc.).
- payments – Procesamiento de pagos.
- pages - Páginas de inicio y contacto
