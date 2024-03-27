from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sign/',views.sign, name="sign"),
    path('perfil/', views.perfil, name="perfil"),
    path('perfil/editar', views.editarPerfil, name="editarPerfil"),
    path('perfil/eliminar', views.eliminarPerfil, name="eliminarPerfil"),
    path('logout/', views.logout, name="logout"),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form2.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done2.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm2.html'), name='password_reset_confirm'),
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete2.html'), name='password_reset_complete'),
]