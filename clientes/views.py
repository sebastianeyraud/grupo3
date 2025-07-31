import re
from django.shortcuts import render, redirect
from .supabase_client import supabase
from .supabase_admin import supabase_admin
from django.contrib.auth.decorators import login_required
from .supabase_service import subir_pdf, guardar_datos_manual, obtener_manuales
from .supabase_service import obtener_manual_por_id
from .supabase_service import obtener_comentarios
from .supabase_service import guardar_comentario  # <--- asegúrate de importar
from .supabase_service import obtener_valoracion_promedio

def inicio_view(request):
    query = request.GET.get('q', '').lower()  # búsqueda opcional
    manuales = obtener_manuales()

    if query:
        manuales = [
            m for m in manuales
            if query in m['titulo'].lower() or query in m['categoria'].lower()
        ]

    return render(request, 'inicio.html', {'manuales': manuales, 'query': query})


def subir_manual_view(request):
    if 'usuario' not in request.session:
        return redirect('login')

    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')

        # Subir PDF a Supabase Storage
        url_pdf = subir_pdf(archivo.name, archivo)

        # Guardar datos en Supabase DB
        guardar_datos_manual(titulo, categoria, descripcion, url_pdf)

        return render(request, 'subir_manual.html', {'mensaje': 'Manual subido correctamente.'})

    return render(request, 'subir_manual.html')


def es_correo_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(patron, email)


def registro_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        # Validar formato de correo
        if not es_correo_valido(email):
            return render(request, 'registro.html', {
                'error': 'El formato del correo no es válido.'
            })

        # Validar contraseña
        if len(password) < 6:
            return render(request, 'registro.html', {
                'error': 'La contraseña debe tener al menos 6 caracteres.'
            })

        # Verificar si ya está registrado
        try:
            response = supabase_admin.auth.admin.list_users()
            usuarios = response
            for usuario in usuarios:
                if hasattr(usuario, 'email') and usuario.email == email:
                    return render(request, 'registro.html', {
                        'error': 'Este correo ya está registrado. Intenta iniciar sesión.'
                    })
        except Exception as e:
            return render(request, 'registro.html', {
                'error': f'Error al verificar el correo: {str(e)}'
            })

        # Registrar nuevo usuario
        try:
            supabase.auth.sign_up({'email': email, 'password': password})
            return render(request, 'registro.html', {
                'mensaje': 'Revisa tu correo electrónico para verificar tu cuenta antes de iniciar sesión.'
            })
        except Exception as e:
            return render(request, 'registro.html', {
                'error': f'Error al registrar: {str(e)}'
            })

    return render(request, 'registro.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        try:
            respuesta = supabase.auth.sign_in_with_password({
                'email': email,
                'password': password
            })

            if respuesta.session:
                request.session['usuario'] = email
                return redirect('bienvenida')
            else:
                return render(request, 'login.html', {'error': 'Login incorrecto'})

        except Exception as e:
            return render(request, 'login.html', {'error': f'Error al iniciar sesión: {str(e)}'})

    return render(request, 'login.html')


def bienvenida_view(request):
    if 'usuario' not in request.session:
        return redirect('inicio')

    usuario = request.session['usuario']
    query = request.GET.get('q', '').lower()
    manuales = obtener_manuales()

    if query:
        manuales = [
            m for m in manuales
            if query in m['titulo'].lower() or query in m['categoria'].lower()
        ]

    return render(request, 'bienvenida.html', {
        'usuario': usuario,
        'manuales': manuales,
        'query': query
    })

def detalle_manual_view(request, id):
    manual = obtener_manual_por_id(id)
    usuario = request.session.get('usuario', None)
    puede_comentar = usuario is not None

    if request.method == "POST" and puede_comentar:
        comentario = request.POST.get("comentario")
        valoracion = int(request.POST.get("valoracion", 0))
        guardar_comentario(id, usuario, comentario, valoracion)
        return redirect('detalle_manual', id=id)  # ✅ Redirección correcta

    comentarios = obtener_comentarios(id)
    promedio_valoracion = obtener_valoracion_promedio(id)

    return render(request, 'detalle_manual.html', {
        'manual': manual,
        'comentarios': comentarios,
        'puede_comentar': puede_comentar,
        'usuario': usuario,
        'promedio_valoracion': promedio_valoracion,
    })


def logout_view(request):
    request.session.flush()
    return redirect('inicio')
