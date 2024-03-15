from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'oposicion/index.html')

@login_required(login_url="sign")
def temario(request):
    return render(request, 'oposicion/temario.html')

def logout(request):

    auth.logout(request)
    return redirect("/")
