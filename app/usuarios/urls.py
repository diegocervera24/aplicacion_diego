from django.urls import path
from . import views
urlpatterns = [
    path('',views.homepage, name=""),
    path('sign/',views.sign, name="sign"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path('logout/', views.logout, name="logout"),
]