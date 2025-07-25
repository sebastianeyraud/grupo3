from django.shortcuts import render
from django.http import FileResponse, Http404
import os
from django.conf import settings

def descargar_manual(request, id):
    # Simula que cada ID tiene un PDF: manual_1.pdf, manual_2.pdf, etc.
    filename = f"manual_{id}.pdf"
    file_path = os.path.join(settings.BASE_DIR, 'media', filename)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("El manual no existe.")


def detalle_manual(request, id):
    manuales_base = [
        {"id": 1, "titulo": "Manual 1", "categoria": "Notebook", "fecha": "Updated today", "descripcion": "Este es el Manual 1.", "peso": "2 MB"},
        {"id": 2, "titulo": "Manual 2", "categoria": "Consolas", "fecha": "Updated yesterday", "descripcion": "Este es el Manual 2.", "peso": "1.5 MB"},
        {"id": 3, "titulo": "Manual 3", "categoria": "Lavadora", "fecha": "Updated 2 days ago", "descripcion": "Este es el Manual 3.", "peso": "3 MB"},
        {"id": 4, "titulo": "Manual 4", "categoria": "Notebook", "fecha": "Updated today", "descripcion": "Este es el Manual 4.", "peso": "2.2 MB"},
        {"id": 5, "titulo": "Manual 5", "categoria": "Celulares", "fecha": "Updated today", "descripcion": "Este es el Manual 5.", "peso": "1.8 MB"},
    ]


    manual = next((m for m in manuales_base if m['id'] == id), None)
    if not manual:
        return render(request, "404.html", status=404)

    return render(request, "detalle_manual.html", {"manual": manual})


def catalogo(request):
    filtro = request.GET.get('categoria', '')
    busqueda = request.GET.get('q', '')

    manuales_base = [
        {"id": 1, "titulo": "Manual 1", "categoria": "Notebook", "fecha": "Updated today", "descripcion": "Este es el Manual 1.", "peso": "2 MB"},
        {"id": 2, "titulo": "Manual 2", "categoria": "Consolas", "fecha": "Updated yesterday", "descripcion": "Este es el Manual 2.", "peso": "1.5 MB"},
        {"id": 3, "titulo": "Manual 3", "categoria": "Lavadora", "fecha": "Updated 2 days ago", "descripcion": "Este es el Manual 3.", "peso": "3 MB"},
        {"id": 4, "titulo": "Manual 4", "categoria": "Notebook", "fecha": "Updated today", "descripcion": "Este es el Manual 4.", "peso": "2.2 MB"},
        {"id": 5, "titulo": "Manual 5", "categoria": "Celulares", "fecha": "Updated today", "descripcion": "Este es el Manual 5.", "peso": "1.8 MB"},
    ]


    # ✅ Lista de categorías (la que usarás en el for del template)
    categorias = ["Notebook", "Consolas", "Lavadora", "Celulares", "Todos"]

    # Filtrado
    manuales = [
        m for m in manuales_base
        if (filtro == '' or m['categoria'] == filtro)
        and (busqueda.lower() in m['titulo'].lower())
    ]

    return render(request, "catalogo.html", {
        "manuales": manuales,
        "filtro_actual": filtro,
        "busqueda_actual": busqueda,
        "categorias": categorias  # 👈 AÑADE esta línea para el template
    })
