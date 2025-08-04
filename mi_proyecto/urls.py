from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from manuales.views import catalogo, detalle_manual, descargar_manual, cerrar_sesion

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo, name='catalogo'),
    path('manual/<int:id>/', detalle_manual, name='detalle_manual'),
    path('manual/<int:id>/descargar/', descargar_manual, name='descargar_manual'),

    # Login y logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'), #Inicio de Sesion
    path('logout/', cerrar_sesion, name='logout'), #Cierre de sesión
]
