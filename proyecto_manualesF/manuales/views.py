from django.shortcuts import render

def catalogo(request):
    filtro = request.GET.get('categoria', '')
    busqueda = request.GET.get('q', '')

    manuales_base = [
        {"titulo": "Manual 1", "categoria": "Notebook", "fecha": "Updated today"},
        {"titulo": "Manual 2", "categoria": "Consolas", "fecha": "Updated yesterday"},
        {"titulo": "Manual 3", "categoria": "Lavadora", "fecha": "Updated 2 days ago"},
        {"titulo": "Manual 4", "categoria": "Notebook", "fecha": "Updated today"},
        {"titulo": "Manual 5", "categoria": "Celulares", "fecha": "Updated today"},
    ]

    # Filtrado
    manuales = [
        m for m in manuales_base
        if (filtro == '' or m['categoria'] == filtro)
        and (busqueda.lower() in m['titulo'].lower())
    ]

    return render(request, "catalogo.html", {
        "manuales": manuales,
        "filtro_actual": filtro,
        "busqueda_actual": busqueda
    })
