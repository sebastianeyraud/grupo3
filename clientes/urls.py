from django.urls import path
from clientes import views
from .views import subir_manual_view, soporte_tecnico_view, recuperar_contrasena_view, nueva_contrasena_view,editar_manual_view, editar_comentario_view,eliminar_comentario_view

urlpatterns = [
    path('', views.inicio_view, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('bienvenida/', views.bienvenida_view, name='bienvenida'),
    path('logout/', views.logout_view, name='logout'),
    path('subir-manual/', subir_manual_view, name='subir_manual'),
    path('manual/<int:id>/', views.detalle_manual_view, name='detalle_manual'),
    
    # Videos
    path('videos/', views.inicio_video_view, name='inicio_video'),
    path('bienvenida/videos/', views.bienvenida_video_view, name='bienvenida_video'),

    path('soporte/', soporte_tecnico_view, name='soporte_tecnico'),
    path('recuperar/', recuperar_contrasena_view, name='recuperar'),
    path('nueva_contrasena/', nueva_contrasena_view, name='nueva_contrasena'),
    path('manual/<int:id>/editar/', editar_manual_view, name='editar_manual'),
    path('comentario/<int:comentario_id>/editar/', editar_comentario_view, name='editar_comentario'),
    path('comentario/<int:comentario_id>/eliminar/', eliminar_comentario_view, name='eliminar_comentario'),


]
