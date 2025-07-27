# Proyecto: Manuales Frecuentes

Este proyecto está construido con Django y utiliza Supabase como base de datos en la nube.

## 🚀 Requisitos

- Python 3.10 o superior
- pip
- PostgreSQL (a través de Supabase)

## ⚙️ Instalación para desarrollo

1. Clona el repositorio:

```bash
git clone https://github.com/TU_USUARIO/TU_REPO.git
cd ManualesFrecuentes
```

2. Crea y activa un entorno virtual:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
```

3. Instala las dependencias (desde el archivo requirements.txt):

```bash
pip install -r requirements.txt
```

> Si en algún momento agregas nuevas librerías con `pip install`, recuerda actualizarlo con:
```bash
pip freeze > requirements.txt
```

4. Configura tus variables de entorno en un archivo `.env`:

```
DB_NAME=postgres
DB_USER=postgres.xfpqibynjihlisljcgim
DB_PASSWORD=Coroico1214.
DB_HOST=aws-0-us-east-2.pooler.supabase.com
DB_PORT=5432
```

5. Ejecuta migraciones:

```bash
python manage.py migrate
```

6. Levanta el servidor:

```bash
python manage.py runserver
```

---

## 📦 Estructura del proyecto

- `backend/`: configuración principal de Django.
- `manuales/`: app para manejar manuales.
- `templates/`: HTML del frontend.
- `.env`: configuración privada (NO SE SUBE).
- `venv/`: entorno virtual local (NO SE SUBE).