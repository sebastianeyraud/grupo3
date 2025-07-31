from supabase import create_client
import datetime

# Configuración de Supabase
SUPABASE_URL = "https://ycvqocpgvrwkykjdunfn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InljdnFvY3BndnJ3a3lramR1bmZuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MzU3MzU4OCwiZXhwIjoyMDY5MTQ5NTg4fQ.pPTK5aoxpiFu32uT_1WKdoG_4ugrHU16Pu7rG_9dzMk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def guardar_comentario(manual_id, usuario, comentario, valoracion):
    datos = {
        "manual_id": manual_id,
        "usuario": usuario,
        "comentario": comentario,
        "valoracion": valoracion,
        "fecha": datetime.datetime.now().isoformat()
    }
    supabase.table("comentarios").insert(datos).execute()

def obtener_comentarios(manual_id):
    response = supabase.table("comentarios").select("*").eq("manual_id", manual_id).execute()
    return response.data if response.data else []

def obtener_manuales():
    response = supabase.table("manuales").select("*").execute()
    return response.data if response.data else []

def obtener_manual_por_id(id):
    data = supabase.table("manuales").select("*").eq("id", id).single().execute()
    return data.data

# 📂 Subir archivo PDF al bucket "manuales"
def subir_pdf(nombre_archivo, archivo):
    contenido = archivo.read()
    ruta = nombre_archivo  # ✅ Subimos directamente al bucket sin carpeta extra

    # Subida del archivo al bucket "manuales"
    supabase.storage.from_("manuales").upload(
        ruta,
        contenido,
        {"content-type": "application/pdf", "x-upsert": "true"}  # Evita errores si subes el mismo archivo
    )

    # Generar URL pública correcta
    url = f"{SUPABASE_URL}/storage/v1/object/public/manuales/{ruta}"
    return url


# 📝 Guardar los datos del manual en la tabla "manuales"
def guardar_datos_manual(titulo, categoria, descripcion, url_pdf):
    datos = {
        "titulo": titulo,
        "categoria": categoria,
        "descripcion": descripcion,
        "url_pdf": url_pdf,
        "fecha_subida": datetime.datetime.now().isoformat()
    }
    supabase.table("manuales").insert(datos).execute()

def obtener_valoracion_promedio(manual_id):
    response = supabase.table("comentarios").select("valoracion").eq("manual_id", manual_id).execute()
    valoraciones = [c["valoracion"] for c in response.data if c["valoracion"] is not None]
    if not valoraciones:
        return 0
    return sum(valoraciones) / len(valoraciones)
