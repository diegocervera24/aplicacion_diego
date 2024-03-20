from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from oposicion.models import Temario, Agrupa_en, Oposicion

def homepage(request):
    return render(request, 'oposicion/index.html')

@login_required(login_url="sign")
def temario(request):
    nombreOposiciones = []
    user=request.user.username
    all_temario = Agrupa_en.objects.all().prefetch_related('IdTemario','IdOposicion').filter(IdTemario__NomUsuario__username=user,IdTemario__TemVisible=True).values_list('IdOposicion', flat=True).distinct()

    for temario in all_temario:
        oposicion = Oposicion.objects.get(id=temario)
        nombreOposiciones.append(oposicion.NomOposicion)

    return render(request, 'oposicion/temario.html',{'nombreOposiciones':nombreOposiciones})

def logout(request):

    auth.logout(request)
    return redirect("/")