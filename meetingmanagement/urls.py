from django.conf.urls import patterns, include, url

urlpatterns = patterns('meetingmanagement.views',
    # Examples:
    # url(r'^$', 'easymeetings.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^index/$', 'index_view', name='index_view'),
    url(r'^cerrar_sesion/$', 'cerrar_sesion', name='cerrar_sesion'),
    url(r'^agregar_proyecto/$', 'agregar_proyecto', name='agregar_proyecto'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/$', 'ver_proyecto', name='ver_proyecto'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/calendario_actas/$', 'ver_calendario_actas', name='ver_calendario_actas'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/kanban/$', 'ver_kanban', name='ver_kanban'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/sintesis_dialogica/$', 'ver_sintesis_dialogica', name='sintesis_dialogica'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/agregar_acta/$', 'agregar_acta', name='agregar_acta'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/editar_acta/(?P<id_acta>\d+)/$', 'editar_acta', name='editar_acta'),
    url(r'^proyectos/ver_proyecto/(?P<id_proyecto>\d+)/eliminar_acta/$', 'eliminar_acta', name='eliminar_acta'),
    url(r'^(?P<id_proyecto>\d+)/filtrar_elementos/$', 'filtrar_elementos', name='filtrar_elementos'),
    url(r'^(?P<id_proyecto>\d+)/agregar_tarjeta/$', 'agregar_tarjeta', name='agregar_tarjeta'),
    url(r'^(?P<id_proyecto>\d+)/cambiar_estado_tarjeta/$', 'cambiar_estado_tarjeta', name='cambiar_estado_tarjeta'),
)
