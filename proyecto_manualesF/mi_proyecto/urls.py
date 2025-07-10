from django.contrib import admin
from django.urls import path
from manuales.views import catalogo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo),  # Página principal
]
