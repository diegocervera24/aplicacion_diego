from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage, name="homepage"),
    path('temario/',views.temario, name="temario"),
    path('logout/', views.logout, name="logout"),
]