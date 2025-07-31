from django.urls import path
from clientes import views
from .views import subir_manual_view

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('bienvenida/', views.bienvenida_view, name='bienvenida'),
    path('logout/', views.logout_view, name='logout'),
    path('subir-manual/', subir_manual_view, name='subir_manual'),
    path('manual/<int:id>/', views.detalle_manual_view, name='detalle_manual')

]
