from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.homepage, name="homepage"),
    path('temario/',views.temario, name="temario"),
    path('logout/', views.logout, name="logout"),
    path('temario/<int:id>/',views.mostrar_temario, name="mostrar_temario"),
    path('eliminartemario/<int:id>/',views.eliminarTemario, name="eliminarTemario"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)