from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.homepage, name="homepage"),
    path('temario/',views.temario, name="temario"),
    path('temario/<int:id>/',views.mostrar_temario, name="mostrar_temario"),
    path('temario/<int:id>/<path:path>', views.ver_pdf, name='ver_pdf'),
    path('temario/eliminartemario/<int:id>/',views.eliminarTemario, name="eliminarTemario"),
    path('pruebas/',views.pruebas, name="pruebas"),
    path('pruebas/<int:id>/',views.mostrar_prueba, name="mostrar_prueba"),
    path('pruebas/eliminarprueba/<int:id>/',views.eliminarPrueba, name="eliminarPrueba"),
    path('pruebas/realizarprueba/<str:titulo>/',views.realizarPrueba, name="realizarPrueba"),
    path('progreso/',views.progreso, name="progreso"),
    path('progreso/<int:id>/',views.progresoOposicion, name="progresoOposicion"),
]
