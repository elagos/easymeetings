# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from models import *
from forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import datetime
from django.core.exceptions import ObjectDoesNotExist
import linecache
import sys, os

@login_required(login_url='/index/')
def agregar_proyecto(request):
    proyectos = Proyecto.objects.all()
    usuarios = Usuario.objects.all()
    posibles_miembros = lista_usuarios(request.user.username)
    if request.method == 'POST':
        nombre = request.POST['agregar_proyecto_nombre'].capitalize()
        descripcion = request.POST['agregar_proyecto_descripcion'].capitalize()
        miembros = request.POST.getlist('agregar_proyecto_miembros')
        fecha_inicio = datetime.datetime.strptime(request.POST['agregar_proyecto_fecha_inicio'], '%d/%m/%Y').strftime('%Y-%m-%d')

        proyecto = Proyecto(nombre_proyecto=nombre, descripcion_proyecto=descripcion, fecha_inicio_proyecto=fecha_inicio).save()
        #print "Proyecto agregado: ", proyecto
        proyecto = Proyecto.objects.get(id=Proyecto.objects.latest('id').id)

        #Agregamos el usuario logueado al proyecto
        user = Usuario.objects.get(user=User.objects.get(username=request.user.username))
        usuario_proyecto = Usuario_Proyecto(usuario=user, proyecto=proyecto, rol_proyecto="Miembro Regular")
        usuario_proyecto.save()

        #Agregamos a los demas miembros escogidos
        for x in miembros:
            user = Usuario.objects.get(id=int(x))
            usuario_proyecto = Usuario_Proyecto(usuario=user, proyecto=proyecto, rol_proyecto="Miembro Regular")
            usuario_proyecto.save()
        proyectos_activos = lista_proyectos_activos(request.user.username)
        ctx = {'success_agregar_proyecto': True, 'lista_usuarios':posibles_miembros, 'lista_proyectos_activos':proyectos_activos, 'proyecto_agregado':proyecto}
    else:
        ctx = {}
    return render(request, 'walo-template/index.html', ctx)

@login_required(login_url='/index/')
def ver_proyecto(request, id_proyecto):
    ctx = {}
    if request.method == 'POST':
        nombre = request.POST.get('editar_proyecto_nombre')
        if request.POST.get('editar_proyecto_fecha_inicio'):
            fecha_inicio = datetime.datetime.strptime(request.POST.get('editar_proyecto_fecha_inicio'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_inicio = None
        if request.POST.get('editar_proyecto_fecha_termino'):
            fecha_termino = datetime.datetime.strptime(request.POST.get('editar_proyecto_fecha_termino'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_termino = None
        descripcion = request.POST.get('editar_proyecto_descripcion')
        miembros = request.POST.getlist('editar_proyecto_miembros')
        proyecto_editar = Proyecto.objects.get(id=id_proyecto)
        proyecto_editar.descripcion_proyecto = descripcion
        proyecto_editar.nombre_proyecto = nombre
        proyecto_editar.fecha_inicio_proyecto = fecha_inicio
        proyecto_editar.fecha_fin_proyecto = fecha_termino

        for x in miembros:
            user = Usuario.objects.get(id=int(x))
            if user not in proyecto_editar.usuario_proyecto_set.all():
                print "Usuario nuevo:", user
                #usuario_proyecto = Usuario_Proyecto(usuario=user, proyecto=proyecto_editar, rol_proyecto="Miembro Regular")
                #usuario_proyecto.save()
        proyecto_editar.save()
        ctx['successEditar'] = True
    proyecto = Proyecto.objects.get(id=id_proyecto)
    posibles_miembros = lista_usuarios(request.user.username)
    ctx['proyecto'] = proyecto
    ctx['lista_usuarios'] = posibles_miembros
    return render(request, 'walo-template/proyectos/ver_proyecto.html',ctx)

@login_required(login_url='/index/')
def agregar_acta(request, id_proyecto):
    proyecto_acta = Proyecto.objects.get(id=id_proyecto)
    usuarios_proyecto = Usuario_Proyecto.objects.filter(proyecto=proyecto_acta)
    actas = Acta.objects.filter(proyecto_acta=proyecto_acta)

    compromisos_pendientes = False
    for acta in actas:
        for tema in acta.tema_set.all():
            for elemento in tema.elemento_set.all():
                if elemento.tipo_elemento == "Compromiso" and (elemento.estado_elemento != "Finalizado" or elemento.estado_elemento != "Eliminado"):
                    compromisos_pendientes = True
                    break

    if request.method == 'POST':
        #Agregamos el acta
        fecha_acta = datetime.datetime.strptime(request.POST['agregar_acta_fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
        resumen_acta = request.POST.get('agregar_acta_resumen')
        nueva_acta = Acta(proyecto_acta=proyecto_acta, fecha_acta=fecha_acta, resumen_acta=resumen_acta).save()
        acta = Acta.objects.get(id=Acta.objects.latest('id').id)

        #Por cada miembro, añadimos usuario_acta
        miembros_presentes = request.POST.getlist('agregar_acta_miembros_presentes')
        miembros_proyecto = Usuario_Proyecto.objects.filter(proyecto=proyecto_acta)
        secretario_proyecto = request.POST.get('agregar_acta_secretario')
        for miembro in miembros_proyecto:
            presente = False
            secretario = False
            usuario = Usuario.objects.get(user=miembro.usuario)
            if str(usuario.id) in miembros_presentes:
                #Solo si estuvo presente, puede ser secretario
                presente = True
                if str(usuario.id) == secretario_proyecto:
                    secretario = True
            usuario_acta=Usuario_Acta(usuario=usuario, acta=acta, presente=presente, secretario=secretario)
            usuario_acta.save()

        #Añadimos cada tema al acta
        cantidad_temas = request.POST.get('cantidad_total_temas')
        nombres_temas = request.POST.getlist('nombre_tema')
        descripcion_temas = request.POST.getlist('descripcion_tema')
        cantidad_elementos_tema = request.POST.getlist('cant_elementos')

        #Valores de los elementos
        nombres_elementos = request.POST.getlist('nombre_elemento_hidden')
        descripcion_elementos = request.POST.getlist('descripcion_elemento_hidden')
        responsables_elementos = request.POST.getlist('responsable_elemento_hidden')
        tipos_elementos = request.POST.getlist('tipo_elemento_hidden')
        estados_elementos = request.POST.getlist('estado_elemento_hidden')
        padres_elementos = request.POST.getlist('padre_elemento_hidden')
        fechas_inicio = request.POST.getlist('fecha_inicio_hidden')
        fechas_termino = request.POST.getlist('fecha_termino_hidden')
        print "cantidad de temas:"+cantidad_temas
        for i in range(int(cantidad_temas)):
            titulo_tema = nombres_temas[i]
            descripcion_tema = descripcion_temas[i]
            nuevo_tema = Tema(acta_tema=acta, titulo_tema=titulo_tema, descripcion_tema=descripcion_tema)
            nuevo_tema.save()

            #Añadimos cada elemento del tema
            tema = Tema.objects.get(id=Tema.objects.latest('id').id)
            cant_elementos_tema_temp = cantidad_elementos_tema[i]
            for j in range(int(cant_elementos_tema_temp)):
                tipo_elemento = tipos_elementos[j]
                titulo_elemento = nombres_elementos[j]
                estado_elemento = estados_elementos[j]
                if tipo_elemento == 'Compromiso' and estado_elemento != "Pendiente por asignar":
                    if responsables_elementos[j]: #Si el usuario no está vacio
                        usuario_responsable = Usuario.objects.get(user=responsables_elementos[j])
                    else:
                        usuario_responsable = None
                else:
                    usuario_responsable = None
                #Validamos fechas
                if fechas_termino[j]:
                    fecha_inicio = datetime.datetime.strptime(fechas_inicio[j], '%d/%m/%Y').strftime('%Y-%m-%d')
                else:
                    fecha_inicio = None
                if fechas_termino[j]:
                    fecha_termino = datetime.datetime.strptime(fechas_termino[j], '%d/%m/%Y').strftime('%Y-%m-%d')
                else:
                    fecha_termino = None

                id_elemento_padre = padres_elementos[j]

                if id_elemento_padre or id_elemento_padre != '':
                    #elemento_padre = Elemento.objects.get(id=id_elemento_padre)
                    print ""
                else:
                    elemento_padre = None
                elemento_padre = None
                nuevo_elemento = Elemento(tipo_elemento=tipo_elemento, elemento_padre=elemento_padre,
                                          usuario_responsable=usuario_responsable, tema=tema, fecha_inicio=fecha_inicio,
                                          fecha_termino=fecha_termino, estado_elemento=estado_elemento,
                                          titulo_elemento=titulo_elemento, descripcion_elemento=descripcion_elementos[j])
                nuevo_elemento.save()

                #Si es un compromiso, se debe crear una tarea en el Kanban
                """
                if tipo_elemento == 'Compromiso':
                    elemento_dialogico = Elemento.objects.get(id=Elemento.objects.latest('id').id)
                    nombre_tarea = elemento_dialogico.titulo_elemento
                    fecha_vencimiento_tarea = elemento_dialogico.fecha_termino
                    fecha_inicio_tarea = elemento_dialogico.fecha_inicio
                    descripcion_tarea = elemento_dialogico.descripcion_elemento
                    checklist_tarea = None
                    nueva_tarea = Tarea_Kanban(elemento_dialogico=elemento_dialogico, nombre_tarea=nombre_tarea,
                                               fecha_vencimiento_tarea=fecha_vencimiento_tarea, descripcion_tarea=descripcion_tarea,
                                               checklist_tarea=checklist_tarea, fecha_inicio_tarea=fecha_inicio_tarea)
                    nueva_tarea.save()

                    #Agregamos Usuario_Tarea para usuario responsable
                    tarea_kanban = Tarea_Kanban.objects.get(id=Tarea_Kanban.objects.latest('id').id)
                    nuevo_usuario_tarea = Usuario_Tarea(usuario=usuario_responsable, tarea=tarea_kanban)
                    nuevo_usuario_tarea.save()
                """

            #Tenemos que sacar de la lista los elementos que ya fueron ingresados, por la forma en la que se leen es la unica forma en que se agreguen correctamente
            for x in range(int(cant_elementos_tema_temp)):
                nombres_elementos.pop(0)
                descripcion_elementos.pop(0)
                responsables_elementos.pop(0)
                tipos_elementos.pop(0)
                estados_elementos.pop(0)
                padres_elementos.pop(0)
                fechas_inicio.pop(0)
                fechas_termino.pop(0)
        ctx={'proyecto':proyecto_acta, 'usuarios_proyecto':usuarios_proyecto, 'success':True, 'compromisos_pendientes':compromisos_pendientes}
    else:

        ctx={'proyecto':proyecto_acta, 'usuarios_proyecto':usuarios_proyecto, 'compromisos_pendientes': compromisos_pendientes}
    return render(request, 'walo-template/proyectos/agregar_acta.html', ctx)

def index_view(request):
    ctx={}
    #Validamos que usuario no esté logueado
    if request.user.is_authenticated():
        posibles_miembros = lista_usuarios(request.user.username)
        proyectos_activos = lista_proyectos_activos(request.user.username)
        ctx = {'lista_usuarios':posibles_miembros, 'lista_proyectos_activos':proyectos_activos}
        return render(request, 'walo-template/index.html', ctx)
    else:
        if request.method == 'POST':
            accion = request.POST['accion']
            if accion == 'agregar_usuario':
                username = request.POST['agregar_usuario_username']
                nombres = request.POST['agregar_usuario_nombres'].title()
                apellidos = request.POST['agregar_usuario_apellidos'].title()
                email = request.POST['agregar_usuario_email']
                password = request.POST['agregar_usuario_password']
                usuario_nuevo = User(username=username, first_name=nombres, last_name=apellidos,
                                     email=email, password=password)
                #Para encriptar la clave
                usuario_nuevo.set_password(password)
                usuario_nuevo.save()
                Usuario(user=usuario_nuevo).save()
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    posibles_miembros = lista_usuarios(request.user.username)
                    proyectos_activos = lista_proyectos_activos(request.user.username)
                    ctx = {'lista_usuarios':posibles_miembros, 'lista_proyectos_activos':proyectos_activos}
                    return render(request, 'walo-template/index.html', ctx)
                else:
                    return render(request, 'walo-template/login.html')
            elif accion == 'login_usuario':
                username = request.POST['login_username']
                password = request.POST['login_password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    posibles_miembros = lista_usuarios(request.user.username)
                    proyectos_activos = lista_proyectos_activos(request.user.username)
                    ctx = {'lista_usuarios':posibles_miembros, 'lista_proyectos_activos':proyectos_activos}
                    return render(request, 'walo-template/index.html', ctx)
                else:
                    #Usuario no existe
                    ctx = {'errorUsuario': True}
                    return render(request, 'walo-template/login.html', ctx)
            else:
                pass
        #cualquier otra accion lleva al login
        return render(request, 'walo-template/login.html')

@login_required(login_url='/index/')
def ver_calendario_actas(request, id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    actas_proyecto = Acta.objects.filter(proyecto_acta=proyecto)
    ctx = {'proyecto': proyecto, 'actas_proyecto':actas_proyecto}
    return render(request, 'walo-template/proyectos/calendario_actas.html', ctx)

@login_required(login_url='/index/')
def editar_acta(request, id_proyecto, id_acta):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios_proyecto = Usuario_Proyecto.objects.filter(proyecto=proyecto)
    acta = Acta.objects.get(id=id_acta)
    usuarios_acta = Usuario_Acta.objects.filter(acta=acta)
    temas = Tema.objects.filter(acta_tema=acta)
    actas = Acta.objects.filter(proyecto_acta=proyecto)
    compromisos_pendientes = False
    for acta in actas:
        for tema in acta.tema_set.all():
            for elemento in tema.elemento_set.all():
                if elemento.tipo_elemento == "Compromiso" and (elemento.estado_elemento != "Finalizado" or elemento.estado_elemento != "Eliminado"):
                    compromisos_pendientes = True
                    break

    ctx = {}
    ctx['proyecto'] = proyecto
    ctx['acta'] = acta
    ctx['temas'] = temas
    ctx['usuarios_acta'] = usuarios_acta
    ctx['usuarios_proyecto'] = usuarios_proyecto
    ctx['compromisos_pendientes'] = compromisos_pendientes
    if request.method == 'POST':
        #Editamos el acta
        fecha_acta = datetime.datetime.strptime(request.POST['editar_acta_fecha'], '%d/%m/%Y').strftime('%Y-%m-%d')
        resumen_acta = request.POST.get('editar_acta_resumen')
        acta.resumen_acta = resumen_acta
        acta.fecha_acta = fecha_acta
        acta.save()

        #Por cada miembro, añadimos usuario_acta
        miembros_presentes = request.POST.getlist('editar_acta_miembros_presentes')
        miembros_proyecto = Usuario_Proyecto.objects.filter(proyecto=proyecto)
        secretario_proyecto = request.POST.get('editar_acta_secretario')
        for miembro in miembros_proyecto:
            presente = False
            secretario = False
            usuario = Usuario.objects.get(user=miembro.usuario)
            if str(usuario.id) in miembros_presentes:
                #Solo si estuvo presente, puede ser secretario
                presente = True
                if str(usuario.id) == secretario_proyecto:
                    secretario = True
            usuario_acta=Usuario_Acta.objects.get(usuario=usuario, acta=acta)
            usuario_acta.presente = presente
            usuario_acta.secretario = secretario
            usuario_acta.save()

        #Añadimos cada tema al acta
        id_temas = request.POST.getlist('id_tema')
        cantidad_temas = request.POST.get('cantidad_total_temas')
        nombres_temas = request.POST.getlist('nombre_tema')
        descripcion_temas = request.POST.getlist('descripcion_tema')
        cantidad_elementos_tema = request.POST.getlist('cant_elementos')

        #Valores de los elementos
        id_elementos = request.POST.getlist('id_elemento_hidden')
        nombres_elementos = request.POST.getlist('nombre_elemento_hidden')
        descripcion_elementos = request.POST.getlist('descripcion_elemento_hidden')
        responsables_elementos = request.POST.getlist('responsable_elemento_hidden')
        tipos_elementos = request.POST.getlist('tipo_elemento_hidden')
        estados_elementos = request.POST.getlist('estado_elemento_hidden')
        padres_elementos = request.POST.getlist('padre_elemento_hidden')
        fechas_inicio = request.POST.getlist('fecha_inicio_hidden')
        fechas_termino = request.POST.getlist('fecha_termino_hidden')

        #Eliminamos temas y elementos, para luego volver a agregar los que tenga el formulario (editados y/o nuevos)
        temas.delete()

        #Añadimos cada tema. Se valida si el tema ya existe (update) o es uno nuevo
        for i in range(int(cantidad_temas)):
            titulo_tema = nombres_temas[i]
            descripcion_tema = descripcion_temas[i]
            nuevo_tema = Tema(acta_tema=acta, titulo_tema=titulo_tema, descripcion_tema=descripcion_tema)
            nuevo_tema.save()
            tema = Tema.objects.get(id=Tema.objects.latest('id').id)

            #Añadimos cada elemento del tema, validando si el elemento existe o no
            cant_elementos_tema_temp = cantidad_elementos_tema[i]

            for j in range(int(cant_elementos_tema_temp)):
                tipo_elemento = tipos_elementos[j]
                titulo_elemento = nombres_elementos[j]
                estado_elemento = estados_elementos[j]
                if tipo_elemento == 'Compromiso' and estado_elemento != "Pendiente por asignar":
                    if responsables_elementos[j]: #Si el usuario no está vacio
                        usuario_responsable = Usuario.objects.get(user=responsables_elementos[j])
                    else:
                        usuario_responsable = None
                else:
                    usuario_responsable = None
                #Validamos fechas
                if fechas_termino[j]:
                    fecha_inicio = datetime.datetime.strptime(fechas_inicio[j], '%d/%m/%Y').strftime('%Y-%m-%d')
                else:
                    fecha_inicio = None
                if fechas_termino[j]:
                    fecha_termino = datetime.datetime.strptime(fechas_termino[j], '%d/%m/%Y').strftime('%Y-%m-%d')
                else:
                    fecha_termino = None

                id_elemento_padre = padres_elementos[j]

                if id_elemento_padre:
                    #elemento_padre = Elemento.objects.get(id=id_elemento_padre)
                    print ""
                else:
                    elemento_padre = None
                elemento_padre = None

                nuevo_elemento = Elemento(tipo_elemento=tipo_elemento, elemento_padre=elemento_padre,
                                          usuario_responsable=usuario_responsable, tema=tema, fecha_inicio=fecha_inicio,
                                          fecha_termino=fecha_termino, estado_elemento=estado_elemento,
                                          titulo_elemento=titulo_elemento, descripcion_elemento=descripcion_elementos[j])
                nuevo_elemento.save()

                """
                #Eliminado momentaneamente pues las tareas del kanban se sacan de los compromisos
                #Si es un compromiso, se debe crear una tarea en el Kanban
                if tipo_elemento == 'Compromiso':
                    elemento_dialogico = Elemento.objects.get(id=Elemento.objects.latest('id').id)
                    nombre_tarea = elemento_dialogico.titulo_elemento
                    fecha_vencimiento_tarea = elemento_dialogico.fecha_termino
                    fecha_inicio_tarea = elemento_dialogico.fecha_inicio
                    descripcion_tarea = elemento_dialogico.descripcion_elemento
                    checklist_tarea = None
                    nueva_tarea = Tarea_Kanban(elemento_dialogico=elemento_dialogico, nombre_tarea=nombre_tarea,
                                               fecha_vencimiento_tarea=fecha_vencimiento_tarea, descripcion_tarea=descripcion_tarea,
                                               checklist_tarea=checklist_tarea, fecha_inicio_tarea=fecha_inicio_tarea)
                    nueva_tarea.save()

                    #Agregamos Usuario_Tarea para usuario responsable
                    tarea_kanban = Tarea_Kanban.objects.get(id=Tarea_Kanban.objects.latest('id').id)
                    nuevo_usuario_tarea = Usuario_Tarea(usuario=usuario_responsable, tarea=tarea_kanban)
                    nuevo_usuario_tarea.save()
                """

            #Tenemos que sacar de la lista los elementos que ya fueron ingresados, por la forma en la que se leen es la unica forma en que se agreguen correctamente
            for x in range(int(cant_elementos_tema_temp)):
                nombres_elementos.pop(0)
                descripcion_elementos.pop(0)
                responsables_elementos.pop(0)
                tipos_elementos.pop(0)
                estados_elementos.pop(0)
                padres_elementos.pop(0)
                fechas_inicio.pop(0)
                fechas_termino.pop(0)
        acta = Acta.objects.get(id=id_acta)
        usuarios_acta = Usuario_Acta.objects.filter(acta=acta)
        temas = Tema.objects.filter(acta_tema=acta)
        ctx = {}
        ctx['proyecto'] = proyecto
        ctx['acta'] = acta
        ctx['temas'] = temas
        ctx['usuarios_acta'] = usuarios_acta
        ctx['usuarios_proyecto'] = usuarios_proyecto
        ctx['success'] = True
    return render(request, 'walo-template/proyectos/editar_acta.html', ctx)

@login_required(login_url='/index/')
@csrf_exempt
def eliminar_acta(request, id_proyecto):
    ctx = {}
    try:
        id_acta = request.POST.get('id_acta')
        print "Eliminando acta ", id_acta
        acta = Acta.objects.get(id=id_acta)
        acta.delete()
        ctx['successEliminar'] = True
    except Exception,e:
        print e
        ctx['errorEliminar'] = True
    return render(request, 'walo-template/proyectos/calendario_actas.html', ctx)

@login_required(login_url='/index/')
@csrf_exempt
def agregar_tarjeta(request, id_proyecto):
    ctx = {}
    try:
        nombre_tarea = request.POST.get('nombre_tarea')
        if request.POST.get('fecha_inicio'):
            fecha_inicio_tarea = datetime.datetime.strptime(request.POST.get('fecha_inicio'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_inicio_tarea = None
        if request.POST.get('fecha_termino'):
            fecha_vencimiento_tarea = datetime.datetime.strptime(request.POST.get('fecha_termino'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_vencimiento_tarea = None
        descripcion_tarea = request.POST.get('descripcion_tarea')
        if request.POST.get('elemento_padre'):
            elemento_padre = Elemento.objects.get(id=request.POST.get('elemento_padre'))
        else:
            elemento_padre = None
        estado_tarea = request.POST.get('estado_tarea')
        usuario_responsable = Usuario.objects.get(user=request.POST.get('usuario_responsable'))
        nueva_tarea = Elemento(tipo_elemento='Compromiso', elemento_padre=elemento_padre,
                                  usuario_responsable=usuario_responsable, tema=None, fecha_inicio=fecha_inicio_tarea,
                                  fecha_termino=fecha_vencimiento_tarea, estado_elemento=estado_tarea,
                                  titulo_elemento=nombre_tarea, descripcion_elemento=descripcion_tarea)
        nueva_tarea.save()

        tarea = Elemento.objects.get(id=Elemento.objects.latest('id').id)
        ctx['success'] = True
        ctx['id_tarea'] = tarea.id
        ctx['nombre_tarea'] = tarea.titulo_elemento
        ctx['descripcion_tarea'] = tarea.descripcion_elemento
        ctx['fecha_inicio'] = tarea.fecha_inicio
        ctx['fecha_termino'] = tarea.fecha_termino
        ctx['usuario_responsable_id'] = tarea.usuario_responsable.id
        ctx['usuario_responsable_nombre'] = tarea.usuario_responsable.user.first_name+" "+tarea.usuario_responsable.user.last_name
        ctx['elemento_padre_id'] = tarea.elemento_padre.id if tarea.elemento_padre else ""
        ctx['elemento_padre_titulo'] = tarea.elemento_padre.titulo_elemento if tarea.elemento_padre else ""
        return JsonResponse(ctx)
    except Exception as e:
        print e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
    return render(request, 'walo-template/proyectos/calendario_actas.html', ctx)

@login_required(login_url='/index/')
@csrf_exempt
def cambiar_estado_tarjeta(request, id_proyecto):
    ctx = {}
    try:
        id_tarea = request.POST.get('id_tarea')
        estado_tarea = request.POST.get('estado_tarea')
        tarea = Elemento.objects.get(id=id_tarea)
        tarea.estado_elemento = estado_tarea
        tarea.save()
        ctx['success'] = True
        return JsonResponse(ctx)
    except Exception,e:
        print e
    return render(request, 'walo-template/proyectos/calendario_actas.html', ctx)

@login_required(login_url='/index/')
def ver_kanban(request, id_proyecto):
    ctx = {}
    actas_con_tema = []
    proyecto = Proyecto.objects.get(id=id_proyecto)
    actas = Acta.objects.filter(proyecto_acta=proyecto)

    for acta in actas:
        if len(acta.tema_set.all())>0: #Si el acta tiene temas, se agrega a la lista
            actas_con_tema.append(acta)
    #Compromisos que no tienen temas (es decir, fueron agregados directamente al tablero kanban)
    tareas = Elemento.objects.filter(tipo_elemento='Compromiso')
    ctx['proyecto'] = proyecto
    ctx['tareas'] = tareas
    ctx['actas_con_tema'] = actas_con_tema
    return render(request, 'walo-template/proyectos/kanban.html', ctx)

@login_required(login_url='/index/')
def ver_sintesis_dialogica(request, id_proyecto):
    ctx = {}
    proyecto = Proyecto.objects.get(id=id_proyecto)
    usuarios_proyecto = Usuario_Proyecto.objects.filter(proyecto=proyecto)
    actas = Acta.objects.filter(proyecto_acta=proyecto)
    ctx['proyecto'] = proyecto
    ctx['usuarios_proyecto'] = usuarios_proyecto
    return render(request, 'walo-template/proyectos/sintesis_dialogica.html', ctx)

@login_required(login_url='/index/')
@csrf_exempt
def filtrar_elementos(request, id_proyecto):
    ctx = {}
    try:
        nombre_elemento = request.POST.get('nombre_elemento')
        if request.POST.get('fecha_inicio'):
            fecha_inicio = datetime.datetime.strptime(request.POST.get('fecha_inicio'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_inicio = None
        if request.POST.get('fecha_termino'):
            fecha_termino = datetime.datetime.strptime(request.POST.get('fecha_termino'), '%d/%m/%Y').strftime('%Y-%m-%d')
        else:
            fecha_termino = None

        usuario_responsable = request.POST.getlist('usuarios_responsables[]')
        if request.POST.get('texto_en_discusion'):
            lista_palabras_discusion = request.POST.get('texto_en_discusion').split()
        else:
            lista_palabras_discusion = []
        elementos_encontrados = []
        #Recorremos todos los elementos de las actas
        proyecto = Proyecto.objects.get(id=id_proyecto)
        actas = Acta.objects.filter(proyecto_acta=proyecto)

        #Se obtienen todos los elementos de la lista y se almacenan en elementos_encontrados. Si alguno de los filtros no calzan, se elimina de la lista

        for acta in actas:
            for tema in acta.tema_set.all():
                for elemento in tema.elemento_set.all():

                    #Si todos los filtros en filtros_aplicados se cumplen, se mantiene el elemento en la lista, pues cumple con los filtros
                    #Si hay al menos un False, significa que no cumple, por lo que se saca de la lista
                    filtros_aplicados = [False] * 5 #Arreglo con 5 falses

                    if nombre_elemento == "" or nombre_elemento.lower() in elemento.titulo_elemento.lower():
                        filtros_aplicados[0] = True
                    #Se puede cambiar any por all para que calcen todas las palabras y no solo una
                    #if not any(palabra in elemento.descripcion_elemento for palabra in lista_palabras_discusion) and not any(palabra in tema.descripcion_tema for palabra in lista_palabras_discusion):
                    if lista_palabras_discusion == [] or any(palabra.lower() in tema.descripcion_tema.lower() for palabra in lista_palabras_discusion):
                        filtros_aplicados[1] = True
                    if fecha_inicio == None or str(fecha_inicio) == str(elemento.fecha_inicio):
                        filtros_aplicados[2] = True
                    if fecha_termino == None or str(fecha_termino) == str(elemento.fecha_termino):
                        filtros_aplicados[3] = True
                    if not usuario_responsable or (elemento.tipo_elemento == "Compromiso" and str(elemento.usuario_responsable.id) in usuario_responsable): #Si se filtra por usuario repsonsable, se borran todos los elementos que no sean comrpomisos pues no tienen usuarios responsables
                        filtros_aplicados[4] = True
                    if not False in filtros_aplicados:
                        elementos_encontrados.append(elemento.id)
        ctx['elementos_filtrados'] = elementos_encontrados
        print ctx
        return JsonResponse(ctx)
    except Exception as e:
        print e
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

"""
Funciones varias
"""

@csrf_exempt
def cerrar_sesion(request):
    logout(request)
    return render(request, 'walo-template/login.html')

def lista_usuarios(usuario_logueado):
    return Usuario.objects.all().exclude(user=User.objects.get(username=usuario_logueado))

def lista_proyectos_activos(usuario_logueado):
    user = User.objects.get(username=usuario_logueado)
    usuario = Usuario.objects.get(user=user)
    #FALTA VALIDAR QUE EL PROYECTO ESTE ACTIVO
    usuario_proyectos = Usuario_Proyecto.objects.filter(usuario=usuario)
    return usuario_proyectos