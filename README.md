# 🛒 App Tecnoshop  
Aplicación web **Ecommerce** desarrollada con **Django**, para la venta de productos electrónicos.

---

## ⚙️ Configuración del entorno

### 1️⃣ Crear e iniciar entorno virtual
```bash
py -m venv venv
Activar el entorno virtual
En Windows:

bash
Copiar código
venv\Scripts\activate
En macOS / Linux:

bash
Copiar código
source venv/bin/activate
2️⃣ Instalar dependencias
Asegúrate de tener el archivo requirements.txt en el directorio raíz del proyecto.

bash
Copiar código
pip install -r requirements.txt
3️⃣ Preparar y migrar la base de datos
Ejecuta las migraciones de Django para crear las tablas necesarias en la base de datos.

bash
Copiar código
python manage.py makemigrations
python manage.py migrate
4️⃣ Crear superusuario
Crea una cuenta de administrador para acceder al panel de administración de Django.

bash
Copiar código
python manage.py createsuperuser
Sigue las instrucciones en consola para ingresar usuario, email y contraseña.

5️⃣ Iniciar el servidor
Por defecto, el proyecto se ejecuta en el puerto 8000.

bash
Copiar código
python manage.py runserver
Luego, accede a la aplicación en tu navegador en:
👉 http://localhost:8000

🧾 Agregar productos al catálogo
Inicia sesión en el panel de administración de Django:
👉 http://localhost:8000/admin

En la sección Catálogo, selecciona la opción para importar productos.

Carga el archivo data_catalog.csv incluido en el repositorio.

🚀 Estructura general de la app
La aplicación se compone de las siguientes apps de Django:

accounts – Gestión de usuarios y autenticación.

cart – Manejo del carrito de compras.

catalog – Gestión de productos y categorías.

orders – Procesamiento de pedidos.

pages – Páginas informativas (home, contacto, etc.).

payments – Procesamiento de pagos.

🧩 Ejecución rápida
bash
Copiar código
# Activar entorno virtual
venv\Scripts\activate

# Aplicar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver