from django.contrib import admin
from django.urls import path
from manuales.views import catalogo, detalle_manual, descargar_manual  # ⬅️ agrega aquí la nueva vista también

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo, name='catalogo'),  # página principal
    path('manual/<int:id>/', detalle_manual, name='detalle_manual'),  # detalle del manual
    path('manual/<int:id>/descargar/', descargar_manual, name='descargar_manual'),  # descarga PDF
]
