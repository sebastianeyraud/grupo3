import re
from django.shortcuts import render, redirect
from .supabase_client import supabase
from .supabase_admin import supabase_admin
from supabase import create_client
from django.contrib.auth.decorators import login_required
from .supabase_service import subir_pdf, guardar_datos_manual, obtener_manuales
from .supabase_service import obtener_manual_por_id, actualizar_manual
from .supabase_service import obtener_comentarios, obtener_comentario_por_id
from .supabase_service import guardar_comentario,eliminar_comentario  # <--- asegúrate de importar
from .supabase_service import obtener_valoracion_promedio, actualizar_comentario
from .supabase_service import guardar_mensaje_soporte

def inicio_view(request):
    q = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    usuario_logueado = request.session.get("usuario")

    manuales = obtener_manuales()  # tu función que trae los manuales desde Supabase

    if q:
        manuales = [m for m in manuales if q.lower() in m["titulo"].lower() or q.lower() in m["descripcion"].lower()]

    if categoria:
        if categoria == "mio" and usuario_logueado:
            manuales = [m for m in manuales if m["usuario"] == usuario_logueado]
        elif categoria != "mio":
            manuales = [m for m in manuales if m["categoria"].lower() == categoria.lower()]

    return render(request, "inicio.html", {
        "manuales": manuales,
        "query": q,
        "categoria": categoria
    })


def subir_manual_view(request):
    if request.method == "POST" and request.FILES.get("archivo"):
        archivo = request.FILES.get("archivo")
        ficha_tecnica = request.FILES.get("ficha_tecnica")  # 👈 nuevo campo

        titulo = request.POST.get("titulo")
        categoria = request.POST.get("categoria")
        descripcion = request.POST.get("descripcion")
        video_url = request.POST.get("video_url")
        usuario = request.session.get("usuario")

        # ✅ Subimos los archivos a Supabase y obtenemos URL
        url_pdf = subir_pdf(archivo.name, archivo) if archivo else None
        url_ficha = subir_pdf(ficha_tecnica.name, ficha_tecnica) if ficha_tecnica else None

        guardar_datos_manual(
            titulo=titulo,
            categoria=categoria,
            descripcion=descripcion,
            url_pdf=url_pdf,
            video_url=video_url,
            ficha_tecnica=url_ficha,
            usuario=usuario
        )

        return render(request, "subir_manual.html", {"mensaje": "Manual subido correctamente"})

    return render(request, "subir_manual.html")

def es_correo_valido(email):
    patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.match(patron, email)


def registro_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        contrasena = request.POST.get("contrasena")

        try:
            supabase.auth.sign_up({
                "email": email,
                "password": contrasena
            })

            return render(request, "registro.html", {
                "mensaje": "Registro completado. Revisa tu correo para verificar tu cuenta."
            })

        except Exception as e:
            print("Error:", e)
            return render(request, "registro.html", {
                "error": "Error durante el registro. Intenta nuevamente."
            })

    return render(request, "registro.html")

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

    usuario = request.session['usuario']  # se guarda el correo completo
    manuales = obtener_manuales()
    query = request.GET.get('q', '').lower()
    categoria = request.GET.get('categoria', '').lower()

    if categoria == "mio":
        manuales = [m for m in manuales if m.get("usuario") == usuario]
    elif categoria:
        manuales = [m for m in manuales if m.get("categoria", "").lower() == categoria]

    if query:
        manuales = [m for m in manuales if query in m.get('titulo', '').lower()]

    return render(request, 'bienvenida.html', {
        'usuario': usuario,
        'manuales': manuales,
        'query': query,
        'categoria': categoria
    })


def detalle_manual_view(request, id):
    manual = obtener_manual_por_id(id)
    usuario = request.session.get('usuario', None)
    puede_comentar = usuario is not None

    if request.method == "POST" and puede_comentar:
        comentario = request.POST.get("comentario")
        valoracion = int(request.POST.get("valoracion", 0))
        guardar_comentario(id, usuario, comentario, valoracion)
        return redirect('detalle_manual', id=id)

    comentarios = obtener_comentarios(id)
    promedio_valoracion = obtener_valoracion_promedio(id)

    # ✅ Agregamos verificación del autor
    es_autor = (manual['usuario'] == usuario) if manual else False

    return render(request, 'detalle_manual.html', {
        'manual': manual,
        'comentarios': comentarios,
        'puede_comentar': puede_comentar,
        'usuario': usuario,
        'promedio_valoracion': promedio_valoracion,
        'es_autor': es_autor,  # ✅ Importante para el botón "Editar"
    })



def logout_view(request):
    request.session.flush()
    return redirect('inicio')

def inicio_video_view(request):
    q = request.GET.get("q", "")
    categoria = request.GET.get("categoria", "")
    usuario_logueado = request.session.get("usuario")

    manuales = obtener_manuales()  # Usa la misma función, pero filtra solo los que tienen video
    manuales = [m for m in manuales if m["video_url"]]

    if q:
        manuales = [m for m in manuales if q.lower() in m["titulo"].lower() or q.lower() in m["descripcion"].lower()]

    if categoria:
        if categoria == "mio" and usuario_logueado:
            manuales = [m for m in manuales if m["usuario"] == usuario_logueado]
        elif categoria != "mio":
            manuales = [m for m in manuales if m["categoria"].lower() == categoria.lower()]

    return render(request, "inicio_video.html", {
        "manuales": manuales,
        "query": q,
        "categoria": categoria
    })



def bienvenida_video_view(request):
    if 'usuario' not in request.session:
        return redirect('inicio')

    usuario = request.session['usuario']
    manuales = obtener_manuales()
    query = request.GET.get('q', '').lower()
    categoria = request.GET.get('categoria', '').lower()

    # Filtrar solo los que tienen video
    manuales_con_video = [m for m in manuales if m.get('video_url')]

    # Filtro por búsqueda
    if query:
        manuales_con_video = [
            m for m in manuales_con_video
            if query in m.get('titulo', '').lower() or query in m.get('descripcion', '').lower()
        ]

    # Filtro por categoría
    if categoria:
        if categoria == "mio":
            manuales_con_video = [m for m in manuales_con_video if m.get("usuario") == usuario]
        elif categoria != "todo":
            manuales_con_video = [m for m in manuales_con_video if m.get("categoria", "").lower() == categoria]

    return render(request, 'bienvenida_video.html', {
        'usuario': usuario,
        'manuales': manuales_con_video,
        'query': query,
        'categoria': categoria,
    })


def soporte_tecnico_view(request):
    if 'usuario' not in request.session:
        return render(request, 'soporte_no_logueado.html')

    usuario = request.session['usuario']

    mensaje_exito = None

    if request.method == "POST":
        mensaje = request.POST.get("mensaje")
        tipo = request.POST.get("tipo")  # "consulta" o "reclamo"

        if mensaje and tipo:
            asunto = "Consulta" if tipo == "consulta" else "Reclamo"
            guardar_mensaje_soporte(usuario, asunto, mensaje)
            mensaje_exito = "¡Gracias! Hemos recibido tu mensaje."

    return render(request, 'soporte_logueado.html', {
        "usuario": usuario,
        "mensaje_exito": mensaje_exito
    })

def recuperar_contrasena_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            # Llama a Supabase para enviar el correo de recuperación
            supabase.auth.reset_password_email(email, {
                'redirect_to': 'http://localhost:8000/nueva_contrasena/'  # Puedes cambiar este link
            })
            mensaje = "Correo enviado. Revisa tu bandeja de entrada."
            return render(request, 'recuperar_contrasena.html', {'mensaje': mensaje})

        except Exception as e:
            return render(request, 'recuperar_contrasena.html', {'error': f'Error: {str(e)}'})

    return render(request, 'recuperar_contrasena.html')

def nueva_contrasena_view(request):
    if request.method == "POST":
        nueva = request.POST.get("nueva")
        confirmar = request.POST.get("confirmar")
        access_token = request.POST.get("access_token")

        if nueva != confirmar:
            return render(request, "nueva_contrasena.html", {
                "error": "Las contraseñas no coinciden",
                "access_token": access_token,
            })

        try:
            # ✅ Establece la sesión usando solo access_token
            supabase.auth.set_session(access_token, access_token)

            # ✅ Ahora actualiza la contraseña
            supabase.auth.update_user({"password": nueva})

            return render(request, "nueva_contrasena.html", {
                "mensaje": "¡Contraseña actualizada correctamente!"
            })

        except Exception as e:
            return render(request, "nueva_contrasena.html", {
                "error": f"Error: {str(e)}",
                "access_token": access_token,
            })

    # Recupera token del fragmento de URL con JS
    return render(request, "nueva_contrasena.html", {})

def editar_manual_view(request, id):
    manual = obtener_manual_por_id(id)
    usuario = request.session.get('usuario', None)

    # Solo el autor puede editar
    if not manual or manual['usuario'] != usuario:
        return redirect('detalle_manual', id=id)

    if request.method == "POST":
        titulo = request.POST.get("titulo")
        categoria = request.POST.get("categoria")
        descripcion = request.POST.get("descripcion")
        video_url = request.POST.get("video_url")
        ficha_tecnica_file = request.FILES.get("ficha_tecnica")
        pdf_file = request.FILES.get("archivo")

        # Subir nuevo PDF si lo cambió
        if pdf_file:
            nuevo_url_pdf = subir_pdf(pdf_file.name, pdf_file)
        else:
            nuevo_url_pdf = manual['url_pdf']

        # Subir nueva ficha técnica si la cambió
        if ficha_tecnica_file:
            nueva_ficha_tecnica = subir_pdf(ficha_tecnica_file.name, ficha_tecnica_file)
        else:
            nueva_ficha_tecnica = manual.get('ficha_tecnica', "")

        # Guardar en Supabase (debes tener esta función)
        actualizar_manual(id, titulo, categoria, descripcion, nuevo_url_pdf, video_url, nueva_ficha_tecnica)

        return redirect('detalle_manual', id=id)

    return render(request, "editar_manual.html", {
        "manual": manual
    })


def editar_comentario_view(request, comentario_id):
    usuario = request.session.get('usuario')
    comentario = obtener_comentario_por_id(comentario_id)

    if not usuario or comentario['usuario'] != usuario:
        return HttpResponseForbidden("No tienes permiso para editar este comentario.")

    if request.method == "POST":
        nuevo_comentario = request.POST.get("comentario")
        nueva_valoracion = int(request.POST.get("valoracion", 0))
        actualizar_comentario(comentario_id, nuevo_comentario, nueva_valoracion)
        return redirect('detalle_manual', id=comentario['manual_id'])

    return render(request, 'editar_comentario.html', {
        'comentario': comentario
    })

def eliminar_comentario_view(request, comentario_id):
    usuario = request.session.get('usuario')
    comentario = obtener_comentario_por_id(comentario_id)

    if not usuario or comentario['usuario'] != usuario:
        return HttpResponseForbidden("No tienes permiso para eliminar este comentario.")

    if request.method == "POST":
        eliminar_comentario(comentario_id)
        return redirect('detalle_manual', id=comentario['manual_id'])

    return render(request, 'confirmar_eliminar_comentario.html', {
        'comentario': comentario
    })

